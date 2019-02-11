# Dokumentation zum Auslesen von Eval-Bögen

## System vorbereiten

Benötigt wird ein Ubuntu-System(18.4 geht) mit root-Rechten. dort muss das Skript `Eval-Auslesen/scripts/prepareSystem` ausgeführt werden, um die notwendigen Pakete herunterzuladen.

## Ordner vorbereiten

Nachdem die Bilder auf dem USB-Stick sind, werden sie in einem Ordner gespeichert, der als Name die Nummer der Veranstaltung trägt. Diese Ordner werden dann in einem gemeinsamen Ordner gesammelt, auf dem das auslesen-Skript ausgeführt wird. Um die Bilder nicht per Hand einsortieren zu müssen, kann hier ein Skript verwendet werden.

- Das Skript structureSystem.sh wurde auf die Scans angewendet und führt dazu, dass die gescannten Bögen vom Programm richtig erkannt wird

## Bilder (der Bögen) auslesen

Um die Daten der Bilder auszulesen, verwenden wir unser eval_neu.vhmi, welches mittels dem Progamm [Virtualbox](https://www.virtualbox.org/) als Festplatte eingebunden werden kann.
TODO: einstellungen für Virtualbox mit aufnehmen.
Mehr dazu dann in der Dokumentation vom Auslesen. Aber es muss `readQuestionary.py` auf den oben erstellten Ordner aufgeführt werden,in dem alle Vorlesungen enthalten sind.

## Daten in SQL-Datenbank übertragen

Die Daten der Bilder werden durch das Programm in ergs.txt im Bilder-Ordner gespeichert. Mittels des Skriptes `orderErgs.py` werden die Daten dann sortiert, bevor sie mittels des Skriptes `ergsToSQL.py` in sql-Code umgewandelt werden. Der SQL-Code wird in der Datei `ergs.sql` gespeichert.

- Bisher gibt es Probleme dabei, dass die ergs.txt Fehler enthällt. mehr dazu im gitlab. Daher muss die Datei bisher nachgearbeitet werden. Für die Suche kann die folgende Regex verwendet werden `^[0-9]+;[0-9]+;39,.*\n^^[0-9]+;[0-9]+;1,.*`