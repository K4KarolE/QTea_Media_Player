## Main features
- Thirty playlists supported by default. More can be generated (via source code only).
- Thumbnail view.
- Cross playlists queue management with dedicated window.
- Cross playlists search.
- Drag & drop - files, folders.
- Start media from the latest point.
- Start the last played media at startup.
- Quick switch to alternative window mode / size / position.
- Playlists saved by default.
- Set video's preferred audio track to default.
- Operating system related databases for dual booting (via source code only).
- Hotkeys, right click menus
- QTea media player can be a viable option for highly organised contentgoers and house party DJs.
Inspired by `Winamp`, `VLC media player` and `Total/Double Commander`.

## Guide
- Screenshots
- [Playlists separation](#Playlists-separation)
- [Thumbnail generation](#thumbnail-generation)
- [Increase the number of playlists beyond the default](#steps-to-increase-the-number-of-playlists-beyond-the-default--to-generate-new-playlist-database)
- [Playlists compiling phases](#playlists-compiling-phases)
- [Operating system related databases](#operating-system-related-databases---linux-windows)
- [Screensaver](#screensaver)
- [File types](#file-types)
- [Workarounds](#workarounds)
- [Requirements](#requirements)


<div align="left">
    <img src="https://github.com/user-attachments/assets/6a14f0a2-48a1-43ea-be04-a2bd1b58d4da">
</div>
<br>
<div align="left">
    <img src="https://github.com/user-attachments/assets/ffe21b93-1b36-455f-a4a2-bbedaf7eccab">
</div>
<br>
<div align="left">
    <img src="https://github.com/user-attachments/assets/ea884bcb-79fd-4fa4-ab0f-8cd665f416fc">
</div>
<br>
<div align="left">
    <img src="https://github.com/user-attachments/assets/b666dd76-2bc2-4bea-b9b1-16bb6a73031e">
</div>
<br>
<div align="left">
    <img src="https://github.com/user-attachments/assets/73c70cea-e2f9-4762-b5c3-c10234b6f29d">
</div>
<br>
<div align="left">
    <img src="https://github.com/user-attachments/assets/f5d65ceb-89a0-481b-afea-575d75cd60a6">
</div>
<br>
<div align="left">
    <img src="https://github.com/user-attachments/assets/3fea0e96-41ae-4051-a871-ec39cbcd51c0">
</div>
<br>
<div align="left">
    <img src="https://github.com/user-attachments/assets/919f35d6-3ffb-4c3a-9355-48593501eae3">
</div>
<br>
<div align="left">
    <img width="260" src="https://github.com/user-attachments/assets/36ebbf70-1db1-490d-9f25-e1c3f6d757f5">
    <img width="260" src="https://github.com/user-attachments/assets/7d2063db-e3f5-45d3-843f-0b5f1a4a4658">
    <img width="260" src="https://github.com/user-attachments/assets/f5635faf-9845-467b-9a96-c313c68b825b">
</div>
<br>

## Playlists separation
- `Playing playlist`: playlist, where the current track is in the playing or paused state / 
playlist where the last track was played.
- `Active playlist`: playlist, which is currently selected / displayed.
- `Thumbnail playlist`: playlist, where the thumbnail generation thread is running / finished.
- It allows the user to control the `playing playlist` while browsing the rest of the playlists.
- If there is no track in the queue:
    - All the below steps actioned on the `Playing playlist` even if the active and playing playlists are different:
        - Paused --> Play
        - Play previous track
        - Play next track
        - Play next track in the playlist automatically after end of the current track
        - Shuffle / repeat functionalities
        - All hotkey functionalities: change audio/subtitle track

## Thumbnail generation
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
- The playlists amount is not affecting the app's startup time, 
more info in the `Playlists compiling phases` section below or in `src / playlists / MyPlaylists` class.
1. Close the app if it is running.
2. Delete the current databases (`playlist_db_linux.db` and `playlist_db_win.db`) or if you would like to save
the current ones, just rename them. There is more information about the databases in the 
`Operating system related databases` section below.
3. In the `src / tables_and_playlists_guide.py` file change the `create_tables(playlists_amount = 30)` function's 
`playlists_amount` argument value to as many playlists you wish, save the Python file.
4. Run the `create_tables()` function -> New `playlist_db_linux.db`, `playlist_db_win.db` will be created.
5. After the next start of the app, all the playlists will be visible with increasing numeric titles.
6. Optional: Change the title of the playlists via the `Settings window / Playlists`.
7. Optional: Remove the previous playlist databases.

##  Playlists compiling phases:
- App started
- Round 0: Dummy playlists created with no content/media.
- Round 1: One playlist, the last played playlist content is loaded, the playlist is displayed.
- Round 2: 10 playlists around the previous playlist are loaded, 5 on the left, 5 on the right side.
- Round 3: The rest of the playlists are filled with content.

Why 5-5 playlists are filled in Round 2:
- Depends on the default window size (size of the app at startup) and tab sizes, less than 10 tabs / playlists
are displayed at the startup.

Achieved:
- Reduced startup time.
- Startup time got independent of the playlists` amount.

## Operating system related databases - Linux, Windows
- There are two databases (`playlist_db_linux.db`, `playlist_db_win.db`) holding the playlist information. Only one is
 in use at the time the app is running. The DB selection depends on the user`s current OS.
- Reason: ease of switching between multiple OS` on the same device.
- Example: A media added in Linux is not usable once switched to Windows** so it needs to be re-added >> solution: 
 multiple OS related databases >> once switched to another OS, the appropriate DB will be in use, where the previously
 added media with the correct path is available
- ** different mounting point of the same drive of the media

## Screensaver
- When video window is displayed and video is playing the screensaver is turned off.
    Otherwise, the screensaver is on as usual.
- LINUX:
  - Please note, it is tailored for Ubuntu, Linux Mint.
  - For other distros, the screensaver management is may not suitable.
- WINDOWS: Works on 10/11.

## File types
- "formats supported depend heavily on the codec packs installed on your system" - [link](https://forum.qt.io/topic/63110/)
- Which files will be added to the playlist when I add a directory?
    - Every file with the extensions listed in the `src / cons_and_vars.py / FILE TYPES` section will be added:
        - `FILE_TYPES_LIST` used to sort the files in the file dialog window - `AT - Add Track` button.
        - `MEDIA_FILES`'s listed file types used to select the correct files from the selected dictionary
      and subdirectories - `AD - Add Directory` button.
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
- Side effect: no visible side effect

### Information displayed as subtitle
- Issue: the video scene composition not following the layout, frame size change
    - Window <- QFrame <- Layout <- QGraphicsView <- QGraphicsScene <- QGraphicsVideoItem
- Solution: the information (track title, volume, ..) displayed as subtitle on the video screen
    - Side effect: When the video is not playing, the information is not displayed

### Adding the same media twice
- Issue: Adding the same media after each other:
  - The duration player's (src / av_player / TrackDuration) `mediaStatusChanged` signal will not be triggered >> 
the second media will not be added to the playlist
  - The duration player get blocked / unresponsive >> not able to add another media
- Solution: when the 2nd, same media added, the `TrackDuration.setSource()` function is skipped (the previous, 
same media is already loaded) and jumps to the "add media the playlist phase" 
(`src / thread_add_media / return_thread_generated_values()`)

### Unnecessary "player.mediaStatusChanged" signal triggers
- Issue: `QMediaPlayer.MediaStatus.LoadedMedia` state is used to play media, unfortunately it is triggered by:
  - Playing media stopped (via stop button)
  - At the end of a media
  - Playing + pause + playing again + jump via hotkey or slider click
- Solution: `cv.ignore_loaded_media_signal` and `br.av_player.is_end_of_media` support variables are used
to avoid the scenarios above
- PyQt 6.11 issue, was not in PyQt 6.5.3

### Player stuck with the new media after double-clicked the previous, same media twice
- Issue: same media double-clicked / started multiple times + start playing another media >> 
the new media is loaded, but the player stuck at the current position >> media is not playing
- Solution: compare the default and the delayed positions of the player, if same >> 
player stuck at the current position >> pause and play the media >> media is playing
  - `src / func_play_coll / after_playing_the_same_media_workaround()` 

## Could not find solution yet
- The video`s own subtitles are not displayed correctly, VLC player recommended for subbed movies
- OS theme overriding the app`s theme:
  - LINUX: Only affecting the header of the app
  - WINDOWS 11: OK - no theme overriding
- WINDOWS 11 only: Video playing + stop + start another video >> the previous video's last played frame
is displayed before the new video starts playing
- `QMediaPlayer` - Memory Leak: `QMediaPlayer's` `.setSource()` function can increase the memory usage,
[QTBUG-36671](https://bugreports.qt.io/browse/QTBUG-36671)
  - Can occur when: 
    - Adding media to the player
    - Playing new media
  - Minimalist "try to fix" test in "docs / learning / player_basic_memory_leak_fix_try.py"


## Requirements
### Python 3 - used: 3.14.6
- https://www.python.org/
- For the `Python-PyQt` compatibility matrix visit: [https://wiki.qt.io/Qt_for_Python](https://wiki.qt.io/Qt_for_Python)
- [Status of Python versions](https://devguide.python.org/versions/)

### Install dependencies (PyQt6, OpenCV)
``` pip install -r requirements.txt ```

### Install testing dependency - not necessary to use the app
``` pip install pytest==9.0.2 ```

### LINUX - Install specific Python and virtual environment version - Ubuntu / Debian / Linux Mint
Used:
- [How do I install a different Python version using apt-get?](https://askubuntu.com/a/682875)
- [Creating venv with python 3.12](https://askubuntu.com/a/1563105)
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12
```
```
sudo apt install python3.12-venv
```
```
python3.12 -m venv your_venv_name
```

More info: [Qt for Python - Getting Started](https://doc.qt.io/qtforpython-6/gettingstarted.html)


### Thank you all who worked on the modules used in this project!
### Thank you all Winamp, VLC player, Total/Double Commander, FFmpeg, OpenCV, PyInstaller, Nuitka and PyQt contributors!
