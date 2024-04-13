project = 'Pycommence'
author = 'PawRequest'
release = '0.1.1'
copyright = f'2024, {author}'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx_rtd_dark_mode',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosectionlabel',
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
autodoc_mock_imports = ["win32com", "pywintypes", "win32api", "win32con", "pywin32", "comtypes", "com_error"]

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']

html_context = {
    'display_github': True,
    'github_user': 'PawRequest',
    'github_repo': 'pycommence',
}
html_baseurl = 'https://pycommence.readthedocs.io/en/latest'
readme_src_files = 'index.rst'
readme_docs_url_type = 'html'
add_module_names = False
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'undoc-members': True,
    # 'no-show-inheritance': True,
    # 'show-inheritance': True,
}
