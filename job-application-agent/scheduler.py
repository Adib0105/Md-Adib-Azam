from __future__ import annotations

import argparse
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()


def windows_task(hour: int, minute: int):
    python = Path(sys.executable).resolve()
    cmd = f'"{python}" "{ROOT / "daily_runner.py"}"'
    time = f"{hour:02d}:{minute:02d}"
    args = ["schtasks", "/Create", "/F", "/SC", "DAILY", "/TN", "WFHJobAgent", "/TR", cmd, "/ST", time]
    subprocess.run(args, check=True)
    print(f"Installed Windows task WFHJobAgent for {time} daily.")


def print_cron(hour: int, minute: int):
    print("Add this cron entry:")
    print(f'{minute} {hour} * * * cd "{ROOT}" && "{sys.executable}" daily_runner.py >> scheduler.log 2>&1')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hour", type=int, default=8)
    ap.add_argument("--minute", type=int, default=0)
    args = ap.parse_args()
    if platform.system() == "Windows": windows_task(args.hour, args.minute)
    else: print_cron(args.hour, args.minute)

if __name__ == "__main__": main()
