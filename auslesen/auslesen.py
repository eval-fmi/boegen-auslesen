import sys
import os
import logging

import  auslesen.readOutQuestionaires as readOutQuestionaires

logging.basicConfig(filename=f'{(__file__)[:-3]}.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s', datefmt = "%H:%M-%x")
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

def path_auslesen():
    argv = sys.argv
    # TODO muss in die Extra-Datei auslesen umgelagert werden (mit raise Exc.)
    if len(argv)<2:
        logger.error('Fehlendes Argument.', exec = True)
        exit()
    path = argv[1]
    return path

def path_vorbereiten(path):
    if not os.path.isdir(path):
        logger.error(path + " ist kein Verzeichnis.", exec = True)
    if not path.endswith("/"):
        path += "/"
    return path

def auslesen_starten(path):
    fbs_liste = readOutQuestionaires.fbs_vorbereiten(path)
    fbs_fertig_liste = readOutQuestionaires.phase1_durchfuehren(fbs_liste)
    readOutQuestionaires.daten_speichern(fbs_fertig_liste)

if __name__ == "__main__":
    path = path_auslesen()
    path = path_vorbereiten(path)
    auslesen_starten(path)
