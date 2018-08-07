# Log

## 04.01.2018

Eval Software

Der folgende Link repräsentiert eine typische Veranstaltungsseite so wie sie hoffentlich heruntergeladen werden kann: 
https://friedolin.uni-jena.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=138462&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung 

Zu beachten ist dabei dass die Nummer 13 8462 veranstaltungsnummer ist alles andere bleibt selbst wenn ich andere Veranstaltung betrachte gleich könnt ich kotzen aufpassen bei unbekannten chatten das muss noch angepasst und verbessert werden nein habe ich nicht okay habe ich denn möglicherweise bleiben komische Zeichen zurück die vor dem inside weitersenden sowas steht aber ich habe keine Ahnung wo die herkommen ok könnte ich kotzen könnte ich da hau 
Holy fuk es hat funktioniert auch wenn ich nicht in der Lage bin mich bei Michael ein zu loggen kann ich wenn ich im Browser aktiviert bin hoffe ich Daten aus der Datenbank herunterladen. 
Dieser Link stimmt was nicht stimmt
https://eval.fmi.uni-jena.de/phpmyadmin/server_export.php?db=&table=&server=1&target=&token=36afa92942a738fc6b5a3a8d206ae927#Export-format

geht doch nicht :(

## 06.01.2018

Wie man für einen vorhandene Benutzer etwas freischaltet: 

Die fertigen Ergebnisse liegen unter webhome File Dozentenname dort fanden kann dann auf sie zugegriffen werden 

Einzelne Veranstaltungen der Datenbank hinzufügen: 

Bisher funktioniert das einzeln hinzufügen von Fridolin Veranstaltung über Test Fang das wird hierbei später noch ändern. 
Das ist momentan nur ein quick fix. Zuerst wird die dozentenliste und die Modulliste aus der SQL Datenbank als JSON heruntergeladen. Sie werden dann an der entsprechenden Stelle positioniert. In een müssen die Kommentare ganz oben entfernt werden. Den TestFunc müssen dann die einzelnen Veranstaltungen ganz unten in die Modulliste eingefügt werden.  Die importfunktion funktioniert nicht man muss also auf die Datenbank eval FME klicken und dann dort auf SQL kopiert man dann den Text dort rein drückt auf gomme das was man möchte. Aufpassen bei Dozenten die bereits vorhanden sind diese können nicht eingefügt werden müssen manuell entfernt werden momentan.