# AWX & Tower Integration

## About

This example shows how to deploy basic **EVPN/VXLAN Fabric** based on **[Arista Validated Design roles](https://github.com/aristanetworks/ansible-avd)** using Ansible Tower/AWX. This repository will be used as a project on AWX, and we will describe how to configure Tower for the following topics:

- Create a project
- Create inventory
- Install collections
- Install Python requirements

All these elements are part of a dedicated demo repository available at [arista-netdevops-community/avd-with-ansible-tower-awx](https://github.com/arista-netdevops-community/avd-with-ansible-tower-awx).

If you want to see how to build your inventory and all related variables, it's recommended to read the following documentation:

- [How to start](first-project.md)
- [L3LS EVPN Abstraction role](../../roles/eos_designs/README.md)

## Requirements

To follow along with this guide, you will need the following:

- An AWX setup running on either Docker Compose or Kubernetes. We will do all the commands for Python configuration on docker-compose, but you can adapt for Kubernetes.
- Understanding of how to configure AVD in a pure Ansible CLI way.

## Install Python requirements

The Ansible CVP collection requires [additional libraries](https://github.com/arista-netdevops-community/avd-with-ansible-tower-awx/blob/master/requirements.txt) not part of a standard Python setup:

- netaddr
- Jinja2
- treelib
- cvprac
- paramiko
- jsonschema
- requests
- PyYAML
- md-toc

### Create virtual-environment

It's required to create a [virtual-env](https://medium.com/@mehdirashidi/setting-up-venv-in-awx-31c4f9952a46); this will reduce any chance of impacting other workflows already deployed on your Tower setup.

```shell
# Docker status
tom@kube-tool:~$ docker ps
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                  NAMES
4a4627b21f93        ansible/awx:15.0.0   "/usr/bin/tini -- /u…"   8 days ago          Up 8 days           8052/tcp               awx_task
6ef41f162226        ansible/awx:15.0.0   "/usr/bin/tini -- /b…"   8 days ago          Up 8 days           0.0.0.0:80->8052/tcp   awx_web
a2fd85d0cc86        postgres:10          "docker-entrypoint.s…"   8 days ago          Up 8 days           5432/tcp               awx_postgres
573d03e33c44        redis                "docker-entrypoint.s…"   8 days ago          Up 8 days           6379/tcp               awx_redis

# Run shell in docker
tom@kube-tool:~$ docker exec -it awx_task bash

$ sudo pip3 install virtualenv
WARNING: Running pip install with root privileges is generally not a good idea. Try `pip3 install --user` instead.
Requirement already satisfied: virtualenv in /usr/local/lib/python3.8/site-packages

$ mkdir /opt/my-envs

$ chmod 0755 /opt/my-envs

$ cd /opt/my-envs/

$ python3 -m venv avd-venv
```

> This configuration [**MUST**](https://github.com/ansible/awx/issues/4140) be replicated on both container `awx_task` and `awx_web`

Instruct AWX to register our new Virtual Environment folder:

```shell
$ curl -X PATCH 'http://admin:password@<IP-of-AWX-INSTANCE>/api/v2/settings/system/' \
    -d '{"CUSTOM_VENV_PATHS": ["/opt/my-envs/"]}' -H 'Content-Type:application/json'

{
    "ACTIVITY_STREAM_ENABLED": true,
    "ACTIVITY_STREAM_ENABLED_FOR_INVENTORY_SYNC": false,
    "ORG_ADMINS_CAN_SEE_ALL_USERS": true,
    "MANAGE_ORGANIZATION_AUTH": true,
    "TOWER_URL_BASE": "http://10.83.28.163",
    "REMOTE_HOST_HEADERS": [
        "REMOTE_ADDR",
        "REMOTE_HOST"
    ],
    "PROXY_IP_ALLOWED_LIST": [],
    "LICENSE": {},
    "REDHAT_USERNAME": "",
    "REDHAT_PASSWORD": "",
    "AUTOMATION_ANALYTICS_URL": "https://example.com",
    "INSTALL_UUID": "f8a54d56-b1f3-4fdf-aa5b-9d6977d00eaa",
    "CUSTOM_VENV_PATHS": [
        "/opt/my-envs"
    ],
    "INSIGHTS_TRACKING_STATE": false,
    "AUTOMATION_ANALYTICS_LAST_GATHER": null,
    "AUTOMATION_ANALYTICS_GATHER_INTERVAL": 14400
}
```

### Provision virtual-environment

Before running playbook in a virtual-env, we have to install the required libraries:

```shell
tom@kube-tool:~$ docker exec -it awx_task bash

# Activate virtual-env
$ cd /opt/my-envs/avd-venv
$ source bin/activate

# Install ansible AWX base lib
$ pip3 install psutil

# Install project requirements
$ curl -fsSL https://raw.githubusercontent.com/aristanetworks/ansible-avd/devel/ansible_collections/arista/avd/requirements.txt -o requirements.txt
$ pip3 install -r requirements.txt
```

From here, you have a clean python environment with all the expected requirements installed on your AWX runner.

## Create AVD project on AWX

### Create a project resource

First go to **Resources > Projects** and create a new one using:

- SCM Type: `Git`
- SCM Branch: `master`
- Ansible Environment: `/your/path/to/venv`
- SCM URL: `https://github.com/arista-netdevops-community/avd-with-ansible-tower-awx.git`

![AWX create project](../_media/awx-create-project-venv.png)

This project will be used for two things:

- Get our inventory and all attached variables.
- Get our playbooks to run in AWX.

### Create Inventory resource

Next action is to create an inventory in AWX. This requires two additional steps:

#### Create Inventory

Go to **Resources > Inventory**

![AWX create inventory](../_media/awx-create-inventory.png)

Once ready, you need to add a source to your inventory.

#### Add source

In your inventory, select **Sources**.

![AWX add sources](../_media/awx-inventory-add-source.png)

Then add a source using your existing project.

![AWX create sources](../_media/awx-create-source.png)

In our example, our inventory file is part of a subdirectory. In this case, we had to type the path manually as it wasn't part of the suggestion list. Also, don't forget to specify virtual-env to use with this inventory.

Once you click on the `Save` button, select **SYNC-ALL** button to get all hosts part of your inventory:

![AWX sync sources](../_media/awx-inventory-add-source.png)

You should get all your devices in **Resources > Inventory > Your inventory Name**

![AWX inventory list](../_media/awx-inventory-list-devices.png)

Now we can focus on the playbook itself.

### Create Playbook resource

Go to **Resources > Templates**.

In this section you have to provide at least:

- Name of your Template: *Build Fabric Configuration -- no-deploy*
- Which inventory to use: *EMEA Demo*
- Which project to use to get playbook: *AVD Demo with CVP*
- Which playbook to use: [`playbooks/dc1-fabric-deploy-cvp.yml`](https://github.com/arista-netdevops-community/avd-with-ansible-tower-awx/blob/master/playbooks/dc1-fabric-deploy-cvp.yml)
- Virtual Environment to use when running the playbook

As AVD implements Ansible `TAGS`, we've only specified the `build` tag, but you can adapt it to your setup.

![Create template in AWX](../_media/awx-create-template.png)

You can configure more than just one playbook, but we will focus on playbook definition as it's not an AWX user's guide.

## Update AVD playbook

### How to install collection within project

Since AVD and CVP collections are not installed by default in AWX, you need to consider how to install them. You have two options: system-wide or per project. Let's consider per project as it's easier to upgrade.

- Create a folder named `collections` in your Git project
- Create a YAML file named [`requirements.yml`](https://github.com/arista-netdevops-community/avd-with-ansible-tower-awx/blob/master/README.md) with the following structure:

```yaml
---
collections:
  - name: arista.avd
    version: 1.1.0
  - name: arista.cvp
    version: 2.1.0
```

### What to change to work with AVD and AWX

Ansible has a default variable that points to the inventory file used in a playbook and named `{{ inventory_file }}`. Since AWX/Tower is using a database, this variable isn't available anymore, and [inventory file does not exist in such environment](https://github.com/ansible/awx/issues/5926).

AVD uses this variable to read inventory and build container topology on CloudVision. So to mitigate this behavior, a slight workaround is to add a task that downloads your inventory from your Git repository and define `{{ inventory_file }}`:

- Define variable:

```yaml
#group_vars/all.yml
---
inventory_file: '/tmp/inventory.yml'
```

- Update playbook

```yaml
- name: Configuration deployment with CVP
  hosts: cv_server
  connection: local
  gather_facts: false
  collections:
    - arista.avd
    - arista.cvp
  tasks:

    - name: Download Inventory file
      tags: [ build ]
      get_url:
        url: 'https://raw.githubusercontent.com/titom73/avd-with-ansible-tower-awx/master/inventory/inventory.yml'
        dest: '{{ inventory_file }}'
        mode: '0755'
      delegate_to: 127.0.0.1

    - name: run CVP provisioning
      import_role:
        name: arista.avd.eos_config_deploy_cvp
      vars:
        container_root: 'DC1_FABRIC'
        configlets_prefix: 'DC1-AVD'
        device_filter: 'DC1'
        state: present
```

## Run your playbook

Under **Resources > Templates** click on the rocket icon to start playbook execution

![AWX run a playbook](../_media/awx-playbook-run.png)
