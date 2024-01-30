'''
THIS FILE CAN BE REACHED OUTSIDE THE APP ONLY

It contains supporting functions only,
which can be run in this file and
which can be used to:
    - Verify the tables availble in the DB
    - Creating new DB
    - Remove a table from the DB
'''

from cons_and_vars import cv, settings, PATH_JSON_SETTINGS, save_json

import sqlite3

connection = sqlite3.connect('playlist.db')
cur = connection.cursor()


''' CURRENT TABLES / PLAYLISTS '''
def list_all_tables():
    cur.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
    for playlist in cur.fetchall():
        print(playlist)
    connection.close()
# list_all_tables()


''' CREATE TABLES / PLAYLISTS '''
def create_tables():

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
    save_json(settings, PATH_JSON_SETTINGS)

create_tables()


''' REMOVE TABLE / PLAYLIST '''
def remove_table(table_name):
    cur.execute("""DROP TABLE IF EXISTS {0}""".format(table_name))
    connection.close()
# remove_table('playlist_12')