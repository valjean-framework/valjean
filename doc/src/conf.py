# -*- coding: utf-8 -*-
#
# valjean documentation build configuration file, created by
# sphinx-quickstart on Mon Oct  2 18:23:32 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
'''Configuration file for sphinx documentation.'''

from pkg_resources import get_distribution
import matplotlib
matplotlib.use('AGG')

# pylint: disable=invalid-name

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.doctest',
              'sphinx.ext.intersphinx',
              'sphinx.ext.graphviz',
              'sphinx.ext.todo',
              'sphinx.ext.coverage',
              'sphinx.ext.viewcode',
              'sphinx.ext.imgmath',
              'matplotlib.sphinxext.plot_directive']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['.templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
author = u'Ève Le Ménédeu, Davide Mancusi'
copyright = u'2017-2019, ' + author  # pylint: disable=redefined-builtin
project = 'valjean'
release = get_distribution(project).version
version = '.'.join(release.split('.')[:2])

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# warn about broken cross-references
nitpicky = False

# do not automatically add parenthesis to :meth: and :func: references
add_function_parentheses = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['.static']

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'valjeandoc'


# -- Options for LaTeX output ---------------------------------------------
latex_engine = 'xelatex'
# no fontpkg: default is Times for text, Helevetica for sans serif and Courier
# for monospace what corresponds to CEA recommandations... but some unicode
# characters missing
latex_elements = {
    'fontpkg': r'''
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}
''',
    'preamble': r'''
\usepackage[titles]{tocloft}
\cftsetpnumwidth {1.25cm}\cftsetrmarg{1.5cm}
\setlength{\cftchapnumwidth}{0.75cm}
\setlength{\cftsecindent}{\cftchapnumwidth}
\setlength{\cftsecnumwidth}{1.25cm}
''',
    'fncychap': r'\usepackage[Bjornstrup]{fncychap}',
    'printindex': r'\footnotesize\raggedright\printindex',
}
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'valjean.tex', 'valjean Documentation',
     u'Ève Le Ménédeu, Davide Mancusi', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'valjean', 'valjean Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'valjean', 'valjean Documentation',
     author, 'valjean', 'One line description of project.',
     'Miscellaneous'),
]

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
    'pytest': ('https://docs.pytest.org/en/latest/', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None),
    'hypothesis': ('https://hypothesis.readthedocs.io/en/latest/', None),
    'virtualenvwrapper': (
        ('https://virtualenvwrapper.readthedocs.io/en/latest/', None)),
    'setuptools': ('https://setuptools.readthedocs.io/en/latest/', None),
    'pip': ('https://pip.pypa.io/en/stable/', None),
    'py': ('https://py.readthedocs.io/en/latest/', None),
    'matplotlib': ('https://matplotlib.org/', None)}

# -- doctest options ------------------------------------------------------

# Do not use doctest to test code examples that are not explicitly marked as
# doctest
doctest_test_doctest_blocks = ''

# -- autodoc options ------------------------------------------------------

# always list all class members
autodoc_default_options = {'members': True,
                           'member-order': 'bysource',
                           'special-members': True}


# pylint: disable=missing-docstring, unused-argument, too-many-arguments
def skip_weakref(app, what, name, obj, skip, options):
    if name in ('__weakref__', '__dict__', '__module__'):
        return True
    return skip


def setup(app):
    app.connect('autodoc-skip-member', skip_weakref)
