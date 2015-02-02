# -*- coding: utf-8 -*-
from __future__ import with_statement

__author__ = 'Marc Abramowitz'
__version__ = '0.0.0'
__license__ = 'MIT'
__all__ = ['convert', 'get_pandoc_formats']

from tempfile import NamedTemporaryFile
import os

import requests

DOCVERTER_DEFAULT_URL = 'http://c.docverter.com/convert'


def convert(source, to, format=None, extra_args=(), encoding='utf-8'):
    '''Converts given `source` from `format` `to` another. `source` may be
    either a file path or a string to be converted. It's possible to pass
    `extra_args` if needed. In case `format` is not provided, it will try to
    invert the format based on given `source`.

    Raises OSError if pandoc is not found! Make sure it has been installed and
    is available at path.

    '''
    return _convert(_read_file, _process_file, source, to,
                    format, extra_args, encoding=encoding)


def _convert(reader, processor, source, to,
             format=None, extra_args=(), encoding=None):
    source, format = reader(source, format, encoding=encoding)

    formats = {
        'dbk': 'docbook',
        'md': 'markdown',
        'rest': 'rst',
        'tex': 'latex',
    }

    format = formats.get(format, format)
    to = formats.get(to, to)

    if not format:
        raise RuntimeError('Missing format!')

    from_formats, to_formats = get_pandoc_formats()

    if format not in from_formats:
        raise RuntimeError(
            'Invalid input format! Expected one of these: ' +
            ', '.join(from_formats))

    if to not in to_formats:
        raise RuntimeError(
            'Invalid to format! Expected one of these: ' +
            ', '.join(to_formats))

    return processor(source, to, format, extra_args)


def _read_file(source, format, encoding='utf-8'):
    try:
        path = os.path.exists(source)
    except UnicodeEncodeError:
        path = os.path.exists(source.encode('utf-8'))
    if path:
        import codecs
        with codecs.open(source, encoding=encoding) as f:
            format = format or os.path.splitext(source)[1].strip('.')
            source = f.read()

    return source, format


def _process_file(source_text, to_format, from_format, extra_args):
    # @todo: allow passing custom url
    url = DOCVERTER_DEFAULT_URL

    with NamedTemporaryFile('w+t') as temp_file:
        temp_file.write(source_text)
        temp_file.seek(0)

        req = requests.Request(
            'POST', url,
            data={'from': from_format, 'to': to_format},
            files={'input_files[]': temp_file},
        )
        prepared = req.prepare()
        session = requests.Session()
        resp = session.send(prepared)
        # import pdb; pdb.set_trace()
        if resp.ok:
            return resp.text
        else:
            if resp.status_code == 500:
                req = prepared
                print('**** Got a 500 error from server *****')
                print('{0}\n{1}\n{2}\n\n{3}'.format(
                    '-----------START-----------',
                    req.method + ' ' + req.url,
                    '\n'.join('{0}: {1}'.format(k, v)
                              for k, v in req.headers.items()),
                    req.body,
                ))
            print('temp_file = %r' % temp_file)
            print('temp_file.name = %r' % temp_file.name)
            raise RuntimeError(
                'Call to docverter failed - resp = %r; resp.content = %r'
                % (resp, resp.content))


def get_pandoc_formats():
    '''
    Dynamic preprocessor for Pandoc formats.
    Return 2 lists. "from_formats" and "to_formats".
    '''
    from_formats = ['markdown', 'texttile', 'rst', 'html', 'docbook', 'latex']
    to_formats = ['markdown', 'rst', 'html', 'latex', 'context', 'mediawiki',
                  'textile', 'org', 'texinfo', 'docbook', 'docx', 'epub',
                  'mobi', 'asciidoc', 'rtf']

    return from_formats, to_formats
