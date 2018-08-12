#!/usr/bin/python3
"""
Wie ist dieses Skript zu nutzen?

Dieses Skript wird auf den Ordner ausgeführt, indem alle Bilddateien der Eval-Bögen enthalten sind.
In diesem liegen die Bilder in der Form "Nummer der Vorlesung"_"Seite". Seite ist dabei eine 4 stellige Zahl.
Bsp.: 112_0002.tif, 11_0034.tif, 23_0123.jpg, etc. .
Dieser Code sortiert die Bilder in Ordner, die als Namen die Nummer der Vorlesung haben.
"""
from pdf2image import convert_from_path
from sys import argv
from os import walk, path, makedirs, rename, mkdir

# pages = convert_from_path('pdf_file', 500)
# Saving pages in jpeg format

# for idx,item in enumerate(pages):
 #    page.save('out.jpg', 'JPEG')

def create_folders_and_move_files():
    for root, dirs, files in walk("."):
        for file_name in files:
            try:
                folder_name = file_name[:-9]
                if not path.exists(folder_name):
                    mkdir(folder_name)
                print(f"create {folder_name}")

                file_path = path.join(root, file_name)
                folder_path = path.join(root, folder_name)
                rename(file_path, path.join(folder_path, file_name))
                print(f"move{file_name}")
            except OSError:
                print ('Error: Creating directory. ' +  folder_name)


if __name__ == "__main__":
    create_folders_and_move_files()
    