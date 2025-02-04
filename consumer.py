from scapy.all import Ether # Pour décoder le paquet reçu et afficher ses détails.
from mqqt_service import MQTTService

MQTT_TOPIC="vehicule/cam"

def on_connect(client,userdata,flags,rc):
    """
    Fonction callback appelée lors de la connexion au broker MQTT.
    
    :param client: L'instance du client MQTT.
    :param rc: Code de retour de la connexion.
    """
    print("Connecté au broker MQTT avec le code retour ✅", rc)
    # Une fois connecté, s'abonner au topic pour recevoir les messages.
    client.subscribe(MQTT_TOPIC)

def on_message(client,userdata,msg):
    """
    Fonction callback appelée lorsqu'un message est reçu.
    
    :param client: L'instance du client MQTT.
    :param msg: L'objet message contenant le topic et le payload.
    """
    print("\n==== Message reçu ===")
    print("Topic : ",msg.topic)
    print("Taille du paquet :", len(msg.payload),"octets")

    try:
        # Tente de décoder le payload en utilisant la couche Ethernet avec Scapy.
        packet=Ether(msg.payload)
        print("Détails du paquet :")
        # Affiche de manière détaillée la structure du paquet.
        packet.show()
    except Exception as e:
        print("Erreur lors de la décodification du paquet :", e)
        print("Contenu brut (hexadécimal) :", msg.payload.hex())

def main():
    # Création et initialisation du service MQTT pour se connecter au broker.
    mqtt_service=MQTTService(broker="localhost",port=1883)
    # Définition de la fonction callback à utiliser lors de la connexion.
    mqtt_service.set_on_connect(on_connect)
    # Définition de la fonction callback à utiliser lorsqu'un message est reçu.
    mqtt_service.set_on_message(on_message)
    # Connexion au broker MQTT.
    mqtt_service.connect()
    print("En attente des messages sur le topic :", MQTT_TOPIC)
    mqtt_service.loop_forever()

if __name__ == '__main__':
    main()
    