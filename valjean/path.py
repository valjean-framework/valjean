'''Utility functions to access the filesystem.'''
from pathlib import Path


def ensure(*paths, is_dir=False):
    '''Make sure that the given path exists.

    :param paths: One or more paths. Multiple arguments will be concatenated
        into a single path.
    :type paths: str or pathlib.Path or pathlib2.Path
    :param bool is_dir: If `True`, the path will be constructed as a directory.
    '''
    path = Path(*(str(path) for path in paths))
    if not path.exists():
        if is_dir:
            path.mkdir(parents=True)
        else:
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            path.touch()
    return path


def sanitize_filename(name):
    '''Check that the `name` string can be used as a filename.

    :raises ValueError: if the string contains characters that are forbidden in
        a filename.
    :returns: `name` unchanged
    '''
    if '\0' in name:
        raise ValueError(r"NULL character ('\0') is not allowed in filename "
                         "{!r}".format(name))
    if '/' in name:
        raise ValueError(r"slash ('/') is not allowed in filename {!r}"
                         .format(name))
    if name in ('.', '..'):
        raise ValueError('{!r} is not a valid filename'.format(name))
    return name
