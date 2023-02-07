# eos_cli_config_gen

**Table of Contents:**

- [eos_cli_config_gen](#eos_cli_config_gen)
  - [Overview](#overview)
  - [Role Inputs and Outputs](#role-inputs-and-outputs)
  - [Requirements](#requirements)
  - [Input Variables](#input-variables)
    - [ACLs](#acls)
      - [IP Extended Access-Lists](#ip-extended-access-lists)
      - [IPv6 Standard Access-Lists](#ipv6-standard-access-lists)
      - [IP Standard Access-Lists](#ip-standard-access-lists)
      - [IPv6 Extended Access-Lists](#ipv6-extended-access-lists)
      - [MAC Access-Lists](#mac-access-lists)
    - [Aliases](#aliases)
    - [Authentication](#authentication)
      - [AAA Authentication](#aaa-authentication)
      - [AAA Authorization](#aaa-authorization)
      - [AAA Accounting](#aaa-accounting)
      - [AAA Root](#aaa-root)
      - [AAA Server Groups](#aaa-server-groups)
      - [Enable Password](#enable-password)
      - [IP RADIUS Source Interfaces](#ip-radius-source-interfaces)
      - [IP TACACS+ Source Interfaces](#ip-tacacs-source-interfaces)
      - [Local Users](#local-users)
      - [Roles](#roles)
      - [Radius Servers](#radius-servers)
      - [Tacacs+ Servers](#tacacs-servers)
    - [Banners](#banners)
    - [Router BFD](#router-bfd)
    - [Custom Templates](#custom-templates)
    - [DHCP Relay](#dhcp-relay)
    - [EOS CLI](#eos-cli)
    - [Errdisable](#errdisable)
    - [Filters](#filters)
      - [Prefix Lists](#prefix-lists)
      - [IPv6 Prefix Lists](#ipv6-prefix-lists)
      - [Community Lists](#community-lists)
      - [IP Extended Community Lists](#ip-extended-community-lists)
      - [IP Extended Community Lists RegExp](#ip-extended-community-lists-regexp)
      - [Peer Filters](#peer-filters)
      - [Route Maps](#route-maps)
      - [Match Lists](#match-lists)
      - [AS Path](#as-path)
    - [Generate Device Documentation](#generate-device-documentation)
    - [Generate Default Config](#generate-default-config)
    - [Hardware](#hardware)
      - [Hardware Counters](#hardware-counters)
      - [Hardware TCAM Profiles](#hardware-tcam-profiles)
      - [Platform](#platform)
      - [Redundancy](#redundancy)
      - [Speed-Group Settings](#speed-group-settings)
    - [Interfaces](#interfaces)
      - [Ethernet Interfaces](#ethernet-interfaces)
        - [Routed Ethernet Interfaces](#routed-ethernet-interfaces)
        - [Switched Ethernet Interfaces](#switched-ethernet-interfaces)
      - [Interface Defaults](#interface-defaults)
      - [Switchport Default](#switchport-default)
      - [Interface Profiles](#interface-profiles)
      - [Loopback Interfaces](#loopback-interfaces)
      - [Port-Channel Interfaces](#port-channel-interfaces)
      - [VLAN Interfaces](#vlan-interfaces)
      - [VxLAN Interface](#vxlan-interface)
    - [Internal VLAN Order](#internal-vlan-order)
    - [IP DHCP Relay](#ip-dhcp-relay)
    - [IP ICMP Redirect](#ip-icmp-redirect)
    - [LACP](#lacp)
    - [Link Tracking Groups](#link-tracking-groups)
    - [LLDP](#lldp)
    - [MACsec](#macsec)
    - [Maintenance Mode](#maintenance-mode)
      - [BGP Groups](#bgp-groups)
      - [Interface Groups](#interface-groups)
      - [Profiles and units](#profiles-and-units)
    - [Management](#management)
      - [Clock](#clock)
      - [DNS Domain](#dns-domain)
      - [Domain Name Servers](#domain-name-servers)
      - [Domain Lookup](#domain-lookup)
      - [Domain-List](#domain-list)
      - [Management Interfaces](#management-interfaces)
      - [Management HTTP](#management-http)
      - [IP HTTP Client Source Interfaces](#ip-http-client-source-interfaces)
      - [Management GNMI](#management-gnmi)
      - [Management Console](#management-console)
      - [Management Security](#management-security)
      - [Management SSH](#management-ssh)
      - [IP SSH Client Source Interfaces](#ip-ssh-client-source-interfaces)
      - [NTP](#ntp)
    - [MPLS](#mpls)
    - [Multi-Chassis LAG - MLAG](#multi-chassis-lag---mlag)
    - [Multicast](#multicast)
      - [IP IGMP Snooping](#ip-igmp-snooping)
      - [Router Multicast](#router-multicast)
      - [Routing PIM Sparse Mode](#routing-pim-sparse-mode)
    - [Monitoring](#monitoring)
      - [Daemon TerminAttr](#daemon-terminattr)
      - [Custom Daemons](#custom-daemons)
      - [Connectivity Monitor](#connectivity-monitor)
      - [Event Handler](#event-handler)
      - [Event Monitor](#event-monitor)
      - [Load Interval](#load-interval)
      - [Logging](#logging)
      - [Sflow](#sflow)
      - [SNMP Settings](#snmp-settings)
      - [Monitor Sessions](#monitor-sessions)
    - [System Control-Plane](#system-control-plane)
      - [VM Tracer Sessions](#vm-tracer-sessions)
    - [Patch Panel](#patch-panel)
    - [PTP](#ptp)
    - [Prompt](#prompt)
    - [Quality of Services](#quality-of-services)
      - [QOS](#qos)
      - [QOS Class-maps](#qos-class-maps)
      - [QOS Policy-map](#qos-policy-map)
      - [QOS Profiles](#qos-profiles)
      - [Queue Monitor Length](#queue-monitor-length)
      - [Queue Monitor Streaming](#queue-monitor-streaming)
    - [Routing](#routing)
      - [ARP](#arp)
      - [Router Virtual MAC Address](#router-virtual-mac-address)
      - [IP Routing](#ip-routing)
      - [IPv6 Routing](#ipv6-routing)
      - [Router General configuration](#router-general-configuration)
      - [Router BGP Configuration](#router-bgp-configuration)
      - [Router IGMP Configuration](#router-igmp-configuration)
      - [Router OSPF Configuration](#router-ospf-configuration)
      - [Router ISIS Configuration](#router-isis-configuration)
      - [Router Traffic Engineering](#router-traffic-engineering)
      - [Service Routing Configuration BGP](#service-routing-configuration-bgp)
      - [Service Routing Protocols Model](#service-routing-protocols-model)
      - [Static Routes](#static-routes)
      - [IPv6 Static Routes](#ipv6-static-routes)
      - [VRF Instances](#vrf-instances)
    - [Router L2 VPN](#router-l2-vpn)
    - [Spanning Tree](#spanning-tree)
    - [Terminal Settings](#terminal-settings)
    - [Traffic Policies](#traffic-policies)
    - [Virtual Source NAT](#virtual-source-nat)
    - [VLANs](#vlans)
    - [MAC Address-table](#mac-address-table)
  - [Upgrade of eos_cli_config_gen data model](#upgrade-of-eos_cli_config_gen-data-model)
    - [Versioning](#versioning)
    - [Example Playbooks](#example-playbooks)
  - [License](#license)

## Overview

**eos_cli_config_gen**, is a role that generates eos cli syntax and device documentation.

The **eos_cli_config_gen** role:

- Designed to generate the intended configuration offline, without relying on switch current state information.
- Facilitates the evaluation of the configuration prior to deployment with tools like [Batfish](https://www.batfish.org/)
- Facilitates the evaluation of the configuration post deployment with [eos_validate_state](../eos_validate_state) role.

## Role Inputs and Outputs

Figure 1 below provides a visualization of the roles inputs, and outputs and tasks in order executed by the role.

![Figure 1: Ansible Role eos_cli_config_gen](media/role_eos_cli_config_gen.gif)

**Inputs:**

- Structured EOS configuration file in yaml format.

**Outputs:**

- EOS configuration in CLI format.
- Device Documentation in Markdown format.

**Tasks:**

1. Include device structured configuration that was previously generated.
2. Generate EOS configuration in CLI format.
3. Generate Device Documentation in Markdown format.

## Requirements

Requirements are located here: [avd-requirements](../../README.md#Requirements)

## Input Variables

- The input variables are documented inline within yaml formatted output with: "< >"
- Variables are organized in order of how they appear in the CLI syntax.
- Available features  and variables may vary by platforms, refer to documentation on arista.com for specifics.
- All values are optional.

### ACLs

#### IP Extended Access-Lists

AVD currently supports 2 different data models for extended ACLs:

- The legacy `access_lists` data model, for compatibility with existing deployments
- The improved `ip_access_lists` data model, for access to more EOS features

Both data models can coexists without conflicts, as different keys are used: `access_lists` vs `ip_access_lists`.
Access list names must be unique.

The legacy data model supports simplified ACL definition with `sequence_number` to `action_string` mapping:

```yaml
access_lists:
  - name: < access_list_name_1 >
    counters_per_entry: < true | false >
    sequence_numbers:
      - sequence: < sequence_id_1 >
        action: "< action as string >"
      - sequence: < sequence_id_2 >
        action: "< action as string >"
  - name: < access_list_name_2 >
    counters_per_entry: < true | false >
    sequence_numbers:
      - sequence: < sequence_id_1 >
        action: "< action as string >"
```

The improved data model has a more sophisticated design documented below:

```yaml
ip_access_lists:
  - name: "< access list name as string >"
    counters_per_entry: < true | false >
    entries:
      # remark entry
      - sequence: < acl entry sequence number >  # optional
        # NOTE: if remark is defined, other keys in acl entry will be ignored
        remark: "< Comment, up to 100 characters >"
      # normal entry
      - sequence: < acl entry sequence number >  # optional
        action: "< permit | deny >"  # required
        protocol: "< ip | tcp | udp | icmp | other protocol name or number >"  # required
        # NOTE: A.B.C.D without a mask means host
        source: "< any | A.B.C.D/E | A.B.C.D >"  # required
        source_ports_match: "< eq | gt | lt | neq | range | default -> eq >"
        source_ports: ["< tcp/udp port name or number >",]  # optional
        # NOTE: A.B.C.D without a mask means host
        destination: "< any | A.B.C.D/E | A.B.C.D >"  # required
        destination_ports_match: "< eq | gt | lt | neq | range| default -> eq >"
        destination_ports: ["< tcp/udp port name or number >",]  # optional
        tcp_flags: ["< tcp flag name >",]  # optional
        fragments: < true | false >  # optional, match non-head fragment packets
        log: < true | false >  # optional, log matches against this rule
        ttl: < <0-254> TTL value >  # optional
        ttl_match: "< eq | gt | lt | neq| default -> eq >"  # optional
        icmp_type: "< Message type name/number for ICMP packets >"  # optional
        icmp_code: "< Message code for ICMP packets >"  # optional
        nexthop_group: "< nexthop-group name >"  # optional
        tracked: < true | false > # optional, match packets in existing ICMP/UDP/TCP connections
        dscp: "< DSCP value or name >"  # optional
        vlan_number: < vlan number >  # optional
        vlan_inner: < true | false| default -> false >  # optional
        vlan_mask: "< 0x000-0xFFF  Vlan mask >"  # optional
```

The improved data model allows to limit the number of ACL entries that AVD is allowed to generate by defining `ip_access_lists_max_entries`.
Only normal entries under `ip_access_lists` will be counted, remarks will be ignored.
If the number is above the limit, the playbook will fail. This provides a simplified control over hardware utilization.
The numbers must be based on the hardware tests and AVD does not provide any guidance. Note that other EOS features may use the same hardware resources and affect the supported scale.

```yaml
ip_access_lists_max_entries: <maximum number of ACL entries allowed per switch>  # optional
```

#### IPv6 Standard Access-Lists

```yaml
ipv6_standard_access_lists:
  - name : < ipv6_access_list_name_1 >
    counters_per_entry: < true | false >
    sequence_numbers:
      - sequence : < sequence_id_1 >
        action: "< action as string >"
      - sequence : < sequence_id_2 >
        action: "< action as string >"
  - name : < ipv6_access_list_name_2 >
    sequence_numbers:
      - sequence : < sequence_id_1 >
        action: "< action as string >"
```

#### IP Standard Access-Lists

```yaml
standard_access_lists:
  - name: < access_list_name_1 >
    counters_per_entry: < true | false >
    sequence_numbers:
      - sequence: < sequence_id_1 >
        action: "< action as string >"
      - sequence: < sequence_id_2 >
        action: "< action as string >"
  - name: < access_list_name_2 >
    sequence_numbers:
      - sequence: < sequence_id_1 >
        action: "< action as string >"
```

#### IPv6 Extended Access-Lists

```yaml
ipv6_access_lists:
  - name: < ipv6_access_list_name_1 >
    counters_per_entry: < true | false >
    sequence_numbers:
      - sequence: < sequence_id_1 >
        action: "< action as string >"
      - sequence: < sequence_id_2 >
        action: "< action as string >"
  - name: < ipv6_access_list_name_2 >
    sequence_numbers:
      - sequence: < sequence_id_1 >
        action: "< action as string >"
```

#### MAC Access-Lists

```yaml
mac_access_lists:
  - name: < mac_access_list_name_1 >
    counters_per_entry: < true | false >
    entries:
      - sequence: < sequence_id_1 >
        action: "< action as string >"
      - sequence: < sequence_id_2 >
        action: "< action as string >"
  - name: < mac_access_list_name_2 >
    entries:
      - sequence: < sequence_id_1 >
        action: "< action as string >"
```

### Aliases

```yaml
aliases: |
< list of alias commands in EOS CLI syntax >
```

### Authentication

#### AAA Authentication

```yaml
aaa_authentication:
  login:
    default: < group group_name | local | none > < group group_name | local | none >
    console: < group group_name | local | none > < group group_name | local | none >
  enable:
    default: < group group_name | local | none > < group group_name | local | none >
  dot1x:
    default: < group group_name >
  policies:
    on_failure_log: < true | false >
    on_success_log: < true | false >
    local:
      allow_nopassword: < false | true >
    lockout:
      failure: < 1-255 >
      duration: < 1-4294967295 >
      window: < 1-4294967295 >
```

#### AAA Authorization

```yaml
aaa_authorization:
  exec:
    default: < group group_name | local | none > < group group_name | local | none >
  config_commands: < true | false >
  serial_console: < true | false >
  commands:
    all_default: < group group_name | local | none > < group group_name | local | none >
    privilege:
      - level: < privilege level(s) 0-15 >
        default: < group group_name | local | none > < group group_name | local | none >
```

#### AAA Accounting

```yaml
aaa_accounting:
  exec:
    console:
      type: < none | start-stop | stop-only >
      group: < group_name >
    default:
      type: < none | start-stop | stop-only >
      group: < group_name >
  system:
    default:
      type: < none | start-stop | stop-only >
      group: < group_name >
  commands:
    console:
      - commands: < all | 0-15 >
        type: < none | start-stop | stop-only >
        group: < group_name >
        logging: < true | false >
      - commands: < all | 0-15 >
        type: < none | start-stop | stop-only >
        group: < group_name >
        logging: < true | false >
    default:
      - commands: < all | 0-15 >
        type: < none | start-stop | stop-only >
        group: < group_name >
        logging: < true | false >
      - commands: < all | 0-15 >
        type: < none | start-stop | stop-only >
        group: < group_name >
        logging: < true | false >
```

#### AAA Root

```yaml
aaa_root:
  secret:
    sha512_password: "< sha_512_password >"
```

#### AAA Server Groups

```yaml
aaa_server_groups:
  - name: < server_group_name >
    type: < tacacs+ | radius | ldap >
    servers:
      - server: < server1_ip_address >
        vrf: < vrf_name >
      - server: < server1_ip_address >
        vrf: < vrf_name >
  - name: < server_group_name >
    type: < tacacs+ | radius | ladp >
    servers:
      - server: < host1_ip_address >
```

#### Enable Password

```yaml
enable_password:
  hash_algorithm: < md5 | sha512 >
  key: "< hashed_password >"
```

#### IP RADIUS Source Interfaces

```yaml
ip_radius_source_interfaces:
  - name: < interface_name_1 >
    vrf: < vrf_name_1 >
  - name: < interface_name_2 >
    vrf: < vrf_name_2 >
```

#### IP TACACS+ Source Interfaces

```yaml
ip_tacacs_source_interfaces:
    - name: <interface_name_1 >
      vrf: < vrf_name_1 >
    - name: <interface_name_2 >
```

#### Local Users

```yaml
local_users:
  - name: < user_1 >
    disabled: < true | false | default -> false >
    privilege: < 1-15 >
    role: < role >
    sha512_password: "< sha_512_password >"
    no_password: < true | do not configure a password for given username. sha512_password MUST not be defined for this user. >
    ssh_key: "< ssh_key_string >"
  - name: < user_2 >
    disabled: < true | false | default -> false >
    privilege: < 1-15 >
    role: < role >
    sha512_password: "< sha_512_password >"
    no_password: < true | do not configure a password for given username. sha512_password MUST not be defined for this user. >
    ssh_key: "< ssh_key_string >"
```

#### Roles

```yaml
roles:
  - name: < role_name >
    sequence_numbers:
      - sequence: < sequence_number_1 >
        action: < permit | deny >
        mode: < "config" | "config-all" | "exec" | "<mode>" >
        command: < command as string >
      - sequence: < sequence_number_2 >
        action: < permit | deny >
        mode: < "config" | "config-all" | "exec" | "<mode>" >
        command: < command as string >
```

#### Radius Servers

```yaml
radius_servers:
  - host: < host IP address or name >
    vrf: < vrf_name >
    key: < encrypted_key >
```

#### Tacacs+ Servers

```yaml
tacacs_servers:
  hosts:
    - host: < host1_ip_address >
      vrf: < vrf_name >
      key: < encrypted_key >
      key_type: < 0 | 7 | 8a | default -> 7 >
      single_connection: < true | false >
    - host: < host2_ip_address >
      key: < encrypted_key >
      timeout: < timeout in seconds >
  policy_unknown_mandatory_attribute_ignore: < true | false >
```

### Banners

```yaml
banners:
  login: |
    < text ending with EOF >
  motd: |
    < text ending with EOF >
```

### Router BFD

```yaml
router_bfd:
  interval: < rate in milliseconds >
  min_rx: < rate in milliseconds >
  multiplier: < 3-50 >
  multihop:
    interval: < rate in milliseconds >
    min_rx: < rate in milliseconds >
    multiplier: < 3-50 >
```

### Custom Templates

```yaml
custom_templates:
  - < template 1 relative path below playbook directory >
  - < template 2 relative path below playbook directory >
```

### DHCP Relay

```yaml
dhcp_relay:
  servers:
    - < server_ip_or_hostname >
  tunnel_requests_disabled: < true | false >
```

### EOS CLI

```yaml
# EOS CLI rendered directly on the root level of the final EOS configuration
eos_cli: |
  < multiline eos cli >
```

### Errdisable

```yaml
errdisable:
  detect:
    causes:
      - acl
      - arp-inspection
      - dot1x
      - link-change
      - tapagg
      - xcvr-misconfigured
      - xcvr-overheat
      - xcvr-power-unsupported
      - xcvr-unsupported
  recovery:
    causes:
      - arp-inspection
      - bpduguard
      - dot1x
      - hitless-reload-down
      - lacp-rate-limit
      - link-flap
      - no-internal-vlan
      - portchannelguard
      - portsec
      - speed-misconfigured
      - tapagg
      - uplink-failure-detection
      - xcvr-misconfigured
      - xcvr-overheat
      - xcvr-power-unsupported
      - xcvr-unsupported
    interval: < seconds | default = 300 >
```

### Filters

#### Prefix Lists

```yaml
prefix_lists:
  - name: < prefix_list_name_1 >
    sequence_numbers:
      - sequence: < sequence_id_1 >
        action: "< action as string >"
      - sequence: < sequence_id_2 >
        action: "< action as string >"
  - name: < prefix_list_name_2 >
    sequence_numbers:
      - sequence: < sequence_id_1 >
        action: "< action as string >"
```

#### IPv6 Prefix Lists

```yaml
ipv6_prefix_lists:
  - name: < ipv6_prefix_list_name_1 >
    sequence_numbers:
      - sequence: < sequence_id_1 >
        action: "< action as string >"
      - sequence: < sequence_id_2 >
        action: "< action as string >"
  - name: < ipv6_prefix_list_name_2 >
    sequence_numbers:
      - sequence: < sequence_id_1 >
        action: "< action as string >"
```

#### Community Lists

```yaml
community_lists:
  - name: < community_list_name_1 >
    action: "< action as string >"
  - name: < community_list_name_2 >
    action: "< action as string >"
```

#### IP Extended Community Lists

```yaml
ip_extcommunity_lists:
  - name: < community_list_name_1 >
    entries:
      - type: < permit | deny >
        extcommunities: "< communities as string >"
  - name: < community_list_name_2 >
    entries:
      - type: < permit | deny >
        extcommunities: "< communities as string >"
```

#### IP Extended Community Lists RegExp

```yaml
ip_extcommunity_lists_regexp:
  - name: < community_list_name >
    entries:
      - type: < permit | deny >
        regexp: "< string >"
```

#### Peer Filters

```yaml
peer_filters:
  - name: < peer_filter_name_1
    sequence_numbers:
      - sequence: < sequence_id_1 >
        match: "< match as string >"
      - sequence: < sequence_id_2 >
        match: "< match as string >"
  - name: < peer_filter_name_2
    sequence_numbers:
      - sequence: < sequence_id_1 >
        match: "< match as string >"
```

#### Route Maps

```yaml
route_maps:
  - name: < route_map_name_1 >
    sequence_numbers:
      - sequence: < sequence_id_1 >
        type: < permit | deny >
        description: < description >
        match:
          - "< match rule 1 as string >"
          - "< match rule 2 as string >"
        set:
          - "< set as string >"
        sub_route_map: < sub-route-map name >
        continue:
          enabled: < true | false >
          sequence_number: < integer >
      - sequence: < sequence_id_2 >
        type: < permit | deny >
        match:
          - "< match as string >"
  - name: < route_map_name_2 >
    sequence_numbers:
      - sequence: < sequence_id_1 >
        type: < permit | deny >
        description: < description >
        set:
          - "< set rule 1 as string >"
          - "< set rule 2 as string >"
```

#### Match Lists

```yaml
match_list_input:
  string:
    - name: < match_list_1 >
      sequence_numbers:
        - sequence: < sequence_id 1 >
          match_regex: < match string >
```

#### AS Path

```yaml
as_path:
  regex_mode: < asn | string >
  access_lists:
    - name: < access_list_name_1 >
      entries:
        - type: < permit | deny >
          match: "< regex to match >"
          origin: < "any" | "egp" | "igp" | "incomplete" | default -> "any" >
```

### Generate Device Documentation

```yaml
generate_device_documentation: < true | false | default -> true >
```

### Generate Default Config

The `generate_default_config` knob allows to omit default EOS configuration.
This can be useful when leveraging `eos_cli_config_gen` to generate configlets with CloudVision.

The following commands will be omitted when `generate_default_config` is set to `false`:

- RANCID Content Type
- Hostname
- Default configuration for `aaa`
- Default configuration for `enable password`
- Transceiver qsfp default mode
- End of configuration delimiter

```yaml
generate_default_config: < true | false | default -> true >
```

### Hardware

#### Hardware Counters

```yaml
hardware_counters:
  features:
    - name: <feature_1>
      direction: < in | out >
    - name: <feature_1>
      direction: < in | out >
```

#### Hardware TCAM Profiles

```yaml
tcam_profile:
  system: < tcam profile name to activate >
  profiles:
    - name: < tcam_profile 01 >
      config: "{{ lookup('file', '< path to TCAM profile using EOS syntax >') }}"
```

#### Platform

```yaml
platform:
  trident:
    forwarding_table_partition: < partition >
  sand:
    lag:
      hardware_only: < true | false >
      mode: < mode | default -> 1024x16 >
    forwarding_mode: < petraA | arad >
    multicast_replication:
      default: ingress
```

#### Redundancy

```yaml
redundancy:
  protocol: < redundancy_protocol >
```

#### Speed-Group Settings

```yaml
hardware:
  speed_groups:
    - speed_group: <group>
      serdes: < 10g | 25g >
    - speed_group: <group>
      serdes: < 10g | 25g >
    ...
```

### Interfaces

#### Ethernet Interfaces

##### Routed Ethernet Interfaces

```yaml
# Routed Interfaces
ethernet_interfaces:
  - name: <Ethernet_interface_1 >
    description: < description >
    shutdown: < true | false >
    speed: < interface_speed | forced interface_speed | auto interface_speed >
    mtu: < mtu >
    # l3dot1q and l2dot1q are used for sub-interfaces.
    # The parent interface should be defined as routed.
    type: < routed | switched | l3dot1q | l2dot1q >
    vrf: < vrf_name >
    error_correction_encoding:
      enabled: < true | false | default -> true >
      fire_code: < true | false >
      reed_solomon: < true | false >
    link_tracking_groups:
      - name: < group_name >
        direction: < upstream | downstream >
    encapsulation_dot1q_vlan: < vlan tag to configure on sub-interface >
    encapsulation_vlan:
      client:
        dot1q:
          vlan: < Client VLAN ID >
        outer: < Client Outer VLAN ID >
        inner: < Client Inner VLAN ID >
        unmatched: < true | false >
      # network encapsulation is all optional, and skipped if using client unmatched.
      network:
        dot1q:
          vlan: < Network VLAN ID >
        outer: < Network Outer VLAN ID >
        inner: < Network Inner VLAN ID >
        client: < true | false >
    vlan_id: < 1-4094 >
    ip_address: < IPv4_address/Mask >
    ip_address_secondaries:
      - < IPv4_address/Mask >
      - < IPv4_address/Mask >
    ip_helpers:
      - ip_helper: < ip_helper1 >
        source_interface: < source_interface_name >
        vrf: < vrf_name >
      - ip_helper: < ip_helper2 >
        source_interface: < source_interface_name >
        vrf: < vrf_name >
    ipv6_enable: < true | false >
    ipv6_address: < IPv6_address/Mask >
    ipv6_address_link_local: < link_local_IPv6_address/Mask >
    ipv6_nd_ra_disabled: < true | false >
    ipv6_nd_managed_config_flag: < true | false >
    ipv6_nd_prefixes:
      - ipv6_prefix: < IPv6_address_1/Mask >
        valid_lifetime: < infinite or lifetime in seconds >
        preferred_lifetime: < infinite or lifetime in seconds >
        no_autoconfig_flag: < true | false >
      - ipv6_prefix: < IPv6_address_2/Mask >
    access_group_in: < access_list_name >
    access_group_out: < access_list_name >
    ipv6_access_group_in: < ipv6_access_list_name >
    ipv6_access_group_out: < ipv6_access_list_name >
    mac_access_group_in: < mac_access_list_name >
    mac_access_group_out: < mac_access_list_name >
    ospf_network_point_to_point: < true | false >
    ospf_area: < ospf_area >
    ospf_cost: < ospf_cost >
    ospf_authentication: < none | simple | message-digest >
    ospf_authentication_key: "< encrypted_password >"
    ospf_message_digest_keys:
      - id: < id >
        hash_algorithm: < md5 | sha1 | sha 256 | sha384 | sha512 >
        key: "< encrypted_password >"
    pim:
      ipv4:
        sparse_mode: < true | false >
    mac_security:
      profile: < profile >
    isis_enable: < ISIS Instance >
    isis_passive: < boolean >
    isis_metric: < integer >
    isis_network_point_to_point: < boolean >
    isis_circuit_type: < level-1-2 | level-1 | level-2 >
    isis_hello_padding: < true | false >
    isis_authentication_mode: < text | md5 >
    isis_authentication_key: < type-7 encrypted password >
    ptp:
      enable: < true | false >
      announce:
        interval: < integer >
        timeout: < integer >
      delay_req: < integer >
      delay_mechanism: < e2e | p2p >
      sync_message:
        interval: < integer >
      role: < master | dynamic >
      vlan: < all | list of vlans as string >
      transport: < ipv4 | ipv6 | layer2 >
    logging:
      event:
        link_status: < true | false >
        congestion_drops: < true | false >
    lldp:
      transmit: < true | false >
      receive: < true | false >
    service_profile: < qos_profile >
    shape:
      rate: < "< rate > kbps" | "1-100 percent" | "< rate > pps" , supported options are platform dependent >
    qos:
      trust: < dscp | cos | disabled >
      dscp: < dscp-value >
      cos: < cos-value >
    priority_flow_control:
      enabled: < true | false >
      priorities:
        - priority: < 0-7 >
          no_drop: < true | false >
    bfd:
      interval: < rate in milliseconds >
      min_rx: < rate in milliseconds >
      multiplier: < 3-50 >
    service_policy:
      pbr:
        input: < policy-map name >
    mpls:
      ip: < true | false >
      ldp:
        interface: < true | false >
        igp_sync: < true | false >
    lacp_timer:
      mode: < fast | normal >
      multiplier: < 3 - 3000 >
    transceiver:
      media:
        override: < transceiver_type >
    ip_proxy_arp: < true | false >
    # EOS CLI rendered directly on the ethernet interface in the final EOS configuration
    eos_cli: |
      < multiline eos cli >
```

##### Switched Ethernet Interfaces

```yaml
# Switched Interfaces
ethernet_interfaces:
  - name: <Ethernet_interface_2 >
    description: < description >
    shutdown: < true | false >
    speed: < interface_speed | forced interface_speed | auto interface_speed >
    mtu: < mtu >
    l2_mtu: < l2-mtu - if defined this profile should only be used for platforms supporting the "l2 mtu" CLI >
    vlans: "< list of vlans as string >"
    # If setting both native_vlan and native_vlan_tag, native_vlan_tag takes precedence
    native_vlan: < native_vlan_number >
    native_vlan_tag: < boolean | default -> false >
    mode: < access | dot1q-tunnel | trunk | "trunk phone" >
    phone:
      trunk: < tagged | untagged >
      vlan: < 1-4094 >
    trunk_groups:
      - < trunk_group_name_1 >
      - < trunk_group_name_2 >
    l2_protocol:
      encapsulation_dot1q_vlan: < vlan number >
    error_correction_encoding:
      enabled: < true | false | default -> true >
      fire_code: < true | false >
      reed_solomon: < true | false >
    link_tracking_groups:
      - name: < group_name >
        direction: < upstream | downstream >
    evpn_ethernet_segment:
      identifier: < EVPN Ethernet Segment Identifier (Type 1 format) >
      redundancy: < all-active | single-active >
      designated_forwarder_election:
        algorithm: < modulus | preference >
        # preference_value and dont_preempt are set for preference algorithm and are optional
        preference_value: < 0-65535 >
        dont_preempt: < true | false | default -> false >
        hold_time: < integer >
        subsequent_hold_time: < integer >
        candidate_reachability_required: < true | false >
      mpls:
        shared_index: < 1-1024 >
        tunnel_flood_filter_time: < integer >
      route_target: < EVPN Route Target for ESI with format xx:xx:xx:xx:xx:xx >
    flowcontrol:
      received: < "received" | "send" | "on" >
    mac_security:
      profile: < profile >
    channel_group:
      id: < Port-Channel_id >
      mode: < "on" | "active" | "passive" >
    qos:
      trust: < dscp | cos | disabled >
      dscp: < dscp-value >
      cos: < cos-value >
    spanning_tree_bpdufilter: < "enabled" | true | "disabled" >
    spanning_tree_bpduguard: < "enabled" | true | "disabled" >
    spanning_tree_guard: < loop | root | disabled >
    spanning_tree_portfast: < edge | network >
    vmtracer: < true | false >
    ptp:
      enable: < true | false >
      announce:
        interval: < integer >
        timeout: < integer >
      delay_req: < integer >
      delay_mechanism: < e2e | p2p >
      sync_message:
        interval: < integer >
      role: < master | dynamic >
      vlan: < all | list of vlans as string >
      transport: < ipv4 | ipv6 | layer2 >
    service_profile: < qos_profile >
    profile: < interface_profile >
    shape:
      rate: < "< rate > kbps" | "1-100 percent" | "< rate > pps" , supported options are platform dependent >
    storm_control:
      all:
        level: < Configure maximum storm-control level >
        unit: < percent* | pps (optional and is hardware dependant - default is percent)>
      broadcast:
        level: < Configure maximum storm-control level >
        unit: < percent* | pps (optional and is hardware dependant - default is percent)>
      multicast:
        level: < Configure maximum storm-control level >
        unit: < percent* | pps (optional and is hardware dependant - default is percent) >
      unknown_unicast:
        level: < Configure maximum storm-control level >
        unit: < percent* | pps (optional and is hardware dependant - default is percent)>
    bfd:
      interval: < rate in milliseconds >
      min_rx: < rate in milliseconds >
      multiplier: < 3-50 >
    lacp_timer:
      mode: < fast | normal >
      multiplier: < 3 - 3000 >
    lacp_port_priority: < 0-65535 >
    lldp:
      transmit: < true | false >
      receive: < true | false >
      ztp_vlan: < ztp vlan number >
    trunk_private_vlan_secondary: < true | false >
    pvlan_mapping: "< list of vlans as string >"
    vlan_translations:
      - from: < list of vlans as string (only one vlan if direction is "both") >
        to: < vlan_id >
        direction: < in | out | both | default -> both >
    # EOS CLI rendered directly on the ethernet interface in the final EOS configuration
    eos_cli: |
      < multiline eos cli >
```

#### Interface Defaults

```yaml
interface_defaults:
  ethernet:
    shutdown: < true | false >
  mtu: < mtu >
```

#### Switchport Default

```yaml
switchport_default:
  mode: < routed | access >
  phone:
    cos: < 0-7 >
    trunk: < tagged | untagged >
    vlan: < 1-4094 >
```

#### Interface Profiles

```yaml
interface_profiles:
  - name: < interface_profile_1 >
    commands:
      - < command_1 >
      - < command_2 >
```

#### Loopback Interfaces

```yaml
loopback_interfaces:
  - name: < Loopback_interface_1 >
    description: < description >
    shutdown: < true | false >
    vrf: < vrf_name >
    ip_address: < IPv4_address/Mask >
    ip_address_secondaries:
      - < IPv4_address/Mask >
      - < IPv4_address/Mask >
    ipv6_enable: < true | false >
    ipv6_address: < IPv6_address/Mask >
    ip_proxy_arp: < true | false >
    ospf_area: < ospf_area >
    mpls:
      ldp:
        interface: < true | false >

  - name: < Loopback_interface_2 >
    description: < description >
    ip_address: < IPv4_address/Mask >
    isis_enable: < ISIS Instance >
    isis_passive: < boolean >
    isis_metric: < integer >
    isis_network_point_to_point: < boolean >
    node_segment:
      ipv4_index: < integer >
      ipv6_index: < integer >
```

#### Port-Channel Interfaces

```yaml
port_channel_interfaces:
  - name: < Port-Channel_interface_1 >
    description: < description >
    logging:
      event:
        link_status: < true | false >
    shutdown: < true | false >
    vlans: "< list of vlans as string >"
    # l3dot1q and l2dot1q are used for sub-interfaces.
    # The parent interface should be defined as routed.
    type: < routed | switched | l3dot1q | l2dot1q >
    encapsulation_dot1q_vlan: < vlan tag to configure on sub-interface >
    encapsulation_vlan:
      client:
        dot1q:
          vlan: < Client VLAN ID >
        outer: < Client Outer VLAN ID >
        inner: < Client Inner VLAN ID >
        unmatched: < true | false >
      # network encapsulation is all optional, and skipped if using client unmatched.
      network:
        dot1q:
          vlan: < Network VLAN ID >
        outer: < Network Outer VLAN ID >
        inner: < Network Inner VLAN ID >
        client: < true | false >
    vlan_id: < 1-4094 >
    mode: < access | dot1q-tunnel | trunk | "trunk phone" >
    # If setting both native_vlan and native_vlan_tag, native_vlan_tag takes precedence
    native_vlan: < native_vlan_number >
    native_vlan_tag: < boolean | default -> false >
    link_tracking_groups:
      - name: < group_name >
        direction: < upstream | downstream >
    phone:
      trunk: < tagged | untagged >
      vlan: < 1-4094 >
    l2_protocol:
      encapsulation_dot1q_vlan: < vlan number >
    mtu: < mtu >
    mlag: < mlag_id >
    trunk_groups:
      - < trunk_group_name_1 >
      - < trunk_group_name_2 >
    lacp_fallback_timeout: <timeout in seconds, 0-300 (default 90) >
    lacp_fallback_mode: < individual | static >
    qos:
      trust: < dscp | cos | disabled >
      dscp: < dscp-value >
      cos: < cos-value >
    bfd:
      interval: < rate in milliseconds >
      min_rx: < rate in milliseconds >
      multiplier: < 3-50 >
    service_policy:
      pbr:
        input: < policy-map name >
    mpls:
      ip: < true | false >
      ldp:
        interface: < true | false >
        igp_sync: < true | false >
    trunk_private_vlan_secondary: < true | false >
    pvlan_mapping: "< list of vlans as string >"
    vlan_translations:
      - from: < list of vlans as string (only one vlan if direction is "both") >
        to: < vlan_id >
        direction: < in | out | both | default -> both >
    shape:
      rate: < "< rate > kbps" | "1-100 percent" | "< rate > pps" , supported options are platform dependent >
    storm_control:
      all:
        level: < Configure maximum storm-control level >
        unit: < percent* | pps (optional and is hardware dependant - default is percent)>
      broadcast:
        level: < Configure maximum storm-control level >
        unit: < percent* | pps (optional and is hardware dependant - default is percent)>
      multicast:
        level: < Configure maximum storm-control level >
        unit: < percent* | pps (optional and is hardware dependant - default is percent) >
      unknown_unicast:
        level: < Configure maximum storm-control level >
        unit: < percent* | pps (optional and is hardware dependant - default is percent)>
    ip_proxy_arp: < true | false >
    isis_enable: < ISIS Instance >
    isis_passive: < boolean >
    isis_metric: < integer >
    isis_network_point_to_point: < boolean >
    isis_circuit_type: < level-1-2 | level-1 | level-2 >
    isis_hello_padding: < true | false >
    isis_authentication_mode: < text | md5 >
    isis_authentication_key: < type-7 encrypted password >
    # EOS CLI rendered directly on the port-channel interface in the final EOS configuration
    eos_cli: |
      < multiline eos cli >
  - name: < Port-Channel_interface_2 >
    description: < description >
    vlans: "< list of vlans as string >"
    mode: < access | dot1q-tunnel | trunk | "trunk phone" >
    evpn_ethernet_segment:
      redundancy: < all-active | single-active >
      designated_forwarder_election:
        algorithm: < modulus | preference >
        # preference_value and dont_preempt are set for preference algorithm and are optional
        preference_value: < 0-65535 >
        dont_preempt: < true | false | default -> false >
        hold_time: < integer >
        subsequent_hold_time: < integer >
        candidate_reachability_required: < true | false >
      mpls:
        shared_index: < 1-1024 >
        tunnel_flood_filter_time: < integer >
    esi: < EVPN Ethernet Segment Identifier (Type 1 format) >
    rt: < EVPN Route Target for ESI with format xx:xx:xx:xx:xx:xx >
    lacp_id: < LACP ID with format xxxx.xxxx.xxxx >
  - name: < Port-Channel_interface_3 >
    description: < description >
    vlans: "< list of vlans as string >"
    type: < routed | switched | l3dot1q | l2dot1q >
    mode: < access | dot1q-tunnel | trunk | "trunk phone" >
    spanning_tree_bpdufilter: < "enabled" | true | "disabled" >
    spanning_tree_bpduguard: < "enabled" | true | "disabled" >
    spanning_tree_guard: < loop | root | disabled >
    spanning_tree_portfast: < edge | network >
    vmtracer: < true | false >
    ptp:
      enable: < true | false >
      announce:
        interval: < integer >
        timeout: < integer >
      delay_req: < integer >
      delay_mechanism: < e2e | p2p >
      sync_message:
        interval: < integer >
      role: < master | dynamic >
      vlan: < all | list of vlans as string >
      transport: < ipv4 | ipv6 | layer2 >
  - name: < Port-Channel_interface_4 >
    description: < description >
    mtu: < mtu >
    type: < routed | switched | l3dot1q | l2dot1q >
    ip_address: < IP_address/mask >
    ipv6_enable: < true | false >
    ipv6_address: < IPv6_address/mask >
    ipv6_address_link_local: < link_local_IPv6_address/mask >
    ipv6_nd_ra_disabled: < true | false >
    ipv6_nd_managed_config_flag: < true | false >
    ipv6_nd_prefixes:
      - ipv6_prefix: < IPv6_address_1/Mask >
        valid_lifetime: < infinite or lifetime in seconds >
        preferred_lifetime: < infinite or lifetime in seconds >
        no_autoconfig_flag: < true | false >
      - ipv6_prefix: < IPv6_address_2/Mask >
    access_group_in: < access_list_name >
    access_group_out: < access_list_name >
    ipv6_access_group_in: < ipv6_access_list_name >
    ipv6_access_group_out: < ipv6_access_list_name >
    mac_access_group_in: < mac_access_list_name >
    mac_access_group_out: < mac_access_list_name >
    pim:
      ipv4:
        sparse_mode: < true | false >
    service_profile: < qos_profile >
    ospf_network_point_to_point: < true | false >
    ospf_area: < ospf_area >
    ospf_cost: < ospf_cost >
    ospf_authentication: < none | simple | message-digest >
    ospf_authentication_key: "< encrypted_password >"
    ospf_message_digest_keys:
      - id: < id >
        hash_algorithm: < md5 | sha1 | sha 256 | sha384 | sha512 >
        key: "< encrypted_password >"
```

#### VLAN Interfaces

```yaml
vlan_interfaces:
  - name: < Vlan_id_1 >
    description: < description >
    shutdown: < true | false >
    vrf: < vrf_name >
    arp_aging_timeout: < arp_timeout >
    arp_cache_dynamic_capacity: < 0-4294967295 >
    arp_gratuitous_accept: < true | false >
    arp_monitor_mac_address: < true | false >
    ip_proxy_arp: < true | false >
    ip_direct_broadcast: < true | false >
    ip_address: < IPv4_address/Mask >
    ip_address_secondaries:
      - < IPv4_address/Mask >
      - < IPv4_address/Mask >
    ip_virtual_router_addresses:
      - < IPv4_address/Mask | IPv4_address >
      - < IPv4_address/Mask | IPv4_address >
    ip_address_virtual: < IPv4_address/Mask >
    ip_address_virtual_secondaries:
      - < IPv4_address/Mask >
      - < IPv4_address/Mask >
    ip_igmp: < true | false >
    ip_helpers:
      - ip_helper: < ip_helper_address_1 >
        source_interface: < source_interface_name >
        vrf: < vrf_name >
      - ip_helper: < ip_helper_address_2 >
        source_interface: < source_interface_name >
    ipv6_enable: < true | false >
    ipv6_address: < IPv6_address/Mask >
    ipv6_address_virtual: < IPv6_address/Mask >
    ipv6_address_link_local: < link_local_IPv6_address/Mask >
    ipv6_nd_ra_disabled: < true | false >
    ipv6_nd_managed_config_flag: < true | false >
    ipv6_nd_prefixes:
      - ipv6_prefix: < IPv6_address_1/Mask >
        valid_lifetime: < infinite or lifetime in seconds >
        preferred_lifetime: < infinite or lifetime in seconds >
        no_autoconfig_flag: < true | false >
      - ipv6_prefix: < IPv6_address_2/Mask >
    access_group_in: < access_list_name >
    access_group_out: < access_list_name >
    ipv6_access_group_in: < ipv6_access_list_name >
    ipv6_access_group_out: < ipv6_access_list_name >
    multicast:
      ipv4:
        source_route_export:
          enabled: < true | false >
          administrative_distance: < 1-255 >
    ospf_network_point_to_point: < true | false >
    ospf_area: < ospf_area >
    ospf_cost: < ospf_cost >
    ospf_authentication: < none | simple | message-digest >
    ospf_authentication_key: "< encrypted_password >"
    ospf_message_digest_keys:
      - id: < id >
        hash_algorithm: < md5 | sha1 | sha 256 | sha384 | sha512 >
        key: "< encrypted_password >"
    pim:
      ipv4:
        sparse_mode: < true | false >
        local_interface: < local_interface_name >
    ipv6_virtual_router_address: < IPv6_address >
    isis_enable: < ISIS Instance >
    isis_passive: < boolean >
    isis_metric: < integer >
    isis_network_point_to_point: < boolean >
    mtu: < mtu >
    no_autostate: < true | false >
    vrrp:
      virtual_router: < virtual_router_id >
      priority: < instance_priority >
      advertisement_interval: < advertisement_interval>
      preempt_delay_minimum: < minimum_preemption_delay >
      ipv4: < virtual_ip_address >
      ipv6: < virtual_ip_address >
    ip_attached_host_route_export:
      distance: < distance >
    bfd:
      interval: < rate in milliseconds >
      min_rx: < rate in milliseconds >
      multiplier: < 3-50 >
    service_policy:
      pbr:
        input: < policy-map name >
    pvlan_mapping: "< list of vlans as string >"
    # EOS CLI rendered directly on the VLAN interface in the final EOS configuration
    eos_cli: |
      < multiline eos cli >
  - name: < Vlan_id_2 >
    description: < description >
    ip_address: < IPv4_address/Mask >
```

#### VxLAN Interface

```yaml
vxlan_interface:
  Vxlan1:
    description: < description >
    vxlan:
      source_interface: < source_interface_name >
      mlag_source_interface: < source_interface_name >
      udp_port: < udp_port >
      virtual_router_encapsulation_mac_address: < mlag-system-id | ethernet_address (H.H.H) >
      qos:
        # !!!Warning, only few hardware types with software version >= 4.26.0 support the below knobs to configure Vxlan DSCP mapping.
        # For the Traffic Class to be derived based on the outer DSCP field of the incoming VxLan packet, the core ports must be in "DSCP Trust" mode.
        dscp_propagation_encapsulation: < true | false >
        map_dscp_to_traffic_class_decapsulation: < true | false >
      vlans:
        - id: < vlan_id_1 >
          vni: < vni_id_1 >
          multicast_group: < ip_multicast_group_address >
          flood_vteps:
            - < remote_vtep_1_ip_address >
            - < remote_vtep_2_ip_address >
        - id: < vlan_id_2 >
          vni: < vni_id_2 >
          multicast_group: < ip_multicast_group_address >
          flood_vteps:
            - < remote_vtep_1_ip_address >
            - < remote_vtep_2_ip_address >
      vrfs:
        - name: < vrf_name_1 >
          vni: < vni_id_3 >
          multicast_group: < ip_multicast_group_address >
        - name: < vrf_name_2 >
          vni: < vni_id_4 >
          multicast_group: < ip_multicast_group_address >
      flood_vteps:
        - < remote_vtep_1_ip_address >
        - < remote_vtep_2_ip_address >
      flood_vtep_learned_data_plane: < true | false >
    # EOS CLI rendered directly on the Vxlan interface in the final EOS configuration
    eos_cli: |
      < multiline eos cli >
```

### Internal VLAN Order

```yaml
vlan_internal_order:
  allocation: < ascending | descending >
  range:
    beginning: < vlan_id >
    ending: < vlan_id >
```

### IP DHCP Relay

```yaml
ip_dhcp_relay:
  information_option: < true | false >

```

### IP ICMP Redirect

```yaml
ip_icmp_redirect: < true | false >
ipv6_icmp_redirect: < true | false >
```

### LACP

```yaml
lacp:
  port_id:
    range:
      begin: < min_port >
      end: < max_port >
  rate_limit:
    default: < true | false >
  system_priority: < 0-65535 >
```

### Link Tracking Groups

```yaml
link_tracking_groups:
  - name: < group_name >
    links_minimum: < 1-100000 >
    recovery_delay: < 0-3600 >
```

### LLDP

```yaml
lldp:
  timer: < transmission_time >
  timer_reinitialization: < re-init_time >
  holdtime: < hold_time_period >
  management_address: < all | ethernetN | loopbackN | managementN | port-channelN | vlanN >
  vrf: < vrf_name >
  receive_packet_tagged_drop: < true | false >
  tlvs:
    - name: < tlv name 1 >
      transmit: < true | false >
    - name: < tlv name 2 >
      transmit: < true | false >
  run: < true | false >
```

### MACsec

```yaml
mac_security:
  license:
    license_name: < license-name >
    license_key: < license-number >
  fips_restrictions: < true | false >
  profiles:
    - name: < profile >
      cipher: < valid-cipher-string >
      connection_keys:
        - id: "< key_id >"
          encrypted_key: "< encrypted_key >"
          fallback: < true | false -> default >
      mka:
        key_server_priority: < 0 - 255 >
        session:
          rekey_period: < 30-100000 in seconds >
      sci: < true | false >
      l2_protocols:
        ethernet_flow_control:
          mode: < encrypt | bypass >
        lldp:
          mode: < bypass | bypass unauthorized >
```

### Maintenance Mode

#### BGP Groups

```yaml
bgp_groups:
  - name: < group_name >
    vrf: "< vrf_name >"
    neighbors:
      - "< ip_address >"
      - "< ipv6_address >"
      - "< peer_group_name >"
    bgp_maintenance_profiles:
      - < profile_name >
```

#### Interface Groups

```yaml
interface_groups:
  - name: < group_name >
    interfaces:
      - "< interface_or_interface_range >"
    bgp_maintenance_profiles:
      - "< profile_name >"
    interface_maintenance_profiles:
      - "< profile_name >"
```

#### Profiles and units

```yaml
maintenance:
  default_interface_profile: < interface_profile_1 >
  default_bgp_profile: < bgp_profile_1 >
  default_unit_profile: < unit_profile_1 >
  interface_profiles:
    - name: < interface_profile_1 >
      rate_monitoring:
        load_interval: < seconds >
        threshold: < kbps >
      shutdown:
        max_delay: < seconds >
  bgp_profiles:
    - name: < bgp_profile_1 >
      initiator:
        route_map_inout: < route_map >
  unit_profiles:
    - name: < unit_profile_1 >
      on_boot:
        duration: < 300-3600 >
  units:
    - name: < unit_name_1 >
      quiesce: < true | false >
      profile: < unit_profile_1 >
      groups:
        bgp_groups:
          - < bgp_group_1>
          - < bgp_group_2>
        interface_groups:
          - < interface_group_1>
          - < interface_group_2>
```

### Management

#### Clock

```yaml
clock:
  timezone: < timezone >
```

#### DNS Domain

```yaml
dns_domain: < domain_name >
```

#### Domain Name Servers

```yaml
name_server:
  source:
    vrf: < vrf_name >
  nodes:
    - < name_server_1 >
    - < name_server_2 >
```

#### Domain Lookup

```yaml
ip_domain_lookup:
  source_interfaces:
    - name: < source_interface_1 >
      vrf: < vrf_name >
```

#### Domain-List

```yaml
domain_list:
  - < domain_name_1 >
  - < domain_name_2 >
```

#### Management Interfaces

```yaml
management_interfaces:
  - name: < Management_interface_1 >
    description: < description >
    shutdown: < true | false >
    vrf: < vrf_name >
    ip_address: < IPv4_address/Mask >
    ipv6_enable: < true | false >
    ipv6_address: < IPv6_address/Mask >
    type: < oob | inband | default -> oob >
    # For documentation purpose only
    gateway: < IPv4 address of default gateway in management VRF >
    ipv6_gateway: < IPv6 address of default gateway in management VRF >
```

#### Management HTTP

```yaml
management_api_http:
  enable_http: < true | false >
  enable_https: < true | false >
  https_ssl_profile: < SSL Profile Name >
  enable_vrfs:
    - name: < vrf_name_1 >
      access_group: < Standard IPv4 ACL name >
      ipv6_access_group: < Standard IPv6 ACL name >
    - name: < vrf_name_2 >
      access_group: < Standard IPv4 ACL name >
      ipv6_access_group: < Standard IPv6 ACL name >
  protocol_https_certificate:
    # Both < certificate > and < private_key > must be defined for this feature to work
    certificate: < Certificate >
    private_key: < Private Key >
```

#### IP HTTP Client Source Interfaces

```yaml
ip_http_client_source_interfaces:
    - name: <interface_name_1>
      vrf: <vrf_name_1>
    - name: <interface_name_2>
      vrf: <vrf_name_2>
```

#### Management GNMI

```yaml
management_api_gnmi:
  enable_vrfs:
    - name: < vrf_name_1 >
      access_group: < Standard IPv4 ACL name >
    - name: < vrf_name_2 >
      access_group: < Standard IPv4 ACL name >
  octa:
```

!!! info "gNMI provider"
    Octa activates `eos-native` provider and it is the only provider currently supported by EOS.

#### Management Console

```yaml
management_console:
  idle_timeout: < 0-86400 in minutes >
```

#### Management Security

```yaml
management_security:
  entropy_source: < entropy_source >
  password:
    minimum_length: < 1-32 >
    encryption_key_common: < true | false >
    encryption_reversible: < aes-256-gcm >
  ssl_profiles:
    - name: <ssl_profile_1>
      tls_versions: < list of allowed tls versions as string >
      # cipher_list syntax follows the openssl cipher strings format
      cipher_list: < column separated list of allowed ciphers as a string >
      certificate:
        file: < certificate filename >
        key: < key filename >
    - name: <ssl_profile_2>
      tls_versions: < list of allowed tls versions as string >
```

#### Management SSH

```yaml
management_ssh:
  access_groups:
    - name: < standard_acl_name_1 >
    - name: < standard_acl_name_2 >
      vrf: < vrf name >
  ipv6_access_groups:
    - name: < standard_acl_name_1 >
    - name: < standard_acl_name_2 >
      vrf: < vrf name >
  idle_timeout: < 0-86400 in minutes >
  cipher:
    - < cipher1 >
    - < cipher2 >
  key_exchange:
    - < method1 >
    - < method2 >
  mac:
    - < mac_algorithm1 >
    - < mac_algorithm2 >
  hostkey:
    server:
      - < algorithm1 >
      - < algorithm2 >
  enable: < true | false >
  connection:
    limit: < 1-100 SSH Connections >
    per_host: < 1-20 max sessions from a host >
  vrfs:
    - name: < vrf_name_1 >
      enable: < true | false >
    - name: < vrf_name_2 >
      enable: < true | false >
  log_level: < SSH daemon log level >
```

#### IP SSH Client Source Interfaces

```yaml
ip_ssh_client_source_interfaces:
  - name: < interface_name_1 >
    vrf: < vrf_name_1 | default -> "default" >
  - name: < interface_name_2 >
    vrf: < vrf_name_2 | default -> "default" >
```

#### NTP

```yaml
ntp:
  local_interface:
    name: < source_interface >
    vrf: < vrf_name >
  servers:
    - name: < IP | hostname >
      burst: < true | false >
      iburst: < true | false >
      key: < 1 - 65535 >
      local_interface: < source_interface >
      maxpoll: < 3 - 17 (Logarithmic) >
      minpoll: < 3 - 17 (Logarithmic) >
      preferred: < true | false >
      version: < 1 - 4 >
      vrf: < vrf_name >
  authenticate: <true | false >
  authentication_keys:
    - id: < key_identifier | 1-65534 >
      hash_algorithm: < md5 | sha1 >
      key: "< type7_obfuscated_key >"
  trusted_keys: "< list of trusted-keys as string ex. 10-12,15 >"
```

### MPLS

```yaml
mpls:
  ip: < true | false >
  ldp:
    interface_disabled_default: < true | false >
    router_id: < string >
    shutdown: < true | false >
    transport_address_interface: < interface_name >
```

### Multi-Chassis LAG - MLAG

```yaml
mlag_configuration:
  domain_id: < domain_id_name >
  heartbeat_interval: < milliseconds >
  local_interface: < interface_name >
  peer_address: < IPv4_address >
  peer_address_heartbeat:
    peer_ip: < IPv4_address >
    vrf: < vrf_name >
  dual_primary_detection_delay: < seconds >
  dual_primary_recovery_delay_mlag: < 0 - 1000 >
  dual_primary_recovery_delay_non_mlag: < 0 - 1000 >
  peer_link: < Port-Channel_id >
  reload_delay_mlag: < seconds >
  reload_delay_non_mlag: < seconds >
```

### Multicast

#### IP IGMP Snooping

```yaml
ip_igmp_snooping:
  globally_enabled: < true | false | default -> true >
  robustness_variable: < 1-3 >
  restart_query_interval: < int >
  interface_restart_query: < int >
  fast_leave: < true | false >
  querier:
    enabled: < true | false >
    address: < IP_address >
    query_interval: < int >
    max_response_time: < 1-25 >
    last_member_query_interval: < 1-25 >
    last_member_query_count: < 1-3 >
    startup_query_interval: < int >
    startup_query_count: < 1-3 >
    version: < 1-3 >
  proxy: < true | false >
  vlans:
    - id: < vlan_id >
      enabled: < true | false >
      querier:
        enabled: < true | false >
        address: < IP_address >
        query_interval: < int >
        max_response_time: < 1-25 >
        last_member_query_interval: < 1-25 >
        last_member_query_count: < 1-3 >
        startup_query_interval: < int >
        startup_query_count: < 1-3 >
        version: < 1-3 >
      max_groups: < 0-65534 >
      fast_leave: < true | false >
      # Global proxy settings should be enabled before enabling per-vlan
      proxy: < true | false >
```

`globally_enabled` allows to activate or deactivate IGMP snooping for all vlans where `vlans` allows user to activate / deactivate IGMP snooping per vlan.

#### Router Multicast

```yaml
router_multicast:
  ipv4:
    routing: < true | false >
    multipath: < none | deterministic | "deterministic color" | "deterministic router-id" >
    software_forwarding: < kernel | sfe >
  vrfs:
    - name: < vrf_name >
      ipv4:
        routing: < true | false >
```

#### Routing PIM Sparse Mode

```yaml
router_pim_sparse_mode:
  ipv4:
    bfd: < true | false >
    ssm_range: < range >
    rp_addresses:
      - address: < rp_address_1 >
        groups:
          - < group_prefix_1/mask >
          - < group_prefix_2/mask >
      - address: < rp_address_2 >
    anycast_rps:
      - address: < anycast_rp_address_1 >
        other_anycast_rp_addresses:
          - address: < ip_address_other_anycast_rp_1 >
            register_count: < register_count_nb >
  vrfs:
    - name: < vrf_name >
      ipv4:
        bfd: < true | false >
        rp_addresses:
          - address: < rp_address_1 >
            groups:
              - < group_prefix_1/mask >
              - < group_prefix_2/mask >
```

### Monitoring

#### Daemon TerminAttr

```yaml
daemon_terminattr:
  # Address of the gRPC server on CloudVision
  # TCP 9910 is used on on-prem
  # TCP 443 is used on CV as a Service
  cvaddrs: # For single cluster
    - < ip/fqdn >:<port>
    - < ip/fqdn >:<port>
    - < ip/fqdn >:<port>
  clusters: # For multiple cluster support
    - name: < cluster_name >
      cvaddrs:
        - < ip/fqdn >:<port>
        - < ip/fqdn >:<port>
        - < ip/fqdn >:<port>
      cvauth:
        method: < "token" | "token-secure" | "key" >
        key: < key >
        token_file: < path | e.g. "/tmp/token" >
      cvobscurekeyfile: < true | false >
      cvproxy: < URL >
      cvsourceip: < IP Address >
      cvvrf: < vrf >
  # Authentication scheme used to connect to CloudVision
  cvauth:
    method: < "token" | "token-secure" | "key" >
    key: < key >
    token_file: < path | e.g. "/tmp/token" >
  # The default compression scheme when streaming to CloudVision is gzip since TerminAttr 1.6.1 and CVP 2019.1.0. There is no need to change the compression scheme.
  # Encrypt the private key used for authentication to CloudVision
  cvobscurekeyfile: < true | false >
  # Proxy server through which CloudVision is reachable. Useful when the CloudVision server is hosted in the cloud.
  # The expected form is http://[user:password@]ip:port, e.g.: 'http://arista:arista@10.83.12.78:3128'
  # Available as of TerminAttr v1.13.0
  cvproxy: < URL >
  # set source IP address in case of in-band managament
  cvsourceip: < IP Address >
  # Name of the VRF to use to connect to CloudVision
  cvvrf: < vrf >
  # Stream states from EOS GNMI servers (Openconfig) to CloudVision
  # Available as of TerminAttr v1.13.1
  cvgnmi: < true | false >
  # Disable AAA authorization and accounting. When setting this flag, all commands pushed
  # from CloudVision are applied directly to the CLI without authorization
  disable_aaa: < true | false >
  # Set the gRPC server address, the default is 127.0.0.1:6042
  grpcaddr: < string | e.g. "MGMT/0.0.0.0:6042" >
  # gNMI read-only mode – Disable gnmi.Set()
  grpcreadonly: < true | false >
  # Exclude paths from Sysdb on the ingest side
  ingestexclude: < string | e.g. "/Sysdb/cell/1/agent,/Sysdb/cell/2/agent" >
  # Exclude paths from the shared memory table
  smashexcludes: < string | e.g. "ale,flexCounter,hardware,kni,pulse,strata" >
  # Enable log file collection; /var/log/messages is streamed by default if no path is set.
  taillogs: < path | e.g. "/var/log/messages" >
  # ECO DHCP Collector address or ECO DHCP Fingerprint listening addressin standalone mode (default "127.0.0.1:67")
  ecodhcpaddr: < IPV4_address:port >
  # Enable IPFIX provider (default true)
  # This flag is enabled by default and does not have to be added to the daemon configuration.
  ipfix: < true | false >
  # ECO IPFIX Collector address to listen on to receive IPFIX packets (default "127.0.0.1:4739")
  # This flag is enabled by default and does not have to be added to the daemon configuration
  ipfixaddr: < IPV4_address:port >
  # Enable sFlow provider (default true)
  # This flag is enabled by default and does not have to be added to the daemon configuration
  sflow: < true | false >
  # ECO sFlow Collector address to listen on to receive sFlow packets (default "127.0.0.1:6343")
  # This flag is enabled by default and does not have to be added to the daemon configuration
  sflowaddr: < IPV4_address:port >
  # Subscribe to dynamic device configuration from CloudVision (default false)
  cvconfig: < true | false >
```

You can either provide a list of IPs/FQDNs to target on-premise Cloudvision cluster or use DNS name for your Cloudvision as a Service instance. Streaming to multiple clusters both on-prem and cloud service is supported.

> Note For TerminAttr version recommendation and EOS compatibility matrix, please refer to the latest TerminAttr Release Notes which always contain the latest recommended versions and minimum required versions per EOS release.

#### Custom Daemons

```yaml
daemons:
  - name: < daemon_name >
    exec: "< command to run as a daemon >"
    enabled: "< true | false | default -> true >"
```

This will add a daemon to the eos configuration that is most useful when trying to run OpenConfig clients like ocprometheus

#### Connectivity Monitor

```yaml
monitor_connectivity:
  shutdown: < true | false >
  interval: < probing_interval >
  interface_sets:
    - name: < interface_set >
      # Interface range(s) should be of same type, Ethernet, Loopback, Management etc.
      # Multiple interface ranges can be specified separated by ","
      interfaces: < interface_or_interface_range(s) >
  local_interfaces: < interface_set_name >
  hosts:
    - name: < host_name >
      description: < description >
      ip: < ipv4 >
      local_interfaces: < interface_set_name >
      url: < url >
  vrfs:
    - name: < vrf_name >
      description: < description >
      interface_sets:
        - name: < interface_set >
          interfaces: < interface_or_interface_range(s) >
      local_interfaces: < interface_set_name >
      hosts:
        - name: < host_name >
          description: < description >
          ip: < ipv4 >
          local_interfaces: < interface_set_name >
          url: < url >
```

#### Event Handler

```yaml
### Event Handler ###
event_handlers:
  - name: < event_handler_name >
    action_type: < Type of action. [bash, increment, log] >
    action: < Command to execute >
    delay: < Event-handler delay in seconds >
    trigger: < Configure event trigger condition. Only supports on-logging >
    regex: < Regular expression to use for searching log messages. Required for on-logging trigger >
    asynchronous: < Set the action to be non-blocking. if unset, default is False >
```

#### Event Monitor

```yaml
event_monitor:
  enabled: < true | false >
```

#### Load Interval

```yaml
load_interval:
  default: < seconds >
```

#### Logging

```yaml
logging:
  console: < "<severity_level>" | "disabled" >
  monitor: < "<severity_level>" | "disabled" >
  buffered:
    size: < messages_nb (minimum of 10) >
    level: < "<severity_level>" | "disabled" >
  trap: < "<severity_level>" | "disabled" >
  synchronous:
    level: < "<severity_level>" | "disabled" | default --> critical >
  format:
    timestamp: < high-resolution | traditional >
    hostname: < fqdn | ipv4 >
    sequence_numbers: < true | false >
  facility: < syslog_facility_value >
  source_interface: < source_interface_name >
  vrfs:
    - name: < vrf_name >
      source_interface: < source_interface_name >
      hosts:
        - name: < syslog_server_1 >
          protocol: < tcp | udp (default udp) >
          ports:
            - < custom_port_1 >
            - < custom_port_2 >
        - name: < syslog_server_2 >
          ports:
            - < custom_port_1 >
  policy:
    match:
      match_lists:
        - name: < match_list >
          action: < discard >
```

#### Sflow

```yaml
sflow:
  sample: < sample_rate >
  dangerous: < true | false >
  vrfs:
    - name: <vrf_name_1>
      destinations:
        - destination: < sflow_destination_ip_1>
        - destination: < sflow_destination_ip_2>
          port: < port_number >
      source_interface: < source_interface >
    - name: <vrf_name_2>
      destinations:
        - destination: < sflow_destination_ip_1>
      source_interface: < source_interface >
  destinations:
    - destination: < sflow_destination_ip_1 >
      port: < port_number >
    - destination: < sflow_destination_ip_2 >
  source_interface: < source_interface >
  run: < true | false >
```

#### SNMP Settings

```yaml
snmp_server:
  contact: < contact_name >
  location: < location >
  communities:
    - name: < community_name_1 >
      access: < ro | rw >
      access_list_ipv4:
        name: < acl_ipv4_name >
      access_list_ipv6:
        name: < acl_ipv6_name >
      view: < view_name >
    - name: < community_name_2 >
      access: < ro | rw >
      access_list_ipv4:
        name: < acl_ipv4_name >
      access_list_ipv6:
        name: < acl_ipv6_name >
      view: < view_name >
  ipv4_acls:
    - name: < ipv4-access-list >
      vrf: < vrf >
    - name: < ipv4-access-list >
  ipv6_acls:
    - name: < ipv6-access-list >
      vrf: < vrf >
    - name: < ipv6-access-list >
  local_interfaces:
    - name: < interface_name_1 >
      vrf: < vrf_name >
    - name: < interface_name_2 >
    - name: < interface_name_3 >
      vrf: < vrf_name >
  views:
    - name: < view_name >
      MIB_family_name: < MIB_family_name >
      included: < true | false >
    - name: < view_name >
      MIB_family_name: < MIB_family_name >
      included: < true | false >
  groups:
    - name: < group_name >
      version: < v1 | v2c | v3 >
      authentication: < auth | noauth | priv >
      read: < read_view >
      write: < write_view >
      notify: < notify_view >
    - name: < group_name >
      version: < v1 | v2c | v3 >
      authentication: < auth | noauth | priv >
      read: < read_view >
  users:
    - name: < username >
      group: < group_name >
      version: < v1 | v2c | v3 >
      auth: < hash_algorithm >
      auth_passphrase: < encrypted_auth_passphrase >
      priv: < encryption_algorithm >
      priv_passphrase: < encrypted_priv_passphrase >
    - name: < username >
      group: < group_name >
      version: < v1 | v2c | v3 >
  hosts:
    - host: < host IP address or name >
      vrf: < vrf_name >
      version: < 1 | 2c | 3 >
      community: < community_name >
      users:
        - username: < username >
          authentication_level: < auth | noauth | priv >
    - host: < host IP address or name >
      vrf: < vrf_name >
      community: < community_name >
      users:
        - username: < username >
          authentication_level: < auth | noauth | priv >
  traps:
    # Enable or disable all snmp-traps
    enable: < true | false | default -> false >
    # Enable or disable specific snmp-traps and their sub_traps
    snmp_traps:
      - name: < snmp_trap_type | snmp_trap_type snmp_sub_trap_type >
        enabled: < true | false | default -> true >
      - name: < snmp_trap_type | snmp_trap_type snmp_sub_trap_type >
  vrfs:
    - name: < vrf_name >
      enable: < true | false >
    - name: < vrf_name >
      enable: < true | false >
```

#### Monitor Sessions

```yaml
monitor_sessions:
  - name: < session_name_1 >
    sources:
      - name: < interface_name, range or comma separated list >
        direction: < rx | tx | both >
        access_group:
          type: < ip | ipv6 | mac >
          name: < acl_name >
          priority: < priority >
    destinations:
      - < interface(s) | cpu >
    encapsulation_gre_metadata_tx: < true | false >
    header_remove_size: < bytes >
    access_group:
      type: < ip | ipv6 | mac >
      name: < acl_name >
    rate_limit_per_ingress_chip: < "<int> bps" | "<int> kbps" | "<int> mbps" >
    rate_limit_per_egress_chip: < "<int> bps" | "<int> kbps" | "<int> mbps" >
    sample: < integer >
    truncate:
      enabled: < true | false >
      size: < bytes >
```

### System Control-Plane

```yaml
system:
  control_plane:
    tcp_mss:
      ipv4: < Segment size >
      ipv6: < Segment size >
    ipv4_access_groups:
      - acl_name: < access-list name >
        vrf: < Optional vrf field >
    ipv6_access_groups:
      - acl_name: < access-list name >
        vrf: < Optional vrf field >
```

#### VM Tracer Sessions

```yaml
vmtracer_sessions:
  - name: < vmtracer_session_name_1 >
    url: < url >
    username: < username >
    password: "< encrypted_password >"
    autovlan_disable: < true | false >
    source_interface: < interface_name >
  - name: < vmtracer_session_name_2 >
    url: < url >
    username: < username >
    password: "< encrypted_password >"
```

### Patch Panel

```yaml
patch_panel:
  patches:
    - name: < name >
      enabled: < true | false >
      connectors:
        # Must have exactly two connectors to a patch of which at least one must be of type "interface"
      - id: < string or integer >
        type: < interface | pseudowire >
        endpoint: < interface_name | interface_name dot1q vlan 123 | bgp vpws TENANT_A pseudowire WPWS_PW_1 | ldp LDP_PW_1 >
      - id: < string or integer >
        type: < interface | pseudowire >
        endpoint: < interface_name | interface_name dot1q vlan 123 | bgp vpws TENANT_A pseudowire WPWS_PW_1 | ldp LDP_PW_1 >
```

### PTP

```yaml
ptp:
  mode: < mode >
  forward_unicast: < true | false >
  clock_identity: < clock-id >
  source:
    ip: < source-ip>
  priority1: < priority1 >
  priority2: < priority2 >
  ttl: < ttl >
  domain: < integer >
  message_type:
    general:
      dscp: < dscp-value >
    event:
      dscp: < dscp-Value >
  monitor:
    threshold:
      offset_from_master: < offset >
      mean_path_delay: < delay >
```

### Prompt

```yaml
prompt: <string >
```

### Quality of Services

#### QOS

```yaml
qos:
  map:
    cos:
      - "< cos_mapping_to_tc >"
      - "< cos_mapping_to_tc >"
    dscp:
      - "< dscp_mapping_to_tc >"
      - "< dscp_mapping_to_tc >"
    traffic_class:
      - "< tc_mapping_to_cos >"
      - "< tc_mapping_to_dscp >"
      - "< tc_mapping_to_tx_queue >"
  rewrite_dscp: < true | false >
```

#### QOS Class-maps

```yaml
class_maps:
  pbr:
    - name: < class-map name >
      ip:
        access_group: < Standard access-list name >
  qos:
    - name: < class-map name >
      vlan: < VLAN value(s) or range(s) of VLAN values >
      cos: < CoS value(s) or range(s) of CoS values >
      ip:
        access_group: < IPv4 access-list name >
      ipv6:
        access_group: < IPv6 access-list name >
```

#### QOS Policy-map

```yaml
policy_maps:
  pbr:
    - name: < policy-map name >
      classes:
        - name: < class name >
          index: < integer > # Optional
          # Set only one of the below actions per class
          drop: < true | false >
          set:
            nexthop:
              ip_address: < IPv4_address | IPv6_address >
              recursive: < true | false >
  qos:
    - name: < policy-map name >
      classes:
        - name: < class name >
          set:
            cos: < cos_value >
            dscp: < dscp-code >
            traffic_class: < traffic-class ID >
            drop_precedence: < drop-precedence value >
```

#### QOS Profiles

```yaml
qos_profiles:
  - name: < profile-1 >
    trust: < dscp | cos | disabled >
    cos: < cos-value >
    dscp: < dscp-value >
    shape:
      rate: < "< rate > kbps" | "1-100 percent" | "< rate > pps" , supported options are platform dependent >
    service_policy:
      type:
        qos_input: < policy_map_name >
    tx_queues:
      - id: < tx-queue-id >
        bandwidth_percent: < value >
        # The below knob is platform dependent
        bandwidth_guaranteed_percent: < value >
        priority: < string >
        shape:
          rate: < "< rate > kbps" | "1-100 percent" | "< rate > pps" , supported options are platform dependent >
      - id: < tx-queue-id >
        bandwidth_percent: < value >
        priority: < string >
        shape:
          rate: < "< rate > kbps" | "1-100 percent" | "< rate > pps" , supported options are platform dependent >
  - name: < profile-2 >
    trust: < dscp | cos | disabled >
    cos: < cos-value >
    dscp: < dscp-value >
    tx_queues:
      - id: < tx-queue-id >
        bandwidth_percent: < value >
        priority: < string >
      - id: < tx-queue-id >
        bandwidth_percent: < value >
        priority: < string >
```

#### Queue Monitor Length

```yaml
queue_monitor_length:
  log: < seconds >
  notifying: < true | false - should only be used for platforms supporting the "queue-monitor length notifying" CLI >
```

#### Queue Monitor Streaming

```yaml
queue_monitor_streaming:
  enable: < true | false >
  ip_access_group: < access_list_name >
  ipv6_access_group: < ipv6_access_list_name >
  max_connections: < 1-100 >
  vrf: < vrf_name >
```

### Routing

#### ARP

```yaml
arp:
  aging:
    timeout_default: < timeout-in-seconds >
```

#### Router Virtual MAC Address

```yaml
ip_virtual_router_mac_address: < mac_address (hh:hh:hh:hh:hh:hh) >
```

#### IP Routing

```yaml
ip_routing: < true | false >
```

#### IPv6 Routing

```yaml
ipv6_unicast_routing: < true | false >
ip_routing_ipv6_interfaces: < true | false >
```

#### Router General configuration

```yaml
router_general:
  router_id:
    ipv4: < IPv4_address >
    ipv6: < IPv6_address >
  nexthop_fast_failover: < true | false | default -> false >
  vrfs:
    - name: < destination-vrf >
      leak_routes:
        - source_vrf: < source-vrf >
          subscribe_policy: < route-map policy >
        - source_vrf: < source-vrf >
          subscribe_policy: < route-map policy >
```

#### Router BGP Configuration

```yaml
router_bgp:
  as: < bgp_as >
  router_id: < IPv4_address >
  distance:
    external_routes: < 1-255 >
    internal_routes: < 1-255 >
    local_routes: < 1-255 >
  graceful_restart:
    enabled: < true | false >
    restart_time: < 1-3600 >
    stalepath_time: < 1-3600 >
  # graceful-restart-help long-lived and restart-time are mutually exclusive in CLI
  # restart-time will take precedence if both are configured.
  graceful_restart_helper:
    enabled: < true | false >
    restart_time: < 1-100000000>
    long_lived: < true | false >
  maximum_paths:
    paths: < 1-600 >
    ecmp: < 1-600 >
  updates:
    wait_for_convergence: < true | false >
    wait_install: < true | false >
  bgp_cluster_id: < IPv4_address >
  bgp_defaults:
    - "< bgp command as string >"
    - "< bgp command as string >"
  bgp:
    bestpath:
      d_path: < true | false >
  peer_groups:
    - name: < peer_group_name_1>
      type: < ipv4 | evpn >
      remote_as: < bgp_as >
      local_as: < bgp_as >
      description: "< description as string >"
      shutdown: < true | false >
      peer_filter: < peer_filter >
      next_hop_unchanged: < true | false >
      update_source: < interface >
      route_reflector_client: < true | false >
      bfd: < true | false >
      ebgp_multihop: < integer >
      next_hop_self: < true | false >
      password: "< encrypted_password >"
      default_originate:
        enabled: < true | false >
        always: < true | false >
        route_map: < route_map_name >
      send_community: < standard | extended | large | all >
      maximum_routes: < integer >
      maximum_routes_warning_limit: < "<integer>" | "<0-100> percent" >
      maximum_routes_warning_only: < true | false >
      allowas_in:
        enabled: < true | false >
        times: < 1-10 >
      weight: < weight_value >
      timers: < keepalive_hold_timer_values >
      route_map_in: < inbound route-map >
      route_map_out: < outbound route-map >
    - name: < peer_group_name_2 >
      type: < ipv4 | evpn >
      bgp_listen_range_prefix: < IP prefix range >
      peer_filter: < peer_filter >
      password: "< encrypted_password >"
      maximum_routes: < integer >
  neighbors:
    - ip_address: < IPv4_address_1 >
      peer_group: < peer_group_name >
      remote_as: < bgp_as >
      local_as: < bgp_as >
      description: "< description as string >"
      shutdown: < true | false >
      update_source: < interface >
      bfd: < true | false >
      weight: < weight_value >
      timers: < keepalive_hold_timer_values >
      route_map_in: < inbound route-map >
      route_map_out: < outbound route-map >
      default_originate:
        enabled: < true | false >
        always: < true | false >
        route_map: < route_map_name >
      send_community: < all | extended | large | standard >
      maximum_routes: < integer >
      maximum_routes_warning_limit: < "<integer>" | "<0-100> percent" >
      maximum_routes_warning_only: < true | false >
      allowas_in:
        enabled: < true | false >
        times: < 1-10 >
    - ip_address: < IPv4_address_2 >
      remote_as: < bgp_as >
      next_hop_self: < true | false >
      password: "< encrypted_password >"
    - ip_address: < IPv6_address_1 >
      remote_as: < bgp_as >
  neighbor_interfaces:
    - name: < interface >
      peer_group: < peer_group_name >
      remote_as: < bgp_as >
      description: "< description as string >"
  aggregate_addresses:
    - prefix: < aggregate_address_1/mask >
      advertise_only: < true | false >
    - prefix: < aggregate_address_2/mask >
    - prefix: < aggregate_address_3/mask >
      as_set: < true | false >
      summary_only: < true | false >
      attribute_map: < route_map_name >
      match_map: < route_map_name >
      advertise_only: < true | false >
  redistribute_routes:
    - source_protocol: < route_type >
      route_map: < route_map_name >
    - source_protocol: < route_type >
      route_map: < route_map_name >
  vlan_aware_bundles:
    - name: < vlan_aware_bundle_name_1 >
      rd: "< route distinguisher >"
      rd_evpn_domain:
        domain: < all | remote >
        rd: "< route distinguisher >"
      route_targets:
        both:
          - "< route_target >"
        import:
          - "< route_target >"
          - "< route_target >"
        export:
          - "< route_target >"
          - "< route_target >"
        import_evpn_domains:
          - domain: < all | remote >
            route_target: "< route_target >"
        export_evpn_domains:
          - domain: < all | remote >
            route_target: "< route_target >"
        import_export_evpn_domains:
          - domain: < all | remote >
            route_target: "< route_target >"
      redistribute_routes:
        - < learned >
      no_redistribute_routes:
        - < host-route >
      vlan: < vlan_range >
    - name: < vlan_aware_bundle_name_2 >
      rd: "< route distinguisher >"
      route_targets:
        both:
          - "< route_target >"
        import:
          - "< route_target >"
          - "< route_target >"
        export:
          - "< route_target >"
          - "< route_target >"
        import_evpn_domains:
          - domain: < all | remote >
            route_target: "< route_target >"
        export_evpn_domains:
          - domain: < all | remote >
            route_target: "< route_target >"
      redistribute_routes:
        - < connected >
        - < learned >
      vlan: < vlan_range >
  vlans:
    - id: < vlan_id_1>
      rd: "< route distinguisher >"
      rd_evpn_domain:
        domain: < all | remote >
        rd: "< route distinguisher >"
      route_targets:
        both:
          - "< route_target >"
        import:
          - "< route_target >"
          - "< route_target >"
        export:
          - "< route_target >"
          - "< route_target >"
        import_evpn_domains:
          - domain: < all | remote >
            route_target: "< route_target >"
        export_evpn_domains:
          - domain: < all | remote >
            route_target: "< route_target >"
        import_export_evpn_domains:
          - domain: < all | remote >
            route_target: "< route_target >"
      redistribute_routes:
        - < connected >
        - < learned >
      no_redistribute_routes:
        - < host-route >
    - id: < vlan_id_2 >
      rd: "< route distinguisher >"
      route_targets:
        import:
          - "< route_target >"
          - "< route_target >"
        export:
          - "< route_target >"
          - "< route_target >"
      redistribute_routes:
        - < connected >
        - < learned >
  vpws:
    - name: < vpws instance name >
      rd: < route distinguisher >
      route_targets:
        import_export: < route target >
      mpls_control_word: < true | false, Default -> false >
      label_flow: < true | false, Default -> false >
      mtu: < mtu >
      pseudowires:
        - name: < pseudowire name >
          id_local: < integer, must match id_remote on other pe >
          id_remote: < integer, must match id_local on other pe >
  address_family_evpn:
    domain_identifier: < string >
    neighbor_default:
      encapsulation: < vxlan | mpls >
      next_hop_self_source_interface: < source interface >
      next_hop_self_received_evpn_routes:
        enable: < true | false >
        inter_domain: < true | false >
    peer_groups:
      - name: < peer_group_name >
        activate: < true | false >
        route_map_in: < route_map_name >
        route_map_out: < route_map_name >
        domain_remote: < true | false >
    evpn_hostflap_detection:
      enabled: < true | false >
      threshold: < integer >
      window: < integer >
    route:
      import_match_failure_action: < 'discard' >
  address_family_rtc:
    peer_groups:
      - name: < peer_group_name >
        activate: < true | false >
        default_route_target:
          only: < true | false >
          encoding_origin_as_omit:
  address_family_ipv4:
    networks:
      - prefix: < prefix_ipv4 >
        route_map: < route_map_name >
    peer_groups:
      - name: < peer_group_name >
        route_map_in: < route_map_name >
        route_map_out: < route_map_name >
        activate: < true | false >
      - name: < peer_group_name >
        activate: < true | false >
        prefix_list_in: < prefix_list_name >
        prefix_list_out: < prefix_list_name >
        default_originate:
          always: < true | false >
          route_map: < route_map_name >
        next_hop:
          address_family_ipv6_originate: < true | false >
    neighbors:
      - ip_address: < neighbor_ip_address>
        route_map_in: < route_map_name >
        route_map_out: < route_map_name >
        activate: < true | false >
        prefix_list_in: < prefix_list_name >
        prefix_list_out: < prefix_list_name >
      - ip_address: < neighbor_ip_address>
        activate: < true | false >
        default_originate:
          always: < true | false >
          route_map: < route_map_name >
  address_family_ipv4_multicast:
    peer_groups:
      - name: < peer_group_name >
        route_map_in: < route_map_name >
        route_map_out: < route_map_name >
        activate: < true | false >
      - name: < peer_group_name >
        activate: < true | false >
    neighbors:
      - ip_address: < neighbor_ip_address >
        route_map_in: < route_map_name >
        route_map_out: < route_map_name >
        activate: < true | false >
    redistribute_routes:
      - source_protocol: < route_type >
        route_map: < route_map_name >
  address_family_ipv6:
    networks:
      - prefix: < prefix_ipv6 >
        route_map: < route_map_name >
    peer_groups:
      - name: < peer_group_name >
        activate: < true | false >
        route_map_in: < route_map_name >
        route_map_out: < route_map_name >
        prefix_list_in: < prefix_list_name >
        prefix_list_out: < prefix_list_name >
      - name: < peer_group_name >
        activate: true
    neighbors:
      - ip_address: < neighbor_ip_address >
        route_map_in: < route_map_name >
        route_map_out: < route_map_name >
        prefix_list_in: < prefix_list_name >
        prefix_list_out: < prefix_list_name >
        activate: < true | false >
    redistribute_routes:
      - source_protocol: < route_type >
        route_map: < route_map_name >
      - source_protocol: < route_type >
        route_map: < route_map_name >
  address_family_vpn_ipv4:
    domain_identifier: < string >
    peer_groups:
      - name: < peer_group_name >
        activate: < true | false >
    neighbors:
      - ip_address: < neighbor_ip_address >
        activate: < true | false >
    neighbor_default_encapsulation_mpls_next_hop_self:
      source_interface: < interface >
  address_family_vpn_ipv6:
    domain_identifier: < string >
    peer_groups:
      - name: < peer_group_name >
        activate: < true | false >
    neighbors:
      - name: < neighbor_ip_address >
        activate: < true | false >
    neighbor_default_encapsulation_mpls_next_hop_self:
      source_interface: < interface >
  vrfs:
    - name: < vrf_name_1 >
      rd: "< route distinguisher >"
      evpn_multicast: < true | false >
      # evpn_multicast_address_family requires evpn_multicast: true to be set
      evpn_multicast_address_family:
        ipv4:
          transit: < true | false >
      route_targets:
        import:
          - address_family: < address_family >
            route_targets:
              - "< route_target >"
              - "< route_target >"
          - address_family: < address_family >
            route_targets:
              - "< route_target >"
              - "< route_target >"
        export:
          - address_family: < address_family >
            route_targets:
              - "< route_target >"
              - "< route_target >"
      router_id: < IPv4_address >
      timers: < keepalive_hold_timer_values >
      networks:
        - prefix: < prefix_ipv4 >
          route_map: < route_map_name >
      neighbors:
        - ip_address: < neighbor_ip_address >
          remote_as: < asn >
          peer_group: < peer_group_name >
          password: "< encrypted_password >"
          weight: < weight_value >
          local_as: < asn >
          description: < description >
          ebgp_multihop: < integer >
          next_hop_self: < true | false >
          bfd: < true | false >
          timers: < keepalive_hold_timer_values >
          send_community: < standard | extended | large | all >
          maximum_routes: < integer >
          maximum_routes_warning_limit: < "<integer>" | "<0-100> percent" >
          maximum_routes_warning_only: < true | false >
          allowas_in:
            enabled: < true | false >
            times: < 1-10 >
          default_originate:
            always: < true | false >
            route_map: < route_map_name >
          update_source: < interface >
          route_map_out: < route-map name >
          route_map_in: < route-map name >
          prefix_list_in: < prefix_list_name >
          prefix_list_out: < prefix_list_name >
        - ip_address: < neighbor_ip_address >
          remote_as: < asn >
          description: < description >
          next_hop_self: < true | false >
          timers: < keepalive_hold_timer_values >
          send_community: < standard | extended | large | all >
          shutdown: < true | false >
      redistribute_routes:
        - source_protocol: < route_type >
          route_map: < route_map_name >
        - source_protocol: < route_type >
          route_map: < route_map_name >
      aggregate_addresses:
        - aggregate_addres: < aggregate_address_1/mask >
          advertise_only: < true | false >
        - aggregate_addres: < aggregate_address_2/mask >
        - aggregate_addres: < aggregate_address_3/mask >
          as_set: < true | false >
          summary_only: < true | false >
          attribute_map: < route_map_name >
          match_map: < route_map_name >
          advertise_only: < true | false >
      address_families:
        - address_family: < address_family >
          neighbors:
            - ip_address: < neighbor_ip_address >
              activate: < true | false >
              route_map_out: < route_map_name >
              route_map_in: < route_map_name >
          peer_groups:
            - name: < peer_group >
              activate: < true | false >
              next_hop:
                address_family_ipv6_originate: < true | false >
          networks:
            - prefix: < prefix_address >
              route_map: < route_map_name >
      # EOS CLI rendered directly on the Router BGP, VRF definition in the final EOS configuration
      eos_cli: |
        < multiline eos cli >
    - name: < vrf_name_2 >
      rd: "<route distinguisher >"
      route_targets:
        import:
          - address_family: < address_family >
            route_targets:
              - "< route_target >"
              - "< route_target >"
          - address_family: < address_family >
            route_targets:
              - "< route_target >"
              - "< route_target >"
        export:
          - address_family: < address_family >
            route_targets:
              - "< route_target >"
              - "< route_target >"
      redistribute_routes:
        - source_protocol: < route_type >
          route_map: < route_map_name >
        - source_protocol: < route_type >
          route_map: < route_map_name >
```

#### Router IGMP Configuration

```yaml
router_igmp:
  ssm_aware: < true | false >
```

#### Router OSPF Configuration

```yaml
router_ospf:
  process_ids:
    - id: < process_id >
      vrf: < vrf_name_for_process_id >
      passive_interface_default: < true | false >
      router_id: < IPv4_address >
      distance:
        external: < 1-255 >
        inter_area: < 1-255 >
        intra_area: < 1-255 >
      log_adjacency_changes_detail: < true | false >
      network_prefixes:
        - ipv4_prefix: < IPv4 subnet / netmask >
          area: < area >
        - ipv4_prefix: < IPv4 subnet / netmask >
          area: < area >
      bfd_enable: < true | false >
      no_passive_interfaces:
        - < interface_1 >
        - < interface_2 >
      distribute_list_in:
        route_map: < route_map >
      max_lsa: < integer >
      timers:
        lsa:
          rx_min_interval: < 0-600000 - Min interval in msecs between accepting the same LSA >
          tx_delay:
            initial: < 0-600000 - Delay to generate first occurrence of LSA in msecs >
            min: < 1-600000 Min delay between originating the same LSA in msecs >
            max: < 1-600000 Maximum delay between originating the same LSA in msecs >
        spf_delay:
          initial: < 0-600000 - Initial SPF schedule delay in msecs >
          min: < 0-65535000  Min Hold time between two SPFs in msecs >
          max: < 0-65535000  Max wait time between two SPFs in msecs >
      default_information_originate:
        always: true
      summary_addresses:
        - prefix: < summary_prefix_01 >
          tag: < string >
        - prefix: < summary_prefix_02 >
          attribute_map: < string >
        - prefix: < summary_prefix_03 >
          not_advertise: < true >
        - prefix: < summary_prefix_04 >
        - prefix: < summary_prefix_05 >
      redistribute:
        static:
          route_map: < route_map_name >
        connected:
          route_map: < route_map_name >
        bgp:
          route_map: < route_map_name >
      auto_cost_reference_bandwidth: < bandwidth in mbps >
      areas:
        - id: < area >
          filter:
            networks:
              - < IPv4 subnet / netmask >
              - < IPv4 subnet / netmask >
            prefix_list: < prefix list name >
        - id: < area >
          type: < normal | stub | nssa | default -> normal >
          no_summary: < true | false >
          nssa_only: < true | false >
          default_information_originate:
            metric: < Integer 1-65535 > # Value of the route metric
            metric_type: < 1 | 2 > # OSPF metric type
      maximum_paths: < Integer 1-32 >
      max_metric:
        router_lsa:
          external_lsa:
            override_metric: < Integer 1-16777215 >
          include_stub: < true | false >
          on_startup: < "wait-for-bgp" | Integer 5-86400 >
          summary_lsa:
            override_metric: < Integer 1-16777215 >
      mpls_ldp_sync_default: < true | false >
```

#### Router ISIS Configuration

```yaml

router_isis:
  instance: < ISIS Instance Name >
  net: < CLNS Address to run ISIS | format 49.0001.0001.0000.0001.00 >
  router_id: < IPv4_address >
  is_type: < level-1 | level-1-2 | level-2 >
  log_adjacency_changes: < true | false >
  mpls_ldp_sync_default: < true | false >
  timers:
    local_convergence:
      protected_prefixes: < true | false >
      delay: < number of milliseconds (Optional, default is 10000) >
  advertise:
    passive_only: < true | false >
  address_family: < List of Address Families >
  isis_af_defaults:
    - maximum-paths < Integer 1-128 >
  redistribute_routes:
    - source_protocol: < bgp | connected | isis | ospf | ospfv3 | static >
      route_map: < route_map_name >
      include_leaked: < true | false >
      # ospf_route_type is required with source_protocols 'ospf' and 'ospfv3'
      ospf_route_type: < internal | external | nssa-external >
  address_family_ipv4:
    maximum_paths: < Integer 1-128 >
    fast_reroute_ti_lfa:
      mode: < link-protection | node-protection >
      level: < level-1 | level-2 >
      srlg:
        enable: < true | false >
        strict: < true | false >
    tunnel_source_labeled_unicast:
      enabled: < true | false >
      rcf: < routing_control_function() >
  address_family_ipv6:
    maximum_paths: < Integer 1-128 >
    fast_reroute_ti_lfa:
      mode: < link-protection | node-protection >
      level: < level-1 | level-2 (Optional, default is to protect all levels) >
      srlg:
        enable: < true | false >
        strict: < true | false >
  segment_routing_mpls:
    enabled: < true | false >
    router_id: < router_id >
    prefix_segments:
      - prefix: < IPv4_network/Mask | IPv6_network/Mask >
        index: < integer >
```

#### Router Traffic Engineering

```yaml
router_traffic_engineering:
  router_id:
    ipv4: < IPv4_address >
    ipv6: < IPv6_address >
  segment_routing:
    colored_tunnel_rib: true
    policy_endpoints:
      - address: < IPv4_address | IPv6_address >
        colors:
          - value: < integer >
            binding_sid: < integer >
            description: < description >
            name: < name >
            path_group:
              - preference: < integer >
                explicit_null: < "ipv4" | "ipv6" | "ipv4 ipv6" | "none" >
                segment_list:
                  - label_stack: < integer > < integer > < integer >
                    weight: < integer >
                    index: < integer >
          - value: < integer >
            binding_sid: < integer >
            description: < description >
            name: < name >
            path_group:
              - preference: < integer >
                explicit_null: < "ipv4" | "ipv6" | "ipv4 ipv6" | "none" >
                segment_list:
                  - label_stack: < integer > < integer > < integer >
                    weight: < integer >
                    index: < integer >
```

#### Service Routing Configuration BGP

```yaml
service_routing_configuration_bgp:
  no_equals_default: < true | false >
```

#### Service Routing Protocols Model

```yaml
service_routing_protocols_model: < multi-agent | ribd >
```

#### Static Routes

```yaml
static_routes:
  - vrf: < vrf_name, if vrf_name = default the route will be placed in the GRT >
    destination_address_prefix: < IPv4_network/Mask >
    interface: < interface >
    gateway: < IPv4_address >
    distance: < 1-255 >
    tag: < 0-4294967295 >
    name: < description >
    metric: < 0-4294967295 >
  - destination_address_prefix: < IPv4_network/Mask >
    gateway: < IPv4_address >
```

#### IPv6 Static Routes

```yaml
ipv6_static_routes:
  - vrf: < vrf_name, if vrf_name = default the route will be placed in the GRT >
    destination_address_prefix: < IPv6_network/Mask >
    interface: < interface >
    gateway: < IPv6_address >
    distance: < 1-255 >
    tag: < 0-4294967295 >
    name: < description >
    metric: < 0-4294967295 >
  - destination_address_prefix: < IPv6_network/Mask >
    gateway: < IPv6_address >
```

#### VRF Instances

```yaml
vrfs:
  - name: < vrf_name >
    description: < description>
    ip_routing: < true | false >
    ipv6_routing: < true | false >
  - name: < vrf_name >
    description: < description>
    ip_routing: < true | false >
    ipv6_routing: < true | false >
```

### Router L2 VPN

```yaml
router_l2_vpn:
  nd_rs_flooding_disabled: < true | false >
  virtual_router_nd_ra_flooding_disabled: < true | false >
  arp_selective_install: < true | false >
  arp_proxy:
    prefix_list: < prefix_list_name >
```

### Spanning Tree

```yaml
spanning_tree:
  root_super: < true | false >
  edge_port:
    bpdufilter_default: < true | false >
    bpduguard_default: < true | false >
  mode: < mstp | rstp | rapid-pvst | none >
  rstp_priority: < priority >
  mst:
    pvst_border: < true | false >
    configuration:
      name: < name >
      revision: < 0-65535 >
      instances:
        - id: "< instance_id >"
          vlans: "< vlan_id >, < vlan_id >-< vlan_id >"
        - id: "< instance_id >"
          vlans: "< vlan_id >, < vlan_id >-< vlan_id >"
  mst_instances:
    - id: "< instance_id >"
      priority: < priority >
    - id: "< instance_id >"
      priority: < priority >
  no_spanning_tree_vlan: "< vlan_id >, < vlan_id >-< vlan_id >"
  rapid_pvst_instances:
    - id: "< vlan_id >"
      priority: < priority >
    - id: "< vlan_id >, < vlan_id >-< vlan_id >"
      priority: < priority >
```

### Terminal Settings

```yaml
terminal:
  length: < 0-32767 >
  width: < 0-32767 >
```

### Traffic Policies

```yaml
traffic_policies:
  options:
    counter_per_interface: < true | false >
  field_sets:
    ipv4:
      - name: < PREFIX FIELD SET NAME >
        prefixes:
          - < IPv4 prefix 01>
          - < IPv4 prefix 02>
          - < IPv4 prefix 03>
    ipv6:
      - name: < PREFIX FIELD SET NAME >
        prefixes:
          - < IPv6 prefix 01>
          - < IPv6 prefix 02>
          - < IPv6 prefix 03>
    ports:
      - name: < L4 PORT FIELD SET NAME >
        port_range: "< vlan range >"
  policies:
    - name: < TRAFFIC POLICY NAME >
      matches:
        - name: < TRAFFIC POLICY ITEM >
          type: < ipv4 | ipv6 >
          source:
            prefixes:
              - < prefix 01 >
              - < prefix 02 >
            prefix_lists:
              - < Field Set List 01 >
              - < Field Set List 02 >
          destination:
            prefixes:
              - < prefix 01 >
              - < prefix 02 >
            prefix_lists:
              - < Field Set List 01 >
              - < Field Set List 02 >
          ttl: "< ttl range>"
          # The 'fragment' command is not supported when 'source port'
          # or 'destination port' command is configured
          fragment:
            offset: "< fragment offset range >"
          protocols:
            - protocol: tcp
              src_port: "< port range >"
              dst_port: "< port range >"
              src_field: "< L4 port range field set >"
              dst_field: "< L4 port range field set >"
              flags:
                - established
                - initial
            - protocol: icmp
              icmp_type:
                - < ICMP message type >
                - < ICMP message type >
            - protocol: udp
              src_port: "< port range >"
              dst_port: "< port range >"
              src_field: "< L4 port range field set >"
              dst_field: "< L4 port range field set >"
            - protocol: ahp
            - protocol: bgp
            - protocol: icmp
            - protocol: igmp
            - protocol: ospf
            - protocol: pim
            - protocol: rsvp
            - protocol: vrrp
            # The 'protocol neighbors' subcommand is not supported when any
            # other match subcommands are configured
            - protocol: neighbors
          actions:
            dscp: < dscp code value >
            traffic_class: < traffic class id >
            count: < counter name >
            drop: < true | false (default false) >
            # Only supported when action is set to drop
            log: < true | false (default false) >
          # Last resort policy
          default_actions:
            ipv4:
              dscp: < dscp code value >
              traffic_class: < traffic class id >
              count: < counter name >
              drop: < true | false (default false) >
              # Only supported when action is set to drop
              log: < true | false (default false) >
            ipv6:
              dscp: < dscp code value >
              traffic_class: < traffic class id >
              count: < counter name >
              drop: < true | false (default false) >
              # Only supported when action is set to drop
              log: < true | false (default false) >
```

### Virtual Source NAT

```yaml
virtual_source_nat_vrfs:
  - name: < vrf_name_1 >
    ip_address: < IPv4_address >
  - name: < vrf_name_2 >
    ip_address: < IPv4_address >
```

### VLANs

```yaml
vlans:
  - id: < vlan_id >
    name: < vlan_name >
    state: < active | suspend >
    trunk_groups:
      - < trunk_group_name_1 >
      - < trunk_group_name_2 >
    private_vlan:
      type: < community | isolated >
      primary_vlan: < vlan_id >
  - id: < vlan_id >
    name: < vlan_name >
```

### MAC Address-table

```yaml
mac_address_table:
  aging_time: < aging_time_in_seconds >
  notification_host_flap:
    logging: < true | false >
    detection:
      window: < 2-300 >
      moves: < 2-10 >
```

## Upgrade of eos_cli_config_gen data model

The AVD **major** releases can contain breaking changes to the data models.
Data model changes requires a change to the `group_vars` and `host_vars`. To help identify needed changes and provide a smoother transition, the AVD 3.0 `eos_cli_config_gen`
role can provide automatic upgrade of the data model for AVD 2.x to 3.0 upgrades.

To leverage this upgrade functionality, the playbook must include `tasks_from: upgrade` or `tasks_from: upgrade-and-run` for the `import_role` of `eos_cli_config_gen`. Using `upgrade` alone will output the upgraded data files as described below. `upgrade-and-run` will also
run the regular `eos_cli_config_gen` tasks after upgrading the data model.

The upgraded data will be saved in `{{ inventory_dir }}/eos_cli_config_gen_upgrade_2.x_to_3.0` directory.

The user should then replace the old data structures manually in `group_vars` and `host_vars` files as applicable until no files are created in the upgrade directory when
running the playbook. After all data has been upgraded, the `tasks_from: upgrade` can be removed again.

This `eos_cli_config_gen` upgrade feature is not required when using `eos_designs`. Upgrade should be done on `eos_designs` instead.
See [README](https://www.avd.sh/en/devel/roles/eos_designs/#upgrade-of-eos_designs-data-model) for details on the `eos_designs` upgrade feature.

### Versioning

To support future upgrades the relevant upgrade tasks can be chosen using a new upgrade setting.

```yaml
avd_eos_cli_config_gen_upgrade: < "2.x-to-3.0" | default -> "2.x-to-3.0" >
```

### Example Playbooks

Running upgrade only

```yaml
---
- hosts: DC1_FABRIC
  tasks:
    - name: Run AVD eos_cli_config_gen
      import_role:
        tasks_from: upgrade
        name: arista.avd.eos_cli_config_gen
```

Running upgrade and the regular `eos_cli_config_gen` tasks

```yaml
---
- hosts: DC1_FABRIC
  tasks:
    - name: Run AVD eos_cli_config_gen
      import_role:
        tasks_from: upgrade-and-run
        name: arista.avd.eos_cli_config_gen
```

Alternative with separate tasks:

```yaml
---
- hosts: DC1_FABRIC
  tasks:
    - name: Upgrade AVD eos_cli_config_gen data model
      import_role:
        tasks_from: upgrade
        name: arista.avd.eos_cli_config_gen
    - name: Run AVD eos_cli_config_gen
      import_role:
        name: arista.avd.eos_cli_config_gen
```

## License

Project is published under [Apache 2.0 License](../../LICENSE)
