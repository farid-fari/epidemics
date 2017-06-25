''' Outil permettant de convertir le format des données de trajectométrie.'''

import sqlite3
import csv

try:
    f = open('trajecto.csv', encoding='ANSI')
except FileNotFoundError:
    raise FileNotFoundError("Le fichier n'existe pas")

cols = f.readline().strip().split(';') # Les étiquettes
cols = [t.replace(":", "") for t in cols] # On enlève les séparateurs des heures
ancien = csv.reader(f, delimiter=";")
nouveau = sqlite3.connect('trajecto_other.db')
curs = nouveau.cursor()

try:
    curs.execute("CREATE TABLE Personnes"
                 " (cle BIGINT PRIMARY KEY, secteur INTEGER, age INTEGER,"
                 " redressement FLOAT, occupation INTEGER,"
                 " '0000' INTEGER,"
                 " '0015' INTEGER,"
                 " '0030' INTEGER,"
                 " '0045' INTEGER,"
                 " '0100' INTEGER,"
                 " '0115' INTEGER,"
                 " '0130' INTEGER,"
                 " '0145' INTEGER,"
                 " '0200' INTEGER,"
                 " '0215' INTEGER,"
                 " '0230' INTEGER,"
                 " '0245' INTEGER,"
                 " '0300' INTEGER,"
                 " '0315' INTEGER,"
                 " '0330' INTEGER,"
                 " '0345' INTEGER,"
                 " '0400' INTEGER,"
                 " '0415' INTEGER,"
                 " '0430' INTEGER,"
                 " '0445' INTEGER,"
                 " '0500' INTEGER,"
                 " '0515' INTEGER,"
                 " '0530' INTEGER,"
                 " '0545' INTEGER,"
                 " '0600' INTEGER,"
                 " '0615' INTEGER,"
                 " '0630' INTEGER,"
                 " '0645' INTEGER,"
                 " '0700' INTEGER,"
                 " '0715' INTEGER,"
                 " '0730' INTEGER,"
                 " '0745' INTEGER,"
                 " '0800' INTEGER,"
                 " '0815' INTEGER,"
                 " '0830' INTEGER,"
                 " '0845' INTEGER,"
                 " '0900' INTEGER,"
                 " '0915' INTEGER,"
                 " '0930' INTEGER,"
                 " '0945' INTEGER,"
                 " '1000' INTEGER,"
                 " '1015' INTEGER,"
                 " '1030' INTEGER,"
                 " '1045' INTEGER,"
                 " '1100' INTEGER,"
                 " '1115' INTEGER,"
                 " '1130' INTEGER,"
                 " '1145' INTEGER,"
                 " '1200' INTEGER,"
                 " '1215' INTEGER,"
                 " '1230' INTEGER,"
                 " '1245' INTEGER,"
                 " '1300' INTEGER,"
                 " '1315' INTEGER,"
                 " '1330' INTEGER,"
                 " '1345' INTEGER,"
                 " '1400' INTEGER,"
                 " '1415' INTEGER,"
                 " '1430' INTEGER,"
                 " '1445' INTEGER,"
                 " '1500' INTEGER,"
                 " '1515' INTEGER,"
                 " '1530' INTEGER,"
                 " '1545' INTEGER,"
                 " '1600' INTEGER,"
                 " '1615' INTEGER,"
                 " '1630' INTEGER,"
                 " '1645' INTEGER,"
                 " '1700' INTEGER,"
                 " '1715' INTEGER,"
                 " '1730' INTEGER,"
                 " '1745' INTEGER,"
                 " '1800' INTEGER,"
                 " '1815' INTEGER,"
                 " '1830' INTEGER,"
                 " '1845' INTEGER,"
                 " '1900' INTEGER,"
                 " '1915' INTEGER,"
                 " '1930' INTEGER,"
                 " '1945' INTEGER,"
                 " '2000' INTEGER,"
                 " '2015' INTEGER,"
                 " '2030' INTEGER,"
                 " '2045' INTEGER,"
                 " '2100' INTEGER,"
                 " '2115' INTEGER,"
                 " '2130' INTEGER,"
                 " '2145' INTEGER,"
                 " '2200' INTEGER,"
                 " '2215' INTEGER,"
                 " '2230' INTEGER,"
                 " '2245' INTEGER,"
                 " '2300' INTEGER,"
                 " '2315' INTEGER,"
                 " '2330' INTEGER,"
                 " '2345' INTEGER)")
except sqlite3.OperationalError:
    raise FileExistsError("La table de données convertie existe déja.")

q = ["?"]*101
q = "(" +  ",".join(q) + ")"

# On prendra garde aux lignes nulles
for k in ancien:
    if k[0]:
        curs.execute("INSERT INTO Personnes VALUES " + q,
                     tuple(k))

curs.execute("SELECT COUNT(*) FROM Personnes")
pers = curs.fetchone()[0]

print(f"{pers} personnes converties.")

nouveau.commit()
curs.close()
nouveau.close()
f.close()
