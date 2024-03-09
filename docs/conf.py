project = 'Pycommence'
author = 'PawRequest'
release = '0.0.1'
copyright = f'2024, {author}'
extensions = [
    'autodoc2',
    # 'sphinx_autodoc_typehints',
    'sphinx_readme',
    "myst_parser",
    'sphinx.ext.napoleon',

]
autodoc2_docstring_parser_regexes = [
    (r".*", "myst"),  # This will render all docstrings as Markdown
]
autodoc2_packages = [
    "../src/pycommence",
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
html_static_path = ['_static']

html_context = {
    'display_github': True,
    'github_user': 'PawRequest',
    'github_repo': 'pycommence',
}
html_baseurl = "https://pycommence.readthedocs.io/en/latest"
readme_src_files = "index.md"
readme_docs_url_type = "html"
add_module_names = False
