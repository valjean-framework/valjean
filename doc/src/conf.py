# -*- coding: utf-8 -*-
#
# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: valjean developers
# valjean-support@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

'''Configuration file for sphinx documentation.'''

import sys
from pathlib import Path
from datetime import datetime
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
              'matplotlib.sphinxext.plot_directive',
              'nbsphinx']

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
author = u'valjean developers'
copyright = f'2017-{datetime.now().year}, {author}'
project = 'valjean'
release = get_distribution(project).version
version = '.'.join(release.split('.')[:2])

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['Thumbs.db', '.DS_Store']

if not tags.has('tests'):
    exclude_patterns.append('tests.rst')
else:
    # The tests are not installed along with the valjean package. Therefore, we
    # need to set up Sphinx to import the modules from the source tree
    src_path = Path().resolve().parents[1]
    sys.path.insert(0, str(src_path))

if tags.has('no_notebooks'):
    exclude_patterns.append('**/*.ipynb')

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
    (master_doc, 'valjean.tex', 'The valjean documentation',
     u'Ève Le Ménédeu, Davide Mancusi', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'valjean', 'The valjean documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'valjean', 'The valjean documentation',
     author, 'valjean', "VALidation, Journal d'Évolution et ANalyse",
     'Miscellaneous'),
]

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
    'pytest': ('https://docs.pytest.org/en/latest/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
    'hypothesis': ('https://hypothesis.readthedocs.io/en/latest/', None),
    'virtualenvwrapper': (
        ('https://virtualenvwrapper.readthedocs.io/en/latest/', None)),
    'setuptools': ('https://setuptools.pypa.io/en/latest/', None),
    'pip': ('https://pip.pypa.io/en/stable/', None),
    'py': ('https://py.readthedocs.io/en/latest/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'h5py': ('https://docs.h5py.org/en/stable/', None)}


# Ignore internal CEA links in linkcheck
linkcheck_ignore = [r'https://.*\.intra.cea.fr/.*',
                    r'https://agupubs.onlinelibrary.wiley.com/*']

# -- doctest options ------------------------------------------------------

# Do not use doctest to test code examples that are not explicitly marked as
# doctest
doctest_test_doctest_blocks = ''

# -- autodoc options ------------------------------------------------------

# always list all class members
autodoc_default_options = {'members': True,
                           'member-order': 'bysource',
                           'special-members': True}

# nbsphinx options
nbsphinx_allow_errors = False

# pylint: disable=missing-docstring, unused-argument, too-many-arguments
def skip_weakref(app, what, name, obj, skip, options):
    if name in ('__weakref__', '__dict__', '__module__'):
        return True
    return skip


def setup(app):
    app.connect('autodoc-skip-member', skip_weakref)
