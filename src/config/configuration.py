from src.entity.config_entity import DataIngestionConfig
from src.utils.commonutils import read_yaml, create_directories
from src.constants import *


class ConfiguratonManager:
    def __init__(self,
                 config_filepath = CONFIG_FILE_PATH,
                 params_filepath = PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
    
    def get_data_ingestion_config(self):
        try:
            config = self.config.data_ingestion
            create_directories([config.root_dir])
            data_ingestion_config = DataIngestionConfig(
                root_dir= config.root_dir,
                source_URL= config.source_URL,
                raw_data_file=config.raw_data_file,
                train_data_file=config.train_data_file,
                test_data_file=config.test_data_file
            )
            return data_ingestion_config
        except Exception as e:
            raise e