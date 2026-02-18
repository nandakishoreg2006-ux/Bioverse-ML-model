import time
import random
import requests

FIREBASE_URL = "https://biochamber-52607-default-rtdb.firebaseio.com"

def get_sensors():
    response = requests.get(f"{FIREBASE_URL}/sensors.json")
    return response.json()

def update_prediction(data):
    requests.put(f"{FIREBASE_URL}/prediction.json", json=data)
while True:
    sensor_data = {
        "pH": round(random.uniform(6.5,7.5),2),
        "Temp": round(random.uniform(35,39),2),
        "DO": round(random.uniform(75,90),2),
        "OD": round(random.uniform(0.5,1.0),2)
    }

    db.reference("sensors").push(sensor_data)
    print("Sent:", sensor_data)


    time.sleep(5)
