import ffmpeg
from pathlib import Path
import sys
from threading import Event
from typing import Callable


class ConversionCancelled(Exception):
    """Raised when a media conversion is cancelled by the user."""


def konvertera_mediafil(
    indata_sökväg: str,
    utdata_format: str,
    progress_callback: Callable[[float], None] | None = None,
    cancel_event: Event | None = None,
) -> Path:
    """
    Konverterar en fil till angivet format via FFmpeg.
    Returnerar sökvägen till den nya filen.
    """
    indata = Path(indata_sökväg)
    utdata = indata.with_suffix(f".{utdata_format}")
    cancel_event = cancel_event or Event()
    ffmpeg_path = Path(getattr(sys, "_MEIPASS", Path(__file__).parent)) / "ffmpeg.exe"
    ffprobe_path = Path(getattr(sys, "_MEIPASS", Path(__file__).parent)) / "ffprobe.exe"

    probe_data = ffmpeg.probe(str(indata), cmd=str(ffprobe_path))
    duration = float(probe_data["format"].get("duration", 0))

    process = (
        ffmpeg
        .input(str(indata))
        .output(str(utdata))
        .overwrite_output()
        .global_args("-progress", "pipe:1", "-nostats")
        .run_async(cmd=str(ffmpeg_path), pipe_stdout=True, pipe_stderr=True)
    )

    try:
        for line in process.stdout:
            if cancel_event.is_set():
                process.terminate()
                process.wait()
                if utdata.exists():
                    utdata.unlink()
                raise ConversionCancelled()

            key, _, value = line.decode().strip().partition("=")
            if key == "out_time_ms" and duration and progress_callback:
                progress_callback(min(float(value) / (duration * 1_000_000), 1.0))

        process.wait()
        if process.returncode:
            error_output = process.stderr.read().decode(errors="replace")
            raise RuntimeError(error_output or "FFmpeg conversion failed.")
    except Exception:
        if process.poll() is None:
            process.terminate()
            process.wait()
        raise

    if progress_callback:
        progress_callback(1.0)
    return utdata
