import os
from typing import TypedDict

from utils import resolve_and_validate_path


class FileInfo(TypedDict):
    name: str
    size: int
    is_dir: bool


def get_path_contents_info(full_path_abs: str) -> list[FileInfo]:
    """Gather raw file information"""
    return [
        {
            "name": item,
            "size": os.path.getsize(os.path.join(full_path_abs, item)),
            "is_dir": os.path.isdir(os.path.join(full_path_abs, item)),
        }
        for item in os.listdir(full_path_abs)
    ]


def format_contents_info(contents_info: list[FileInfo]) -> str:
    """Present file information in expected format"""
    lines = [
        f"- {item['name']}: file_size={item['size']} bytes, is_dir={item['is_dir']}"
        for item in contents_info
    ]
    return "\n".join(lines)


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        path, error = resolve_and_validate_path(working_directory, directory)
        if error:
            return error

        # path is a valid string at this point
        assert path is not None

        if not os.path.isdir(path):
            return f'Error: "{directory}" is not a directory'

        return format_contents_info(get_path_contents_info(path))

    except Exception as ex:
        return f"Error: {ex}"
