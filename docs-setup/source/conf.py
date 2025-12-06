# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

project = 'cs-audio-docs'
copyright = '2025, Lulu Ceccon, Charles Beard'
author = 'Lulu Ceccon, Charles Beard'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

import sphinx_rtd_theme

extensions = [
    # ... other extensions if you have them ...
    "sphinx_rtd_theme",
    'sphinx.ext.autodoc'
]

html_theme = "sphinx_rtd_theme"

autodoc_mock_imports = [
    "simpleaudio",
    "pyaudio",
    "pydub",
    "pyaudioop",
    "numpy",
    "wave",
    "matplotlib",
    "matplotlib.pyplot",
    "scipy"
    # Add any other library cs101audio uses that isn't standard python
]

html_static_path = ['_static']