import json
import threading
import time
from flask import Flask, render_template, jsonify
from mqtt_service import MQTTService

app = Flask(__name__)

MQTT_BROKER = "localhost"
MQTT_TOPIC = "vehicule/cam"

positions = {}
mqtt_service = None  # Will hold our MQTTService instance

def on_connect(client, userdata, flags, rc):
    """
    Callback called when the MQTT client connects to the broker.
    """
    print(f"[MQTT] Connected with result code {rc}")
    # Subscribe to the topic after a successful connection
    mqtt_service.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    """
    Callback called each time a message is received on a subscribed topic.
    """
    global positions
    try:
        payload_str = msg.payload.decode("utf-8")
        data = json.loads(payload_str)
        station_id = data["stationId"]
        positions[station_id] = data  # Store/update the station's position

        print(f"[MQTT] Reçu : {data}")

    except json.JSONDecodeError as e:
        print(f"[Erreur] JSONDecodeError: {e}")

def mqtt_loop():
    """
    Separate thread handling the MQTT loop.
    """
    global mqtt_service
    mqtt_service = MQTTService(broker=MQTT_BROKER)
    
    # Set callbacks
    mqtt_service.set_on_connect(on_connect)
    mqtt_service.set_on_message(on_message)

    # Connect and start the loop
    mqtt_service.connect()
    mqtt_service.loop_forever()

@app.route("/")
def index():
    return render_template("map.html")

@app.route("/data")
def get_data():
    """
    Returns the current positions in JSON format.
    """
    return jsonify(list(positions.values()))

def main():
    # Launch the MQTT loop in a background thread
    mqtt_thread = threading.Thread(target=mqtt_loop, daemon=True)
    mqtt_thread.start()

    # Launch the Flask application
    app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    main()
