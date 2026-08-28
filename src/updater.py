import json
import argparse
from pathlib import Path
import subprocess
import tempfile
import tkinter as tk
from tkinter import messagebox
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


GITHUB_REPOSITORY = "styrman-g/P-Tools"
RELEASES_API_URL = (
    f"https://api.github.com/repos/{GITHUB_REPOSITORY}/releases/latest"
)


def download_latest_installer():
    request = Request(RELEASES_API_URL, headers={"User-Agent": "P-Tools-Updater"})
    with urlopen(request, timeout=15) as response:
        release = json.load(response)

    installer_url = next(
        asset["browser_download_url"]
        for asset in release.get("assets", [])
        if asset.get("name") == "P-Tools-Setup.exe"
    )
    installer_file = tempfile.NamedTemporaryFile(
        prefix="P-Tools-Setup-", suffix=".exe", delete=False
    )
    installer_path = Path(installer_file.name)
    installer_file.close()
    installer_request = Request(
        installer_url, headers={"User-Agent": "P-Tools-Updater"}
    )
    with urlopen(installer_request, timeout=60) as response:
        installer_path.write_bytes(response.read())
    return installer_path


def wait_for_parent(parent_pid):
    if not parent_pid:
        return
    while True:
        try:
            import os

            os.kill(parent_pid, 0)
        except (OSError, ProcessLookupError):
            return


def update(parent_pid):
    try:
        installer_path = download_latest_installer()
        wait_for_parent(parent_pid)
        subprocess.Popen(
            [str(installer_path), "/CLOSEAPPLICATIONS"], close_fds=True
        )
    except (HTTPError, URLError, KeyError, StopIteration, OSError, ValueError) as error:
        messagebox.showerror("Update failed", str(error), parent=root)
        return
    root.destroy()


parser = argparse.ArgumentParser()
parser.add_argument("--parent-pid", type=int)
arguments = parser.parse_args()


root = tk.Tk()
root.title("P-Tools Updater")
root.resizable(False, False)
tk.Label(root, text="Download the latest P-Tools version?").pack(
    padx=30, pady=(25, 15)
)
tk.Button(
    root,
    text="Update",
    command=lambda: update(arguments.parent_pid),
).pack(pady=(0, 25))
root.mainloop()