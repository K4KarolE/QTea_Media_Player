# QTea Media Player
- The media player supports twenty playlists at the same time. Inspired by `Winamp` and `VLC media player`. 

<div align="left">
    <img src="docs/promo/screenshot_0.png">
</div>
<br>
<div align="left">
    <img src="docs/promo/screenshot_1.png">
</div>
<br>
<div align="left">
    <img src="docs/promo/screenshot_2.png">
</div>
<br>
<div align="left">
    <img src="docs/promo/screenshot_3.png">
</div>
<br>

## Buttons under playlists section
- `AT - Add Track`: add a single media/file to the playlist
- `AD - Add Directory`: adding all the media files listed in the selected directory and subdirectories
- `RT - Remove Track`: removes the current/selected track
- `CP - Clear Playlist`: removes all the items from the current playlist
- `Settings button`: opens the `Settings window`, where the user:
    - Able to update the playlists titles - hide/show the playlists
    - Adjust the shortcut keyboard values (work in progress)
    - Adjust the player's jump values (work in progress)

## Settings
### Playlist management
- Twenty playlists are available by default. To create playlists beyond the default amount, please see next section.
- In the `Settings window / Playlists` tab all the available playlists are listed
    - To make a playlist visible:
        - Add a title to the playlist
        - If the playlist will be used the first time: empty playlist will be displayed after restart
        - If playlist had tracks before it was hidden: the records will be loaded automatically after restart
    - To hide a playlist:
        - Remove the title of the playlist
        - Playlists without a title will be hidden after restart
        - At least one of the playlist remains visible - not able to remove all the playlist titles
        - The hidden playlist's records/media information remains in the database
- Add/remove tracks: the current playlist is saved automatically
- At startup all playlists loading automatically
    - The last played track's playlist will be active/selected
    - The last played track will be selected

## Steps to increase the number of playlists beyond the default / to generate new playlist database
- The `Settings window` tabs are not scrollable, which put a limitation on how much playlists will be visible on the `Settings window / Playlist` tab
1. Review how much space the `Settings window` occupies of your screen
2. Change the `src / settings_window.py / WINDOW_HEIGHT ` value to your screen height
3. Rename the current playlist database: `playlist.db`
4. In the `src / cons_and_vars.py` file change the `playlist_amount = 10` value to as many playlists you wish / your screen allows, save the file
5. In the `src / tables_and_playlists_guide.py` run the `create_tables()` function -> New `playlist.db` will be created
6. After the next start of the app, all the playlists will be visible with increasing numeric titles
7. Optional: Change the title of the playlists via the `Settings window / Playlists`
8. Optional: Remove the previous playlist database

## File types
- Currently available: *.mp3 *.wav *.flac *.midi *.aac *.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg
- Not all the listed file types are tested
- To update the file types lists, please see the `src / cons_and_vars.py / FILE TYPES` section
    - `FILE_TYPES_LIST` used to sort the files in the file dialog window - `AT - Add Track` button
    - `MEDIA_FILES`'s listed file types used to select the correct files from the selected dictionary and subdirectories - `AD - Add Directory` button

## Requirements
### Python 3 - used: 3.11.5
- https://www.python.org/

### Install dependencies
``` pip install -r requirements_pyqt.txt ```

### OS
- Tested on Windows 11

## Thank you all who worked on the modules used in this project!