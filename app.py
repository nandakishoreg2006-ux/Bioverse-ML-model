import time
import numpy as np
import requests
from tensorflow.keras.models import load_model
import joblib

FIREBASE_URL = "https://biochamber-52607-default-rtdb.firebaseio.com"

# Load model and scalers
model = load_model("lstm_model.h5")
feature_scaler = joblib.load("feature_scaler.save")
target_scaler = joblib.load("target_scaler.save")

def predict_growth(sensor_window):
    scaled = feature_scaler.transform(sensor_window)
    scaled = scaled.reshape(1, 20, 4)

    pred_scaled = model.predict(scaled)
    pred = target_scaler.inverse_transform(pred_scaled)[0][0]

    return pred

def run_background_ai():
    print("AI Backend Running...")

    while True:
        response = requests.get(f"{FIREBASE_URL}/sensors.json")
        data = response.json()

        if data and len(data) >= 20:
            last_20 = list(data.values())[-20:]

            sensor_window = np.array([
                [d['pH'], d['Temp'], d['DO'], d['OD']]
                for d in last_20
            ])

            prediction = predict_growth(sensor_window)

            control = "Stable"
            if prediction < -0.5:
                control = "Increase Aeration"
            elif prediction > 0:
                control = "Reduce Nutrient Feed"

            requests.put(
                f"{FIREBASE_URL}/prediction.json",
                json={
                    "growth_prediction": float(prediction),
                    "control_action": control,
                    "timestamp": time.time()
                }
            )

            print("Prediction:", prediction, "| Control:", control)

        time.sleep(5)

if __name__ == "__main__":
    run_background_ai()
