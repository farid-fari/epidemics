''' Fournit des classes utiles à l'étude d'une table de données de trajectométrie.

Définit la classe Person qui décrit une ligne de la base de données.'''

import sqlite3 as sq
import warnings

MAP = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
       121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140,
       141, 142, 143, 201, 202, 203, 204, 205, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312,
       313, 314, 401, 402, 403, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515,
       516, 517, 518, 519, 601, 602, 603, 701, 801, 802, 803, 804, 805, 806, 901, 902, 903, 990]

TIMES = [0, 15, 30, 45, 100, 115, 130, 145, 200, 215, 230, 245, 300, 315, 330, 345, 400, 415, 430, 445, 500,
         515, 530, 545, 600, 615, 630, 645, 700, 715, 730, 745, 800, 815, 830, 845, 900, 915, 930, 945, 1000,
         1015, 1030, 1045, 1100, 1115, 1130, 1145, 1200, 1215, 1230, 1245, 1300, 1315, 1330, 1345, 1400, 1415,
         1430, 1445, 1500, 1515, 1530, 1545, 1600, 1615, 1630, 1645, 1700, 1715, 1730, 1745, 1800, 1815, 1830,
         1845, 1900, 1915, 1930, 1945, 2000, 2015, 2030, 2045, 2100, 2115, 2130, 2145, 2200, 2215, 2230, 2245,
         2300, 2315, 2330, 2345]

class Person:
    ''' Crée un objet Person facilement manipulable en lisant la base de données
        donnée par cursor afin de récupérer la clé demandée.'''
    def __init__(self, cursor, cle=None):
        '''cursor (sqlite.Cursor): le curseur pointant sur la base de données à quérir
           cle (int/str): la clé de la personne en question'''
        if cle is None:
            cursor.execute("SELECT * FROM Personnes LIMIT 1")
        else:
            cursor.execute("SELECT * FROM Personnes WHERE cle = ? LIMIT 1", (str(cle),))
        data = cursor.fetchone()
        if data is None:
            raise LookupError
        # On profite des entiers de taille arbitraire, BIGINT en SQL
        self.cle = int(data[0])
        if not cle is None and self.cle != cle:
            warnings.warn("La clé ne correspond pas à celle spécifiée.")
        self.secteur = int(data[1])
        self.age = int(data[2])
        self.redressement = float(data[3])
        self.occupation = int(data[4])
        self.positions = []
        # On récupére les 96 horaires et positions
        for h in cursor.execute("SELECT endroit FROM Positions WHERE cle=? ORDER BY heure ASC LIMIT 100", (self.cle,)):
            self.positions.append(h[0])

    def __str__(self):
        return "id=" + str(self.cle) + "\nsecteur=" + str(self.secteur) + "\npositions=" + str(self.positions)

class Secteur:
    '''Gère un secteur entier composé de Persons.'''
    def __init__(self, cursor, secteur=101, verbose=True):
        '''cursor (sqlite.Cursor): le curseur pointant sur la base de données à quérir
           secteur (int): le numéro de secteur à indexer
           verbose (bool) s'il faut notifier du chargement'''
        if verbose:
            print("Chargement du secteur", secteur, "...")
        cursor.execute("SELECT * FROM Personnes WHERE secteur = ?", (secteur,))
        self.code = secteur
        self.people = {}
        for k in cursor.fetchall():
            self.people[k[0]] = Person(cursor, k[0])
        self.nombre = len(self.people)

    def __str__(self):
        return "code=" + str(self.code) + "\nnombre=" + str(self.nombre)

if __name__ == "__main__":
    _conn = sq.connect('trajecto_nouv.db')
    _curs = _conn.cursor()
    p = Person(_curs)
    print(p)

    print("---")

    # Peut prendre un bout de temps
    s = Secteur(_curs, 101)
    print(s)
    _curs.close()
    _conn.close()
