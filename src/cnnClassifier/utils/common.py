import os
from box.exceptions import BoxValueError
from ensure import ensure_annotations
from pathlib import Path
from typing import Any
import yaml
import json
import joblib
import base64
from box import ConfigBox
from cnnClassifier import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns it as a ConfigBox.

    Args:
        path_to_yaml (Path): Path to the YAML file.

    Raises:
        ValueError: If the YAML file is empty or invalid.
        e: Exception raised during YAML file reading.

    Returns:
        ConfigBox: ConfigBox object containing the YAML content.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError as e:
        raise ValueError(f"yaml file: {path_to_yaml} is invalid") from e
    except Exception as e:
        raise e



@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Creates directories if they don't exist.

    Args:
        path_to_directories (list[Path]): List of paths to the directories to be created.
        ignore_log(bool, optional): ignore if multiple directories is to be created. Defaults to False.

    Returns:
        None
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"directory created at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Saves a dictionary to a JSON file.

    Args:
        path (Path): Path to the JSON file.
        data (dict): Dictionary/data to be saved in json file.

    Returns:
        None
    """
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    logger.info(f"json file: {path} saved successfully")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Loads a JSON file and returns it as a ConfigBox.

    Args:
        path (Path): Path to the JSON file.

    Returns:
        ConfigBox: ConfigBox object containing the JSON content.
    """
    with open(path, 'r') as json_file:
        content = json.load(json_file)
    logger.info(f"json file: {path} loaded successfully")
    return ConfigBox(content)


@ensure_annotations
def save_bin(path: Path, data: Any):
    """
    Saves binary data to a file.

    Args:
        path (Path): Path to the binary file.
        data (Any): Binary data to be saved.

    Returns:
        None
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file: {path} saved successfully")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Loads binary data from a file.

    Args:
        path (Path): Path to the binary file.

    Returns:
        Any: Binary data loaded from the file.
    """
    data = joblib.load(filename=path)
    logger.info(f"binary file: {path} loaded successfully")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """
    Returns the size of a file in bytes.

    Args:
        path (Path): Path to the file.

    Returns:
        str: Size of the file in kilo bytes.
    """
    size_in_kb = round(os.path.getsize(path)/float(1024))
    logger.info(f"file: {path} size: {size_in_kb} KB")
    return f"~ {size_in_kb} KB"


def decodeImage(imgstring: str, filename: Path):
    imgdata = base64.b64decode(imgstring)
    with open(filename, 'wb') as f:
        f.write(imgdata)
        f.close()
    logger.info(f"image file: {filename} decoded successfully")


def encodeImageIntoBase64(cropped_image_path):
    """
    Encodes an image file into a base64 string.

    Args:
        cropped_image_path (Path): Path to the cropped image file.

    Returns:
        str: Base64 encoded string of the image.
    """
    with open(cropped_image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    logger.info(f"image file: {cropped_image_path} encoded successfully")
    return encoded_string
