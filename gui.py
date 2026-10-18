#!/usr/bin/env python3

import threading
import tkinter as tk
from functools import partial
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

from sort_media import sort_media_core


class MediaSorterGUI:
    def __init__(self, root):
        self.root = root
        root.title("Media Sorter")
        root.geometry("720x540")
        root.minsize(600, 450)

        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()
        self.move_var = tk.BooleanVar(value=False)
        self.dry_run_var = tk.BooleanVar(value=False)
        self.running = False

        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 5}

        source_frame = ttk.Frame(self.root)
        source_frame.pack(fill="x", **pad)
        ttk.Label(source_frame, text="Source Folder:").pack(anchor="w")
        source_row = ttk.Frame(source_frame)
        source_row.pack(fill="x")
        ttk.Entry(source_row, textvariable=self.source_path).pack(side="left", fill="x", expand=True)
        ttk.Button(source_row, text="Browse...", command=self._browse_source).pack(side="right", padx=(5, 0))

        dest_frame = ttk.Frame(self.root)
        dest_frame.pack(fill="x", **pad)
        ttk.Label(dest_frame, text="Destination Folder (optional):").pack(anchor="w")
        dest_row = ttk.Frame(dest_frame)
        dest_row.pack(fill="x")
        ttk.Entry(dest_row, textvariable=self.dest_path).pack(side="left", fill="x", expand=True)
        ttk.Button(dest_row, text="Browse...", command=self._browse_dest).pack(side="right", padx=(5, 0))

        options_frame = ttk.Frame(self.root)
        options_frame.pack(fill="x", **pad)
        ttk.Checkbutton(options_frame, text="Move files (instead of copy)", variable=self.move_var).pack(side="left")
        ttk.Checkbutton(options_frame, text="Dry run", variable=self.dry_run_var).pack(side="left", padx=(20, 0))

        self.progress = ttk.Progressbar(self.root, mode="determinate")
        self.progress.pack(fill="x", **pad)

        self.status_label = ttk.Label(self.root, text="Ready")
        self.status_label.pack(anchor="w", padx=10)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", **pad)
        self.run_button = ttk.Button(btn_frame, text="Sort Media", command=self._on_run)
        self.run_button.pack(side="left")
        ttk.Button(btn_frame, text="Clear Log", command=self._clear_log).pack(side="left", padx=(5, 0))

        ttk.Label(self.root, text="Log:").pack(anchor="w", padx=10)
        self.log_area = scrolledtext.ScrolledText(self.root, height=15, state="disabled")
        self.log_area.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _browse_source(self):
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            self.source_path.set(folder)
            if not self.dest_path.get():
                self.dest_path.set(str(Path(folder) / "Sorted_Media"))

    def _browse_dest(self):
        folder = filedialog.askdirectory(title="Select Destination Folder")
        if folder:
            self.dest_path.set(folder)

    def _clear_log(self):
        self.log_area.config(state="normal")
        self.log_area.delete("1.0", "end")
        self.log_area.config(state="disabled")

    def _append_log(self, text):
        self.log_area.config(state="normal")
        self.log_area.insert("end", text + "\n")
        self.log_area.see("end")
        self.log_area.config(state="disabled")

    def _update_progress(self, current, total, message):
        pct = (current / total * 100) if total > 0 else 0
        self.progress["value"] = pct
        self.status_label.config(text=f"{current}/{total} — {message[:80]}")
        if message != "DONE":
            self._append_log(message)

    def _on_run(self):
        if self.running:
            return

        source = Path(self.source_path.get()).expanduser().resolve()
        if not source.is_dir():
            messagebox.showerror("Error", f"Folder not found:\n{source}")
            return

        dest_str = self.dest_path.get().strip()
        dest = Path(dest_str).expanduser().resolve() if dest_str else source / "Sorted_Media"

        self.running = True
        self.run_button.config(state="disabled")
        self.progress["value"] = 0
        self._clear_log()
        self._append_log(f"Source: {source}")
        self._append_log(f"Destination: {dest}")
        self._append_log(f"Mode: {'MOVE' if self.move_var.get() else 'COPY'}")
        self._append_log("-" * 50)

        worker = threading.Thread(
            target=self._run_sort,
            args=(source, dest, self.move_var.get(), self.dry_run_var.get()),
            daemon=True,
        )
        worker.start()

    def _run_sort(self, source, dest, move, dry_run):
        try:
            summary = sort_media_core(
                source,
                dest,
                move=move,
                dry_run=dry_run,
                progress_callback=partial(self.root.after, 0, self._update_progress),
            )
        except Exception as exc:
            self.root.after(0, lambda: self._append_log(f"ERROR: {exc}"))
            self.root.after(0, lambda: messagebox.showerror("Error", str(exc)))
        else:
            done_msg = "Dry run, nothing was changed." if summary["dry_run"] else "Done!"
            self.root.after(0, lambda: self._append_log("-" * 50))
            self.root.after(0, lambda: self._append_log(done_msg))
            self.root.after(0, lambda: self._append_log(
                f"Photos: {summary['photos']} | Videos: {summary['videos']} | Skipped: {summary['skipped']}"
            ))
            self.root.after(0, lambda: self._append_log(f"Output folder: {summary['dest']}"))
        finally:
            self.root.after(0, self._on_sort_complete)

    def _on_sort_complete(self):
        self.running = False
        self.run_button.config(state="normal")
        self.status_label.config(text="Ready")


def main():
    root = tk.Tk()
    MediaSorterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
