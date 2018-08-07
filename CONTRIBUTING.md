# Contributing

## Setup

### VM

Um das Auslesen zu nutzen, sollte eine VM (Ubuntu 18.4) genutzt werden.
Mittels der `prepareSystem.sh` werden die notwendigen Pakete installiert.

Muss überarbeitet werden:

### Python und Pipenv

- Es wird Python 3 verwendet.
- Paketverwaltung mittels [Pipenv](http://pipenv.readthedocs.io/en/latest/)
    - sollte lokal installiert werden
    - install, uninstall, run, shell sollten bekannt sein
    - Pipfile für neue Setups verwenden

### Workflow

- Die neuste Version wird vom dev-branch geladen
- `pipenv` wird ausgeführt um alle Abhängigkeiten zu lösen und alle benötigten Pakete zu laden.
- mit `pipenv shell` wird die Umgebung gestartet

## Testen

mittels der context.py werden Bibliotheken zum Testen verfügbar gemacht.