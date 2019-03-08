"""
    Mit diesem Modul werden die pytesseract-Funktionen zur Verfügung gestellt
    Dieses Modul wurde nur erstellt, damit hier, bei einer Windows installation
    der Pfad zur *tesseract.exe* hinzugefügt werden kann und damit im ganzen 
    Projekt die Benutzung kosistent ist. Daher sind hier die Funktionsnamen auch
    Englisch. So kann das ganze auch getestet werden
""" 
import pytesseract
# Dabe muss unter Windows noch folgendes gemacht werden,
# falls tesseract nicht in Path liegt:
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

def image_to_string(bild, sprache):
    """
        gibt den Text in einem Bild als String zurück
        bei Problemen, bitte bei pytesseract.image_to_string gucken
    """
    return pytesseract.image_to_string(bild, sprache)
