# ContentCopy
ContentCopy merges directory contents, deduplicating files based on their content.

If a file with differing contents but the same name is encountered, the copied filename will automatically have a number appended, making it easy to see duplicate filenames. No folder structure will be copied.

## Usage
```
python3 contentcopy.py <source> <dest>
```

e.g.

```
python3 contentcopy.py old_pictures new_pictures
```

Will copy all pictures in old_pictures that are not yet in new_pictures to new_pictures. After this you can safely delete old_pictures without worrying about data loss.

## Installation
```
pip install contentcopy
```