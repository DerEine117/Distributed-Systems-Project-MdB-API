# Vertielte Systeme Abgabe: MdB API
## Von Robert Knabe
## DHBW Stuttgart, Kurs WWI2023F (Data Science)

### Architekrur
Der Programmentwurf wurde in Python mittels der Pakete fastapi, requests und dotenv entwickelt. Über requests findet die Abfrage der mdb-Daten API statt und mit fastapi wird die eigene API implementiert. Um dem Prinzip 3 der "12 Factor Apps" nachzukommen, sind alle Parameter mittels Umgebungsvariablen anpassbar, die sich ändern können (Bsp: API-Key, eigener Port, Addresse von mdb-Data). Die Reihenfolge der Priorität der Umgebungsvariablen ist dabei wie folgt:

1. Docker-Run-Argumente (--env) → Höchste Priorität
2. Variablen aus der .env-Datei im Docker-Image
3. Fallback im Code/Dockerfile (:-default_value) → Niedrigste Priorität

Da die .env Datei aufgrund der Erwähnung in der .gitignore sowie der .dockerignore weder im Repository noch im Docker Image enthalten ist, sind an dieser Stelle für die Installation auf neuen Systemen vor allem die Docker-Run-Argumente sowie die festgelegten Default Werte in der config.py relevant. Die Standardwerte sind nur dann abzuändern, wenn von den hier aufgeführten Installationsintruktionen abgewichen wird (Bsp: anderer Name im Docker Netzwerk, andere Ports).

### Installation
