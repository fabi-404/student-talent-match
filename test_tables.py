from database import get_db_connection

def check ():
    try:
        conn = get_db_connection()
        
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        
        print("\n Datenbank-Check")
        if not tables:
            print("Keine Tabellen in der Datenbank gefunden.")
        else:
            print("Tabellen in der Datenbank:")
            for table in tables:
                if table['name'] != 'sqlite_sequence':
                    print(f" - {table['name']}")
                
    except Exception as e:
        print(f"git add check_tables.py Verbindung fehlgeschlagen: {e}")

if __name__ == '__main__':
    check()
         