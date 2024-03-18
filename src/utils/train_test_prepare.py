import numpy as np
import pandas as pd


def to_chunks(df):
  '''
  divide data into chunks
  '''
  try:
    chunk_id = np.unique(df['chunkID'])
    chunks = dict()
    for id in chunk_id:
        chunks[id] = df[df['chunkID']==id]
    return chunks
  except Exception as e:
    return e



def split_train_test(chunks):
  '''
  # split each chunk into train data and test data (first five days for train and the rest three days test)
  '''
  try: 
    train = dict()
    test = dict()
    # first five days of hourly observations for train
    cut_point = 5*24
    for id, data in chunks.items():
        train_rows = data[data['position_within_chunk'] <= cut_point]
        test_rows = data[data['position_within_chunk'] > cut_point]
        if len(train_rows)==0 or len(test_rows)==0:
            print(f"drop chunk {id}")
            continue
        index = [1,2,5] + [x for x in range(56, 95)]
        train[id] = train_rows.iloc[:,index]
        test[id] = test_rows.iloc[:,index]
    return train, test
  except Exception as e:
    return e


def get_lead_times():
  '''
  return a list of relative forecast lead times
  '''
  try: 
    return [1,2,3,4,5,10,17,24,48,72]
  except Exception as e:
    raise e


def to_forecasts(test):
  '''
  convert the rows in a test chunk to forecast
  '''
  try:
    forecasts = list()
    lead_times = get_lead_times()
    cut_point = 24*5
    for tau in lead_times:
        offset = cut_point+tau
        for id, data in test.items():
            row_for_tau = data[data['position_within_chunk']==offset]
            if len(row_for_tau)==0:
        # create a mock row [chunkID, position, hour]+[nan...]
                row = [id, offset, np.nan] + [np.nan for _ in range(39)]
                forecasts.append(row)
            else:
                forecasts.append(row_for_tau.values.tolist()[0])
    return forecasts
  except Exception as e:
     raise e
  

def array_to_chunks(data):
  try:
    chunks = list()
    chunk_id = np.unique(data[:,0])
    for id in chunk_id:
      chunks.append(data[data[:,0]== id,:])
    return chunks
  except Exception as e:
     return e


def value_to_series(chunk_train,col_ix, n_length = 24*5):
  '''
  chunk_train is data for single chunk, col_ix is the variable index
  '''
  try: 
    series = [np.nan for _ in range(n_length)]
    for i in range(len(chunk_train)):
      position = int(chunk_train[i,1]-1)
      series[position] =  chunk_train[i,col_ix]
    return series
  except Exception as e:
     raise e

def interpolate_hours(hours):
  try:
    ix = -1
    for i in range(len(hours)):
      if not np.isnan(hours[i]):
        ix = i
        break
    # forward
    hour =  hours[ix]
    for i in range(ix+1,len(hours),1):
      hour+=1
      if np.isnan(hours[i]):
        hours[i] = hour % 24
    # backward
    hour = hours[ix]
    for i in range(ix-1,-1,-1):
      hour-=1
      if np.isnan(hours[i]):
        hours[i] = hour % 24
  except Exception as e:
     raise e
  
def impute_missing_values(train_chunks,series, hours,col_ix):
    '''
     impute missing values cross chunks
    '''
    try:
      if np.count_nonzero(np.isnan(series))> 0:
        imputed_series = []
        for i in range(len(series)):
          if np.isnan(series[i]):
            all_rows = []
            for chunk in train_chunks:
              [all_rows.append(row) for row in chunk[chunk[:,2]== hours[i],col_ix]]
            all_rows = np.array(all_rows)
            value = np.nanmedian(all_rows)
            if np.isnan(value):
              value = 0.0
            imputed_series.append(value)
          else:
            imputed_series.append(series[i])
        return imputed_series
      else:
        return series
    except Exception as e:
      return e
    
# prepare data to supervised learning given n_lags and lead_time
def stack_series_to_supervised(series,n_lags,lead_time):
  try:
      '''
      prepare data to supervised learning given n_lags and lead_time
      '''
      X=list()
      y=list()
      for i in range(len(series)):
          end_ix = i+n_lags+lead_time-1
          if end_ix >= len(series):
              break
          else:
              seq_x = series[i:i+n_lags, :]
              seq_y = series[end_ix, :]
              X.append(seq_x)
              y.append(seq_y)
      return np.array(X), np.array(y)
  except Exception as e:
     raise e


def target_to_supervised(chunks,chunk_train,n_lags,lead_time,n_var=39):
  '''
  prepare target column to supervised learning for given lead_time and chunk
  
  '''
  try:
      data = list()
      for i in range(n_var):
        col_ix = 3+i
        # get the target series and hours
        series = value_to_series(chunk_train, col_ix)
        hours = value_to_series(chunk_train, 2)
        # interpolate hours
        interpolate_hours(hours)
        # impute missing values
        imputed_series = impute_missing_values(chunks,series, hours, col_ix)
        imputed_series = np.array(imputed_series).reshape((len(imputed_series), 1))
        data.append(imputed_series)
      data = np.hstack(data)
      # prepared test sample
      test_sample = data[-n_lags:,:]
      # for each lead_time, series_to_superivsed
      X, y = stack_series_to_supervised(data,n_lags,lead_time)
      return X,y,test_sample
  except Exception as e:
     raise e
