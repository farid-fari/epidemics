''' Fournit des classes utiles à l'étude d'une table de données de trajectométrie.

Définit la classe Person qui décrit une ligne de la base de données.'''

import sqlite3 as sq
import warnings

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
    def __init__(self, cursor, secteur=101):
        '''cursor (sqlite.Cursor): le curseur pointant sur la base de données à quérir
           secteur (int): le numéro de secteur à indexer'''
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
