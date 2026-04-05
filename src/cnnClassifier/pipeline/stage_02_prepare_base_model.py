from cnnClassifier.config import ConfigurationManager
from cnnClassifier.components.prepare_base_model import PrepareBaseModel
from cnnClassifier import logger

STAGE_NAME = "Prepare Base Model"

class PrepareBaseModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        prepare_base_model_config = config.get_prepare_base_model_config()
        prepare_base_model = PrepareBaseModel(prepare_base_model_config)
        prepare_base_model.get_base_model()
        prepare_base_model.update_base_model()

        logger.info("PrepareBaseModelTrainingPipeline completed")


if __name__ == "__main__":
    try:
        logger.info(f"\n{'='*80}")
        logger.info(f"{' ' * 30}{STAGE_NAME} started")
        logger.info(f"{'='*80}\n")
        obj = PrepareBaseModelTrainingPipeline()
        obj.main()
        logger.info(f"{' ' * 30}{STAGE_NAME} completed")
        logger.info(f"{'='*80}\n")
    except Exception as e:
        logger.exception(e)
        raise e