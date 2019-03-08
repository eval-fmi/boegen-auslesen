import auslesen.auslesen as auslesen

if __name__ == "__main__":
    path = auslesen.path_auslesen()
    path = auslesen.path_vorbereiten(path)
    auslesen.auslesen_starten(path)