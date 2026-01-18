import sqlite3
import os

database= 'student_talent.db'

def get_db_connection():

    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    #Aktiviert den Fremdschlüssel für die Beziehung zwischen Tabellen.
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    if not os.path.exists(database):
        # Nur erstellen, wenn sie noch NICHT existiert
        conn = get_db_connection()
        with open('schema.sql') as f:
            conn.executescript(f.read())
        
        conn.commit()  # <--- HIER WAR ES WICHTIG
        conn.close()
        print("Neue Datenbank wurde erstellt.")

    else:
        print("Datenbank existiert bereits - keine Änderungen vorgenommen.")

if __name__ == '__main__':
    init_db()