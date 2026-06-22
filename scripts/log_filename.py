#!/usr/bin/env python3
"""Reads FILENAME from the acquisition config file and logs it every 10 minutes,
including the current size of the data file and whether it grew since last check."""

import configparser
import time
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

SCRIPT_DIR = Path(__file__).parent.resolve()
CONFIG_PATH = SCRIPT_DIR.parent / "config.ini"
LOG_FILE = SCRIPT_DIR / "filename_log.txt"
INTERVAL_SECONDS = 10 * 60                          #minutes in seconds


def read_config(config_path: Path) -> Tuple[Optional[str], Optional[Path]]:
    parser = configparser.ConfigParser(
        inline_comment_prefixes=("#", ";"),
        comment_prefixes=("#", ";"),
    )
    parser.read(config_path)
    try:
        filename = parser.get("ACQUISITION", "FILENAME").strip()
        data_path = Path(parser.get("ACQUISITION", "DATA_PATH").strip())
        return filename, data_path
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"[{datetime.now()}] Config read error: {e}", file=sys.stderr)
        return None, None


def get_file_size(data_path: Path, filename: str) -> Optional[int]:
    root_file = data_path / (filename + ".root")
    if root_file.exists():
        return root_file.stat().st_size
    return None


def format_size(size_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def log_status(config_path: Path, prev_size: Optional[int]) -> Optional[int]:
    filename, data_path = read_config(config_path)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not filename:
        entry = f"{timestamp}  <FILENAME not found>\n"
        with open(LOG_FILE, "a") as f:
            f.write(entry)
        print(entry, end="")
        return prev_size

    size = get_file_size(data_path, filename) if data_path else None

    if size is None:
        size_str = "file not found"
        status = "UNKNOWN"
    else:
        size_str = format_size(size)
        if prev_size is None:
            status = "first check"
        elif size > prev_size:
            status = f"GROWING (+{format_size(size - prev_size)})"
        else:
            status = "WARNING: size unchanged"

    entry = f"{timestamp}  {filename}  |  size: {size_str}  |  {status}\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)
    print(entry, end="")

    return size


def main():
    config_path = CONFIG_PATH
    if not config_path.exists():
        print(f"Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Monitoring config: {config_path}")
    print(f"Logging to:        {LOG_FILE}")
    print(f"Interval:          {INTERVAL_SECONDS // 60} minutes\n")

    prev_size = None
    while True:
        prev_size = log_status(config_path, prev_size)
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
