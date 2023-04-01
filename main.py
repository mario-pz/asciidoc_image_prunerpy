from os import makedirs, listdir
from os.path import isfile, join, isdir
from typing import List, Set
from re import findall, MULTILINE
from shutil import move
from os import path


def filter_unused_images(assets_dir: str, tags: List[str]) -> List[str]:
    """
    Given a path to an assets directory and a list of image tags extracted from
    AsciiDoc files, returns a list of image filenames in the assets directory
    that are not used in any of the AsciiDoc files.

    Args:
        assets_dir (str):
            The path to the assets directory to search for images.
        tags (List[str]):
            A list of image tags extracted from AsciiDoc files.

    Returns:
        List[str]: A list of image filenames in the assets directory that are
        not used in any of the AsciiDoc files.
    """
    used_images: Set[str] = set(tag.split("/")[-1] for tag in tags)
    unused_images: list[str] = []
    for filename in listdir(assets_dir):
        if isfile(join(assets_dir, filename)) and filename not in used_images:
            unused_images.append(filename)
    return unused_images


def extract_ascii_tags(data: bytes) -> List[str]:
    """
    Given a bytes object containing the content of an AsciiDoc file, extracts
    all image tags in the file and returns them in a list.

    Args:
        data (bytes): The content of an AsciiDoc file.

    Returns:
        List[str]: A list of all image tags in the AsciiDoc file.
    """
    pattern = r"^image::(.*)\[\]$"
    ascii_tags = findall(pattern, data.decode("utf-8"), flags=MULTILINE)
    return ascii_tags


def search_ascii_tags(files: list[str]) -> List[str]:
    """
    Given a list of AsciiDoc files, extracts all image tags in each file and
    returns them in a list.

    Args:
        files (list[str]): A list of file paths to AsciiDoc files.

    Returns:
        List[str]: A list of all image tags in all AsciiDoc files.
    """
    tags: List[str] = []
    for file in files:
        with open(file, "rb") as f:
            data = f.read()
            tags.extend(extract_ascii_tags(data))
    return tags


def find_asciidoc_files(subdir_path: str) -> List[str] | None:
    """
    Given a path to a directory, returns a list of file paths to all AsciiDoc
    files in the directory.

    Args:
        subdir_path (str): The path of the directory to search.

    Returns:
        List[str]: A list of file paths to all AsciiDoc files in the directory.
    """
    ascii_docs: List[str] = []
    for filename in listdir(subdir_path):
        file_path = join(subdir_path, filename)
        if isfile(file_path) and (
            filename.endswith(".adoc") or filename.endswith(".asciidoc")
        ):
            ascii_docs.append(file_path)

    return ascii_docs


def move_to_unused_dir(
    assets_dir_path: str, filtered_images: List[str], unused_images_dir: str
) -> None:
    """
    Moves the unused image files to a directory called "unused-images"
    in the parent folder with the python script.

    Args:
        assets_dir_path (str):
            The path to the directory that contains the image files.
        filtered_images (List[str]):
            A list of filenames that are not used in any of the AsciiDoc files.
        unused_images_dir (str):
            The path to the "unused-images" directory
            where the unused image files will be moved to.
    """
    for filename in filtered_images:
        source_path = join(assets_dir_path, filename)
        dest_path = join(unused_images_dir, filename)
        if path.exists(source_path):
            move(source_path, dest_path)
            print(f"{source_path} is unused")


def main() -> None:
    parent_directory: str = "."
    unused_images_dir = join(parent_directory, "unused-images")
    makedirs(unused_images_dir, exist_ok=True)

    for subdir in listdir(parent_directory):
        subdir_path = join(parent_directory, subdir)
        if isdir(subdir_path) and subdir != "unused-images":
            assets_dir_path = join(subdir_path, "assets")
            if isdir(assets_dir_path):
                ascii_docs = find_asciidoc_files(subdir_path)
                if ascii_docs is not None:
                    tags = search_ascii_tags(ascii_docs)
                    filtered_images = filter_unused_images(
                        assets_dir_path, tags
                    )
                    move_to_unused_dir(
                        assets_dir_path, filtered_images, unused_images_dir
                    )


if __name__ == "__main__":
    main()
