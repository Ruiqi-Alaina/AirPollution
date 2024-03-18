from src import logger
from src.utils.train_test_prepare import to_chunks,split_train_test,to_forecasts
from src.entity.config_entity import DataIngestionConfig
from urllib import request
import os
import pandas as pd
import numpy as np

class DataIngestion:
    def __init__(self, config:DataIngestionConfig):
        self.config = config
    
    def download_data(self):
        try:
            if not os.path.exists(self.config.raw_data_file):
                response = request.urlopen(url = self.config.source_URL)
                os.makedirs(self.config.root_dir, exist_ok=True)
                with open(self.config.raw_data_file, 'wb') as f:
                    f.write(response.read())
                logger.info("data has been downloaded")
            else:
                logger.info(f"File exists")
        except Exception as e:
            raise e
            
    def save_train_test_split(self):
        try: 
            if os.path.exists(self.config.raw_data_file):
                df = pd.read_csv(self.config.raw_data_file)
                chunks = to_chunks(df)
                train,test = split_train_test(chunks)
                forecasts = to_forecasts(test)
                test_array = np.array(forecasts)
                train_array=[]
                for values in train.values():
                    list_value = values.values.tolist()
                    train_array.extend(list_value)
                train_array = np.array(train_array)
                np.savetxt(self.config.train_data_file, train_array)
                np.savetxt(self.config.test_data_file, test_array)
                logger.log('data has been split into test and train')
                return (
                    self.config.train_data_file,
                    self.config.test_data_file
                    )
            else:
                logger.info("data has not been downloaded")
        except Exception as e:
            raise e 


            


        