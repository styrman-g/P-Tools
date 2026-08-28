import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tkinter as tk
from tkinter import messagebox
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
    installer_path = Path(tempfile.gettempdir()) / "P-Tools-Setup.exe"
    installer_request = Request(
        installer_url, headers={"User-Agent": "P-Tools-Updater"}
    )
    with urlopen(installer_request, timeout=60) as response:
        installer_path.write_bytes(response.read())
    subprocess.Popen([str(installer_path)], close_fds=True)


def update():
    try:
        download_latest_installer()
    except (KeyError, StopIteration, OSError, ValueError) as error:
        messagebox.showerror("Update failed", str(error), parent=root)
        return
    root.destroy()


root = tk.Tk()
root.title("P-Tools Updater")
root.resizable(False, False)
tk.Label(root, text="Download the latest P-Tools version?").pack(
    padx=30, pady=(25, 15)
)
tk.Button(root, text="Update", command=update).pack(pady=(0, 25))
root.mainloop()