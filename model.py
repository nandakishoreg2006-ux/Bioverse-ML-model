# model.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib

# Simulated training data
np.random.seed(42)
time_steps = 2000

pH = np.sin(np.linspace(0, 20, time_steps)) * 0.3 + 7
temp = np.sin(np.linspace(0, 10, time_steps)) * 1.5 + 37
do = np.sin(np.linspace(0, 15, time_steps)) * 5 + 85
od = np.linspace(0.2, 1.2, time_steps) + np.random.normal(0, 0.05, time_steps)

growth = (
    -abs(pH - 7)*0.5
    -abs(temp - 37)*0.3
    -abs(do - 85)*0.2
    -abs(od - 0.8)*0.4
)

data = pd.DataFrame({
    'pH': pH,
    'Temp': temp,
    'DO': do,
    'OD': od,
    'Growth': growth
})

features = data[['pH','Temp','DO','OD']]
target = data[['Growth']]

feature_scaler = MinMaxScaler()
target_scaler = MinMaxScaler()

scaled_features = feature_scaler.fit_transform(features)
scaled_target = target_scaler.fit_transform(target)

scaled_data = np.hstack((scaled_features, scaled_target))

def create_sequences(data, seq_length=20):
    X, y = [], []
    for i in range(len(data)-seq_length):
        X.append(data[i:i+seq_length,:-1])
        y.append(data[i+seq_length,-1])
    return np.array(X), np.array(y)

X, y = create_sequences(scaled_data)

model = Sequential()
model.add(LSTM(64, return_sequences=True, input_shape=(20,4)))
model.add(LSTM(32))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')
model.fit(X, y, epochs=10, batch_size=32)

model.save("lstm_model.h5")
joblib.dump(feature_scaler, "feature_scaler.save")
joblib.dump(target_scaler, "target_scaler.save")

print("Model Saved.")