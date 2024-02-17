# Sensorsysteme Projektarbeit
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

# Referenzen
Als Referenzen wurden die folgenden Links genutzt:
- `https://github.com/ArduCAM/Arducam_tof_camera`
- `https://docs.arducam.com/Raspberry-Pi-Camera/Tof-camera/Getting-Started/`