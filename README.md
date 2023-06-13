# Solar-Edge-Visualisierung
<br>
Informationsdashboard für SolarEdge Anlagen unter einem Account
<br>
Angezeigt wir die Aktuelle Leistung sowie die Produktion am Tag, im Monat, im Jahr sowie auf die gesamte Laufzeit.
<br>
Zusätzlich gibt es einen Grafisch aufbereitete anzeige der Leistung im Tagesverlauf sowie der Produktion der letzten 7 Tage.

<hr>

## Wie wird das Programm genutzt

### Vorraussetzungen
Um die Vorrausetzungen zu erfüllen muss erstens min. Python 3.9 installiert sein.
Starten des Programms müssen die Python Pakete installiert werden. Mit folgendem Kommando werden die Pakete auf Systemebene installiert.


```bash
pip install -r www/requirements.txt
```

Es kann auch zu Test zwecken das VENV verwendet werden, dann müssen keine Pakete installiert werden. Hier muss lediglich das VENV aktiviert werden.

```bash
./www/venv/activate
```

In einer Produktiven Umgebung MUSS ein WSGI Server installiert und konfiguriert werden!

### Initiale Konfiguration
Damit Daten abgerufen werden können, müssen Folgende variablen in der Datei ```Solar_Config.py``` definiert werden.

```python
API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # Hier den Account API Schlüssel einfügen
SITE_IDs = ['XXXXXXX', 'XXXXXXX'] # Hier werden die Standort ID´s als Liste hinterlegt
```

<span style="color: red; font-weight: bolder;">!WICHTIG!</span>
<br>
Unter ```API_KEY``` bitte NUR den API Schlüssel des Accounts keinen Seiten API Schlüssel eintragen!<br>
Bei ```SITE_IDs``` können beliebig viele Standort ID´s hinterlegt werden. <span style="color: red; font-weight: bold">!Bitte beachten!</span> In der Ansicht werden nacher die Daten aller Anlagen Zusammengerechnet. 
<br>

Die folgenden Variablen geben sind für das Aussehen und die Beschreibung zuständig: <br>
Es ist nicht Notwendig diese Variablen zu verändern oder anzupassen <br>

```python
TITLE_MAIN = '' # Hier wird der Titel auf der Hautpseite festgelegt
TITLE_EMBED = '' # Hier den Titel für die Einbettungs Seite festlegen 
COLOR_TEXT = '#505050' # Hier wird die Farbe des Textes Definiert
COLOR_TOP_BACKGROUND = '#bee75e' # Hier die Hintergrundfarbe des Header definieren
COLOR_TOP_TEXT = 'white' # Hier die Textfarbe des Headers festlegen 
```

### Programm zu Testzwecken starten
Zum starten folgenden Befehl ausführen

```bash
flask --app serve run --host 0.0.0.0
```

### Dashboard einbetten
Um das Dashboard in eine vorhandene Website einzubinden, kann die Folgende URL verwendet werden:

```url
http://ip-or-hostname-of-server:5000/?embed=true
```

Der folgende HTML tag kann auch genutzt werden:

```html
<iframe src="http://ip-or-hostname-of-server:5000/?embed=true" frameborder="0" height="550px" width="550px"></iframe>
```

## Screenshots

Dashboard Ansicht:

![](https://github.com/hiberniastudents/SolarEdge-Visualisierung/blob/main/dashboard-view.png?raw=true)


Einbettungs Ansicht:

![](https://github.com/hiberniastudents/SolarEdge-Visualisierung/blob/main/embed-view.png?raw=true)



