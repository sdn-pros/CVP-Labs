# route-maps
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
- [Multicast](#multicast)
- [Filters](#filters)
  - [Route-maps](#route-maps)
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

# Multicast

# Filters

## Route-maps

### Route-maps Summary

#### RM-10.2.3.4-SET-NEXT-HOP-OUT

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | - | ip next-hop 10.2.3.4 | - | - |

#### RM-CONN-BL-BGP

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | deny | ip address prefix-list PL-MLAG | - | - | - |
| 20 | permit | ip address prefix-list PL-SUBRM | - | RM-HIDE-ASPATH-IN | - |
| 30 | permit | ip address prefix-list PL-CONTINUE | - | - | 40 |
| 40 | permit | ip address prefix-list PL-CONTINUE | - | - | Next Sequence |
| 50 | permit | - | - | - | - |

#### RM-HIDE-ASPATH-IN

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | - | as-path match all replacement auto<br>community 65000:1 additive | - | - |

#### RM-HIDE-ASPATH-OUT

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | deny | community LIST-COM | - | - | - |
| 20 | permit | - | as-path match all replacement auto | - | - |

#### RM-MLAG-PEER-IN

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | - | origin incomplete | - | - |

#### RM-STATIC-2-BGP

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | - | tag 65100 | - | - |

### Route-maps Device Configuration

```eos
!
route-map RM-10.2.3.4-SET-NEXT-HOP-OUT permit 10
   set ip next-hop 10.2.3.4
!
route-map RM-CONN-BL-BGP deny 10
   match ip address prefix-list PL-MLAG
!
route-map RM-CONN-BL-BGP permit 20
   match ip address prefix-list PL-SUBRM
   sub-route-map RM-HIDE-ASPATH-IN
!
route-map RM-CONN-BL-BGP permit 30
   match ip address prefix-list PL-CONTINUE
   continue 40
!
route-map RM-CONN-BL-BGP permit 40
   match ip address prefix-list PL-CONTINUE
   continue
!
route-map RM-CONN-BL-BGP permit 50
!
route-map RM-HIDE-ASPATH-IN permit 10
   set as-path match all replacement auto
   set community 65000:1 additive
!
route-map RM-HIDE-ASPATH-OUT deny 10
   match community LIST-COM
!
route-map RM-HIDE-ASPATH-OUT permit 20
   set as-path match all replacement auto
!
route-map RM-MLAG-PEER-IN permit 10
   set origin incomplete
!
route-map RM-STATIC-2-BGP permit 10
   description tag for static routes
   set tag 65100
```

# ACL

# Quality Of Service
