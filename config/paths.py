"""
Path resolution utilities for both development and PyInstaller-packaged modes.

In development: all paths resolve relative to the project root.
When packaged: bundled read-only resources are in sys._MEIPASS (_internal),
               writable files (config) are next to the executable.
"""

import os
import sys


def is_packaged():
    """Return True if running as a PyInstaller-packaged executable."""
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


def get_bundle_dir():
    """
    Get the directory containing bundled read-only resources.

    Returns sys._MEIPASS when packaged (the _internal temp directory),
    or the project root directory when running in development.
    """
    if is_packaged():
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_app_dir():
    """
    Get the application directory for writable files.

    Returns the directory containing the executable when packaged,
    or the project root directory when running in development.
    """
    if is_packaged():
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_config_path():
    """
    Get the absolute path to the writable league_config.json.

    When packaged: <exe_dir>/config/league_config.json
    When in dev: <project_root>/config/league_config.json
    """
    return os.path.join(get_app_dir(), "config", "league_config.json")


def get_default_config_path():
    """
    Get the path to the bundled default config (read-only in packaged mode).

    Used as the source when copying the initial config to the writable
    location on first run of a packaged executable.
    """
    return os.path.join(get_bundle_dir(), "config", "league_config.json")


def resolve_resource_path(relative_path):
    """
    Resolve a relative resource path (e.g., './data/wktownffbllogo.png')
    to an absolute path that works in both dev and packaged modes.

    Resolution order:
    1. If the path is already absolute, return it as-is.
    2. Check relative to get_app_dir() (user-placed files next to exe).
    3. Check relative to get_bundle_dir() (bundled default resources).
    4. Fall back to the bundle dir path even if not found.
    """
    if not relative_path:
        return relative_path

    # If already absolute, return as-is
    if os.path.isabs(relative_path):
        return relative_path

    # Strip leading './' or '.\\'
    cleaned = relative_path.replace('\\', '/')
    if cleaned.startswith('./'):
        cleaned = cleaned[2:]

    # Check app dir first (user files / writable area)
    app_path = os.path.join(get_app_dir(), cleaned)
    if os.path.exists(app_path):
        return app_path

    # Check bundle dir (read-only bundled resources)
    bundle_path = os.path.join(get_bundle_dir(), cleaned)
    return bundle_path
