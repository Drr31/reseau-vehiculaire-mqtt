# Projet de communication MQTT avec RabbitMQ

## Description
Ce projet implémente une communication entre un **producteur** et un **consommateur** via **RabbitMQ** en utilisant le protocole **MQTT**. L'objectif est de transmettre des **traces CAM** enregistrées sous format **PCAP** à travers un **broker MQTT**, afin que le consommateur puisse les recevoir et afficher les informations de position des véhicules.

## Fonctionnalités
- Lecture d'un fichier **PCAP** contenant des traces **CAM**.
- Envoi des paquets via un **broker MQTT** sur un topic défini.
- Réception et décodage des paquets par le consommateur.
- Extraction et affichage des coordonnées GPS des véhicules.

## Prérequis
### Outils nécessaires
- **Python 3.7+**
- **RabbitMQ avec le plugin MQTT activé**
- **Wireshark (optionnel, pour visualiser les traces PCAP)**

### Installation des dépendances
Avant d'exécuter le projet, installez les dépendances requises avec :

```sh
pip install -r requirements.txt
```

### Installation et démarrage de RabbitMQ 
#### macOS 
```sh
brew install rabbitmq
brew services start rabbitmq
```
Vérifiez que RabbitMQ fonctionne :
```sh
brew services list
```

#### Windows
Utilisez [Chocolatey](https://chocolatey.org/) pour une installation facile :
```sh
choco install rabbitmq
```
Démarrez RabbitMQ :
```sh
rabbitmq-server
```
Ou, si installé manuellement, exécutez :
```sh
C:\Program Files\RabbitMQ Server\sbin\rabbitmq-server.bat
```


## Structure du projet
```
|
├── producer.py        # Producteur MQTT : envoie les paquets du fichier PCAP
├── consumer.py        # Consommateur MQTT : reçoit et analyse les paquets
├── mqtt_service.py    # Service MQTT réutilisable pour gérer la connexion au broker
├── requirements.txt   # Dépendances du projet
├── etsi-its-cam-unsecured.pcapng  # Fichier de traces à envoyer
```

## Utilisation

### 1️⃣ Lancer le **broker MQTT** (RabbitMQ)

### 2️⃣ Exécuter le **consommateur** (récepteur des messages MQTT)
Dans un terminal, lancez :
```sh
python consumer.py
```

Ce programme attend les messages du producteur et affiche les informations des véhicules.

### 3️⃣ Exécuter le **producteur** (envoi des paquets MQTT)
Dans un autre terminal, lancez :
```sh
python producer.py
```

Le producteur va :
1. Lire le fichier **PCAP**.
2. Publier chaque paquet sur le broker MQTT.
3. Attendre un court délai entre chaque envoi pour éviter la saturation du réseau.

### 4️⃣ Observer les résultats
Une fois le **producteur** en marche, le **consommateur** affichera les détails des paquets reçus, y compris la **position GPS des véhicules**.

Exemple de sortie :
```
==== Message reçu ===
Topic : vehicule/cam
Taille du paquet : 101 octets

==== Position du véhicule ====
Latitude: 43.5534660°
Longitude: 10.3034184°
```

## Compatibilité
✅ **MacOS (M1/M2)**  
✅ **Windows** (avec [WSL](https://learn.microsoft.com/fr-fr/windows/wsl/) ou un environnement Python natif)  
✅ **Linux**

### Installation sur **Windows**
Pour exécuter ce projet sur Windows :
1. **Installer Python 3** (depuis [python.org](https://www.python.org/)).
2. Installer **RabbitMQ** en activant le plugin MQTT.
3. Installer [Wireshark](https://www.wireshark.org/) (optionnel) pour analyser les paquets PCAP.
4. Exécuter le projet comme indiqué ci-dessus.


