# Use NAT Gateway With eAPI

## Abstract

This post will show how to create a local environment to leverage AVD Collection to build EVPN/VXLAN configuration for a set of devices and deploy configuration using EOS eAPI through a NAT gateway.

When we use a lab solution like [EVE-NG](https://www.eve-ng.net/) or GNS3, it might be complex to configure the same VLANs for your runner and your EOS devices. So instead, we can use a NAT gateway to expose the eAPI port to your Ansible runner consuming a single IP address.

Below is a standard lab we use for development. And, of course, our laptops aren't directly connected to the EOS management plane.

![Standard EVE-NG lab with NAT](../_media/lab-nat-topology-example.png)

## Requirements

- A dedicated VLAN for EOS out of band management
- A Linux server connected on both out of band management network and ansible-runner network.
  - This lab will be based on [Ubuntu 20.04](https://ubuntu.com/download/server)
  - SSH access to server enable.
- An [AVD setup](../installation/collection-installation.md) already configured on your ansible-runner.

All devices must have a basic network configuration to allow access to eAPI. Below is a very basic example of how to activate eAPI over HTTPS

```eos
!
username admin privilege 15 role network-admin secret sha512 .....
!
management api http-commands
   no shutdown
   !
   vrf MGMT
      no shutdown
!
```

## Configure network interfaces

First of all, we have to configure your network interfaces. So let's configure the following:

- **`ens3`**: connected to ansible-runner
- **`ens4`**: connected to out-of-band management network

With latest Ubuntu, this configuration is part of netplan configuration file:

```yaml
$ sudo vim /etc/netplan/00-installer-config.yaml
# This is the network config written by 'subiquity'
network:
  ethernets:
    ens3:
      addresses:
      - < YOUR RUNNER NETWORK>/<RUNNER NETWORK NETMASK >
      gateway4: < DEFAULT GATEWAY >
      nameservers:
        addresses:
        - 1.1.1.1
        - 8.8.8.8
    ens4:
      addresses:
      - < OOB NETWORK IP > / < OOB NETWORK SUBNET >
      nameservers: {}
  version: 2
```

Then apply your changes on your server:

```shell
sudo netplan apply
```

## Configure NAT access to eAPI

We can now define NAT rules to forward traffic from the network-runner to your EOS devices. Here we will create a minimal shell script to do:

- Activate IP routing
- Reset NAT tables
- Configure forwarding to eAPI and SSH ports
- Activate NAT masquerading IN and OUT

The script below is an example and uses `10.73.1.0/24` as the OOB network

```shell
$ vim expose-eos.sh
#!/bin/bash

echo "Jumphost Remote access configuration"

_EAPI_PORT=443
_SSH_PORT=22
_SRC_IF='ens3'
_DST_IF='ens4'

echo '* Activate kernel routing'
sysctl -w net.ipv4.ip_forward=1

echo '* Flush Current IPTables settings'
iptables --flush
iptables --delete-chain
iptables --table nat --flush
iptables --table nat --delete-chain

echo '* Activate default forwarding'

iptables -P FORWARD ACCEPT
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT

echo '* Activate masquerading'

iptables -t nat -A POSTROUTING -o ${_SRC_IF} -j MASQUERADE
iptables -t nat -A POSTROUTING -o ${_DST_IF} -j MASQUERADE

echo '* Activate eAPI forwarding with base port 800x'

# Do this configuration for any EOS device.
echo '* Activate eAPI forwarding with base port 800x'
iptables -t nat -A PREROUTING -p tcp -i ${_SRC_IF} --dport 8001 -j DNAT --to-destination 10.73.1.11:${_EAPI_PORT}
echo '* Activate SSH forwarding with base port 810x'
iptables -t nat -A PREROUTING -p tcp -i ${_SRC_IF} --dport 8101 -j DNAT --to-destination 10.73.1.11:${_SSH_PORT}

# Configure at the end of the file
iptables -A FORWARD -p tcp -d 10.73.1.0/24 --dport ${_EAPI_PORT} -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -p tcp -d 10.73.1.0/24 --dport ${_SSH_PORT} -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT

echo "-> Configuration done"
```

Then, copy this script on your NAT gateway and run it using **sudo** or with root permission:

```shell
$ sudo sh expose-eos.sh
[sudo] password for tom:
Flush Current IPTables settings
Activate masquerading
* Activate eAPI forwarding with base port 800x
* Activate SSH forwarding with base port 810x
-> Configuration done
```

## Test remote access

Before running an Ansible script with eAPI, you can manually test end-to-end connectivity using either cURL or your browser:

```bash
$ curl -k -D - https://< NAT GATEWAY IP >:8001
HTTP/1.1 301 Moved Permanently
Server: nginx
[...]
```

## Configure Ansible inventory

So as we now have a single IP address to connect to all devices in our lab, we will leverage `ansible_port` for per device connectivity.

```yaml
---
all:
  children:
    DC1:
      vars:
        ansible_host: 10.83.28.162
      children:
        DC1_FABRIC:
          children:
            DC1_SPINES:
              hosts:
                DC1-SPINE1:
                  ansible_port: 8001
                DC1-SPINE2:
                  ansible_port: 8002
```
