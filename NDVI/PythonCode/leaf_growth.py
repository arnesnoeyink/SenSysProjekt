import os
import cv2
import numpy as np


def colorcounter(image):
    ranges = {
        "rot": ([0, 0, 128], [60, 60, 255]),
        "grün": ([0, 190, 210], [128, 255, 255]),
        'blau': ([0, 0, 0], [255, 0,0]),
        'all':  ([[0, 0, 0], [255, 255,255]])
    }
    pixel_count=[0,0,0,0]
    n = 0
    for color, (lower_range, upper_range) in ranges.items():
                mask = cv2.inRange(image, np.array(lower_range), np.array(upper_range))
                pixel_count [n]= np.sum(mask)
                n=n+1
        #print(pixel_count)

    return pixel_count
def percentCol(pC):
    ppC= [0,0,0]
    ppC=[pC[0],pC[1],pC[2]]/((pC[0]+pC[1]+pC[2]))*100
    return ppC

def bilddateien_auslesen(ordner_pfad):
    bilddateien = []
    erlaubte_dateiendungen = (".jpg", ".jpeg", ".png", ".gif")

    for datei in os.listdir(ordner_pfad):
        datei_pfad = os.path.join(ordner_pfad, datei)
        if os.path.isfile(datei_pfad) and datei.lower().endswith(erlaubte_dateiendungen):
            bilddateien.append(datei_pfad)

    return bilddateien
# import
mein_ordner = "NDVI/Data/Bilder_ersterLauf"
#mein_ordner = "NDVI/Data/Bilder_zweiterLauf"

alle_bilder = bilddateien_auslesen(mein_ordner)

# output  ad math
daten = [0,0,0]
n=0
daten_Mat=np.zeros((85,3))
for bild in alle_bilder:
    original = cv2.imread(bild)
    daten = (percentCol(colorcounter(original)))
    daten_Mat[n][0] = daten[0]
    daten_Mat[n][1] = daten[1]
    daten_Mat[n][2] = daten[2]
    n = n+1
np.savetxt("Auswertung.csv", daten_Mat, delimiter=";")

print("fertig")