import unittest
import inspect
import os
import logging
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageTk 

logging.basicConfig(filename=f'{(__file__)[:-3]}.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s', datefmt = "%H:%M-%x")
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

import auslesen.readOutQuestionaires as readOutQuestionaires
import auslesen.boegen_vorbereiten as vorbereiten

class EvalTest(unittest.TestCase):

    def test_testordner(self):
        """
            gibt den Pfad zum Testordner zurück, in dem sich auch die Testbögen
            befinden.
        """
        root = Path(os.path.abspath(__file__))
        print(root)
        test_ordner = root.parent /'test_Boegen'
        return test_ordner

class AuslesenTest(EvalTest):
        
    def test_frageboegen_lesen(self):

        testordner = self.test_testordner()
        testordner = str(testordner.resolve())
        fbs_liste = readOutQuestionaires.fbs_vorbereiten(testordner)
        print("vorbereitung abgeschlossen")
        fbs_fertig_liste = readOutQuestionaires.phase1_durchfuehren(fbs_liste)
        print("phase1 durchgeführt")
        readOutQuestionaires.daten_speichern(fbs_fertig_liste)
        print("alle daten gespeichert")


class BoegenVorbereiten(EvalTest):
    """ testet alle Funktionen, die den Bogen vorbereiten, bevor er ausgewertet
        werden kann. """ 

    def setUp(self):
        """ 
            in dieser Methode werden alle wichtigen Imports getätigt und 
            die restlichen Testfälle werden vorbereitet
        """
        # Imports
        import os
        
        import numpy as np
        from numpy import linalg as LA
        from numpy import array, dot, arccos, pi
        from PIL import Image, ImageDraw, ImageFilter, ImageTk 

    def test_bild_vorbereiten(self):
        # Bild bearbeiten 1 (im = Image, fb = Fragebogen)
        testordner = self.test_testordner()
        test_bild_name = "42_0001.tif"
        test_bild_pfad = testordner / "42" / test_bild_name 
        # testordner = str(testordner.resolve())
        im = Image.open(test_bild_pfad)
        a,b = im.size
        im_schwarz_weiß = im.convert("1", dither = None)
        im_gefiltert = im_schwarz_weiß.filter(ImageFilter.MedianFilter(5))
        fb = im_gefiltert.load()

        # stellt die Schrittweite ein, in der nach den Ecken gesucht wird
        sum = 0
        stepx = 5
        stepy = 10
        # Zum anzeigen verwendet
        pic = []
        # das Dokument wird durchgegangen und auf die Farbwerte überprüft einzelnen
        for i in range(0,a,stepx):
            x = []
            for j in range (0,b,stepy):
                if fb[i,j] == 0:
                    x.append("B")
                elif fb[i,j] == 255:
                    x.append(" ")
                else:
                    x.append("?")
                sum += fb[i,j]
            pic.append(x)  

        # überprüft, ob der Bogen leer ist

        # es ist unklar, ob der Bogen leer ist, deshalb wird
        # nochmal genauer getestet

        if sum*stepx*stepy/(a*b)>252:
            sum=0
            for i in range(0,a):
                for j in range (0,b):
                    sum += fb[i,j]
            if sum/(a*b)>254: 
                print("empty")

    def test_phase1(self):
        """
            testet, ob die phase1 korrekt funktioniert.
            momentan wird es vorallem zum Debuggen verwendet.
        """
        testordner = self.test_testordner()
        test_bild_name = "42_0001.tif"
        test_bild_pfad = testordner / "42" / test_bild_name
        vorbereitet_liste = vorbereiten.phase1(test_bild_pfad)
        print(vorbereitet_liste)

import auslesen.my_tesseract as tesseract

class TesseractTest(EvalTest):
    """ testet, ob das Tesseract-Modul angemessen funktioniert"""
    
    def test_lese_vorlesung(self):

        testordner = self.test_testordner()
        test_bild_name = "42_0001.tif.crop"
        test_bild_pfad = testordner / "42" / test_bild_name
        im = Image.open(test_bild_pfad)
        test_string = vorbereiten.typ_des_fbs(im)
        # self.assertEquals("- Fragebogen für Vorlesungen -", test_string)
        self.assertEqual("Vorlesung1", test_string)
if __name__ == '__main__':
    unittest.main()