# router-multicast
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
  - [Router Multicast](#router-multicast)
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

# Multicast

## Router Multicast

### IP Router Multicast Summary

- Counters rate period decay is set for 300 seconds
- Routing for IPv4 multicast is enabled.
- Multipathing deterministically by selecting the same upstream router.
- Software forwarding by the Software Forwarding Engine (SFE)

### IP Router Multicast RPF Routes

| Source Prefix | Next Hop | Administrative Distance |
| ------------- | -------- | ----------------------- |
| 10.10.10.1/32 | 10.9.9.9 | 2 |
| 10.10.10.1/32 | Ethernet1 | 1 |
| 10.10.10.2/32 | Ethernet2 | - |

### IP Router Multicast VRFs

| VRF Name | Multicast Routing |
| -------- | ----------------- |
| MCAST_VRF1 | enabled |
| MCAST_VRF2 | enabled |

### Router Multicast Device Configuration

```eos
!
router multicast
   ipv4
      rpf route 10.10.10.1/32 10.9.9.9 2
      rpf route 10.10.10.1/32 Ethernet1 1
      rpf route 10.10.10.2/32 Ethernet2
      counters rate period decay 300 seconds
      routing
      multipath deterministic router-id
      software-forwarding sfe
      !
      vrf MCAST_VRF1
         ipv4
            routing
      !
      vrf MCAST_VRF2
         ipv4
            routing
```


# Filters

# ACL

# Quality Of Service
