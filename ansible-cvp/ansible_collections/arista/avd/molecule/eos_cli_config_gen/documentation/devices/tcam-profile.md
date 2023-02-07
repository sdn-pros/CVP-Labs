# tcam-profile
# Table of Contents

- [Management](#management)
  - [Management Interfaces](#management-interfaces)
- [Authentication](#authentication)
- [Monitoring](#monitoring)
- [Hardware TCAM Profile](#hardware-tcam-profile)
  - [Custom TCAM profiles](#custom-tcam-profiles)
  - [Hardware TCAM configuration](#hardware-tcam-configuration)
- [Internal VLAN Allocation Policy](#internal-vlan-allocation-policy)
  - [Internal VLAN Allocation Policy Summary](#internal-vlan-allocation-policy-summary)
- [Interfaces](#interfaces)
- [Routing](#routing)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
- [Multicast](#multicast)
- [Filters](#filters)
- [ACL](#acl)
- [Quality Of Service](#quality-of-service)

# Management

## Management Interfaces

### Management Interfaces Summary

#### IPv4

| Management Interface | description | Type | VRF | IP Address | Gateway |
| -------------------- | ----------- | ---- | --- | ---------- | ------- |
| Management1 | oob_management | oob | MGMT | 10.73.255.122/24 | 10.73.255.2 |

#### IPv6

| Management Interface | description | Type | VRF | IPv6 Address | IPv6 Gateway |
| -------------------- | ----------- | ---- | --- | ------------ | ------------ |
| Management1 | oob_management | oob | MGMT | - | - |

### Management Interfaces Device Configuration

```eos
!
interface Management1
   description oob_management
   vrf MGMT
   ip address 10.73.255.122/24
```

# Authentication

# Monitoring

# Hardware TCAM Profile

TCAM profile __`traffic_policy`__ is active

## Custom TCAM profiles

Following TCAM profiles are configured on device:

- Profile Name: `traffic_policy`

## Hardware TCAM configuration

```eos
!
hardware tcam
   profile traffic_policy
      feature acl port mac
          sequence 55
          key size limit 160
          key field dst-mac ether-type src-mac
          action count drop
          packet ipv4 forwarding bridged
          packet ipv4 forwarding routed
          packet ipv4 forwarding routed multicast
          packet ipv4 mpls ipv4 forwarding mpls decap
          packet ipv4 mpls ipv6 forwarding mpls decap
          packet ipv4 non-vxlan forwarding routed decap
          packet ipv4 vxlan forwarding bridged decap
          packet ipv6 forwarding bridged
          packet ipv6 forwarding routed
          packet ipv6 forwarding routed decap
          packet ipv6 forwarding routed multicast
          packet ipv6 ipv6 forwarding routed decap
          packet mpls forwarding bridged decap
          packet mpls ipv4 forwarding mpls
          packet mpls ipv6 forwarding mpls
          packet mpls non-ip forwarding mpls
          packet non-ip forwarding bridged
      !
      feature forwarding-destination mpls
          sequence 100
      !
      feature mirror ip
          sequence 80
          key size limit 160
          key field dscp dst-ip ip-frag ip-protocol l4-dst-port l4-ops l4-src-port src-ip tcp-control
          action count mirror set-policer
          packet ipv4 forwarding bridged
          packet ipv4 forwarding routed
          packet ipv4 forwarding routed multicast
          packet ipv4 non-vxlan forwarding routed decap
      !
      feature mpls
          sequence 5
          key size limit 160
          action drop redirect set-ecn
          packet ipv4 mpls ipv4 forwarding mpls decap
          packet ipv4 mpls ipv6 forwarding mpls decap
          packet mpls ipv4 forwarding mpls
          packet mpls ipv6 forwarding mpls
          packet mpls non-ip forwarding mpls
      !
      feature pbr ip
          sequence 60
          key size limit 160
          key field dscp dst-ip ip-frag ip-protocol l4-dst-port l4-ops-18b l4-src-port src-ip tcp-control
          action count redirect
          packet ipv4 forwarding routed
          packet ipv4 mpls ipv4 forwarding mpls decap
          packet ipv4 mpls ipv6 forwarding mpls decap
          packet ipv4 non-vxlan forwarding routed decap
          packet ipv4 vxlan forwarding bridged decap
      !
      feature pbr ipv6
          sequence 30
          key field dst-ipv6 ipv6-next-header l4-dst-port l4-src-port src-ipv6-high src-ipv6-low tcp-control
          action count redirect
          packet ipv6 forwarding routed
      !
      feature pbr mpls
          sequence 65
          key size limit 160
          key field mpls-inner-ip-tos
          action count drop redirect
          packet mpls ipv4 forwarding mpls
          packet mpls ipv6 forwarding mpls
          packet mpls non-ip forwarding mpls
      !
      feature qos ip
          sequence 75
          key size limit 160
          key field dscp dst-ip ip-frag ip-protocol l4-dst-port l4-ops l4-src-port src-ip tcp-control
          action set-dscp set-policer set-tc
          packet ipv4 forwarding routed
          packet ipv4 forwarding routed multicast
          packet ipv4 mpls ipv4 forwarding mpls decap
          packet ipv4 mpls ipv6 forwarding mpls decap
          packet ipv4 non-vxlan forwarding routed decap
      !
      feature qos ipv6
          sequence 70
          key field dst-ipv6 ipv6-next-header ipv6-traffic-class l4-dst-port l4-src-port src-ipv6-high src-ipv6-low
          action set-dscp set-policer set-tc
          packet ipv6 forwarding routed
      !
      feature traffic-policy port ipv4
          sequence 45
          key size limit 160
          key field dscp dst-ip-label icmp-type-code ip-frag ip-fragment-offset ip-length ip-protocol l4-dst-port l4-src-port src-ip-label tcp-control ttl
          action count drop log set-dscp set-tc
          packet ipv4 forwarding routed
      !
      feature traffic-policy port ipv6
          sequence 25
          key field dst-ipv6-label hop-limit icmp-type-code ipv6-length ipv6-next-header ipv6-traffic-class l4-dst-port l4-src-port src-ipv6-label tcp-control
          action count drop log set-dscp set-tc
          packet ipv6 forwarding routed
      !
      feature tunnel vxlan
          sequence 50
          key size limit 160
          packet ipv4 vxlan eth ipv4 forwarding routed decap
          packet ipv4 vxlan forwarding bridged decap
   !
   system profile traffic_policy
```

# Internal VLAN Allocation Policy

## Internal VLAN Allocation Policy Summary

**Default Allocation Policy**

| Policy Allocation | Range Beginning | Range Ending |
| ------------------| --------------- | ------------ |
| ascending | 1006 | 4094 |

# Interfaces

# Routing

## IP Routing

### IP Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |

### IP Routing Device Configuration

```eos
```
## IPv6 Routing

### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |

# Multicast

# Filters

# ACL

# Quality Of Service
