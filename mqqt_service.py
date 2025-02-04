import paho.mqtt.client as mqtt

class MQTTService:
    def __init__(self, broker="localhost",port=1883,client_id=None,clean_session=True):
        """
        Initialisation du service MQTT.
        
        :param broker: Adresse du broker MQTT (par défaut "localhost").
        :param port: Port du broker (par défaut 1883).
        :param client_id: Identifiant du client MQTT (optionnel).
        :param clean_session: Indique si la session doit être propre (True) ou persistante (False).
        """
        self.broker= broker
        self.port = port
        self.client_id= client_id
        self.clean_session=clean_session
        # Création d'une instance client MQTT avec les paramètres fournis.
        self.client = mqtt.Client(client_id=client_id,clean_session=clean_session)


    
    def connect(self):
        """
        Se connecte au broker MQTT en utilisant l'adresse et le port définis.
        Le troisième paramètre (60) correspond au keepalive (durée en secondes entre deux messages ping).
        """
        self.client.connect(self.broker, self.port, 60)

    
    def publish(self, topic, payload, qos=0):
        """
        Publie un message sur un topic donné.
        
        :param topic: Le topic sur lequel publier le message.
        :param payload: Le contenu du message (peut être de type bytes).
        :param qos: Niveau de qualité de service (0, 1 ou 2).
        :return: Le résultat de la publication.
        """
        result= self.client.publish(topic,payload,qos=qos)
        return result
    
    def subscribe(self,topic,qos=0):
        """
        S'abonne à un topic pour recevoir des messages.
        
        :param topic: Le topic auquel s'abonner.
        :param qos: Niveau de qualité de service pour la réception.
        """
        self.client.subscribe(topic,qos=qos)
    
    def set_on_message(self,on_message_callback):
        """
        Définit la fonction de callback qui sera appelée lorsqu'un message est reçu.
        
        :param on_message_callback: La fonction callback pour le traitement des messages reçus.
        """
        self.client.on_message=on_message_callback
    
    def set_on_connect(self,on_connect_callback):
        """
        Définit la fonction de callback qui sera appelée lors de la connexion au broker.
        
        :param on_connect_callback: La fonction callback pour le traitement de la connexion.
        """
        self.client.on_connect=on_connect_callback
    
    def loop_forever(self):
        """
        Démarre une boucle infinie pour maintenir la connexion active et écouter les messages.
        """
        self.client.loop_forever()
    
    def disconnect(self):
        """
        Ferme proprement la connexion avec le broker MQTT.
        """
        self.client.disconnect()
        
        
        
        