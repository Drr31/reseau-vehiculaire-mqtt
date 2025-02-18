import os
import time
import json
import pyshark
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_TOPIC = "vehicule/cam"
PCAP_FILENAME = "v2v-EVA-2-0-filtered.pcap" 

def main():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, 1883, 60)
    pcap_path = os.path.join(os.path.dirname(__file__), PCAP_FILENAME)
    print(f"Lecture du fichier: {pcap_path}")
    cap = pyshark.FileCapture(pcap_path)

    for i, packet in enumerate(cap):
        try:
            if hasattr(packet, 'its'):
                station_id = int(packet.its.stationid)
                latitude   = int(packet.its.latitude) / 1e7
                longitude  = int(packet.its.longitude) / 1e7
                speed      = int(packet.its.speedvalue) / 100.0
                heading    = int(packet.its.headingvalue)

                # Build the JSON data
                cam_data = {
                    "stationId": station_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "speed": speed,
                    "heading": heading
                }

                json_str = json.dumps(cam_data)
                client.publish(MQTT_TOPIC, json_str)
                print(f"Envoyé {i+1} : {cam_data}")

                time.sleep(0.1)
            else:
                print(f"Paquet #{i+1} ne contient pas de couche 'its'. Ignoré.")
        except AttributeError:
            print(f"Paquet #{i+1} ignoré (champs manquants).")

    cap.close()
    client.disconnect()
    print("Fin de l'envoi des données.")

if __name__ == "__main__":
    main()
