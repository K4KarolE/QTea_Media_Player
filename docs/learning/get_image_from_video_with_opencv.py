import cv2
import os
from datetime import datetime
from pathlib import Path

"""
TEST RESULT - TV SHOW ALL SEASONS - 200+ videos
    cap.release() out of loop: 10.93 seconds
    cap.release() in loop: 10.01 seconds
    cap.release() and cv2.destroyAllWindows() in the loop: 9.9 seconds

FFmpeg result for the same tv show: 26.8 seconds
    via "learning / thumbnail_view / thumbnail_img_creation_ffmpeg.py"

Used & Cheers all: https://opencv.org/resizing-and-rescaling-images-with-opencv/#h-resizing-with-a-scaling-factor
"""


img_size = 200
frame_take_at_second = 70       # make sure the videos in the "path_vids" folder are longer
target_folder = "opencv_extracted_images"
path_vids = '/../test_vids/'    # path of a folder containing .mp4 or .mkv video files
list_vids_path = []


def generate_vids_list():
    for dir_path, dir_names, file_names in os.walk(path_vids):
        for file in file_names:
            if file.split('.')[-1] in ['mp4', 'mkv']:
                list_vids_path.append(Path(dir_path, file))



start_time = datetime.now().timestamp()
generate_vids_list()
os.makedirs(target_folder, exist_ok=True)

for video_path in list_vids_path:
    # LOAD VIDEO
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file: ", video_path)

    # GET FRAME
    cap.set(cv2.CAP_PROP_POS_MSEC, frame_take_at_second*1000)
    ret, frame = cap.read()
    if not ret:
            print("Error: Could not read video frame.")

    # RESIZE FRAME
    frame_height, frame_width, _  = frame.shape
    frame_width_new = img_size
    frame_height_new = int(frame_height  * frame_width_new / frame_width)
    frame = cv2.resize(frame, (frame_width_new, frame_height_new))

    # SAVE IMAGE
    file_name = Path(video_path).stem
    frame_filename = os.path.join(target_folder, f"{int(start_time)}_{file_name}_{img_size}_.jpg")
    cv2.imwrite(frame_filename, frame)  # Save frame as an image

    cap.release()
    cv2.destroyAllWindows()

print(f"Frames extracted and saved successfully")
end_time = datetime.now().timestamp()
print("\nOpenCV - SUM: ", end_time - start_time)