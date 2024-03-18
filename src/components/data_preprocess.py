import numpy as np
from src.utils.train_test_prepare import target_to_supervised, array_to_chunks
from pathlib import Path
class DataPreprocess:
    def __init__(self):
        pass
    
    def prepare_training(self,train_data_config:Path, n_lags, lead_time):
        '''
        Prepare training data for given lead_time and n_lag: put all chunks data together
        '''
        try:
            train_data = np.loadtxt(train_data_config)
            chunks = array_to_chunks(train_data)
            X_train_prepared = list()
            y_train_prepared = list()
            test_prepared = [[] for _ in range(len(chunks))]
            for i in range(len(chunks)):
                print(f'chunk{i} starts preparing')
                chunk_train = chunks[i]
                X,y,test_sample = target_to_supervised(chunks,chunk_train,n_lags,lead_time)
                X_train_prepared.extend(X)
                y_train_prepared.extend(y)
                test_prepared[i] = test_sample
            X_train_prepared = np.array(X_train_prepared)
            y_train_prepared = np.array(y_train_prepared)
            test_prepared = np.array(test_prepared)
            return np.array(X_train_prepared),np.array(y_train_prepared),np.array(test_prepared)
        except Exception as e:
            raise e
