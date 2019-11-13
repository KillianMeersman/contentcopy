import hashlib
import logging
import os
from shutil import copyfile
from typing import Dict, Iterator, Tuple


def hash_file_content(filepath: str) -> str:
    ''' Hash a file's content using the sha256 hashing algorithm '''

    md5_hash = hashlib.sha256()
    with open(filepath, 'rb') as f:
        # Read in chunks if larger than 100MB
        if os.path.getsize(filepath) > 1e+8:
            for chunk in iter(lambda: f.read(4096), b''):
                md5_hash.update(chunk)
        else:
            md5_hash.update(f.read())

    return md5_hash.hexdigest()


def walk_files(path: str, max_depth=-1) -> Iterator[str]:
    '''
    Walk all subdirectories and list all file paths
    Accepts a max_depth parameter, -1 indicates no max_depth
    '''

    for (dirpath, dirnames, filenames) in os.walk(path):
        # Check depth
        if max_depth > -1:
            depth = dirpath.count(os.path.sep) - 1
            if depth >= max_depth:
                continue

        # Yield all file paths
        for filename in filenames:
            yield os.path.join(dirpath, filename)


def index_file_contents(path: str, filter_func=lambda x: True) -> Dict[str, str]:
    '''
    Creates a dictionary containing the
    file content hash as key and the file path as value
    '''
    file_contents: Dict[str, str] = {}

    filepath = ''
    for filepath in filter(filter_func, walk_files(path)):
        file_contents[hash_file_content(filepath)] = filepath

    return file_contents


def difference(a: Dict, b: Dict) -> Iterator[Tuple[str, str]]:
    '''Returns the items in b that are not in a'''

    for key, value in b.items():
        if a.get(key, None) is None:
            yield key, value


def merge_filetrees(source: str, dest: str, file_filter=lambda x: True):
    '''Merge dest into source, deduplicating files based on file content'''

    logger = logging.getLogger(__name__)

    logger.debug('indexing {}'.format(source))
    source_index = index_file_contents(args.source, file_filter)

    logger.debug('indexing {}'.format(dest))
    destination_index = index_file_contents(args.destination, file_filter)

    for fcontent, fpath in difference(destination_index, source_index):
        # split extension from filename and append to destination path
        original_fname = fpath.rsplit('/', 1)[1]
        fname = original_fname
        dest = os.path.join(args.destination, fname)

        # check if destination file already exists,
        # if so append _<i> until a filename is available
        i = 1
        renamed = False
        while os.path.isfile(dest):
            renamed = True
            # split the extension from the filepath
            path, extension = os.path.splitext(fpath)

            # split the filename from the filepath
            fname = path.rsplit('/', 1)[1]

            # construct a new filename based on i
            fname = '{}_{}{}'.format(fname, i, extension)
            dest = os.path.join(args.destination, fname)
            i += 1

        if renamed:
            logger.debug('file exists, renaming {} to {}'.format(
                original_fname, fname))

        logger.debug('copying {} => {}'.format(fpath, dest))

        # create destination file and copy
        with open(dest, 'w+'):
            copyfile(fpath, dest)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Merge two folders based on file content hash')
    parser.add_argument('source')
    parser.add_argument('destination')
    parser.add_argument('--dry-run', dest='dryrun',
                        default=False, action='store_true')
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    form = logging.Formatter('%(asctime)s %(message)s',
                             datefmt='%m/%d/%Y %I:%M:%S')

    ch.setFormatter(form)
    logger.addHandler(ch)

    def picture_filter(x):
        return not x.endswith('.mp4')

    merge_filetrees(args.source, args.destination, picture_filter)

    logger.info('done')
