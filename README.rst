pydocverter
===========

Python client for Docverter_ service

Docverter_ is a hosted service
that can do convert documents from one format to another (using pandoc_).
For example, it can be used to convert Markdown_ documents to reStructuredText_.
This is very useful if you prefer to write your ``README`` in Markdown,
but want to publish your package to PyPI,
which only knows how to do nice rendering of descriptions
written in reStructuredText.

This module is a Python client to the Docverter service.

It has a very similar API to that of pypandoc_, so that you can do stuff like:

.. code-block:: python

    try:
        import pypandoc as converter
    except ImportError:
        import pydocverter as converter

    converter.convert('somefile.md', 'rst')


.. _Docverter: http://www.docverter.com/
.. _pandoc: http://johnmacfarlane.net/pandoc
.. _Markdown: http://daringfireball.net/projects/markdown/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _pypandoc: https://github.com/bebraw/pypandoc
