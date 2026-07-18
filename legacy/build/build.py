#!/usr/bin/env python
"""
Build script for Fantasy Football Lottery Application
This script creates a standalone executable using PyInstaller
"""

import os
import sys
import shutil
import subprocess


def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed")
        print(e.stderr)
        return False


def main():
    """Main build function."""
    print("\n" + "="*60)
    print("Fantasy Football Lottery - Build Script")
    print("="*60)

    # Change to project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    print(f"Working directory: {os.getcwd()}")

    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        sys.exit(1)

    print(f"Python version: {sys.version}")

    # Step 1: Install dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r build{os.sep}requirements.txt",
        "[1/4] Installing dependencies..."
    ):
        sys.exit(1)

    # Step 2: Clean previous build
    print("\n[2/4] Cleaning previous build...")
    for folder in ['build_output', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  Removed {folder}/")

    # Step 3: Build with PyInstaller
    if not run_command(
        f"{sys.executable} -m PyInstaller build{os.sep}fantasy_football_lottery.spec --clean",
        "[3/4] Building executable with PyInstaller..."
    ):
        sys.exit(1)

    # Step 4: Success message
    print("\n" + "="*60)
    print("[4/4] Build complete!")
    print("="*60)
    print(f"\nExecutable location: dist{os.sep}FantasyFootballLottery{os.sep}FantasyFootballLottery.exe")
    print("\nYou can now:")
    print("1. Run the executable from dist/FantasyFootballLottery/")
    print("2. Copy the entire FantasyFootballLottery folder to distribute")
    print("="*60)


if __name__ == "__main__":
    main()
