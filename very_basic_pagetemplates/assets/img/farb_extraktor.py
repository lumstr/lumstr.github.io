{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import csv\
import os\
from PIL import Image\
import extcolors\
\
def rgb_to_hex(rgb):\
    return "#\{:02x\}\{:02x\}\{:02x\}".format(rgb[0], rgb[1], rgb[2])\
\
def rgb_to_cmyk(rgb):\
    r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0\
    k = 1.0 - max(r, g, b)\
    if k == 1.0:\
        return 0, 0, 0, 100\
    c = (1.0 - r - k) / (1.0 - k)\
    m = (1.0 - g - k) / (1.0 - k)\
    y = (1.0 - b - k) / (1.0 - k)\
    return int(c * 100), int(m * 100), int(y * 100), int(k * 100)\
\
csv_file = "farbcodes_bilder.csv"\
valid_extensions = (".jpg", ".jpeg", ".png", ".webp", ".bmp")\
\
print("Starte Farbanalyse...")\
\
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:\
    writer = csv.writer(file, delimiter=";")\
    writer.writerow(["Bildname", "HEX", "RGB", "CMYK (C-M-Y-K)"])\
\
    for datei in sorted(os.listdir(".")):\
        if datei.lower().endswith(valid_extensions):\
            try:\
                img = Image.open(datei)\
                img.thumbnail((150, 150))\
                colors, _ = extcolors.extract_from_image(img, tolerance=20, limit=1)\
                if colors:\
                    dominant_rgb = colors[0][0]\
                    hex_code = rgb_to_hex(dominant_rgb)\
                    cmyk_vals = rgb_to_cmyk(dominant_rgb)\
                    cmyk_str = f"\{cmyk_vals[0]\}-\{cmyk_vals[1]\}-\{cmyk_vals[2]\}-\{cmyk_vals[3]\}"\
                    rgb_str = f"\{dominant_rgb[0]\},\{dominant_rgb[1]\},\{dominant_rgb[2]\}"\
                    writer.writerow([datei, hex_code, rgb_str, cmyk_str])\
                    print(f"Erfolgreich analysiert: \{datei\}")\
            except Exception as e:\
                print(f"Fehler bei Datei \{datei\}: \{e\}")\
\
print(f"\\nFertig! Die Tabelle wurde als '\{csv_file\}' im Ordner gespeichert.")}