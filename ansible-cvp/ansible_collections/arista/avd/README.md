# Ansible Collection for Arista Validated Designs

<center><img src="media/avd-logo.png" alt="Arista AVD Overview" width="800"/></center>

[Arista Networks](https://www.arista.com/) supports Ansible for managing devices running Arista's **Extensible Operating System (EOS)** natively through it's **EOS API (eAPI)** or [**CloudVision Portal (CVP)**](https://www.arista.com/en/products/eos/eos-cloudvision). This collection includes a set of Ansible roles and modules to help kick-start your automation with Arista. The various roles and templates provided are designed to be customized and extended to your needs.

Full documentation for the collection:

- [stable version](https://www.avd.sh/en/stable/)
- [collection development version](https://www.avd.sh/en/devel/)

## Features

- **Flexibility with Open Data Models:** Extensible fabric-wide network models, simplifying configuration, delivering consistency, and reducing errors
- **Simplification through Multi-Domain Automation:** A framework that can automate the data center, campus or wide area network, enabled by a consistent EOS software image and management platform
- **Comprehensive Workflows:** Automating the full life cycle of network provisioning from config generation to pre and post-deployment validation, and self-documentation of the network

## Reference designs

- [L3LS VXLAN-EVPN, L2LS, and MPLS (beta)](https://avd.sh/en/stable/roles/eos_designs/index.html)

## Roles overview

This repository provides content for Arista's **arista.avd** collection. The following roles are included.

- [**arista.avd.eos_designs**](roles/eos_designs/README.md) - Opinionated Data model to assist with the deployment of Arista Validated Designs.
- [**arista.avd.eos_cli_config_gen**](roles/eos_cli_config_gen/README.md) - Generate Arista EOS cli syntax and device documentation.
- [**arista.avd.eos_config_deploy_cvp**](roles/eos_config_deploy_cvp/README.md) - Deploys intended configuration via CloudVision.
- [**arista.avd.eos_config_deploy_eapi**](roles/eos_config_deploy_eapi/README.md) - Deploys intended configuration via eAPI.
- [**arista.avd.cvp_configlet_upload**](roles/cvp_configlet_upload/README.md) - Uploads configlets from a local folder to CloudVision Server.
- [**arista.avd.eos_validate_state**](roles/eos_validate_state/README.md) - Validate operational states of Arista EOS devices.
- [**arista.avd.eos_snapshot**](roles/eos_snapshot/README.md) - Collect commands on EOS devices and generate reports.
- [**arista.avd.dhcp_provisioner**](roles/dhcp_provisioner/README.md) - Configure an ISC-DHCP server to provide ZTP services and CloudVision registration.

![Arista AVD Overview](docs/_media/avd_roles_dark.svg#only-dark)
![Arista AVD Overview](docs/_media/avd_roles_light.svg#only-light)

## Custom plugins & modules

This repository provides custom plugins for Arista's AVD collection:

- [Arista AVD Plugins](plugins/README.md)

## Collection installation

Ansible galaxy hosts all stable versions of this collection. Installation from ansible-galaxy is the most convenient approach for consuming `arista.avd` content. Please follow the collection installation [guide](https://avd.sh/en/stable/docs/installation/collection-installation.html).

## Examples

- [Getting started examples](./docs/getting-started/intro-to-ansible-and-avd.md)
- [Arista NetDevOps Examples](https://github.com/aristanetworks/netdevops-examples)

## Additional resources

- Ansible [EOS modules](https://docs.ansible.com/ansible/latest/collections/arista/eos/index.html) on ansible documentation.
- Ansible [CloudVision modules](https://cvp.avd.sh/en/stable/)
- [CloudVision Portal](https://www.arista.com/en/products/eos/eos-cloudvision)
- [Arista Design and Deployment Guides](https://www.arista.com/en/solutions/design-guides)

## Ask a question

Support for this `arista.avd` collection is provided by the community directly in this repository. If you have any questions, please leverage the GitHub [discussions board](https://github.com/aristanetworks/ansible-avd/discussions).

## Contributing

Contributing pull requests are gladly welcomed for this repository. If you are planning a big change, please start a discussion first to make sure we'll be able to merge it. Please see [contribution guide](https://avd.sh/en/stable/docs/contribution/overview.html) for additional details.

You can also open an [issue](https://github.com/aristanetworks/ansible-avd/issues) to report any problems or submit enhancements.

## License

The project is published under [Apache 2.0 License](https://github.com/aristanetworks/ansible-avd/blob/devel/ansible_collections/arista/avd/LICENSE)
