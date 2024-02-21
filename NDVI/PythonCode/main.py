from __future__ import print_function
import os
import cv2
import numpy as np
from fastiecm import fastiecm
import os

# Verzeichnis mit den Bildern
image_directory = "NDVI/Data/Bilder_ersterLauf"
#image_directory = "NDVI/Data/Bilder_zweiterLauf"

# Ausgabedatei für die Werte
output_file = 'bild_werte.txt'  # Dateiname für die Ausgabedatei

def calculate_color_percentages(image):
    # Konvertiere das Bild von BGR zu RGB, da OpenCV standardmäßig BGR verwendet
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Definiere die Schwellenwerte für Weiß, Grau und Schwarz (in RGB)
    white_threshold = 240
    gray_threshold = 100
    black_threshold = 15

    # Berechne die Summe der Pixel in jedem Farbkanal
    total_pixels = image_rgb.shape[0] * image_rgb.shape[1]
    red_pixels = np.sum(image_rgb[:, :, 0])
    green_pixels = np.sum(image_rgb[:, :, 1])
    blue_pixels = np.sum(image_rgb[:, :, 2])

    # Zähle die Pixel in den Bereichen Weiß, Grau und Schwarz
    white_pixels = np.sum(np.all(image_rgb >= white_threshold, axis=2))
    gray_pixels = np.sum(np.all((image_rgb >= gray_threshold) & (image_rgb < white_threshold), axis=2))
    black_pixels = np.sum(np.all(image_rgb < black_threshold, axis=2))

    relevantpixels = red_pixels+green_pixels+blue_pixels+gray_pixels+white_pixels+black_pixels
    # Berechne die prozentualen Anteile
    red_percentage = (red_pixels / (relevantpixels)) * 100
    green_percentage = (green_pixels / (relevantpixels)) * 100
    blue_percentage = (blue_pixels / (relevantpixels))  * 100
    white_percentage = (white_pixels / (relevantpixels)) * 100
    gray_percentage = (gray_pixels / (relevantpixels)) * 100
    black_percentage = (black_pixels / (relevantpixels)) * 100

    return red_percentage, green_percentage, blue_percentage, white_percentage, gray_percentage, black_percentage



def display(image, image_name):
    image = np.array(image, dtype=float)/float(255)
    shape = image.shape
    height = int(shape[0] / 2)
    width = int(shape[1] / 2)
    image = cv2.resize(image, (width, height))
    cv2.namedWindow(image_name)
    cv2.imshow(image_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def to_cut_image(image, h_top, h_bottom, w_left, w_right):
    cut_image = image[h_top:h_bottom, w_left:w_right]
    return cut_image


def contrast_stretch(im):
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom == 0] = 0.01
    # ndvi = (r.astype(float) - b) / bottom
    ndvi = (r.astype(float) - (b)) / bottom  # THIS IS THE CHANGED LINE
    return ndvi



# Öffne die Ausgabedatei
with open(output_file, 'w') as f:
    f.write("Bildname,Rot,Grün,Blau,Weiß,Grau,Schwarz\n")  # Schreibe die Überschriften

    # Schleife durch alle Dateien im Verzeichnis
    for filename in os.listdir(image_directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # Nur Bilddateien berücksichtigen
            # Lade das Bild
            image_path = os.path.join(image_directory, filename)
            image = cv2.imread(image_path)
            # display(original, 'Original')
            # Cutting the size of the image to the only one reference plant pot.
            # 1. test series: h_top =345 h_bottom = 950 w_left = 640 w_right = 1290
            # 2. test series: h_top =365 h_bottom = 925 w_left = 200 w_right = 780
            cut = to_cut_image(image, 390, 950, 120, 700)
            #display(cut, 'Original')
            contrasted = contrast_stretch(cut)
            #display(contrasted, 'Contrasted original')
            cv2.imwrite('contrasted.png', contrasted)
            ndvi = calc_ndvi(contrasted)
            # display(ndvi, 'NDVI')
            ndvi_contrasted = contrast_stretch(ndvi)
            #display(ndvi_contrasted, 'NDVI Contrasted')
            cv2.imwrite('ndvi_contrasted.png', ndvi_contrasted)
            color_mapped_prep = ndvi_contrasted.astype(np.uint8)
            color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
            #display(color_mapped_image, 'Color mapped')
            cv2.imwrite('color_mapped_image.png', color_mapped_image)
            # Berechne die Farbanteile
            red_percentage, green_percentage, blue_percentage, white_percentage, gray_percentage, black_percentage = calculate_color_percentages(color_mapped_image)

            # Schreibe die Werte in die Ausgabedatei
            f.write("{},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}\n".format(filename, red_percentage, green_percentage, blue_percentage, white_percentage,gray_percentage, black_percentage))

    print("Die Werte wurden in '{}' gespeichert.".format(output_file))