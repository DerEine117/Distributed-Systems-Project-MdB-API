# Verteilte Systeme Abgabe: MdB API
## Von Robert Knabe
## DHBW Stuttgart, Kurs WWI2023F (Data Science)

### Architektur
Der Programmentwurf wurde in Python mittels der Pakete fastapi, requests und dotenv entwickelt. Über requests findet die Abfrage der mdb-Daten API statt und mit fastapi wird die eigene API implementiert. Um dem Prinzip 3 der "12 Factor Apps" nachzukommen, sind alle Parameter mittels Umgebungsvariablen anpassbar, die sich ändern können (Bsp: API-Key, eigener Port, Addresse von mdb-Data). Die Reihenfolge der Priorität der Umgebungsvariablen ist dabei wie folgt:

1. (Docker) Run-Argumente (--env) → Höchste Priorität
2. Variablen aus der .env-Datei im Docker-Image
3. Fallback im Code/Dockerfile (:-default_value) → Niedrigste Priorität

Da die .env Datei aufgrund der Erwähnung in der .gitignore sowie der .dockerignore weder im Repository noch im Docker Image enthalten ist, sind an dieser Stelle für die Installation auf neuen Systemen vor allem die Docker-Run-Argumente sowie die festgelegten Default Werte in der config.py relevant. Die Standardwerte sind nur dann abzuändern, wenn von den hier aufgeführten Installationsintruktionen abgewichen wird (Bsp: anderer Name im Docker Netzwerk, andere Ports).

#### Beschreibung Dockerfile und .dockerignore
Die Dockerfile basiert auf einer schlanken python:3.9-slim Basis. Dadurch, dass zuerst ins workdir gewechselt und und dann die requirements.txt kopiert wird, wird caching ermöglicht. Als nächstes werden dann die Abhängigkeiten mittels "pip" installiert, was jedoch aufgrund der Anordnung NUR DANN geschieht, wenn sich die requirements.txt geändert haben. Erst im Anschluss wird nun der Rest kopiert, der Port geöffnet und der Service gestartet.

#### Beschreibung Kubernetes
Tbd.; teilweise unten schon indirekt Vorhanden

### Installation und Start der Anwendung:

