# media-sorter

Sort photos and videos into folders by the month they were created.

## Features

- Sorts photos and videos into folders by the month they were created
- Makes a `Photos` and a `Videos` folder inside each month
- Copies files by default, so your originals stay safe
- Has a dry run mode to preview changes first
- Handles duplicate file names without overwriting anything
- No extra packages needed, only Python 3
- GUI with folder picker, progress bar, and live log
- Can be built as a standalone executable

## CLI Usage

```
python3 sort_media.py /path/to/your/folder
```

Options:

- `--dry-run` shows what would happen, changes nothing
- `--move` moves files instead of copying them
- `--dest /path/to/output` saves the sorted folders somewhere else

## GUI Usage

```
python3 gui.py
```

1. Click **Browse...** to select a source folder
2. Optionally change the destination folder
3. Choose **Move files** or **Dry run** if needed
4. Click **Sort Media** and watch progress in the log

## Build as Standalone Executable

Install PyInstaller and run:

```
pip install pyinstaller
pyinstaller --onefile --windowed gui.py --name MediaSorter
```

The executable will be at `dist/MediaSorter` (macOS) or `dist/MediaSorter.exe` (Windows).

## Result

### sample na run oh!
<img width="506" height="402" alt="media-sorter-sample-run" src="https://github.com/user-attachments/assets/3b0019f0-4f80-42bb-912a-79ddb5fccb18" />

### inani diay iyahang nawng pag ma sort na
<img width="752" height="98" alt="image" src="https://github.com/user-attachments/assets/45b1df5c-f1a1-4dd6-8409-4e0dace0bbdd" />

```
Sorted_Media/
  2026-10 October/
    Photos/
    Videos/
  2026-09 September/
    Photos/
    Videos/
```
