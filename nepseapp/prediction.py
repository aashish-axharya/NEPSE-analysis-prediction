# Importing Libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
from matplotlib import pyplot as plt
df = pd.read_csv('ADBL.csv')
df.head()
closedf = df.reset_index()['Close']
# Dropping Null values from data
closedf = closedf.dropna()
closedf
scaler = MinMaxScaler(feature_range=(0,1))
df1 = scaler.fit_transform(np.array(closedf).reshape(-1,1))
df1
# Splitting dataset into train and test split
split_ratio = 0.7
train_size=int(len(df1)*split_ratio)
test_size=len(df1)-train_size
train_data, test_data = df1[0:train_size,:], df1[train_size:len(df1),:]
# Convert the data into a sequence of past time steps and future time steps
def create_dataset(data, time_steps):
    x, y = [], []
    for i in range(len(data) - time_steps - 1):
        a = data[i:(i + time_steps), 0]
        x.append(a)
        y.append(data[i + time_steps, 0])
    return np.array(x), np.array(y)
# Create Dataset
time_steps = 60
x_train, y_train = create_dataset(train_data, time_steps)
x_test, y_test = create_dataset(test_data, time_steps)
# Reshape the data for the LSTM model
x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))
# Build the LSTM model
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(1,time_steps)))
model.add(LSTM(128, return_sequences=True))
model.add(LSTM(128))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='mean_squared_error', optimizer='adam',metrics=['accuracy'])
model.summary()
# Train the model
history1 = model.fit(x_train, y_train, epochs=100, verbose=1, validation_data=(x_test, y_test))
history1
model.save('ADBL.h5')
# Test the model
# prediction_test = model.predict(x_test)
# prediction_test = scaler.inverse_transform(prediction_test)
# # Calculate Accuracy
# #calculate accuracy
# print('Accuracy: %.2f' % (model.evaluate(x_train, y_train)[1]*100))
# # Calculate the root mean squared error
# y_inverse = scaler.inverse_transform(y_test.reshape(-1,1))
# rmse_test = np.sqrt(np.mean(((prediction_test - y_inverse) ** 2)))
# print('RMSE:', rmse_test)
# # Plotting Model
# # Get the most recent 60 days of stock price data
# recent_data = df1[-60:]

# # Reshape the data for the LSTM model
# x_recent = recent_data.reshape(1, 1, 60)

# # Predict the stock prices for the next day and append to the input data
# predicted_price = model.predict(x_recent)
# df1 = np.append(df1, predicted_price)

# # Shift the input data by one day
# for i in range(6):
#     recent_data = df1[-60:]
#     x_recent = recent_data.reshape(1, 1, 60)
#     predicted_price = model.predict(x_recent)
#     df1 = np.append(df1, predicted_price)
    
# # Inverse transform the predicted prices
# predicted_prices = scaler.inverse_transform(df1[-7:].reshape(-1, 1))

# # Print the predicted prices for the next 7 days
# df_predicted = pd.DataFrame(predicted_prices, columns=['Predicted Prices'])
# df_predicted.to_csv('predicted_prices.csv', index=False)
