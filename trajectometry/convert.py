''' Outil permettant de convertir le format des données de trajectométrie.'''

import sqlite3
import csv
import warnings

try:
    f = open('trajecto.csv', encoding='ANSI')
except FileNotFoundError:
    raise FileNotFoundError("Le fichier n'existe pas")

cols = f.readline().strip().split(';') # Les étiquettes
cols = [t.replace(":", "") for t in cols] # On enlève les séparateurs des heures
ancien = csv.reader(f, delimiter=";")
nouveau = sqlite3.connect('trajecto.db')
curs = nouveau.cursor()

try:
    curs.execute("CREATE TABLE Personnes (cle BIGINT PRIMARY KEY, secteur INTEGER, age INTEGER, redressement FLOAT, occupation INTEGER)")
    curs.execute("CREATE TABLE Positions (id INTEGER PRIMARY KEY AUTOINCREMENT, cle BIGINT, heure INTEGER, endroit INTEGER, FOREIGN KEY(cle) REFERENCES Personnes(cle))")
except sqlite3.OperationalError:
    raise FileExistsError("Les tables de données converties existent déja.")

# On prendra garde aux lignes nulles
for k in ancien:
    # On insère d'abord la personne afin de vérifier la FOREIGN KEY
    curs.execute("INSERT INTO Personnes (cle, secteur, age, redressement, occupation) VALUES (?,?,?,?,?)", (k[0], k[1], k[2], k[3], k[4]))
    # Ce sont les noms de colonnes des heures
    heures = [int(x) for x in cols[5:]]
    for i, j in enumerate(k[5:]):
        curs.execute("INSERT INTO Positions (cle, heure, endroit) VALUES (?,?,?)", (k[0], heures[i], j))

curs.execute("SELECT COUNT(*) FROM Personnes")
pers = curs.fetchone()[0]

curs.execute("SELECT COUNT(*) FROM Positions")
pos = curs.fetchone()[0]

if 96*pers == pos:
    print(f"{pers} personnes converties ({pos} positions).")
    # Les personnes ne sont pas littéralement converties
else:
    warnings.warn(f"{pers} personnes converties mais {pos} positions, au lieu de {96*pers} (delta: {abs(96*pers-pos)}).")

nouveau.commit()
curs.close()
nouveau.close()
f.close()
