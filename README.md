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

## Terminology
- `Playing playlist` = playlist where the current track is in the playing or paused state / playlist where the last track was played
- `Active playlist` = playlist which is currently selected / displayed

## Play buttons
- to come 

## Playlist buttons (under playlists section)
- `AT - Add Track`: add a single media/file to the playlist
- `AD - Add Directory`: adding all the media files listed in the selected directory and subdirectories
- `RT - Remove Track`: removes the current/selected track
- `CP - Clear Playlist`: removes all the items from the current playlist
- `Settings button`: opens the `Settings window`

## Settings - Settings window
- To open the `Setting window` click on the `Cog/Settings icon` under the playlists section 
- `Playlists tab:`Able to update the playlists titles - hide/show the playlists
- `Genereal tab:` Adjust the shortcut keyboard values (work in progress)
- `Hotkeys tab:` Adjust the player's jump values (work in progress)
- Saving the `Settings window` values by clicking on the `Save button`:
    - Saves all the values from all the tabs if there is no invalid value
    - Else: 
        - Pop-up window displayed with the error message for all the invalid scenarios
        - Error message includes the name of the field with the invalid value and the rule it should follow
        - The pop-up window title: ERROR - TAB'S NAME (where the invalid value occurred)

### Playlists
- Twenty playlists are available by default.
- In the `Settings window / Playlists` tab all the available playlists are listed
    - To make a playlist visible:
        - Add a title to the playlist
        - If the playlist will be used the first time: empty playlist will be displayed after restart
        - If playlist had tracks before it was hidden: the records will be loaded automatically after restart
    - To hide a playlist:
        - Remove the title of the playlist
        - Playlists without a title will be hidden after restart
        - At least one of the playlist remains visible - not able to remove all the playlist titles
            - In this case clicking on the `Save button`: pop-up window will be displayed with the error message
        - The hidden playlist's records/media information remains in the database

### General
- coming

### Hotkeys
- Acceptable hotkey formats: `M`, `m`, `Ctrl`, `ctrl`, `M+Ctrl`, `M+Ctrl+Space`
- Acceptable hotkey list in `src / cons_and_vars.py / keys_list`
- more to come

<br>
<div align="left">
    <img width="260" src="docs/promo/screenshot_sett_win_playlists.png">
    <img width="260" src="docs/promo/screenshot_sett_win_general.png">
    <img width="260" src="docs/promo/screenshot_sett_win_hotkeys.png">
</div>


## Behavior
- `Volume`
    - Changing the volume after the app is muted:
        - It switches back to the un-muted state
        - New volume = volume before muted -/+ the change
    - The volume range is less wide compare to `VLC media player`
- `Scree saver`
    - When video window is displayed and video is playing the screen saver is turned off
        - Otherwise the screen saver is on as usual
- `Playlists`
    - On any playlist able to add/remove tracks: the playlist is saved automatically
    - At startup:
        - All playlists loading automatically
        - On all playlist the last played track is selected
        - The `Playing playlist` is active/displayed    

### Active and Playing playlists separation
- All the below steps actioned on the `Playing playlist` even if the active and playing playists are different:
    - Paused --> Play
    - Play previous track
    - Play next track
    - Play next track in the playlist automatically after end of the current track
    - Shuffle / repeat functionalities
    - All hotkeys functionalities: change audio/subtitle track
- Window title = Playing playlist title | Track title

## Steps to increase the number of playlists beyond the default / to generate new playlist database
- The `Settings window` tabs are not scrollable, which put a limitation on how much playlists can be visible on the `Settings window / Playlist` tab:
    - Display(27" - 2560*1440 - 150% scale) ~ 50+ playlists
    - Display(15.6" - 2560*1440 - 150% scale) ~ 30 playlists
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
