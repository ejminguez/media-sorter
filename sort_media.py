#!/usr/bin/env python3
"""
Sort photos and videos into folders by the month they were created.

Result looks like this:
    Sorted_Media/
        2026-10 October/
            Photos/
            Videos/
        2026-09 September/
            Photos/
            Videos/

Usage:
    python3 sort_media.py /path/to/your/folder
    python3 sort_media.py /path/to/your/folder --dry-run
    python3 sort_media.py /path/to/your/folder --move
    python3 sort_media.py /path/to/your/folder --dest /path/to/output

By default the script COPIES files, so your originals stay safe.
Use --move if you want the files moved instead.
No extra packages needed. It only uses Python's standard library.
"""

import argparse
import shutil
from datetime import datetime
from pathlib import Path

PHOTO_EXTS = {
    ".jpg", ".jpeg", ".png", ".heic", ".heif", ".gif", ".tif", ".tiff",
    ".bmp", ".webp", ".dng", ".cr2", ".cr3", ".nef", ".arw", ".raf",
}
VIDEO_EXTS = {
    ".mp4", ".mov", ".m4v", ".avi", ".mkv", ".wmv", ".webm", ".mts",
    ".m2ts", ".3gp", ".flv",
}


def get_modified_date(path: Path) -> datetime:
    return datetime.fromtimestamp(path.stat().st_mtime)


def unique_path(target: Path) -> Path:
    if not target.exists():
        return target
    counter = 1
    while True:
        candidate = target.with_name(f"{target.stem}_{counter}{target.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def sort_media_core(source: Path, dest: Path, move: bool = False, dry_run: bool = False, progress_callback=None):
    count_photos = 0
    count_videos = 0
    skipped = 0

    all_files = sorted(source.rglob("*"))
    media_files = []
    for file in all_files:
        if not file.is_file() or file.name.startswith("."):
            continue
        if dest in file.parents:
            continue
        ext = file.suffix.lower()
        if ext in PHOTO_EXTS or ext in VIDEO_EXTS:
            media_files.append(file)
        else:
            skipped += 1

    total = len(media_files)
    for idx, file in enumerate(media_files, 1):
        ext = file.suffix.lower()
        if ext in PHOTO_EXTS:
            kind = "Photos"
        else:
            kind = "Videos"

        modified = get_modified_date(file)
        month_folder = modified.strftime("%Y-%m %B")
        target_dir = dest / month_folder / kind
        target = unique_path(target_dir / file.name)

        action = "MOVE" if move else "COPY"
        log_line = f"{action}: {file.name}  ->  {month_folder}/{kind}/"

        if progress_callback:
            progress_callback(idx, total, log_line)
        else:
            print(log_line)

        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
            if move:
                shutil.move(str(file), str(target))
            else:
                shutil.copy2(str(file), str(target))

        if kind == "Photos":
            count_photos += 1
        else:
            count_videos += 1

    summary = {
        "photos": count_photos,
        "videos": count_videos,
        "skipped": skipped,
        "dest": str(dest),
        "dry_run": dry_run,
    }

    if progress_callback:
        progress_callback(total, total, "DONE")
    return summary


def main():
    parser = argparse.ArgumentParser(description="Sort media by month, then by photo or video.")
    parser.add_argument("source", help="Folder that has your media files")
    parser.add_argument("--dest", help="Where to put the sorted folders (default: <source>/Sorted_Media)")
    parser.add_argument("--move", action="store_true", help="Move files instead of copying them")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without changing anything")
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    if not source.is_dir():
        raise SystemExit(f"Folder not found: {source}")

    dest = Path(args.dest).expanduser().resolve() if args.dest else source / "Sorted_Media"

    summary = sort_media_core(source, dest, move=args.move, dry_run=args.dry_run)

    print()
    print("Dry run, nothing was changed." if summary["dry_run"] else "Done!")
    print(f"Photos: {summary['photos']} | Videos: {summary['videos']} | Skipped (not media): {summary['skipped']}")
    print(f"Output folder: {summary['dest']}")


if __name__ == "__main__":
    main()
