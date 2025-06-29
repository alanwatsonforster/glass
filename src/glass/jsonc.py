"""
The :mod:`jsonc` module reads JSON with whole-line // comments.

It does not support trailing // comments or block /* */ comments.

"""

import json
import re

from json import JSONDecodeError

__all__ = ["load", "loads", "JSONDecodeError"]


def loads(s):
    """
    Deserialize a string to an object.

    :param s: A string containing the JSONC document to be deserialized.
    :return: The deserialized object.
    """

    # Strip whole-line // comments.
    r = re.compile("^[ \t]*//.*$", re.MULTILINE)
    s = re.sub(r, "", s)

    return json.loads(s)


def load(f, **kwargs):
    """
    Deserialize a file-like object to an object.

    :param f: A `.read()`-supporting text file or binary file containing the JSONC document to be deserialized.
    :return: The deserialized object.
    """
    return loads(f.read(-1), **kwargs)