### Variante 1: lokale Ausführung
Zur lokalen Ausführung muss zuerst das Repository geklont (https://github.com/DerEine117/Distributed-Systems-Project-MdB-API)  bzw die .zip Datei entpackt werden. Im Projektverzeichnis sollten sich nun neben der requirements.txt noch einige andere Dateien sowie ein Verzeichnis "app" befinden, in welchem sich der Python Programmcode befindet. Öffnen Sie für den folgenden Command ein Terminal und stellen Sie sicher, dass sie sich im Hauptverzeichnis "Distributed-Systems-Project-MdB-API" befinden und nicht im Ordner "app"!

1. Schritt: Virtuelles Environment erstellen (optional aber empfehlenswert)
- python -m venv .venv
- source .venv/bin/activate   für macOS/Linux
- .venv\Scripts\activate      für Windows
- Alternativ lassen sich die Schritte 1 und 2 bequem in VSCode ausführen, indem mit (F1) der Command "Python: Create Envirement..." ausgeführt wird 

2. Schritt: Verwendete Pakete installieren:
pip install -r requirements.txt
(Hinweis: Falls der Befehl nicht gefunden wird, ist möglicherweise pip nicht in der PATH Variable hinterlegt. In diesem Fall ein python -m vor den Command setzen.)

Hinweis: Stelle sicher, dass die für dieses Projekt vorgegebene Anwendung mdb-Data gestartet ist, um den Zugriff auf dessen API zu ermöglichen. Andernfalls wird bei Abfragen an diese Anwendung ein Timeout auftreten. Mittels default Werten in der Python Datei config.py liegen die Variablen zum Verbinden mit dem mdb-Data Service so vor, dass sie in einem Docker Netzwerk kommunizieren können. Damit die Anwendung aber lokal läuft und dennoch auf die mdb-Data API zugreifen kann, müssen die Umgebungsvariablen entsprechend gesetzt werden.

3. Schritt: .env Datei erstellen (Optional, siehe Hinweis!)
Erstelle eine Datei ".env" in der Hauptverzeichnisebene, also im gleichen Ordner wie die requirements.txt liegt. Deklariere die folgenden drei Variablen:

- MDB_API_KEY=der API Key des mdb-Data Services
- MDB_DATA_URL=http://localhost:8001/api/v1/byName = Adresse des Endpoints zur Datenabfrage

Hinweis: In der Abgabe aus Moodle ist die .env Datei bereits enthalten, nicht jedoch im GitHub Repository (siehe .gitignore). Dies soll einerseits ein direktes lokales Ausführen ermöglichen und andererseits die Anpassbarkeit für einen Produktiveinsatz verdeutlichen. Zusätzlich wurde folgende Annahme gemacht: Der API Key für den mdb-Data Service ist nicht im Produktiveinsatz. Er ist in der config.py als Standardwert angegeben, um zusätzliche Konfigurationsnotwendigkeit beim Ausführen der Anwendung zu vermeiden.


4. Schritt: Anwendung starten.
Zum Starten der Anwendung folgenden Befehl ins Terminal eingeben:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
(Hinweis: Auch hier kann eine fehlende PATH Variable für uvicorn ein Problem auslösen (unter Windows getestet). In diesem Fall ein python -m vor den Command setzen: 
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8002)



Testen der Anwendung; Abfragebeispiele:
Im Chrome Webbrowser: http://127.0.0.1:8002/api/v1/getByName?name=scholz

In Windwows Powershell: C:\Windows\System32\curl.exe "http://127.0.0.1:8002/api/v1/getByName?name=scholz" 

Im Linux Terminal (Ubuntu, macOS, WSL): curl "http://127.0.0.1:8002/api/v1/getByName?name=scholz"

Für den Namen "scholz" kommt folgende JSON Antwort von der API:

[
  {
    "id": "7506",
    "titel": "Olaf Scholz, Bundeskanzl."
  }
]

### Variante 2: Ausführung als Docker Container
1. Schritt: Um den Docker lokal zu bauen, muss ebenfalls das Repository geklont bzw. die abgegebene .zip Datei entpackt werden. Öffne nun ein Terminal (wichtig: gleiche Verzeichnisebene wie die requirements.txt, nicht im Ordner "app" befinden!)

2. Schritt: Ausführen des Docker build Befehls. Dieser Befehl baut mithilfe der Dockerfile sowie dier .dockerignore das Docker image.
- docker build -t dist-syst-mdb-api .

3. Schritt: Erstellen des docker Netzwerks "dhbw":
- docker network create dhbw

4. Schritt: Starten der beiden Docker Container, haraldu/mdb-data sowie dist-syst-mdb-api. Führe dazu die beiden folgenden Befehle aus:
- docker run --name mdb-data -dp 8001:8001 --network dhbw --env DELAY=0 haraldu/mdb-data:1
docker run --name mdb-api -dp 8002:8002 --network dhbw -e MDB_DATA_API_KEY=doyi6ohchieKaeL9 dist-syst-mdb-api

Erklärung der Befehle:
- --name vergibt dem Container einen Namen, der sozusagen als Hostname fungiert. Über diesen wird der Service vom anderen Container angesprochen, anstelle einer IP Adresse oder "localhost"
- --network fügt den Docker zu einem bestehendem Netzwerk hinzu. Essentiell für die Kommunikation zwischen den Containern!
- Der Port 8001 für mdb-Data ist standardmäßig in der mdb-api konfiguriert. Falls der Port hier angepasst wird, kann dies über ein ändern der Umgebungsvariable MDB_DATA_URL angepasst werden.
- --env im mdb-data Service ist für schnelle Reaktionszeit auf 0 gesetzt. Erhöhung auf 2+ führt zum Timeout.

Testen der Anwendung; Abfragebeispiele:
Im Chrome Webbrowser: http://127.0.0.1:8002/api/v1/getByName?name=scholz

In Windows Powershell: C:\Windows\System32\curl.exe "http://127.0.0.1:8002/api/v1/getByName?name=scholz" 

Im Linux Terminal (Ubuntu, macOS, WSL): curl "http://127.0.0.1:8002/api/v1/getByName?name=scholz"

Für den Namen "scholz" kommt folgende JSON Antwort von der API:

[
  {
    "id": "7506",
    "titel": "Olaf Scholz, Bundeskanzl."
  }
]


### Variante 3: Ausführung in Kubernetes
Voraussetzungen: Kubeadm (Windows/Docker Desktop) oder minikube (Linux/macOS) gestartet

1. Schritt: Wie bei den Varianten 1 und 2 das Repository klonen bzw die abgegebene .zip entpacken. Ebenfalls minikube starten (wenn nicht bereits durch Docker Desktop geschehen. Befehl für die bwLehrpool-VM: minikube start --cpus 2 --memory 6144 --driver docker)

2. Schritt: Docker bauen. (Falls nicht bereits geschehen)
- docker build -t dist-syst-mdb-api .

Hinweis: Ich habe das gesamte Projekt auf Windows mit Docker Desktop durchgeführt. Bei der Durchführung auf der bw-Lehrpool Ubuntu-VM ist zusätzlich folgender Schritt notwendig, da hier minikube verwendet wird, was eine eigene Docker-Engine nutzt:
- minikube image load dist-syst-mdb-api:latest

3. Die Objekte aus dem Verzeichnis "deployment" (hier im Ordner/ Repo) anlegen. Folgenden Befehl im Terminal im Hauptverzeichnis ausführen.
- kubectl apply -f deployment/

- Ergebnis:
```sh
configmap/mdb-api-config created
deployment.apps/mdb-api created
secret/mdb-api-secret created
service/mdb-api created
```

Hinweis: Diesen Schritt ebenfalls für den mdb-data Service durchführen, siehe gegebenes Dokument "Portfolioprüfung".

4. Status überprüfen, um erfolgreiches Deployment sicherzustellen:
- kubectl get pods

- Ergebnis: (Name bei Reproduktion nicht identisch)
```sh
NAME                        READY   STATUS    RESTARTS   AGE
mdb-api-cc74b8fc5-5mjvn     1/1     Running   0          32s
mdb-data-6c8d9bf95c-fd7d4   1/1     Running   0          50s
```

5. NodePort für Zugriff herausfinden/ überprüfen (festgelegt in service.yaml -> 30002)
- kubectl get svc mdb-api

- Ergebnis:
```sh
NAME      TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
mdb-api   NodePort   10.101.111.147   <none>        8002:30002/TCP   22m
```

Geschafft! Nun sind beide Services in Kubernetes deployed, der Service mdb-api kann auf mdb-data zugreifen und ist wiederum extern unter dem Nodeport 30002 erreichbar. Dies kann nun ausprobiert werden!
- Auf der Lehrpool ubuntu-VM ist der Service Dank minikube einfach aufrufbar:
```sh
minikube service mdb-api
```
Dies öffnet im Standwebbrowser die entsprechende Webaddresse des Services mdb-api. Nun kann der Pfad in der URL auf /health oder /api/v1/getByName?name=müller abgeändert werden.

- unter Docker Dektop mit Kubeadm auf Windows ist der Service unter localhost:Nodeport erreichbar:

Abfragebeispiele mit NodePort 30002:
Im Chrome Webbrowser: http://127.0.0.1:30002/api/v1/getByName?name=scholz

In Windwows Powershell: C:\Windows\System32\curl.exe "http://127.0.0.1:30002/api/v1/getByName?name=scholz" 

Im Linux Terminal (Ubuntu, macOS, WSL): curl "http://127.0.0.1:30002/api/v1/getByName?name=scholz"