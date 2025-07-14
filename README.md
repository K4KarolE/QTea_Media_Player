## Main features
- Thirty playlists supported by default. More can be generated.
- Thumbnail view.
- Cross playlists queue management with dedicated window.
- Cross playlists search.
- Drag & drop - files, folders.
- Start media from the latest point.
- Start the last played media at startup.
- Quick switch to alternative window mode / size / position.
- Playlists saved by default.
- Set video's preferred audio track to default.
- Hotkeys, right click menus, selectables:
    - Audio and subtitle tracks
    - Full screen on the current display or on the selected display
- QTea media player can be a viable option for highly organised contentgoers and house party DJs.
Inspired by `Winamp`, `VLC media player` and `Total/Double Commander`.

## Guide
- [Screenshots](#screenshots)
- [Terminology](#terminology)
- [Buttons](#buttons)
    - [Play buttons](#play-buttons)
    - [Playlist buttons](#playlist-buttons-under-playlists-section)
- [Settings window](#settings-window)
   - [General](#general)
   - [Hotkeys](#hotkeys)
   - [Playlists](#playlists)
- [Active and Playing playlists separation](#active-and-playing-playlists-separation)
- [Thumbnail View](#thumbnail-view)
- [Increase the number of playlists beyond the default](#steps-to-increase-the-number-of-playlists-beyond-the-default--to-generate-new-playlist-database)
- [Other Behaviour](#other-behaviour)
    - Volume
    - Screen saver
    - Drag & Drop
- [File types](#file-types)
- [Workarounds](#workarounds)
    - [Dummy track](#dummy-track)
    - [Dummy playlist tab](#dummy-playlist-tab)
    - [Information displayed as subtitle](#information-displayed-as-subtitle)
    - [Audio delay - LINUX only](#audio-delay---linux-only)
    - [No solution yet](#could-not-find-solution-yet)
- [Requirements](#requirements)

## Screenshots
<div align="left">
    <img src="https://github.com/user-attachments/assets/5f8abf75-7f97-48d8-a979-30550915a306">
</div>
<br>
<div align="left">
    <img src="https://github.com/user-attachments/assets/d9334f75-d459-4354-8401-7b33b33fe25e">
</div>
<br>
<div align="left">
    <img src="https://github.com/user-attachments/assets/7b956b27-5a1d-4c37-94a5-2e9a0a4905d0">
</div>
<br>
<div align="left">
    <img src="https://github.com/user-attachments/assets/67521950-75c7-4767-924a-dbd16e31620c">
</div>
<br>
<div align="left">
    <img src="https://github.com/user-attachments/assets/1acf7a47-ffd5-4586-ae63-c49a31b13c2d">
</div>
<br>
<div align="left">
    <img src="https://github.com/user-attachments/assets/577c5064-e2ff-4789-9a0a-d63925c9153e">
</div>
<br>
<div align="left">
    <img src="https://github.com/user-attachments/assets/4c99a7c8-95f8-4281-b935-9c4c0fb3b4a2">
</div>
<br>


## Terminology
- `Playing playlist`: playlist, where the current track is in the playing or paused state / 
playlist where the last track was played.
- `Active playlist`: playlist, which is currently selected / displayed.
- `Thumbnail playlist`: playlist, where the thumbnail generation thread is running on

## Buttons
### Play buttons
- The `Play`, `Stop`, `Previous track`, `Next track` and `Shuffle` buttons behave as usual
  - When `Shuffle` is on, the played media is tracked. If no switch between playlists has been made,
the last "X" tracks can be played back when the `Previous track` button/hotkey is triggered.
    - The amount "X" declared in `src / class_data / shuffle_played_tracks_list_size`.
- The `Repeat playlist` button has 3 states:
    - Disabled
    - Repeat playlist - the button is flat.
    - Repeat currently playing track - the button is flat and a square shape displayed in the middle of the icon.
- `Toggle Video and Playlist` buttons show/hide the video or playlist section.
    - Can not hide both the same time.
    - At startup both the video and playlist section are visible as default.
- Tooltip is displayed when the mouse moved over the current button.

### Playlist buttons (under playlists section)
- `AT - Add Track`: add a single media/file to the playlist.
- `AD - Add Directory`: adding all the media files listed in the selected directory and subdirectories.
- `RT - Remove Track`: removes the current/selected track.
- `CP - Clear Playlist`: removes all the items from the current playlist.
- `Q`: opens the `Queue and Search Window`
- `Settings button`: opens the `Settings window`.
- `Thumbnail View`: switches between the standard and the `Thumbnail View` playlists
- Tooltip is displayed when the mouse moved over the current button.

## Settings window
- To open the `Setting window` click on the `Cog/Settings icon` under the playlists section. 
- `Playlists tab:` Able to update the playlists titles - hide/show the playlists.
- `General tab:` Adjust the media player's and hotkeys' behaviour.
- `Hotkeys tab:` Adjust the hotkeys' keybinds.
- Saving the `Settings window` values by clicking on the `Save button`:
    - Saves all the values from all the tabs (Playlists, General, Hotkeys) if there is no invalid value.
    - Else: 
        - Pop-up window displayed with the error message for all the fields with invalid value.
        - Error message includes the name of the field and the rule it should follow.
        - The pop-up window title: ERROR - TAB'S NAME (where the invalid value occurred).

### General
- `Always on top`: Keeps the player on top of other currently running applications
- `Continue playback`:
    - Saves the duration of the currently playing track every 5 seconds.
    - When revisiting the same track, the play continuous from the latest, saved position.
- `Play at startup`:
    - Automatically plays the last played track at startup.
    - If the track was removed while playing, at the next startup it plays the track in the same row.
    - If the last play track removed and there is no track in the same row:
        - If the playlist is not empty: It plays the first track of the playlist.
        - If the playlist is empty: No track played.
- `Small / Medium / Big jump`: 
    - Seconds the player position will be moved (forward/backward)
    - Hotkeys of the direction/jump type are in the `Hotkeys tab`
    - Amending the jump values in the `General tab`
- `Window width-height / alt. / 2nd alt.`:
    - Values of the different window sizes.
    - To switch between the different window sizes:
        - `Window alt. size` hotkey (`Hotkeys tab`) or
        -  Right-click on the video area (if applicable) and select `Alter - Toggle`
    - `Window width-height`:
        - The size of the window at startup.
        - Both video and playlist section/window are visible.
    - `Window alt. width-height`: 
        - The size of the window after the window size alter toggle actioned once
        - Only the video window is visible, the playlist window is hidden.
    - `Window 2nd alt. width-height`: 
        - The size of the window after the window size alter toggle actioned twice.
        - Only the video window is visible, the playlist window is hidden.
    - `Window alt. repositioning`:
        - Repositioning the window depending on the selected size.
        - Default and 1st: middle of the screen / 2nd: right, bottom corner of the screen.
    - `Default audio track`:
        - Video starts with the selected audio track.
        - Can be useful while watching multiple episodes of a tv show in one sitting where the preferred audio
    track is not the first/default one.
    - `Thumbnail image size`: Min:100, Max:500 pixels.
    - `Remove unused thumbnails older than (days)`: When closing the app, it removes the unused thumbnails older
  than the added value and updates the `_thumbnail_history.json` including the logs for the failed /
  uncreated thumbnails.
    - `Search result - parent folders' text length`: The separate text length of the 2nd and 1st parent
    directory of the media in the search result displayed as:
  2nd degree parent directory(sized) / 1st degree parent directory(sized) - file name
    - Ideas:
        - Use the first alt. window size when the user is close to a wide screen (e.g.: having a lunch).
        - Use the second alt. window size when player is secondary and it can be placed in the right,
bottom corner of the screen (e.g: while browsing).
        - Adjust the sizes according the currently played TV show`s video ratio to avoid black bars.

### Hotkeys
- Acceptable hotkey formats: `M`, `m`, `Ctrl`, `ctRL`, `M+Ctrl`, `M+Ctrl+Space`, `M | P`, `M+Ctrl | P`
- Able to add multiple hotkeys for the same action: `Up | P`
- Acceptable hotkey list in `src / cons_and_vars.py / keys_list`
- `Small / Medium / Big jump - backward/forward`:
    - The values of the jump types are defined in the `General tab`.
- `Play\pause` vs `Play`:
    - `Play\pause`:
        - If a track is in the playing/paused state: pauses or continues to play the track independently
      from the current active playlist.
        - If no track is in the playing/paused state: starts the selected track on the active playlist.
    - `Play`: Starts the selected track on the active playlist even if there is a track in the
  playing/paused state from any playlist.
- `Volume - Increase / Decrease`: Changes the volume with +/- 5%.
- `Audio track - use next`: Toggles between the available audio channels, there is no disabled state.
- `Subtitle track - use next`: Toggles between the available subtitles and a disabled state.
- `Toggle - Full screen`: Next to the value set up in this field the `Escape` button is hard-coded to quit
from the full screen mode.
- `Toggle - Window alt. size`:
    - Toggles between the default / alt. / 2nd alt. window sizes defined in the `General tab`.
    - Default: both video and playlist sections are visible.
    - Alt. and 2nd alt.: only the video section is visible. 
- `Playlist - Select previous / next`: Jumps between the playlists available.
- `Queue / Dequeue track`:
    - Add track to / removes track from the queue list.
    - This hotkey takes action on the `Active playlist`.
    - On the `Queue and Search window`s track list the right-click / Queue-Dequeue should be used.
- The rest of the hotkeys are self-explanatory.

### Playlists
- In the `Settings window / Playlists` tab all playlists are listed.
    - To make a playlist visible:
        - Add a title to the playlist.
        - If the playlist is used the first time: empty playlist will be displayed after saving.
        - If playlist had tracks before it was hidden: the records will be loaded automatically after restart.
    - To hide a playlist:
        - Remove the title of the playlist.
        - At least one of the playlists remains visible:
            - Not able to remove all the playlist titles: clicking on the `Save button`: pop-up window will be
        displayed with the error message.
        - The hidden playlist's records/media information remains in the database.
- Able to add/remove tracks to any of playlists: the playlist is saved automatically
    - At startup:
        - All playlists loading automatically.
        - On all playlist the last played track is selected.
        - The `Playing playlist` is active/displayed.

<div align="left">
    <img width="260" src="https://github.com/user-attachments/assets/c46365e5-26af-4ad2-b6a3-837636aea9ab">
    <img width="260" src="https://github.com/user-attachments/assets/9172c9ce-f762-4c24-9198-c4e0572ea880">
    <img width="260" src="https://github.com/user-attachments/assets/f0140e2e-eef4-4ca0-8760-eeee17972184">
</div>
<br>

## Active and Playing playlists separation
- It allows the user to control the `playing or queued tracks playlist` while browsing the rest of the playlists
- If there is no track in the queue:
    - All the below steps actioned on the `Playing playlist` even if the active and playing playlists are different:
        - Paused --> Play
        - Play previous track
        - Play next track
        - Play next track in the playlist automatically after end of the current track
        - Shuffle / repeat functionalities
        - All hotkey functionalities: change audio/subtitle track
- If there are tracks in the queue:
    - All the above behaviours are actioned on the `queued tracks playlist` (apart from shuffle)
- Window title = Playing playlist title | Track title

## Thumbnail View
### General
- If `FFmpeg` is installed, the `Thumbnail View` button is active under the Playlist area.
  - Otherwise, the button is inactive and "FFmpeg installation needed" message is displayed
once the cursor is over the button.
  - There is more information below in the `Requirements` section.
- Adding/removing media to/from a playlist where the `Thumbnail View` is active: automatically switching back to the 
standard playlist view.
- Once the `Thumbnail View` button is clicked, the thumbnail generation is running for the current playlist until
it is completed.
  - Or the `Thumbnail View` button is clicked again "on" the same or "on" another playlist.
- The `Thumbnail View` and standard playlist view are in sync regarding the selection and currently playing and
selected track style.
### Thumbnail generation
- Every audio file has the same, default audio thumbnail.
- Every new thumbnail image is placed in the `thumbnails` folder with a unique title: 
"filename.ext"."raw duration"."image size".jpg
  - `Image title: current time` key-value pair is added to the `thumbnails / _thumbnail_history.json / completed`.
  - If the thumbnail generation was unsuccessful, it is logged in the `thumbnails / _thumbnail_history.json / failed` 
  with the `image title: current time` key-value pair.
- Every thumbnail generation process starts by checking if the image title(key) exists in the 
`_thumbnail_history.json / completed` or in the `failed` dictionary before the actual thumbnail image generation.
  - In `failed`: not trying to generate thumbnail image, `image title: current time` value will be updated
  with the current time.
  - In `completed`: checks if the file exists.
    - Yes: image will be used for the thumbnail, `image title: current time` value will be updated with the current time.
    - No: try to generate a new thumbnail image.
- The "image taken from point" is video duration dependent.
  - Logic in `src / func_thumbnails / get_time_frame_taken_from()`

## Steps to increase the number of playlists beyond the default / to generate new playlist database
1. Close the app if it is running.
2. Rename the current playlist database: `playlist.db`.
3. In the `src / tables_and_playlists_guide.py` file change the `create_tables(playlists_amount = 30)` function's 
`playlists_amount` argument value to as many playlists you wish, save the Python file.
4. Run the `create_tables()` function -> New `playlist.db` will be created.
5. After the next start of the app, all the playlists will be visible with increasing numeric titles.
6. Optional: Change the title of the playlists via the `Settings window / Playlists`.
7. Optional: Remove the previous playlist database.

## Other Behaviour
- `Volume`
    - Changing the volume after the app is muted:
        - It switches back to the un-muted state.
        - New volume = volume before muted -/+ the change.
    - The volume range is less wide compared to `VLC media player`.
- `Screen saver`
    - When video window is displayed and video is playing the screen saver is turned off.
        - Otherwise the screen saver is on as usual.
- `Drag & Drop`
    - Internal: able to relocate/move a playlist item.
    - External: selected files and/or folders can be grabbed and dropped on the active playlist from
  File Explorer, Desktop,  .. . 

## File types
- "formats supported depend heavily on the codec packs installed on your system" - [link](https://forum.qt.io/topic/63110/)
- Which files will be added to the playlist when I add a directory?
    - Every file with the extensions listed in the `src / cons_and_vars.py / FILE TYPES` section will be added:
        - `FILE_TYPES_LIST` used to sort the files in the file dialog window - `AT - Add Track` button.
        - `MEDIA_FILES`'s listed file types used to select the correct files from the selected dictionary
      and subdirectories - `AD - Add Directory` button.
    - Currently listed extensions:
        - Audio: *.aac *.dts *.flac *.m4a *.midi *.mp3 *.ogg *.wav
        - Video: *.avi *.flv *.mkv *.mov *.mp4 *.mpeg *.mts *.webm *.wmv
- To check if a file with unlisted extension is payable:
    - Click `AT - Add Track` button
    - In the pop-up window navigate to the file location
    - At the bottom of the pop-up window change the `Files of type` to `All files (*.*)`
    - Add the file to the playlist and try to play it

## Workarounds
### Dummy track
- Issue: the first track has to be played from the start till the end before be able to switch to another track
- Solution: dummy, empty track (< 1 second) played at startup
- More info: `src / av_player.py`
- Side-effect:
    - No visible side-effect
    - Unlikely adding much to the launch time (Legion 5 laptop):
        - Windows 11: 1.2 seconds
        - Linux Mint 22: 0.4 seconds

### Dummy playlist tab
- Issue: if the last playlist tab is hidden, the whole playlist tab list is not reachable via the arrow buttons 
- Solution: The last, dummy, disabled playlist tab always visible
    - More info: `src / playlists.py`
    - Side-effect: disabled, not clickable, small pice is visible on the right side of the playlists bar

### Information displayed as subtitle
- Issue: the video scene composition not following the layout, frame size change
    - Window <- QFrame <- Layout <- QGraphicsView <- QGraphicsScene <- QGraphicsVideoItem
- Solution: the information (track title, volume, ..) displayed as subtitle on the video screen
    - Side-effect: When the video is not playing, the information is not displayed

### Audio delay - LINUX only
- Issue: video or audio paused + continue playing
    - Video continue normally
    - Audio is not playing for a while (2-10s)
- Solution: saving the current player`s position at pause and apply it at the continue phase

### Audio device change - LINUX only
- Issue: Switching audio device on PC/laptop >> **freezes the app, no error message.
  - ** src / av_player updated to avoid
  - It is working without any issue with PyQt(6.9.0).
- Solution: right-click on the video and select the preferred audio device or restart the app

### Could not find solution yet
- Issue: the video`s own subtitles are not displayed correctly, VLC player recommended for subbed movies


## Requirements
### Python 3 - used: 3.11.5
- https://www.python.org/

### Install dependencies
``` pip install -r requirements.txt ```

### Additional dependency for Linux
``` sudo apt install libxcb-cursor-dev ```

### FFmpeg [(link)](https://ffmpeg.org/)
- `FFmpeg` used to generate thumbnail images from the video media
- Without `FFmpeg`
  - The `Thumbnail View button` is disabled
  - The media player is still fully functioning 
- WINDOWS
    - [Install FFmpeg on Windows 10/11](https://techtactician.com/how-to-install-ffmpeg-and-add-it-to-path-on-windows/)
- LINUX
    - Via `Software Manager`


### OS
- Tested on Windows 11, Linux Mint 22

## Thank you all who worked on the modules used in this project!
## Thank you all Winamp, VLC player and Total/Double Commander contributors!