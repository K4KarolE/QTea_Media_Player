import os
from pathlib import Path
from datetime import timedelta

path_vids = '/../test_vids/'
path_thumbnails = f'{path_vids}/thumbnails'
list_vids_path = []

def generate_vids_list():
    for dir_path, dir_names, file_names in os.walk(path_vids):
        for file in file_names:
            if file.split('.')[-1] in ['mp4', 'mkv']:
                list_vids_path.append(Path(dir_path, file))

def generate_thumbnails():
    target_img_scale = 200
    at_seconds_raw = 3
    at_seconds = timedelta(seconds=at_seconds_raw)
    for vid_path in list_vids_path:
        file_name = f'{vid_path.name}.{target_img_scale}.jpg'
        target_path = Path(path_thumbnails,file_name)
        if not target_path.is_file():
            ffmpeg_action = f"ffmpeg -ss {at_seconds} -i '{vid_path}' -vf 'scale={target_img_scale}:{target_img_scale}:force_original_aspect_ratio=decrease' -vframes 1 '{target_path}' -hide_banner"
            os.system(ffmpeg_action)

generate_vids_list()
generate_thumbnails()