# AVD Coding Style

This page provides a list of guidelines to apply when developing Python code or Jinja2 template in the AVD context. These rules apply for either creation or update of any Python or Jinja2 file available in a `aristanetworks/ansible-avd` repository.

## Python code style

As AVD is an Ansible collection, we're required to follow guidelines from the official [Ansible documentation](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html) for all Python code.

Furthermore the CI Pipeline (& pre-commit) for AVD enforces:

- Maximum line length 160
- [Black](https://black.readthedocs.io/en/stable/index.html) version 22.8.0
- [isort](https://pycqa.github.io/isort/) version 5.10.1
- [Flake-8](https://flake8.pycqa.org/en/4.0.1/index.html) version 4.0.1
- [pylint](https://pylint.pycqa.org/en/2.6/) version 2.6.0

Configurations for above tools can be found in:

- [pyproject.toml](https://github.com/aristanetworks/ansible-avd/blob/devel/pyproject.toml)
- [.pre-commit-config.yaml](https://github.com/aristanetworks/ansible-avd/blob/devel/.pre-commit-config.yaml)
- [.flake8](https://github.com/aristanetworks/ansible-avd/blob/devel/.flake8)
- [pylintrc](https://github.com/aristanetworks/ansible-avd/blob/devel/pylintrc)

## Jinja2 Syntax guidelines

### SYNTAX-1 - Use variable in Jinja

- *Description*

  A single space shall be added between Jinja2 curly brackets and a variable's name

- *Example*

  ```jinja
  {{ ethernet_interface }}
  ```

### SYNTAX-2 - Filter syntax

- *Description*

  When variables are used in combination with a filter, `|` shall be enclosed by space

- *Example*

  ```jinja
  {{ my_value | to_json }}
  ```

### SYNTAX-3 - Indentation for statement blocks

- *Description*

  Nested jinja code block shall follow the next rules:

  - All J2 statements must be enclosed by 1 space
  - All J2 statements must be indented by 4 more spaces within the jinja delimiter
  - To close a control, the end tag must have the same indentation level as the opening tag
  - Indentation must be 4 spaces and NOT tabulation

- *Example*

  ```jinja
  {# Initial block indentation #}
  {% if my_variable is arista.avd.defined %}

  {# Nested block indentation #}
  {% for ethernet_interface in ethernet_interfaces %}
  {%     if ethernet_interface.name is arista.avd.defined %}
  {%         set result = ethernet_interface.name %}
  {# ..... output truncated ..... #}
  {%     endif %}
  {% endfor %}
  ```

### SYNTAX-4 - Expand list on a single line

- *Description*

  Instead of doing a for loop on a single line, the `join` filter should be leveraged as much as possible

- *Example*

  ```jinja
  {{ ciphers | join(", ") }}
  ```

### SYNTAX-5 - Test if a variable in a list

- *Description*

  To test if a variable is part of a list, the `in` operator should be used as much as possible to avoid long `if/elif/else` block.

- *Example*

  ```jinja
  {% if underlay_routing_protocol is arista.avd.defined and underlay_routing_protocol in ['isis', 'ospf'] %}
  ```

### SYNTAX-6 - Render long CLI

- *Description*

  When a long CLI with multiple options needs to be built, use pure J2 logic and then print

- *Example*

  ```jinja
  {% for ip_helper in vlan_interfaces[vlan_interface].ip_helpers | arista.avd.natural_sort %}
  {%     set ip_helper_cli = "ip helper-address " ~ ip_helper %}
  {%     if vlan_interfaces[vlan_interface].ip_helpers[ip_helper].vrf is arista.avd.defined %}
  {%         set ip_helper_cli = ip_helper_cli ~ " vrf " ~ vlan_interfaces[vlan_interface].ip_helpers[ip_helper].vrf %}
  {%     endif %}
  {%     if vlan_interfaces[vlan_interface].ip_helpers[ip_helper].source_interface is arista.avd.defined %}
  {%         set ip_helper_cli = ip_helper_cli ~ " source-interface " ~ vlan_interfaces[vlan_interface].ip_helpers[ip_helper].source_interface %}
  {%     endif %}
     {{ ip_helper_cli }}
  {% endfor %}
  ```

## YAML Variable definition

### VAR-1 - Variable name case

- *Description*

  All variables shall use lower case

- *Example*

  ```jinja
  {{ variable }}
  ```

### VAR-2 - Variable name format

- *Description*

  If a variable is multi-words, underscore `_` shall be used as a separator.

- *Example*

  ```jinja
  {{ my_variable_name }}
  ```

### VAR-3 - Iterable variables

- *Description*

  For an iterable variable, the plural form shall be used

- *Example*

  ```jinja
  {{ ethernet_interfaces }}
  ```

### VAR-4 - Variables in a For Loop

- *Description*

  For variables in a for loop, the singular form shall be used

- *Example*

  ```jinja
  {{ ethernet_interfaces[ethernet_interface] }}
  ```

### VAR-5 - Variables concatenation

- *Description*

  Tilde `~` should be used for string concatenation as it automatically converts variables to a string.

- *Example*

  ```jinja
  {% set ip_helper_cli = ip_helper_cli ~ " source-interface " ~ vlan_interfaces[vlan_interface].ip_helpers[ip_helper].source_interface %}
  ```

### VAR-6 - Variable type comparison

- *Description*

  To test the type of a variable, it's recommended to use `is`/`is not` keywords

- *Example*

  ```jinja
  {# Test if variable is string #}
  {% if ethernet_interface is string %}

  {# Test if variable is not a string #}
  {% if ethernet_interface is not string %}
  ```

### VAR-7 - Variable content comparison

- *Description*

  To test the content of a variable, it's recommended to use `==`/`!=` keywords

- *Example*

  ```jinja
  {# Test if variable is equal to 'Ethernet1' #}
  {% if ethernet_interface == 'Ethernet1' %}

  {# Test if variable is not equal to 'Ethernet1' #}
  {% if ethernet_interface != 'Ethernet1' %}
  ```

  !!! info
      [PLUGIN-2](#plugin-2-test-if-variable-exists-with-a-given-value) can do a test if the variable is defined and has a specific value

### VAR-8 - String comparison

- *Description*

  All strings should be compared based on lowercase format.

- *Example*

  ```jinja
  {% if underlay_routing_protocol is arista.avd.defined and underlay_routing_protocol | lower in ['isis', 'ospf'] %}
  ```

---

## AVD Plugins usage

Plugins documentation is available [here](../../plugins/README.md)

### PLUGIN-1 - Test if a variable exists

- *Description*

  All tests to check if a variable is defined shall be done with **`arista.avd.defined`**. This test also does a deep test and doesn't require a test at an upper level.

- *Example*

  ```jinja
  {# Simple test #}
  {% if ethernet_interfaces is arista.avd.defined %}

  {# Deep test #}
  {% if router_bgp.vrfs[vrf].rd is arista.avd.defined %}
  ```

### PLUGIN-2 Test if variable exists with a given value

- *Description*

  To test if a variable is defined and has a specific value, the test **`arista.avd.defined`** shall be used.

- *Example*

  ```jinja
  {% if vlan.name is arista.avd.defined('test') %}
  ```

### PLUGIN-3 - Default value

- *Description*

  If a default value must be used, the `arista.avd.default` plugin shall be used instead of a `if/else` block. The plugin can be used to fallback to different values until one of them is defined and valid.

- *Example*

  ```jinja
  {# Simple default test with one default value #}
  {{ vlan.name | arista.avd.default('test_vlan') }}

  {# Default test with a list of default options #}
  {{ vlan.name | arista.avd.default(default.vlan.name, 'test_vlan') }}
  ```
