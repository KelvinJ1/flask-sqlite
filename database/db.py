import sqlite3
import _sqlite3
#connection to database

def get_connection():
    try:
        con= sqlite3.connect("database\DB.db")

    except sqlite3.error as ex:
        raise  ex #also print() 
    return con
            