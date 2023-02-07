from ansible.module_utils._text import to_text


def template(template_file, template_vars, templar):
    """
    Run Ansible Templar with template file.

    This function does not support the following Ansible features:
    - No template_* vars (rarely used)
    - The template file path is not inserted into searchpath, so "include" must be absolute from searchpath.
    - No configurable convert_data (we set it to False)
    - Maybe something else we have not discovered yet...

    Parameters
    ----------
    template_file : str
        Path to Jinja2 template file
    template_vars : any
        Variables to use when rendering template
    templar : func
        Instance of Ansible Templar class
    searchpath : list of str
        List of Paths

    Returns
    -------
    str
        The rendered template
    """

    dataloader = templar._loader
    searchpath = templar.environment.loader.searchpath
    template_file_path = dataloader.path_dwim_relative_stack(searchpath, "templates", template_file)
    j2template, dummy = dataloader._get_file_contents(template_file_path)
    j2template = to_text(j2template)

    with templar.set_temporary_context(available_variables=template_vars):
        result = templar.template(j2template, convert_data=False, escape_backslashes=False)

    return result
