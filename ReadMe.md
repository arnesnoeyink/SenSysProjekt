![color_mapped_image](https://github.com/arnesnoeyink/SenSysProjekt/assets/61993557/522521dd-74c3-4766-b5e7-3363ff22316a)# Sensorsysteme Projektarbeit
Dieses Projekt dient als elektronischer Anhang zur Projektarbeit im Modul Sensorsysteme.
# Time of flight Kamera
Für die Time of flight Kamera befindet sich der genutzte Code im Verzeichnis `tof/code`. Die Daten der Testreihe 1 und 2 befinden sich im Verzeichnis `tof/data`. Die Ergebnisse sind im Verzeichnis `tof/results` zu finden.
## Code
Die Python Datei `capture_image.py` kann auf dem Raspberry Pi ausgeführt werden, sobald die Software der Arducam Time of flight Kamera installiert ist.

Die Python Datei `read_image.py` kann zur Auswertung der aufgenommen Datein genutzt werden. Zur Auswahl der Testreihe muss die Zeile 17-18 in der Datei `read_image.py` geändert werden. Nachdem das Programm durchgelaufen ist, öffnet sich der Graph und das Video wird erstellt.

Die Ergebnisse werden automatisch im Ordner `tof/results/testreihe_*` abgespeichert. 

```
git clone https://github.com/arnesnoeyink/SenSysProjekt.git
cd SenSysProjekt
python3 tof/code/read_image.py
```

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
