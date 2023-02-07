from __future__ import absolute_import, division, print_function

__metaclass__ = type

import cProfile
import pstats
from collections import ChainMap

from ansible.errors import AnsibleActionFail
from ansible.plugins.action import ActionBase

from ansible_collections.arista.avd.plugins.plugin_utils.eos_designs_facts import EosDesignsFacts
from ansible_collections.arista.avd.plugins.plugin_utils.errors import AristaAvdMissingVariableError
from ansible_collections.arista.avd.plugins.plugin_utils.utils import get_templar


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}

        result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        cprofile_file = self._task.args.get("cprofile_file")
        if cprofile_file:
            profiler = cProfile.Profile()
            profiler.enable()

        set_avd_switch_facts = self._task.args.get("avd_switch_facts", False)
        self.template_output = self._task.args.get("template_output", False)

        groups = task_vars.get("groups", {})
        fabric_name = self._templar.template(task_vars.get("fabric_name", ""))
        fabric_hosts = groups.get(fabric_name, [])
        ansible_play_hosts_all = task_vars.get("ansible_play_hosts_all", [])

        # Check if fabric_name is set and that all play hosts are part Ansible group set in "fabric_name"
        if fabric_name is None or not set(ansible_play_hosts_all).issubset(fabric_hosts):
            raise AnsibleActionFail(
                "Invalid/missing 'fabric_name' variable."
                "All hosts in the play must have the same 'fabric_name' value"
                "which must point to an Ansible Group containing the hosts."
            )

        # This is not all the hostvars, but just the Ansible Hostvars Manager object where we can retrieve hostvars for each host on-demand.
        hostvars = task_vars["hostvars"]

        # Caveat: Since we load default vars only once, it will be templated based on the vars of the random host triggering this task
        #         This should not be too bad, since all hosts are within the same fabric - hence they should also use the same "design"
        default_vars = self._templar.template(self._task._role.get_default_vars())

        # Get updated templar instance to be passed along to our simplified "templater"
        self.templar = get_templar(self, task_vars)

        if set_avd_switch_facts:
            avd_overlay_peers = {}
            avd_topology_peers = {}
            avd_switch_facts_instances = self.create_avd_switch_facts_instances(fabric_hosts, hostvars, default_vars)

            avd_switch_facts = self.render_avd_switch_facts(avd_switch_facts_instances)

            for host in fabric_hosts:
                host_evpn_route_servers = avd_switch_facts[host]["switch"].get("evpn_route_servers", [])
                for peer in host_evpn_route_servers:
                    avd_overlay_peers.setdefault(peer, []).append(host)

                host_mpls_route_reflectors = avd_switch_facts[host]["switch"].get("mpls_route_reflectors", [])
                for peer in host_mpls_route_reflectors:
                    avd_overlay_peers.setdefault(peer, []).append(host)

                host_topology_peers = avd_switch_facts[host]["switch"].get("uplink_peers", [])

                for peer in host_topology_peers:
                    avd_topology_peers.setdefault(peer, []).append(host)

            result["ansible_facts"] = {}
            result["ansible_facts"]["avd_switch_facts"] = avd_switch_facts
            result["ansible_facts"]["avd_overlay_peers"] = avd_overlay_peers
            result["ansible_facts"]["avd_topology_peers"] = avd_topology_peers

        if cprofile_file:
            profiler.disable()
            stats = pstats.Stats(profiler).sort_stats("cumtime")
            stats.dump_stats(cprofile_file)

        return result

    def create_avd_switch_facts_instances(self, fabric_hosts: list, hostvars: object, default_vars: dict):
        """
        Create "avd_switch_facts_instances" dictionary

        Parameters
        ----------
        fabric_hosts : list
            List of hostnames
        hostvars : object
            Ansible "hostvars" object
        default_vars : dict
            Default variables shared between all fabric_hosts

        Returns
        -------
        dict
            hostname1 : dict
                switch : <EosDesignsFacts object>,
            hostname2 : dict
                switch : <EosDesignsFacts object>,
            ...
        """
        avd_switch_facts = {}
        for host in fabric_hosts:
            # Using ChainMap to avoid copying data between defaults, hostvars and local template_vars
            host_hostvars = ChainMap({}, hostvars.get(host), default_vars)
            avd_switch_facts[host] = {}
            # Add reference to dict "avd_switch_facts".
            # This is used to access EosDesignsFacts objects of other switches during rendering of one switch.
            host_hostvars["avd_switch_facts"] = avd_switch_facts
            avd_switch_facts[host] = {"switch": EosDesignsFacts(hostvars=host_hostvars, templar=self.templar)}
            # Add reference to EosDesignsFacts object inside hostvars.
            # This is used to allow templates to access the facts object directly with "switch.*"
            host_hostvars["switch"] = avd_switch_facts[host]["switch"]

        return avd_switch_facts

    def render_avd_switch_facts(self, avd_switch_facts_instances: dict):
        """
        Run the render method on each EosDesignsFacts object

        Parameters
        ----------
        avd_switch_facts_instances : dict of EosDesignsFacts

        Returns
        -------
        dict
            hostname1 : dict
                switch : < switch.* facts >
            hostname2 : dict
                switch : < switch.* facts >
        """
        rendered_facts = {}
        for host in avd_switch_facts_instances:
            try:
                rendered_facts[host] = {"switch": avd_switch_facts_instances[host]["switch"].render()}
            except AristaAvdMissingVariableError as e:
                raise AnsibleActionFail(f"{e} is required but was not found for host '{host}'") from e

            # If the argument 'template_output' is set, run the output data through jinja2 rendering.
            # This is to resolve any input values with inline jinja using variables/facts set by eos_designs_facts.
            if self.template_output:
                with self._templar.set_temporary_context(available_variables=avd_switch_facts_instances[host]["switch"]._hostvars):
                    rendered_facts[host]["switch"] = self._templar.template(rendered_facts[host]["switch"], fail_on_undefined=False)

        return rendered_facts
