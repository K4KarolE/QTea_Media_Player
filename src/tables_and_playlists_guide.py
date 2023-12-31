
from cons_and_vars import cv, settings, PATH_JSON_SETTINGS, save_json

import sqlite3

connection = sqlite3.connect('playlist.db')
cur = connection.cursor()


''' CURRENT TABLES / PLAYLISTS '''
def list_all_tables():
    cur.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
    print(cur.fetchall())
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
                    path TEXT(20)
                    )
                    """.format(table_name))
        
        ''' JSON '''
        settings[table_name] = {
            "tab_index": i,
            "tab_title": str(i + 1),
            "last_track_index": 0
            }
    save_json(settings, PATH_JSON_SETTINGS)
# create_tables()


''' REMOVE TABLE / PLAYLIST '''
def remove_table(table_name):
    cur.execute("""DROP TABLE IF EXISTS {0}""".format(table_name))
# remove_table('playlist_12')


connection.close()

