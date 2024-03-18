from src import logger
import yaml 
from box import ConfigBox
from box.exceptions import BoxValueError
from pathlib import Path
import os

def read_yaml(yaml_file_path:Path):
    try: 
        with open(yaml_file_path, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info("yaml file has been loaded")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e

def create_directories(list_of_dir_path:list):
    try:
        for path in list_of_dir_path:
            os.makedirs(path, exist_ok=True)
    except Exception as e:
        raise e

