''' Fournit des classes utiles à l'étude d'une table de données de trajectométrie.

Définit la classe Person qui décrit une ligne de la base de données.'''

import sqlite3 as sq
import warnings

class Person:
    def __init__(self, cursor, cle=None, tablename="personnes"):
        if cle is None:
            cursor.execute("SELECT * FROM %s LIMIT 1" % tablename)
        else:
            cursor.execute("SELECT * FROM %s WHERE cle = ? LIMIT 1" % tablename, (cle,))
        data = cursor.fetchone()
        if data is None:
            raise LookupError

        self.cle = data[0]
        if not cle is None and self.cle != cle:
            warnings.warn("La clé ne correspond pas à celle spécifiée.")
        self.secteur = data[1]
        self.age = data[2]
        self.redressement = data[3]
        self.occupation = data[4]
        self.times = data[5:]

    def __str__(self):
        return "id=" + str(self.cle)

if __name__ == "__main__":
    _conn = sq.connect('trajecto.db')
    _curs = _conn.cursor()
    p = Person(_curs)
    _curs.close()
    _conn.close()

