from flask import Flask, render_template, jsonify
import folium
import struct
from scapy.all import Ether
from mqtt_service import MQTTService

MQTT_TOPIC = "vehicule/cam"
app = Flask(__name__)

# Store last received GPS data
vehicle_data = {"latitude": 0, "longitude": 0, "speed": 0}

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker ✅, return code:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global vehicle_data
    try:
        packet = Ether(msg.payload)
        raw_payload = bytes(packet.payload)

        # Extract latitude, longitude, and speed
        latitude_raw, longitude_raw = struct.unpack_from(">i i", raw_payload, offset=36)
        speed_raw = struct.unpack_from(">H", raw_payload, offset=50)[0]

        # Convert to real-world values
        latitude = latitude_raw / 10**7
        longitude = longitude_raw / 10**7
        speed = speed_raw * 0.01  # Convert from 0.01 m/s

        vehicle_data = {"latitude": latitude, "longitude": longitude, "speed": speed}
        print(f"Updated Vehicle Data: {vehicle_data}")

    except Exception as e:
        print("Error decoding packet:", e)

# Flask Route: Serve Updated Map
@app.route("/")
def index():
    return render_template("map.html")

@app.route("/data")
def get_data():
    return jsonify(vehicle_data)

# MQTT Initialization
mqtt_service = MQTTService(broker="localhost", port=1883)
mqtt_service.set_on_connect(on_connect)
mqtt_service.set_on_message(on_message)
mqtt_service.connect()

# Run Flask and MQTT together
if __name__ == "__main__":
    import threading
    mqtt_thread = threading.Thread(target=mqtt_service.loop_forever, daemon=True)
    mqtt_thread.start()
    app.run(host="0.0.0.0", port=8080, debug=True)
