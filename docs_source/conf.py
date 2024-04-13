import os
import pathlib

project = 'Pycommence'
author = 'PawRequest'
release = '0.1.1'
copyright = f'2024, {author}'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.linkcode',
    # 'sphinx.ext.viewcode',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.githubpages',
    'sphinx_autodoc_typehints',
    'sphinx_rtd_dark_mode',
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']

html_context = {
    "display_github": True,
    "github_user": "PawRequest",
    "github_repo": "pycommence",
    "github_version": "main",
    "conf_py_path": "/docs_source/",
}
html_baseurl = 'https://pawrequest.github.io/pycommence/'
readme_src_files = 'index.rst'
readme_docs_url_type = 'html'
add_module_names = False
autodoc_default_options = {
    'exclude-members': 'model_config, model_fields, model_computed_fields',
    'members': True,
    'member-order': 'bysource',
    'undoc-members': True,
}

repo_src = 'https://github.com/pawrequest/pycommence/blob/main/src'


# def linkcode_resolve(domain, info):
#     if domain != 'py':
#         return None
#     if not info['module']:
#         return None
#     filename = info['module'].replace('.', '/')
#     return f"{repo_src}/{filename}.py"
def linkcode_resolve(domain, info):
    if domain != 'py':
        return None  # Only resolve links for Python domain
    if not info['module']:
        return None  # Ensure there's a module name available

    # Convert the module path to a GitHub path
    filename = info['module'].replace('.', '/')

    # Determine the full path to check if it's a package or a module
    # full_path = os.path.join(sys.path[0], 'src', 'pycommence', filename)
    full_path = pathlib.Path(filename)

    # Check if the path is a directory (indicating a package)
    if full_path.is_dir():
        # Append __init__.py for packages
        return f"{repo_src}/{filename}/__init__.py"
    else:
        # Append .py for regular modules
        return f"{repo_src}/{filename}.py"
