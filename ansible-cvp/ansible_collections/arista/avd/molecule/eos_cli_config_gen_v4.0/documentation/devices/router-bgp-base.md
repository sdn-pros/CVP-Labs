# router-bgp-base
# Table of Contents

- [Management](#management)
  - [Management Interfaces](#management-interfaces)
- [Authentication](#authentication)
- [Monitoring](#monitoring)
- [Internal VLAN Allocation Policy](#internal-vlan-allocation-policy)
  - [Internal VLAN Allocation Policy Summary](#internal-vlan-allocation-policy-summary)
- [Interfaces](#interfaces)
- [Routing](#routing)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
  - [Router BGP](#router-bgp)
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

## Router BGP

### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65101|  192.168.255.3 |

| BGP Tuning |
| ---------- |
| no bgp default ipv4-unicast |
| graceful-restart restart-time 300 |
| graceful-restart |
| bgp bestpath d-path |
| update wait-for-convergence |
| update wait-install |
| distance bgp 20 200 200 |
| maximum-paths 32 ecmp 32 |

### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- |
| 192.0.3.1 | 65432 | default | - | all | - | - | - | - | - |
| 192.0.3.2 | 65433 | default | - | extended | 10000 | - | - | - | - |
| 192.0.3.3 | 65434 | default | - | standard | - | - | - | - | - |
| 192.0.3.4 | 65435 | default | - | large | - | - | - | - | - |

### BGP Route Aggregation

| Prefix | AS Set | Summary Only | Attribute Map | Match Map | Advertise Only |
| ------ | ------ | ------------ | ------------- | --------- | -------------- |
| 1.1.1.0/24 | False | False | - | - | True |
| 1.12.1.0/24 | True | True | RM-ATTRIBUTE | RM-MATCH | True |
| 2.2.1.0/24 | False | False | - | - | False |

### Router BGP Device Configuration

```eos
!
router bgp 65101
   router-id 192.168.255.3
   distance bgp 20 200 200
   maximum-paths 32 ecmp 32
   update wait-for-convergence
   update wait-install
   no bgp default ipv4-unicast
   graceful-restart restart-time 300
   graceful-restart
   bgp bestpath d-path
   neighbor 192.0.3.1 remote-as 65432
   neighbor 192.0.3.1 default-originate always
   neighbor 192.0.3.1 send-community
   neighbor 192.0.3.2 remote-as 65433
   neighbor 192.0.3.2 default-originate route-map RM-FOO-MATCH3
   neighbor 192.0.3.2 send-community extended
   neighbor 192.0.3.2 maximum-routes 10000
   neighbor 192.0.3.3 remote-as 65434
   neighbor 192.0.3.3 send-community standard
   neighbor 192.0.3.4 remote-as 65435
   neighbor 192.0.3.4 send-community large
   aggregate-address 1.1.1.0/24 advertise-only
   aggregate-address 1.12.1.0/24 as-set summary-only attribute-map RM-ATTRIBUTE match-map RM-MATCH advertise-only
   aggregate-address 2.2.1.0/24
   !
   address-family ipv4
      neighbor foo prefix-list PL-BAR-v4-IN in
      neighbor foo prefix-list PL-BAR-v4-OUT out
      neighbor foo default-originate route-map RM-FOO-MATCH always
      neighbor 192.0.2.1 prefix-list PL-FOO-v4-IN in
      neighbor 192.0.2.1 prefix-list PL-FOO-v4-OUT out
      network 10.0.0.0/8
      network 172.16.0.0/12
      network 192.168.0.0/16 route-map RM-FOO-MATCH
   !
   address-family ipv6
      neighbor baz prefix-list PL-BAR-v6-IN in
      neighbor baz prefix-list PL-BAR-v6-OUT out
      neighbor 2001:db8::1 prefix-list PL-FOO-v6-IN in
      neighbor 2001:db8::1 prefix-list PL-FOO-v6-OUT out
      network 2001:db8:100::/40
      network 2001:db8:200::/40 route-map RM-BAR-MATCH
      redistribute static route-map RM-IPV6-STATIC-TO-BGP
```

# Multicast

# Filters

# ACL

# Quality Of Service
