"""Check the Python version."""
__author__ = "Anthony Pagan <Get-Tony@outlook.com>"
__version__ = "1.0.0"

import argparse
import sys


def main() -> None:
    """Check the Python version and exit 1 if it is too old."""
    parser = argparse.ArgumentParser(description="Check the Python version.")
    parser.add_argument(
        "-v",
        "--version",
        default="3.9.2",
        help="Minimum Python version required. Default is 3.9.2.",
    )
    args = parser.parse_args()
    min_python_version = tuple(map(int, args.version.split(".")))

    current_python_version = sys.version_info[:3]

    if current_python_version < min_python_version:
        print(
            f"Python version is too old. Please upgrade to "
            f"{'.'.join(map(str, min_python_version))} or newer."
        )
        print("Found: Python " f"{'.'.join(map(str, current_python_version))}")
        sys.exit(1)
    else:
        print("Found: Python " f"{'.'.join(map(str, current_python_version))}")


if __name__ == "__main__":
    main()
