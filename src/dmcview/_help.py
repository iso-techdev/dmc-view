"""Module containing bug report helper(s)."""

import json
import platform
import sys
from typing import Any

import matplotlib
import PySide6

from . import __version__ as dmcview_version


def _implementation()-> dict[str, str]:
    """Return a dict with the Python implementation and version.

    Provide both the name and the version of the Python implementation
    currently running. For example, on CPython 3.10.3 it will return
    {'name': 'CPython', 'version': '3.10.3'}.

    This function works best on CPython and PyPy: in particular, it probably
    doesn't work for Jython or IronPython. Future investigation should be done
    to work out the correct shape of the code for those platforms.
    """
    implementation = platform.python_implementation()

    if implementation == "CPython":
        implementation_version = platform.python_version()
    elif implementation == "PyPy":
        pypy = sys.pypy_version_info  # type: ignore[attr-defined]
        implementation_version = f"{pypy.major}.{pypy.minor}.{pypy.micro}"  # pyright: ignore[reportUnknownMemberType]
        if sys.pypy_version_info.releaselevel != "final":  # type: ignore[attr-defined]
            implementation_version = "".join(
                [implementation_version, sys.pypy_version_info.releaselevel]  # type: ignore[attr-defined]
            )
    elif implementation == "Jython":
        implementation_version = platform.python_version()  # Complete Guess
    elif implementation == "IronPython":
        implementation_version = platform.python_version()  # Complete Guess
    else:
        implementation_version = "Unknown"

    return {"name": implementation, "version": implementation_version}


def info() -> dict[str, Any]:
    """Generate information for a bug report."""
    try:
        platform_info = {
            "system": platform.system(),
            "release": platform.release(),
        }
    except OSError:
        platform_info = {
            "system": "Unknown",
            "release": "Unknown",
        }

    implementation_info = _implementation()
    dmcview_info = {"version": dmcview_version}
    PySide6_info = {"version": PySide6.__version__}
    matplotlib_info = {"version": matplotlib.__version__}



    return {
        "platform": platform_info,
        "implementation": implementation_info,
        "PySide6_info": PySide6_info ,
        "matplotlib_info": matplotlib_info,
        "dmcview": {
            "version": dmcview_info,
        },
    }


def bug_reporting()->None:
    """Pretty-print the bug information as JSON."""
    print(json.dumps(info(), sort_keys=True, indent=2))


if __name__ == "__main__":
    bug_reporting()
