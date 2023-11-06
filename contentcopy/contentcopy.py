import hashlib
import logging
import os
from shutil import copyfile
from typing import Dict, Iterator, Tuple
from gooey import Gooey, GooeyParser


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


def merge_filetrees(source: str, dest: str, file_filter=lambda x: True, dry_run=False):
    '''Merge dest into source, deduplicating files based on file content'''

    logger = logging.getLogger(__name__)

    logger.debug('indexing {}'.format(source))
    source_index = index_file_contents(source, file_filter)

    logger.debug('indexing {}'.format(dest))
    destination_index = index_file_contents(dest, file_filter)


    for fcontent, fpath in difference(destination_index, source_index):
        # split extension from filename and append to destination path
        original_fname = fpath.rsplit(os.path.sep, 1)[1]
        fname = original_fname
        fdest = os.path.join(dest, fname)

        # check if destination file already exists,
        # if so append _<i> until a filename is available
        i = 1
        renamed = False
        while os.path.isfile(fdest):
            renamed = True
            # split the extension from the filepath
            path, extension = os.path.splitext(fpath)

            # split the filename from the filepath
            fname = path.rsplit(os.path.sep, 1)[1]

            # construct a new filename based on i
            fname = '{}_{}{}'.format(fname, i, extension)
            fdest = os.path.join(dest, fname)
            i += 1

        if renamed:
            logger.debug('file exists, renaming {} to {}'.format(
                original_fname, fname))

        logger.debug('copying {} => {}'.format(fpath, fdest))

        # create destination file and copy
        if not dry_run:
            with open(fdest, 'w+'):
                copyfile(fpath, fdest)
@Gooey
def main():
    import argparse
    parser = GooeyParser(
    # parser = argparse.ArgumentParser(
        description='''
Merge two folders based on file content hash.
Files will be copied from <source> into <destination> if a file with the same content does not already exist in <destination>.
If a file with differing content but the same filename is encountered, the copied file will have an integer appended to its filename.
''')
    parser.add_argument('source', widget="DirChooser")
    parser.add_argument('destination', widget="DirChooser")
    parser.add_argument('--dry-run', dest='dryrun',
                        default=False, action='store_true', help="Don't copy files, log entries are still generated")
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    form = logging.Formatter('%(asctime)s %(message)s',
                             datefmt='%m/%d/%Y %I:%M:%S')

    ch.setFormatter(form)
    logger.addHandler(ch)

    merge_filetrees(args.source, args.destination, dry_run=args.dryrun)

    logger.info('done')

if __name__ == '__main__':
    main()