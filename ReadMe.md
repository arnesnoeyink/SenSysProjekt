# Sensorsysteme Projektarbeit
Dieses Projekt dient als elektronischer Anhang zur Projektarbeit im Modul Sensorsysteme.
# Time of flight Kamera
Für die Time of flight Kamera befindet sich der genutzte Code im Verzeichnis `tof/code`. Die Daten der Testreihe 1 und 2 befinden sich im Verzeichnis `tof/data`. Zusätzlich befinden sich Test Daten im Verzeichnis `tof/data`. Die Ergebnisse sind im Verzeichnis `tof/results` zu finden.
## Code
```
git clone https://github.com/arnesnoeyink/SenSysProjekt.git
cd SenSysProjekt
```

Die Python Datei `capture_image.py` kann auf dem Raspberry Pi ausgeführt werden, sobald die Software der Arducam Time of flight Kamera installiert ist.

Die Python Datei `read_image.py` kann genutzt werden, um ein Bild zu öffnen und per Mausklick ein Rechteck zu erzeugen von dem die Höhe auf der Kommandozeile ausgegeben wird.

```
python3 tof/code/read_image.py
```

Die Python Datei `highest_point.py` kann genutzt werden, um automatisch geringsten Abstand zur Time of flight Kamera auszugeben. Bei den gemessenen Pflanzen handelt es sich somit um den höhsten Punkt.

```
python3 tof/code/highest_point.py
```

Die Python Datei `analyze_data_series.py` kann zur Auswertung der aufgenommen Datein genutzt werden. Zur Auswahl der Testreihe muss die Zeile 17-18 in der Datei `analyze_data_series.py` geändert werden. Nachdem das Programm durchgelaufen ist, öffnet sich der Graph und das Video wird erstellt.
```
python3 tof/code/analyze_data_series.py
```

Die Ergebnisse werden automatisch im Ordner `tof/results/testreihe_*` abgespeichert. 


# NDVI Kamera 
Für die NDVI Kamera befindet sich der erstellte Code im Verzeichnis `NDVI/PythonCode`. Die Daten der Testreihe 1 und 2 befinden sich im Verzeichnis `NDVI/Data`. Die Ergebnisse befinden im Verzeichnis `NDVI/Results`.

## Code
Die Python Datei `main.py` kann auf jedem Raspberry Pi oder Computer ausgeführt werden um Aufnahmen einer NIR fähigen Kamera umzuwandeln.
Dazu muss innerhalb der `main.py` in Zeile 9 ein Bildordner ausgewählt werden. Die dort enthaltenen Bilder werden dann auf das NIR Spektrum untersucht. 

Die Ergebnisse werden dann in eine Zieldatei namens bild_werte.txt geschrieben um diese weiter zu verarbeiten.


# Referenzen
Als Referenzen wurden die folgenden Links genutzt:
- `https://github.com/ArduCAM/Arducam_tof_camera`
- `https://docs.arducam.com/Raspberry-Pi-Camera/Tof-camera/Getting-Started/`
