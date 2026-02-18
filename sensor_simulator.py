import time
import random
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://biochamber-52607-default-rtdb.firebaseio.com/'
})

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