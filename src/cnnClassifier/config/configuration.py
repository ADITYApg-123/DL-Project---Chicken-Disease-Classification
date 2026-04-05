from cnnClassifier.constants import *
from cnnClassifier.utils.common import read_yaml, create_directories
from cnnClassifier.entity.config_entity import DataIngestionConfig

class ConfigurationManager:
    def __init__(
            self,
            config_filepath = CONFIG_FILE_PATH, # this is the path to the config.yaml file which contains all the configurations for our project.
            params_filepath = PARAMS_FILE_PATH # this is the path to the params.yaml file which contains all the parameters for our project.
    ):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root]) # this creates the required directories for our project.

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion # this is the data_ingestion section of the config.yaml file which contains all the configurations for the data ingestion process.

        create_directories([config.root_dir])

        # this creates an object of the DataIngestionConfig class and passes the required parameters to it.
        data_ingestion_config = DataIngestionConfig (
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )

        return data_ingestion_config