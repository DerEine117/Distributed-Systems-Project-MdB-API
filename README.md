# Vertielte Systeme Abgabe: MdB API
## Von Robert Knabe
## DHBW Stuttgart, Kurs WWI2023F (Data Science)

### Architekrur
Der Programmentwurf wurde in Python mittels der Pakete fastapi, requests und dotenv entwickelt. Über requests findet die Abfrage der mdb-Daten API statt und mit fastapi wird die eigene API implementiert. Um dem Prinzip 3 der "12 Factor Apps" nachzukommen, sind alle Parameter mittels Umgebungsvariablen anpassbar, die sich ändern können (Bsp: API-Key, eigener Port, Addresse von mdb-Data). Die Reihenfolge der Priorität der Umgebungsvariablen ist dabei wie folgt:

1. (Docker) Run-Argumente (--env) → Höchste Priorität
2. Variablen aus der .env-Datei im Docker-Image
3. Fallback im Code/Dockerfile (:-default_value) → Niedrigste Priorität

Da die .env Datei aufgrund der Erwähnung in der .gitignore sowie der .dockerignore weder im Repository noch im Docker Image enthalten ist, sind an dieser Stelle für die Installation auf neuen Systemen vor allem die Docker-Run-Argumente sowie die festgelegten Default Werte in der config.py relevant. Die Standardwerte sind nur dann abzuändern, wenn von den hier aufgeführten Installationsintruktionen abgewichen wird (Bsp: anderer Name im Docker Netzwerk, andere Ports).

### Installation und Start der Anwendung:

#### lokale Ausführung
Zur lokalen AUsführung muss zuerst das Repository geklont (https://github.com/DerEine117/Distributed-Systems-Project-MdB-API)  bzw die .zip Datei entpackt werden. Im Projektverzeichnis sollten sich nun neben der requirements.txt noch einige andere Dateien sowie ein Verzeichnis "app" befinden, in welchem sich der Python Programmcode befindet. Öffnen Sie für den folgenden Command ein Terminal und stellen Sie sicher, dass sie sich im Hauptverzeichnis "Distributed-Systems-Project-MdB-API" befinden und nicht im Ordner "app"!

1. Schritt: Virtuelles Envirement erstellen (optional aber empfehlenswert)
- python -m venv venv
- source venv/bin/activate   für macOS/Linux
- venv\Scripts\activate      für Windows

2. Schritt: Verwendete Pakete installieren:
pip install -r requirements.txt
(Windows: Falls der Befehl nicht gefunden wird, ist möglicherweise pip nicht in der PATH Variable hinterlegt. In diesem Fall ein python -m vor den Command setzen.)

Hinweis: Stelle sicher, dass die für dieses Projekt vorgegebene Anwendung mdb-Data gestartet ist, um den Zugriff auf dessen API zu ermöglichen. Andernfalls wird bei Abfragen an diese Anwendung ein Timeout auftreten. Mittels default Werten in der Python Datei config.py liegen die Variablen zum Verbinden mit dem mdb-Data Service so vor, dass sie in einem Docker Netzwerk kommunizieren können. Damit die Anwendung aber lokal läuft und dennoch auf die mdb-Data API zugreifen kann, müssen die Umgebungsvariablen entsprechend gesetzt werden.

3. Schritt: .env Datei erstellen
Erstelle eine Datei ".env" in der Hauptverzeichnisebene, also im gleichen Ordner wie die requirements.txt liegt. Deklariere die folgenden drei Variablen:

- MDB_API_KEY=doyi6ohchieKaeL9
- MDB_DATA_URL=http://localhost:8001/api/v1/byName
- PORT=8005

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

#### Ausführung als Docker Container
hallo

#### Ausführung in Kubernetes
