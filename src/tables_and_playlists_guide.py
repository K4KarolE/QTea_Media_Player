'''
THIS FILE CAN BE REACHED OUTSIDE THE APP ONLY

It contains supporting functions only,
which can be actioned in this file for:
    - Verify the tables availble in the DB
    - Creating new DB
    - Remove a table from the DB
'''

import sqlite3
from src.class_data import (
    cv,
    settings,
    save_json
    )


connection = sqlite3.connect('playlist.db')
cur = connection.cursor()


def list_all_tables():
    cur.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
    for playlist in cur.fetchall():
        print(playlist)
    connection.close()
# list_all_tables()


def create_tables():
    ''' Creates new DB and updates settings.json '''
    for i in range(0, cv.playlist_amount):
        table_name = f'playlist_{i}'

        ''' SQL '''
        cur.execute("""CREATE TABLE {0}
                    (
                    row_id INTEGER PRIMARY KEY,
                    duration VARCHAR(20),
                    current_duration VARCHAR(20), 
                    path TEXT(20)
                    )
                    """.format(table_name))

        ''' JSON '''
        settings[table_name] = {
            "playlist_title": str(i + 1),
            "playlist_index": i,
            "last_track_index": 0
            }
        
    connection.close()
    save_json()

create_tables()



def remove_table(table_name):
    cur.execute("""DROP TABLE IF EXISTS {0}""".format(table_name))
    connection.close()
# remove_table('playlist_12')