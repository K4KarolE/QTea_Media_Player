'''
THIS FILE CAN BE REACHED OUTSIDE THE APP ONLY

It contains supporting functions only,
which can be actioned in this file for:
    - Verify the tables available in the DB
    - Creating new DB
    - Remove a table from the DB
'''

import sqlite3
from pathlib import Path
from json import load, dump

def open_json():
    with open(PATH_JSON_SETTINGS) as f:
        json_dic = load(f)
    return json_dic

def save_json():
    with open(PATH_JSON_SETTINGS, 'w') as f:
        dump(settings, f, indent=2)
    return


PATH_JSON_SETTINGS = Path(Path().resolve().parent, 'settings.json')
settings = open_json()

""" OS related databases for ease of switching between multiple OS`
    More information in the README
"""
connection_linux = sqlite3.connect('../playlist_db_linux.db')
sql_cur_linux = connection_linux.cursor()

connection_win = sqlite3.connect('../playlist_db_win.db')
sql_cur_win = connection_win.cursor()


def list_all_tables(cur, connection):
    cur.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
    for playlist in cur.fetchall():
        print(playlist)
    connection.close()
# list_all_tables(sql_cur_linux, connection_linux)


def create_tables(playlists_amount = 30):
    """ Creates new DB and updates settings.json
        Rename or delete the previous DB before
        executing the function
    """
    settings['playlists'] = {}

    for i in range(0, playlists_amount):
        table_name = f'playlist_{i}'

        ''' SQL '''
        sql_cur_win.execute("""CREATE TABLE {0}
                    (
                    row_id INTEGER PRIMARY KEY,
                    duration VARCHAR,
                    current_duration VARCHAR, 
                    path TEXT
                    )
                    """.format(table_name))


        sql_cur_linux.execute("""CREATE TABLE {0}
                            (
                            row_id INTEGER PRIMARY KEY,
                            duration VARCHAR,
                            current_duration VARCHAR, 
                            path TEXT
                            )
                            """.format(table_name))

        ''' JSON '''
        settings['playlists'][table_name] = {
            "playlist_title": str(i + 1),
            "playlist_index": i,
            "last_track_index": 0
            }

    connection_win.close()
    connection_linux.close()
    save_json()

# create_tables()



def remove_table(cur, connection, table_name):
    cur.execute("""DROP TABLE IF EXISTS {0}""".format(table_name))
    connection.close()
# remove_table(sql_cur_linux, connection_linux, 'playlist_12')