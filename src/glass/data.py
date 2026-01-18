"""
The :mod:`data` module has procedures for finding and reading data files.
"""

import glass.jsonc

import os
import os.path


def datafilepath(directoryname, filename):
    """
    Return the full path of a data file.

    The full path is given by the root data directory, followed by the directory
    name, followed by the modified file name, with a ".json" extension.

    The root data directory is give by the environment variable AIRPOWERDATADIR.
    If this is not set, the default is "../../../air-power-data", which works if
    the glass and data repositories are in the same directory. Relative paths
    are interpreted with respect to this source file.

    The file name is modified by stripping /<>:\|?* characters.

    :param directoryname: The directory name relative to the root data
        directory.
    :param filename: The file name.
    :return: The path to the data file as a string.
    """

    path = os.getenv("AIRPOWERDATADIR")
    if path is None:
        path = os.path.join("..", "..", "..", "air-power-data")

    # Interpret relative paths with respect to the source directory.
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(__file__), path)

    # Now convert it into an absolute path.
    path = os.path.abspath(path)

    # Strip forbidden printable characters from the file name.
    # https://stackoverflow.com/questions/1976007/what-characters-are-forbidden-in-windows-and-linux-directory-names#31976060
    for c in r"/<>:\|?*":
        filename = filename.replace(c, "")

    return os.path.join(
        path,
        directoryname,
        filename + ".json",
    )


def loaddatafile(directoryname, filename, withinclude=True):
    """
    Return the data object in a data file.

    The data file path is determined by calling glass.data.datafilepath and read
    using glass.jsonc.load.

    :param directoryname: The directory name relative to the root data
        directory.
    :param filename: The file name.
    :param withinclude: If True and if the object read is a dictionary with a
        "_include" key, merge the object with the ones read from the files named
        by the "_include" value, which may either be a string or a list of strings.
    :return: The object read from the data file.

    :raises RuntimeError: If the file cannot be found or read.
    """

    def load(filename):

        filepath = glass.data.datafilepath(directoryname, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = glass.jsonc.load(f)
        except FileNotFoundError:
            raise RuntimeError(
                'unable to find the %s file "%s".' % (directoryname, filename)
            )
        except glass.jsonc.JSONDecodeError as e:
            raise RuntimeError(
                'unable to read the %s file "%s": line %d: %s.'
                % (directoryname, filename, e.lineno, e.msg.lower())
            )

        if withinclude and isinstance(data, dict) and "_include" in data:
            includefilenames = data["_include"]
            if isinstance(includefilenames, str):
                includefilenames = [includefilenames]
            del data["_include"]
            for includefilename in includefilenames:
                includedata = load(includefilename)
                includedata.update(data)
                data = includedata

        return data

    return load(filename)
