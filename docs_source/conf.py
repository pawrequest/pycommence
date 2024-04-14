import sys
import inspect
import pathlib

from loguru import logger

project = 'PyCommence'
author = 'PawRequest'
release = '0.1.1'
copyright = f'2024, {author}'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.linkcode',
    'myst_parser',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.githubpages',
    'sphinx_autodoc_typehints',
    'sphinx_readme',
    'sphinx_rtd_dark_mode',
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
master_doc = 'README'

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
readme_src_files = 'README.rst'
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
#
#     filename = info['module'].replace('.', '/')
#     url = f'{repo_src}/{filename}.py'
#     return url


def linkcode_resolve(domain, info):
    if domain != 'py' or not info['module']:
        return None

    modname = info['module']
    fullname = info['fullname']
    topname = modname.split('.')[0]
    logger.info(f'modname: {modname}')
    logger.info(f'fullname: {fullname}')
    logger.info(f'topname: {topname}')

    topmod = sys.modules.get(topname)

    # Get the module object
    submod = sys.modules.get(modname)
    if submod is None:
        return None

    # Resolve the object from its fullname
    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
        except AttributeError:
            return None

    # Find the source file and adjust path as necessary
    try:
        source_file = inspect.getsourcefile(obj)
        if source_file is None:
            return None
        # Ensure the use of forward slashes
        rel_path = pathlib.Path(source_file).relative_to(
            pathlib.Path(topmod.__file__).parent
        ).as_posix()
        logger.info(f'rel_path: {rel_path}')
    except Exception as e:
        return None

    # Determine line numbers for hyperlinking specific lines
    try:
        source, lineno = inspect.getsourcelines(obj)
        linestart = lineno
        linestop = lineno + len(source) - 1
    except OSError:
        return None

    res = f"{repo_src}/{modname.replace('.', r'/')}.py#L{linestart}-L{linestop}"
    # res = f"{repo_src}/{rel_path}#L{linestart}-L{linestop}"
    logger.info(f'res: {res}')
    return res
