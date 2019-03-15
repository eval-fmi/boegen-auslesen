import sys
import os
import logging

from auslesen.readOutQuestionaires import fbs_vorbereiten, phase1_durchfuehren, daten_speichern

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
    # if not path.endswith("/"):
    #    path += "/"
    return path

def auslesen_starten(path):
    fbs_liste = fbs_vorbereiten(path)
    fbs_fertig_liste = phase1_durchfuehren(fbs_liste)
    daten_speichern(fbs_fertig_liste)

if __name__ == "__main__":
    path = "D://Eval//Ergebnisse_2018-24_1-50//"
    path = path_vorbereiten(path)
    auslesen_starten(path)
