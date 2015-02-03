pydocverter
===========

Python client for [Docverter][] service

[Docverter][] is a hosted service
that can do convert documents from one format to another (using [pandoc][]).
For example, it can be used to convert [Markdown][] documents to [reStructuredText][].
This is very useful if you prefer to write your `README` in Markdown,
but want to publish your package to PyPI,
which only knows how to do nice rendering of descriptions
written in reStructuredText.

This module is a Python client to the Docverter service.

It has a very similar API to that of [pypandoc][], so that you can do stuff like:

.. code-block:: python

    try:
        import pypandoc as converter
    except ImportError:
        import pydocverter as converter

    converter.convert('somefile.md', 'rst')


[Docverter]: http://www.docverter.com/
[pandoc]: http://johnmacfarlane.net/pandoc
[Markdown]: http://daringfireball.net/projects/markdown/
[reStructuredText]: http://docutils.sourceforge.net/rst.html
[pypandoc]: https://github.com/bebraw/pypandoc
