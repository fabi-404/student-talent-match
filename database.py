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
    if os.path.exists(database):
        os.remove(database)
        print(f"Bestehende Datenbank {database} wurde entfernt.")
    
    conn = get_db_connection()
    
    # liest schema.sql aus und führt es aus
    with open('schema.sql') as f:
        conn.executescript(f.read())
        
    conn.commit()
    conn.close()
    print("Neue Datenbank wurde mit allen Tabellen erstellt.")

if __name__ == '__main__':
    init_db()