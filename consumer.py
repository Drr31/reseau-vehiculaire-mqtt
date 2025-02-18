import json
import threading
import time
from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

MQTT_BROKER = "localhost"
MQTT_TOPIC = "vehicule/cam"

positions = {}

def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global positions
    try:
        payload_str = msg.payload.decode("utf-8")
        data = json.loads(payload_str)
        station_id = data["stationId"]
        positions[station_id] = data 

        print(f"[MQTT] Reçu : {data}")

    except json.JSONDecodeError as e:
        print(f"[Erreur] JSONDecodeError: {e}")

def mqtt_loop():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()

@app.route("/")
def index():
    return render_template("map.html")

@app.route("/data")
def get_data():
    return jsonify(list(positions.values()))

def main():
    mqtt_thread = threading.Thread(target=mqtt_loop, daemon=True)
    mqtt_thread.start()

    app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    main()
