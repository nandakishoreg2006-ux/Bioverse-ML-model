# dashboard.py

from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Initialize Firebase (only once)
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://biochamber-52607-default-rtdb.firebaseio.com/'
})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    sensors = db.reference("sensors").get()
    prediction = db.reference("prediction").get()

    sensor_list = list(sensors.values())[-20:] if sensors else []

    return jsonify({
        "sensors": sensor_list,
        "prediction": prediction
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
