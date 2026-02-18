from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

FIREBASE_URL = "https://biochamber-52607-default-rtdb.firebaseio.com"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    sensors = requests.get(f"{FIREBASE_URL}/sensors.json").json()
    prediction = requests.get(f"{FIREBASE_URL}/prediction.json").json()

    sensor_list = list(sensors.values())[-20:] if sensors else []

    return jsonify({
        "sensors": sensor_list,
        "prediction": prediction
    })
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from flask import Flask

app = Flask(__name__)


