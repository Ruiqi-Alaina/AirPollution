import tensorflow as tf

class ModelPrepared:
    def __init__(self):
        pass
    
    def get_vanilla_LSTM_model(self,n_lags, n_features):
        try: 
            model = tf.keras.models.Sequential()
            model.add(tf.keras.layers.LSTM(50, activation='relu', return_sequences = True, input_shape=(n_lags,n_features)))
            model.add(tf.keras.layers.Flatten())
            model.add(tf.keras.layers.Dense(n_features))
            model.compile(optimizer='adam', loss='mse')
            return model
        except Exception as e:
            raise e
    
    def get_stacked_LSTM_model(self, n_lags, n_features):
        try:
            model = tf.keras.models.Sequential()
            model.add(tf.keras.layers.LSTM(50, activation='relu', return_sequences = True, input_shape=(n_lags,n_features)))
            model.add(tf.keras.layers.LSTM(50, activation='relu', return_sequences = True, input_shape=(n_lags,n_features)))
            model.add(tf.keras.layers.Flatten())
            model.add(tf.keras.layers.Dense(n_features))
            model.compile(optimizer='adam', loss='mae')
            return model
        except Exception as e:
            raise e
        
    def get_CNN_model(n_lags, n_features):
        try:
            model = tf.keras.models.Sequential()
            model.add(tf.keras.layers.Conv1D(filters = 64,kernel_size = 2, activation='relu',input_shape=(n_lags,n_features)))
            model.add(tf.keras.layers.MaxPooling1D(pool_size=2))
            model.add(tf.keras.layers.Flatten())
            model.add(tf.keras.layers.Dense(50,activation='relu'))
            model.add(tf.keras.layers.Dense(n_features))
            model.compile(optimizer='adam', loss='mae')
            return model
        except Exception as e:
            raise e

    def get_CNN_LSTM_model(n_lags, n_features):
        try:
            model= tf.keras.models.Sequential()
            model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Conv1D(filters=64, kernel_size=1, activation='relu'), input_shape=(None,n_lags, n_features)))
            model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.MaxPooling1D(pool_size=2)))
            model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Flatten()))
            model.add(tf.keras.layers.LSTM(50,activation='relu'))
            model.add(tf.keras.layers.Flatten())
            model.add(tf.keras.layers.Dense(n_features))
            model.compile(optimizer = 'adam', loss='mae')
            return model
        except Exception as e:
            raise e

        