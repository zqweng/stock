# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
# Feature Scaling
from sklearn.preprocessing import MinMaxScaler

def create_new_record(df, predicted_price):
     df_new = df[['date','close','p_change']]
     
     new_pred = predicted_price.reshape(predicted_price.shape[0])
     df_new['predicted_close']= pd.Series(np.flip(new_pred,0))
     df_new['preclose'] = df_new['close'].shift(-1)
     df_new['pred_p_change'] = 100 * (df_new['predicted_close']-df_new['preclose'])/df_new['preclose']
     return df_new

"""
This function does the following things:
    1. change the order of the record. from latest to earliest, to earilest to latest
    2. scale it to the range of (0,1)
    3. 
"""

def get_training_data(training_set, sc, timestep, test_num):
    
    # change order, add new index, cut the old index
    training_set.sort_index(ascending=False, inplace=True)
    # Reset index will create a new index array, so the stock price column become the second column
    # and the original index array become the first column.
    training_set.reset_index(inplace=True)
    training_set = training_set.iloc[:,1:2]
    
    
    training_set_scaled = sc.fit_transform(training_set)
    
    # Creating a data structure with 60 timesteps and 1 output
    # You can change 60 to other number
    X_train = []
    y_train = []
    
    #serial to parallel, every 60 record form a new row 
    for i in range(timestep, len(training_set_scaled)):
        X_train.append(training_set_scaled[i-timestep:i, 0])
        y_train.append(training_set_scaled[i,0])

    #change it to numpy array, add one more dimension
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_test = X_train[-test_num:]
    X_train = X_train[:-test_num]
    real_stock_price = y_train[-test_num:]
    real_stock_price = real_stock_price.reshape(-1,1)
    y_train = y_train[:-test_num]
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))   
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    return X_train, y_train, X_test, real_stock_price

    
    
#
sc = MinMaxScaler(feature_range = (0,1))    

# Importing the trainging set
dataset_train = pd.read_csv("c:\\Users\\johnny\\stockdata-bao\\day\\002216.csv")
training_set = dataset_train.iloc[:,1:2]

X_train, y_train, X_test, real_stock_price = get_training_data(training_set, sc, 60, 30)

real_stock_price = sc.inverse_transform(real_stock_price)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

# Part 2 - Building the RNN

# Importing the keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

# Initializing the RNN
regressor = Sequential()

# Adding the first LSTM layer and some Dropout regularisation
regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

# Adding the second LSTM layer and some Dropout regularisation
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

# Adding the third LSTM layer and some Dropout regularisation
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

# Adding the fourth LSTM layer and some Dropout regularisation
regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))

# Adding the output layer
regressor.add(Dense(units=1))

# Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Fitting the RNN to the Training set
regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)

# Part 3 - Making the predictions and visualising the results
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

dataset_new = create_new_record(dataset_train, predicted_stock_price)
dataset_new.to_csv("rnn-002216.csv")

# Visualising the results
plt.plot(real_stock_price, color = 'red', label = 'Real Google Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()
plt.savefig('002216.png')





