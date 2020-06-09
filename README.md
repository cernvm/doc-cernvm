### CernVM Virtual Machine Documentation

This contains the rST sources and image assets for the CernVM virtual machine user documentation.

[![Documentation Status](https://readthedocs.org/projects/cernvm/badge/?version=latest)](http://cernvm.readthedocs.org/en/latest/?badge=latest)

#### Building the HTML documentation

The [official CernVM virtual machine documentation](http://cernvm.readthedocs.org/en/latest/) is built automatically by [readthedocs.org](https://readthedocs.org). It can also be build locally for editing purposes or different output formats.

The build requirements for the documentation are [Sphinx](http://sphinx-doc.org) and the [Sphinx RTD theme](https://github.com/snide/sphinx_rtd_theme). Both of which can be conveniently installed via `pip`:

```bash
pip install Sphinx sphinx_rtd_theme
```

Afterwards a simple `make html` in this repository's root directory generates the documentation in `_build/html/`. Opening `_build/html/index.html` in any browser is enough.

