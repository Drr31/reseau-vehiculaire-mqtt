import time
from scapy.all import rdpcap  # Pour lire le fichier PCAP et manipuler les paquets.
from mqqt_service import MQTTService

# Définition du topic sur lequel les paquets seront publiés.
MQTT_TOPIC="vehicule/cam"

def main():
    #Instanciation du service MQTT
    mqtt_service=MQTTService(broker="localhost",port=1883)
    mqtt_service.connect()

    #Lecture du fichier PCAP
    try:
        packets=rdpcap("etsi-its-cam-unsecured.pcapng")
    except Exception as e :
        print("Erreur lors de la lecture du fichier PCAP: ",e)
        return
    
    print(f"Nombre de paquets lus = {len(packets)}")

    #Publication des paquets sur le topic
    for i,pkt in enumerate(packets):
    # Conversion du paquet en bytes pour pouvoir le publier.
        raw_pkt=bytes(pkt)
        print(f"Publication du paquet {i+1}/{len(packets)}")
    # Publication du paquet sur le topic défini avec un QoS de 1 (garantie au moins une livraison).
        mqtt_service.publish(MQTT_TOPIC,payload=raw_pkt,qos=1)
    # Délai de 0,1 seconde entre chaque publication pour ne pas saturer le broker.
        time.sleep(0.1)
    # Déconnexion propre du broker une fois tous les paquets publiés.
    mqtt_service.disconnect()
    print("Tous les paquets ont été publiées ✅.")

if __name__ == '__main__':
    main()
    
