#!/usr/bin/env python3
import subprocess
import sys
import os
import threading
import tkinter as tk
from tkinter import ttk
import webbrowser
from pathlib import Path

REMOTE = "googlesuiteopener:/GoogleSuiteOpener/"

# ------------------ RCLONE UTILS ------------------
def rclone_config_path():
    if os.name == "nt":
        return Path(os.getenv("APPDATA")) / "rclone" / "rclone.conf"
    else:
        return Path.home() / ".config" / "rclone" / "rclone.conf"

def run_rclone(cmd, **kwargs):
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    return subprocess.run(["rclone"] + cmd, **kwargs)

def ensure_rclone_config():
    cfg = rclone_config_path()
    if cfg.exists():
        try:
            result = run_rclone(["listremotes"], capture_output=True, text=True, check=True)
            remotes = [r.strip().rstrip(":") for r in result.stdout.splitlines()]
            if "googlesuiteopener" in remotes:
                return
        except subprocess.CalledProcessError:
            pass
    run_rclone(["config", "create", "googlesuiteopener", "drive", "scope=drive.file", "team_drive="], check=True)

def normalize_path(path):
    if path.startswith("\\\\?\\") or path.startswith("//?/"):
        path = path[4:]
    return os.path.abspath(path)

# ------------------ UI ------------------
class UploadUI:
    def __init__(self, file_path):
        self.root = tk.Tk()
        self.root.title("Google Suite Opener")
        self.root.configure(bg="white")

        # Window size and centering
        w, h = 420, 150
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.resizable(False, False)

        # Status label
        self.label = tk.Label(self.root, text="Starting…", font=("Segoe UI", 12), bg="white")
        self.label.pack(pady=(30, 15))

        # Modern themed progress bar
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Custom.Horizontal.TProgressbar",
                        troughcolor="#f0f0f0", background="#4a90e2",
                        thickness=15, troughrelief="flat", borderwidth=0)

        self.progress = ttk.Progressbar(self.root, length=360, mode="indeterminate",
                                        style="Custom.Horizontal.TProgressbar")
        self.progress.pack(pady=5)
        self.progress.start(15)

        # Start worker thread
        threading.Thread(target=self.upload_file, args=(file_path,), daemon=True).start()

    def update_status(self, text):
        self.label.config(text=text)

    def upload_file(self, file_path):
        try:
            self.update_status("Checking rclone config…")
            ensure_rclone_config()

            file_path = normalize_path(file_path)

            self.update_status("Uploading to Google Drive…")
            run_rclone(["copy", file_path, REMOTE], check=True)

            self.update_status("Getting share link…")
            result = run_rclone(
                ["link", REMOTE + os.path.basename(file_path)],
                capture_output=True, text=True, check=True
            )
            link = result.stdout.strip()

            if link:
                self.update_status("Opening in browser…")
                webbrowser.open(link)
                self.update_status("Done")
            else:
                self.update_status("Failed to get link")

        except subprocess.CalledProcessError:
            self.update_status("Upload failed")
        finally:
            self.progress.stop()
            self.root.after(2000, self.root.destroy)

    def run(self):
        self.root.mainloop()

# ------------------ MAIN ------------------
def main(file_path):
    ui = UploadUI(file_path)
    ui.run()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: open_in_google.py <file_path>")
        sys.exit(1)
    main(sys.argv[1])
