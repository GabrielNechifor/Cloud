
import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        query = '''
                drop table if exists anime;
                '''
        cursor.execute(query)
        

        query = '''create table anime
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                episodes INTEGER
                );
                '''
        cursor.execute(query)


        query = "insert into anime values (null, 'Gurren Lagann', 27);"
        cursor.execute(query)

        query = "insert into anime values (null, 'Death Note', 37);"
        cursor.execute(query)

        conn.commit()


    except Error as e:
        print(e)
    finally:
        if conn:
            cursor.close()
            conn.close()
 
 
if __name__ == '__main__':
    create_connection("database.db")