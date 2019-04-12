'''Utility functions to access the filesystem.'''
from pathlib import Path


def ensure(path, *, is_dir=False):
    '''Make sure that the given path exists.

    :param pathlib.Path path: A path.
    :param bool is_dir: If `True`, the path will be constructed as a directory.
    '''
    path = Path(path)
    if path.exists():
        return
    if is_dir:
        path.mkdir(parents=True)
    else:
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        path.touch()


def sanitize_filename(name):
    '''Sanitize a string so that it may be used as a filename.'''
    return ''.join(c if _allowed_char(c) else '_' for c in name)


def _allowed_char(char):
    return char.isalnum() or char == '.'
