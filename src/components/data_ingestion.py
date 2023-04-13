import os
import sys
import json
from src.exception import CustomException
from src.logger import logging
from src.utils import get_path

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    art_dir_path: str = '/home/studio-lab-user/Krishi/artifacts'
    data_info_path: str = '/home/studio-lab-user/Krishi/artifacts/dataset_info.json'
    
    
class DataIngestion:
    
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self, data_dir_path:str):
        logging.info('Data Ingestion Component initiated.')
        try:
            plant_dirs = list(os.listdir(data_dir_path))
            plants_data = {}
            for plant in plant_dirs:
                data_split_path = {
                    'train': get_path(plant, 'Train'),
                    'test': get_path(plant, 'Test'),
                    'val': get_path(plant, 'Val')
                }

                classes_lst = []
                for cat in os.listdir(get_path(plant,'Train')):
                    classes_lst.append(cat)

                plants_data[plant] = {
                    'data_split':data_split_path,
                    'classes':classes_lst
                }
            
            os.makedirs(self.ingestion_config.art_dir_path, exist_ok = True)
            
            with open(self.ingestion_config.data_info_path, "w") as outfile:
                json.dump(plants_data, outfile)
            
            logging.info('Data Ingestion completed. Saved Dataset info in \'artifacts/dataset_info.json\'')
            
            return self.ingestion_config.data_info_path
            
        except Exception as e:
            raise CustomException(e, sys)
            