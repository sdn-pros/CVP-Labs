from __future__ import absolute_import, division, print_function

__metaclass__ = type

import cProfile
import pstats
from collections import ChainMap
from datetime import datetime

import yaml
from ansible.errors import AnsibleActionFail
from ansible.parsing.yaml.dumper import AnsibleDumper
from ansible.plugins.action import ActionBase
from ansible.utils.vars import isidentifier

from ansible_collections.arista.avd.plugins.plugin_utils.avdfacts import AvdFacts
from ansible_collections.arista.avd.plugins.plugin_utils.errors import AristaAvdMissingVariableError
from ansible_collections.arista.avd.plugins.plugin_utils.merge import merge
from ansible_collections.arista.avd.plugins.plugin_utils.strip_empties import strip_null_from_data
from ansible_collections.arista.avd.plugins.plugin_utils.utils import get_templar, load_python_class
from ansible_collections.arista.avd.plugins.plugin_utils.utils import template as templater

DEFAULT_PYTHON_CLASS_NAME = "AvdStructuredConfig"


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}

        result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        root_key = ""

        if self._task.args:
            cprofile_file = self._task.args.get("cprofile_file")
            if cprofile_file:
                profiler = cProfile.Profile()
                profiler.enable()

            if "root_key" in self._task.args:
                n = self._task.args.get("root_key")
                n = self._templar.template(n)
                if not isidentifier(n):
                    raise AnsibleActionFail(
                        f"The argument 'root_key' value of '{n}' is not valid. Keys must start with a letter or underscore character,                          "
                        "                   and contain only letters, numbers and underscores."
                    )
                root_key = n

            if "templates" in self._task.args:
                t = self._task.args.get("templates")
                if isinstance(t, list):
                    template_list = t
                else:
                    raise AnsibleActionFail("The argument 'templates' is not a list")
            else:
                raise AnsibleActionFail("The argument 'templates' must be set")

            dest = self._task.args.get("dest", False)
            template_output = self._task.args.get("template_output", False)
            debug = self._task.args.get("debug", False)
            remove_avd_switch_facts = self._task.args.get("remove_avd_switch_facts", False)

        else:
            raise AnsibleActionFail("The argument 'templates' must be set")

        # Read ansible variables and perform templating to support inline jinja
        for var in task_vars:
            if str(var).startswith(("ansible", "molecule", "hostvars", "vars")):
                continue
            if self._templar.is_template(task_vars[var]):
                # Var contains a jinja template.
                try:
                    task_vars[var] = self._templar.template(task_vars[var], fail_on_undefined=False)
                except Exception as e:
                    raise AnsibleActionFail(f"Exception during templating of task_var '{var}'") from e

        # Get updated templar instance to be passed along to our simplified "templater"
        self.templar = get_templar(self, task_vars)

        # If the argument 'root_key' is set, output will be assigned to this variable. If not set, the output will be set at as "root" variables.
        # We use ChainMap to avoid copying large amounts of data around, mapping in
        #  - output or { root_key: output }
        #  - templated version of all other vars
        # Any var assignments will end up in output, so all other objects are protected.
        output = {}
        if root_key:
            template_vars = ChainMap({root_key: output}, task_vars)
        else:
            template_vars = ChainMap(output, task_vars)

        # If the argument 'debug' is set, a 'avd_yaml_templates_to_facts_debug' list will be added to the output.
        # This list contains timestamps from every step for every template. This is useful for identifying slow templates.
        # Here we pull in the list from any previous tasks, so we can just add to the list.
        if debug:
            avd_yaml_templates_to_facts_debug = task_vars.get("avd_yaml_templates_to_facts_debug", [])

        # template_list can contain templates or python_modules
        for template_item in template_list:
            if debug:
                debug_item = template_item
                debug_item["timestamps"] = {"starting": datetime.now()}

            template_options = template_item.get("options", {})
            list_merge = template_options.get("list_merge", "append")

            strip_empty_keys = template_options.get("strip_empty_keys", True)

            if "template" in template_item:
                template = template_item["template"]

                if debug:
                    debug_item["timestamps"]["run_template"] = datetime.now()

                # Here we parse the template, expecting the result to be a YAML formatted string
                template_result = templater(template, template_vars, self.templar)

                if debug:
                    debug_item["timestamps"]["load_yaml"] = datetime.now()

                # Load data from the template result.
                template_result_data = yaml.safe_load(template_result)

                # If the argument 'strip_empty_keys' is set, remove keys with value of null / None from the resulting dict (recursively).
                if strip_empty_keys:
                    if debug:
                        debug_item["timestamps"]["strip_empty_keys"] = datetime.now()

                    template_result_data = strip_null_from_data(template_result_data)

            elif "python_module" in template_item:
                module_path = template_item.get("python_module")
                class_name = template_item.get("python_class_name", DEFAULT_PYTHON_CLASS_NAME)
                try:
                    cls = load_python_class(module_path, class_name, AvdFacts)
                except AristaAvdMissingVariableError as exc:
                    raise AnsibleActionFail(f"Missing module_path or class_name in {template_item}") from exc

                cls_instance = cls(hostvars=template_vars, templar=self.templar)

                if debug:
                    debug_item["timestamps"]["render_python_class"] = datetime.now()

                if not (getattr(cls_instance, "render")):
                    raise AnsibleActionFail(f"{cls_instance} has no attribute render")

                try:
                    template_result_data = cls_instance.render()
                except Exception as error:
                    raise AnsibleActionFail(error) from error

            else:
                raise AnsibleActionFail("Invalid template data")

            # If there is any data produced by the template, combine it on top of previous output.
            if template_result_data:
                if debug:
                    debug_item["timestamps"]["combine_data"] = datetime.now()

                merge(output, template_result_data, list_merge=list_merge)

            if debug:
                debug_item["timestamps"]["done"] = datetime.now()
                avd_yaml_templates_to_facts_debug.append(debug_item)

        # If the argument 'template_output' is set, run the output data through another jinja2 rendering.
        # This is to resolve any input values with inline jinja using variables/facts set by the input templates.
        if template_output:
            if debug:
                debug_item = {"action": "template_output", "timestamps": {"templating": datetime.now()}}

            with self._templar.set_temporary_context(available_variables=template_vars):
                output = self._templar.template(output, fail_on_undefined=False)

            if debug:
                debug_item["timestamps"]["done"] = datetime.now()
                avd_yaml_templates_to_facts_debug.append(debug_item)

        # If the argument 'dest' is set, write the output data to a file.
        if dest:
            if debug:
                debug_item = {"action": "dest", "dest": dest, "timestamps": {"write_file": datetime.now()}}

            # Depending on the file suffix of 'dest' (default: 'json') we will format the data to yaml or just write the output data directly.
            # The Copy module used in 'write_file' will convert the output data to json automatically.
            if dest.split(".")[-1] in ["yml", "yaml"]:
                write_file_result = self.write_file(yaml.dump(output, Dumper=AnsibleDumper, indent=2, sort_keys=False, width=130), task_vars)
            else:
                write_file_result = self.write_file(output, task_vars)

            # Overwrite result with the result from the copy operation (setting 'changed' flag accordingly)
            result.update(write_file_result)

            if debug:
                debug_item["timestamps"]["done"] = datetime.now()
                avd_yaml_templates_to_facts_debug.append(debug_item)

        # If 'dest' is not set, hardcode 'changed' to true, since we don't know if something changed and later tasks may depend on this.
        else:
            result["changed"] = True

        if debug:
            output["avd_yaml_templates_to_facts_debug"] = avd_yaml_templates_to_facts_debug

        # If the argument 'root_key' is set, output will be assigned to this variable. If not set, the output will be set at as "root" variables.
        if root_key:
            result["ansible_facts"] = {root_key: output}
        else:
            result["ansible_facts"] = output

        if remove_avd_switch_facts:
            result["ansible_facts"]["avd_switch_facts"] = None

        if cprofile_file:
            profiler.disable()
            stats = pstats.Stats(profiler).sort_stats("cumtime")
            stats.dump_stats(cprofile_file)

        return result

    def write_file(self, content, task_vars):
        # The write_file function is implementing the Ansible 'copy' action_module, to benefit from Ansible builtin functionality like 'changed'.
        # Reuse task data
        new_task = self._task.copy()

        # remove 'yaml_templates_to_facts' options (except 'dest' which will be reused):
        for remove in ("root_key", "templates", "template_output", "debug", "remove_avd_switch_facts"):
            new_task.args.pop(remove, None)

        new_task.args["content"] = content

        copy_action = self._shared_loader_obj.action_loader.get(
            "ansible.legacy.copy",
            task=new_task,
            connection=self._connection,
            play_context=self._play_context,
            loader=self._loader,
            templar=self._templar,
            shared_loader_obj=self._shared_loader_obj,
        )

        return copy_action.run(task_vars=task_vars)
