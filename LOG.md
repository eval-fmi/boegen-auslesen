# Log

## 04.01.2018

Eval Software

Der folgende Link repräsentiert eine typische Veranstaltungsseite so wie sie hoffentlich heruntergeladen werden kann:
`https://friedolin.uni-jena.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=138462&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung`

Zu beachten ist dabei dass die Nummer 13 8462 veranstaltungsnummer ist alles andere bleibt selbst wenn ich andere Veranstaltung betrachte gleich könnt ich kotzen aufpassen bei unbekannten chatten das muss noch angepasst und verbessert werden nein habe ich nicht okay habe ich denn möglicherweise bleiben komische Zeichen zurück die vor dem inside weitersenden so etwas steht aber ich habe keine Ahnung wo die herkommen ok könnte ich kotzen könnte ich da hau
Holy fuk es hat funktioniert auch wenn ich nicht in der Lage bin mich bei Michael ein zu loggen kann ich wenn ich im Browser aktiviert bin hoffe ich Daten aus der Datenbank herunterladen.
Dieser Link stimmt was nicht stimmt
`https://eval.fmi.uni-jena.de/phpmyadmin/server_export.php?db=&table=&server=1&target=&token=36afa92942a738fc6b5a3a8d206ae927#Export-format`

geht doch nicht :(

## 06.01.2018

Wie man für einen vorhandene Benutzer etwas freischaltet:

Die fertigen Ergebnisse liegen unter `.webhome` File Dozentenname dort fanden kann dann auf sie zugegriffen werden

Einzelne Veranstaltungen der Datenbank hinzufügen:

Bisher funktioniert das einzeln hinzufügen von Fridolin Veranstaltung über Test Fang das wird hierbei später noch ändern.
Das ist momentan nur ein quick fix. Zuerst wird die dozentenliste und die Modulliste aus der SQL Datenbank als JSON heruntergeladen. Sie werden dann an der entsprechenden Stelle positioniert. In een müssen die Kommentare ganz oben entfernt werden. Den TestFunc müssen dann die einzelnen Veranstaltungen ganz unten in die Modulliste eingefügt werden.  Die importfunktion funktioniert nicht man muss also auf die Datenbank eval FMI klicken und dann dort auf SQL kopiert man dann den Text dort rein drückt auf go das was man möchte. Aufpassen bei Dozenten die bereits vorhanden sind diese können nicht eingefügt werden müssen manuell entfernt werden momentan.

## 08.08.18

### System für das Auslesen aufsetzen

Es wurde mit VirtualBox eine vhd-Datei (Eval_neu.vhd) erstellt, auf dem ein Ubuntu 18.4 Image draufgespielt wurde.  
Als Tastaturlayout wird Neo2 gewählt benutzername Passwort sind beides "eval". Ich mache dabei eine minimale installation
[gastmodus muss aktiviert werden](https://help.ubuntu.com/community/VirtualBox/SharedFolders)
[pic-1]
Der Benutzer [muss zur Gruppe hinzugefügt werden](https://stackoverflow.com/questions/26740113/virtualbox-shared-folder-permissions) um den gemeinsamen Ordner zu verwenden:
`sudo adduser $USER vboxsf`

Damit alle notwendigen Pakete installiert werden nutze ich das Skript prepareSystem.sh

Damit die Dokumente richtig ausgelesen werden können müssen Sie vorher vorbereitet werden. Dafür gibt es verschiedene Skripte einziger Grill Skripte ist für den schwarzen sturer Scanner.

Dafür benutzen wir pdf2image. Das haben wir [hier](https://stackoverflow.com/questions/46184239/python-extract-a-page-from-a-pdf-as-a-jpeg) gefunden

## 09.08.18

`https://github.com/python-pillow/Pillow/issues/2609`

Ich sollte definitiv tiff ausprobieren. JPG scheint nicht zu funktionieren :-(

Ich habe PhantomPDF heruntergeladen um die PDFs als Tiff-Dateien zu extrahieren.
Ich habe die Pdfs auch extrahiert. dabei muss jedoch bei dem Umbenennen darauf geachtet werden, dass *NummerDerVeranstaltung*.Page*NummerDerSeite* als Format angenommen wird und somit mal *000* und mal *00* für *Page* ersetzt werden muss.
Auch mit Tiff-Dateien funktioniert es nicht, die Dateien auszulesen.

## 10.08.18

Das Skript structureScans_alex.py wurde erstellt und ist für die Einordnung der Bilderdateien verantwortlich.
Das Skript wurde auf den Ordner mit den Bilddateien ausgeführt.
Nach einigen Änderung im Code wurden alle Bilder durchgearbeitet.

## 11.08.2018

Die Daten aus den bisher vorhandenen Bögen wurden ausgelesen. Es fehlen allerdings noch einige. Die Daten wurden auch in die Datenbank mit übertragen.
