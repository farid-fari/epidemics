''' Outil permettant de convertir le format des données de trajectométrie.'''

import sqlite3 as sq

ancien = sq.connect('trajecto.db')
nouveau = sq.connect('trajecto_nouv.db')
ca = ancien.cursor()
cn = nouveau.cursor()

try:
    cn.execute("CREATE TABLE Personnes (cle BIGINT PRIMARY KEY, secteur INTEGER, age INTEGER, redressement FLOAT, occupation INTEGER)")
    cn.execute("CREATE TABLE Positions (id INTEGER PRIMARY KEY AUTOINCREMENT, cle BIGINT, heure INTEGER, endroit INTEGER, FOREIGN KEY(cle) REFERENCES Personnes(cle))")
except sq.OperationalError:
    raise FileExistsError("Les tables de données convertie existe déja.")

for k in ca.execute("SELECT * FROM donnees"):
    cn.execute("INSERT INTO Personnes (cle, secteur, age, redressement, occupation) VALUES (?,?,?,?,?)", (k[0], k[1], k[2], k[3], k[4]))
    heures = [int(x[0]) for x in ca.description[5:]]
    for i, j in enumerate(k[5:]):
        cn.execute("INSERT INTO Positions (cle, heure, endroit) VALUES (?,?,?)", (k[0], heures[i], j))

ancien.commit()
nouveau.commit()
ca.close()
cn.close()
ancien.close()
nouveau.close()
