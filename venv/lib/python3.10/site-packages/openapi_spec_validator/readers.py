import os
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib
import sys

from openapi_spec_validator import all_urls_handler, file_object_handler


def read_from_stdin(filename):
    return file_object_handler(sys.stdin), ''


def read_from_filename(filename):
    if not os.path.isfile(filename):
        raise IOError("No such file: {0}".format(filename))

    filename = os.path.abspath(filename)
    uri = pathlib.Path(filename).as_uri()
    return all_urls_handler(uri), uri
