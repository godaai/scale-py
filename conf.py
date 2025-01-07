author = 'Weizheng Lu'
bibtex_bibfiles = ['references.bib']
bibtex_reference_style = 'author_year'
comments_config = {'hypothesis': False, 'utterances': False}
copyright = '2023-2025'
exclude_patterns = ['**.ipynb_checkpoints', '.DS_Store', 'Thumbs.db', '_build']
extensions = ['sphinx_togglebutton', 'sphinx_copybutton', 'myst_nb', 'jupyter_book', 'sphinx_thebe', 'sphinx_comments', 'sphinx_external_toc', 'sphinx.ext.intersphinx', 'sphinx_design', 'sphinx_book_theme', 'sphinxcontrib.bibtex', 'sphinx_jupyterbook_latex']
external_toc_exclude_missing = True
external_toc_path = '_toc.yml'
html_baseurl = ''
html_favicon = "_static/logo.ico"
html_logo = 'logo.svg'
html_sourcelink_suffix = ''
html_theme = 'sphinx_book_theme'
html_theme_options = {
    'search_bar_text': 'Search...', 
    'launch_buttons': {
        'notebook_interface': 'classic', 
        'binderhub_url': '', 
        'jupyterhub_url': '', 
        'thebe': False, 
        'colab_url': 'https://colab.research.google.com'
    }, 
    'path_to_docs': 'docs', 

    'path_to_docs': './', 
    'repository_url': 'https://github.com/godaai/scale-py', 
    'repository_branch': 'main',
    'icon_links': [
        {
            "name": "中文版",
            "url": "https://scale-py.godaai.org/",  # required
            "icon": "fa fa-language",
            "type": "fontawesome",
        },
        {
            "name": "GitHub",
            "url": "https://github.com/godaai/scale-py",
            "icon": "https://img.shields.io/github/stars/godaai/scale-py?style=for-the-badge",
            "type": "url",
        },
    ],
    'extra_footer': '', 
    'home_page_in_toc': True, 
    'announcement': "If you find this tutorial helpful, please star our <a href=\"https://github.com/godaai/scale-py\">GitHub</a> repo!", 
    'analytics': {'google_analytics_id': ''}, 
    'use_repository_button': True, 
    'use_edit_page_button': False, 
    'use_issues_button': False,
    "toc_title": "On this page",
}
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = 'Scalable Data Science with Python'
latex_engine = 'pdflatex'
myst_enable_extensions = ['colon_fence', 'dollarmath', 'linkify', 'substitution', 'tasklist']
myst_url_schemes = ['mailto', 'http', 'https']
nb_execution_allow_errors = False
nb_execution_cache_path = ''
nb_execution_excludepatterns = []
nb_execution_in_temp = False
nb_execution_mode = 'off'
nb_execution_timeout = 30
nb_output_stderr = 'show'
numfig = True
pygments_style = 'sphinx'
suppress_warnings = ['myst.domains']
use_jupyterbook_latex = True
use_multitoc_numbering = True
