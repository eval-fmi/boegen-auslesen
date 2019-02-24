import sys
import os
import logging

import .readOutQuestionaires

logging.basicConfig(filename=f'{(__file__)[:-3]}.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s', datefmt = "%H:%M-%x")
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())


def auslesen_starten():
    argv = sys.argv
    # TODO muss in die Extra-Datei auslesen umgelagert werden (mit raise Exc.)
    if len(argv)<2:
        logger.error('Fehlendes Argument.', exec = True)
        exit()

    path = argv[1]
    if not os.path.isdir(path):
        logger.error(path + " ist kein Verzeichnis.", exec = True)
    if not path.endswith("/"):
        path += "/"

    fbs_liste = readOutQuestionaires.fbs_vorbereiten(path)
    fbs_fertig_liste = readOutQuestionaires.phase1_durchfuehren(fbs_liste)
    readOutQuestionaires.daten_speichern(fbs_fertig_liste)

if __name__ == "__main__":
    auslesen_starten()
