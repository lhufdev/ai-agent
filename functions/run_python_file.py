import os
import subprocess

from config import PYTHON_RUN_TIMEOUT
from utils import resolve_and_validate_path


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    if args is None:
        args = []
    try:
        path, error = resolve_and_validate_path(working_directory, file_path)
        if error:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        assert path is not None

        if not os.path.isfile(path):
            return f'Error: File "{file_path}" not found.'

        if not path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        completed_process = subprocess.run(
            ["python", path, *args],
            timeout=PYTHON_RUN_TIMEOUT,
            capture_output=True,
            text=True,
        )
        std_out = completed_process.stdout
        std_err = completed_process.stderr
        exit_code = completed_process.returncode

        if not std_out and not std_err:
            return "No output produced"

        std_out_clean = std_out.rstrip("\n")
        std_err_clean = std_err.rstrip("\n")

        parts: list[str] = []

        parts.append(f"STDOUT:\n{std_out_clean}" if std_out_clean else "STDOUT:\n")
        parts.append(f"STDERR:\n{std_err_clean}" if std_err_clean else "STDERR:\n")

        if exit_code != 0:
            parts.append(f"Process exited with code {exit_code}")

        return "\n".join(parts)

    except Exception as ex:
        return f"Error: executing python file: {ex}"
