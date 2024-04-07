project = 'Pycommence'
author = 'PawRequest'
release = '0.0.1'
copyright = f'2024, {author}'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    # 'sphinx_readme',
    'sphinx.ext.napoleon',
    "sphinx_rtd_dark_mode",
    'sphinx.ext.viewcode',
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']

html_context = {
    'display_github': True,
    'github_user': 'PawRequest',
    'github_repo': 'pycommence',
}
html_baseurl = "https://pycommence.readthedocs.io/en/latest"
readme_src_files = "index.rst"
readme_docs_url_type = "html"
add_module_names = False

# def linkcode_resolve(domain, info):
#     if domain != 'py':
#         return None
#     if not info['module']:
#         return None
#     filename = info['module'].replace('.', '/')
#     return f"https://github.com/pawrequest/pycommence/tree/main/src/{filename}.py"
