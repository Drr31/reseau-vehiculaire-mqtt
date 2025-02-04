# Mise en place d'une communication MQTT pour la transmission de traces CAM dans un réseau véhiculaire

**Auteur :** Rochdi DARDOR, Ameur BENSGHAIER, Roy EL HADDAD **IATIC5**  
**Date :** [04/02/2025]

---

## 1. Introduction

Ce projet a pour objectif d'établir une communication entre un producteur et un consommateur en utilisant le protocole MQTT via un broker. Il s'agit de transmettre des traces CAM, enregistrées dans un fichier PCAP, depuis un producteur vers un consommateur via un broker MQTT. Le présent document détaille le contexte, les objectifs, l'architecture, le choix des technologies, l'implémentation et les résultats obtenus.

---

## 2. Contexte et Objectifs

### 2.1 Contexte

Les réseaux véhiculaires sont au cœur des technologies de l'Internet des Objets (IoT) et des systèmes intelligents pour la gestion du trafic. Dans ce contexte, la transmission rapide et fiable de données entre véhicules et infrastructures est essentielle. Ce projet exploite MQTT, un protocole de messagerie léger et efficace, pour simuler la communication dans un environnement de réseau véhiculaire.

### 2.2 Objectifs

- **Transmission des traces CAM :** Lire un fichier PCAP contenant des messages CAM sécurisés et publier chaque paquet via MQTT.
- **Communication décentralisée :** Mettre en œuvre un modèle publication/abonnement pour découpler le producteur et le consommateur.
- **Affichage et décodage :** À la réception, décoder et afficher le contenu des paquets afin de vérifier leur intégrité.

---

## 3. Choix des Technologies et Architecture

### 3.1 Technologies Utilisées

- **Python 3 :** Langage de programmation pour implémenter le producteur, le consommateur et le module MQTT.
- **Paho-MQTT :** Bibliothèque Python pour gérer la communication MQTT.
- **Scapy :** Outil puissant pour la manipulation et l'analyse de paquets réseau.
- **Mosquitto :** Broker MQTT léger et populaire, installé localement (via Homebrew sur Mac).

### 3.2 Architecture du Système

Le système est composé de trois entités principales :

- **Producteur :** Lit le fichier PCAP, convertit chaque paquet en bytes et publie ces paquets sur un topic spécifique du broker MQTT.
- **Broker (Mosquitto) :** Sert de serveur central qui reçoit les messages du producteur et les redistribue aux consommateurs abonnés.
- **Consommateur :** S'abonne au même topic et, à la réception des messages, décode et affiche le contenu des paquets.

**Schéma Simplifié :**

```plaintext
+-------------------+          +-----------------+          +--------------------+
|                   |          |                 |          |                    |
|   Producteur      |          |   Broker MQTT   |          |   Consommateur     |
| (Lecture PCAP et  |  MQTT    |   (Mosquitto)   |  MQTT    | (Affichage des     |
|  publication)     | -------> |                 | -------> |  paquets reçus)    |
+-------------------+          +-----------------+          +--------------------+

```

## 4. Implémentation
Pour une meilleure organisation et réutilisabilité du code, nous avons découpé le projet en trois fichiers principaux :

### 4.1 Module MQTT (mqtt_service.py)
Ce module encapsule toute la logique de connexion, publication et abonnement au broker MQTT.
Il propose une classe MQTTService qui permet de :
  -Se connecter au broker (adresse par défaut : localhost, port : 1883).
  -Publier des messages sur un topic donné.
  -S'abonner à des topics et définir des callbacks pour la gestion des messages.

### 4.2 Producteur (producer.py)
Le producteur lit le fichier PCAP contenant les traces CAM et publie chaque paquet converti en bytes sur le topic "vehicule/cam".
Le délai entre les publications permet d'éviter la saturation du broker et de simuler une transmission séquentielle.

### 4.3 Consommateur (consumer.py)
Le consommateur se connecte au broker, s'abonne au topic "vehicule/cam" et affiche les informations détaillées des paquets reçus.
L'utilisation de Scapy permet d'analyser les différentes couches du paquet, notamment la couche Ethernet et la charge utile brute.

## 5. Expérimentation et Résultats
### 5.1 Mise en place de l'environnement
Installation du broker Mosquitto :
Mosquitto a été installé via Homebrew sur Mac (commande : brew install mosquitto) et lancé avec la commande mosquitto dans un terminal.

Lancement des scripts :
1.Le consommateur a été lancé pour s'abonner au topic et attendre les messages.
2.Le producteur a ensuite été exécuté, lisant le fichier PCAP et publiant les paquets sur le broker.

### 5.2 Exemple de sortie
Un extrait de la sortie du consommateur :

```bash
==== Message reçu ===
Topic : vehicule/cam
Taille du paquet : 101 octets
Détails du paquet :
###[ Ethernet ]###
  dst       = ff:ff:ff:ff:ff:ff
  src       = 08:00:27:50:0f:9b
  type      = 0x8947
###[ Raw ]###
     load      = b"\x11\x00+\x01 P\x80\x00\x00/..."
```

Cette sortie indique que :

- Le message a bien été reçu sur le topic "vehicule/cam".
- La taille du paquet (101 octets) est conforme aux données envoyées.
- La structure du paquet est analysée en deux couches :
  - Ethernet : Indique l'adresse source, l'adresse de destination (ici en broadcast) et le type de protocole (0x8947).
  - Raw : Contient la charge utile brute du paquet (les données CAM).


## 6. Discussion
 Avantages du Modèle Publication/Abonnement
Découplage des composants :
Le producteur et le consommateur n'ont pas besoin de se connaître directement. Le broker (Mosquitto) se charge de la transmission, ce qui simplifie l'architecture.

Scalabilité :
Il est possible d'ajouter plusieurs consommateurs sans modifier le code du producteur.

Fiabilité et QoS :
Le protocole MQTT offre différents niveaux de qualité de service (QoS) pour garantir la livraison des messages, même en cas de déconnexions temporaires.

## 7. Conclusion
Ce projet a permis de mettre en place une communication efficace entre un producteur et un consommateur via un broker MQTT. En utilisant Python, Scapy et Mosquitto, nous avons démontré la faisabilité de transmettre des traces CAM extraites d'un fichier PCAP dans un contexte de réseau véhiculaire. Le découpage du code en modules distincts (gestion MQTT, publication et consommation) offre une architecture modulaire, facilement évolutive et maintenable.

L'approche adoptée illustre l'intérêt du modèle publication/abonnement pour des applications nécessitant flexibilité et scalabilité, particulièrement dans le domaine de l'IoT et des systèmes embarqués. Les améliorations possibles évoquées ouvrent des perspectives pour enrichir ce système, tant au niveau du décodage des messages qu'au niveau de la robustesse générale.
