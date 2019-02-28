import unittest
import inspect
import os
import logging
from pathlib import Path

logging.basicConfig(filename=f'{(__file__)[:-3]}.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s', datefmt = "%H:%M-%x")
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

import auslesen.readOutQuestionaires as readOutQuestionaires

class AuslesenTest (unittest.TestCase):

    def test_testordner(self):

        root = Path(os.path.abspath(__file__))
        print(root)
        test_ordner = root.parent /'test_Boegen'
        return test_ordner
        
    def test_frageboegen_lesen(self):

        testordner = self.test_testordner()
        testordner = str(testordner.resolve())
        fbs_liste = readOutQuestionaires.fbs_vorbereiten(testordner)
        print("vorbereitung abgeschlossen")
        fbs_fertig_liste = readOutQuestionaires.phase1_durchfuehren(fbs_liste)
        print("phase1 durchgeführt")
        readOutQuestionaires.daten_speichern(fbs_fertig_liste)
        print("alle daten gespeichert")

if __name__ == '__main__':
    unittest.main()