# media-sorter

hi, this is a media sorter para organize ka!

features:

- Sorts photos and videos into folders by the month they were created
- Makes a `Photos` and a `Videos` folder inside each month
- Copies files by default, so your originals stay safe
- Has a dry run mode to preview changes first
- Handles duplicate file names without overwriting anything
- No extra packages needed, only Python 3

## how to use

```
python3 sort_media.py /path/to/your/folder
```

options:

- `--dry-run` shows what would happen, changes nothing
- `--move` moves files instead of copying them
- `--dest /path/to/output` saves the sorted folders somewhere else

## result

```
Sorted_Media/
  2026-10 October/
    Photos/
    Videos/
  2026-09 September/
    Photos/
    Videos/
```
