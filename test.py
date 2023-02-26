import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import os

# Load the stock data
# path = 'scrape/data/'
# files = os.listdir(path)
# df = pd.DataFrame()
# for file in files:
#     df = df.append(pd.read_csv(os.path.join(path, file)).dropna())
#     df.reset_index(drop=True)

df = pd.read_csv('scrape/test/ADBL.csv').dropna()

# Extract the closing price and convert it to a numpy array
close_prices = df['Close'].values
try:
    close_prices = np.vectorize(lambda x: float(x.replace(',', '')))(close_prices)
except:
    pass
close_prices = close_prices.reshape(-1, 1)

# Scale the data to the range (0, 1)
scaler = MinMaxScaler(feature_range=(0, 1))
close_prices = scaler.fit_transform(close_prices)

# Split the data into training and test sets
split_ratio = 0.7
train_size = int(len(close_prices) * split_ratio)
test_size = len(close_prices) - train_size
train_data, test_data = close_prices[0:train_size,:], close_prices[train_size:len(close_prices),:]

# Convert the data into a sequence of past time steps and future time steps
def create_dataset(data, time_steps=1):
    X, y = [], []
    for i in range(len(data) - time_steps - 1):
        a = data[i:(i + time_steps), 0]
        X.append(a)
        y.append(data[i + time_steps, 0])
    return np.array(X), np.array(y)

time_steps = 4
X_train, y_train = create_dataset(train_data, time_steps)
X_test, y_test = create_dataset(test_data, time_steps)

#Reshape the data for the LSTM model
X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

# Build the LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(1, time_steps)))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam',metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=2)

# Test the model
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)

accuracy = model.evaluate(X_test, y_test)
print(accuracy)
# Calculate the root mean squared error
rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))
print(model.summary())
print('RMSE:', rmse)