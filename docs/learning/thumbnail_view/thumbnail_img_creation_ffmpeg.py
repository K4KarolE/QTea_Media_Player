import os
from pathlib import Path
from datetime import timedelta, datetime

"""
TEST RESULT - TV SHOW ALL SEASONS - 200+ videos: 26.8 seconds

OpenCV result for the same tv show: 9.9 seconds
    via "learning / get_image_from_video_with_opencv.py"
"""


target_img_scale = 400
at_seconds_raw = 70          # make sure the videos in the "path_vids" folder are longer
path_vids = '/../test_vids/' # path of a folder containing .mp4 or .mkv video files
list_vids_path = []
path_thumbnails = "ffmpeg_extracted_images"
os.makedirs(path_thumbnails, exist_ok=True)

def generate_vids_list():
    for dir_path, dir_names, file_names in os.walk(path_vids):
        for file in file_names:
            if file.split('.')[-1] in ['mp4', 'mkv']:
                list_vids_path.append(Path(dir_path, file))

def generate_thumbnails():
    at_seconds = timedelta(seconds=at_seconds_raw)
    for vid_path in list_vids_path:
        file_name = f'{vid_path.name}.{target_img_scale}.jpg'
        target_path = Path(path_thumbnails,file_name)
        if not target_path.is_file():
            ffmpeg_action = f"ffmpeg -ss {at_seconds} -i '{vid_path}' -vf 'scale={target_img_scale}:{target_img_scale}:force_original_aspect_ratio=decrease' -vframes 1 '{target_path}' -hide_banner"
            os.system(ffmpeg_action)

start_time = datetime.now().timestamp()
generate_vids_list()
generate_thumbnails()
end_time = datetime.now().timestamp()
print("\nFFmpeg - SUM: ", end_time - start_time)