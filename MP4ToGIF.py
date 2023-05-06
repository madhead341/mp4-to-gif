import cv2
import glob
import os
import shutil
import PySimpleGUI as sg

from PIL import Image

file_types = [("MP4 (*.mp4)", "*.mp4"), ("All files (*.*)", "*.*")]

def convert_mp4_to_jpgs(path):
    video_capture = cv2.VideoCapture(path)
    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    frame_duration = int(1000 / frame_rate)  # Duration of each frame in milliseconds
    
    still_reading, image = video_capture.read()
    frame_count = 0
    if os.path.exists("output"):
        shutil.rmtree("output")
    try:
        os.mkdir("output")
    except IOError:
        sg.popup("Error occurred creating output folder")
        return
    
    while still_reading:
        cv2.imwrite(f"output/frame_{frame_count:05d}.jpg", image)
        
        still_reading, image = video_capture.read()
        frame_count += 1
        print(f"Converting frame {frame_count}...")
    
    print("MP4 to JPG's conversion complete.")
    return frame_duration, frame_count

def make_gif(mp4_path, gif_path):
    frame_folder = "output"
    images = glob.glob(f"{frame_folder}/*.jpg")
    images.sort()
    frames = [Image.open(image) for image in images]
    frame_one = frames[0]

    # Get the frame duration based on the frame rate of the video
    frame_rate = cv2.VideoCapture(mp4_path).get(cv2.CAP_PROP_FPS)
    frame_duration = int(1000 / frame_rate)  # Duration of each frame in milliseconds

    frame_one.save(gif_path, format="GIF", append_images=frames,
                   save_all=True, duration=frame_duration, loop=0)

    print(f"GIF created: {gif_path}")
    
    shutil.rmtree(frame_folder)

def main():
    layout = [
        [
            sg.Text("MP4 File"),
            sg.Input(size=(25, 1), key="-FILENAME-", disabled=True),
            sg.FileBrowse(file_types=file_types),
        ],
        [sg.Button("Convert to GIF")],
    ]

    window = sg.Window("MP4 to GIF Converter", layout)

    while True:
        event, values = window.read()
        mp4_path = values["-FILENAME-"]
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Convert to GIF" and mp4_path:
            gif_path = os.path.splitext(mp4_path)[0] + ".gif"
            frame_duration, frame_count = convert_mp4_to_jpgs(mp4_path)
            if frame_count > 0:
                total_duration = frame_duration * frame_count / 1000  # Total duration in seconds
                print(f"Converting to .gif... (This will take {total_duration:.1f}s)")
                make_gif(mp4_path, gif_path)
                sg.popup(f"GIF created: {gif_path}")

    window.close()

if __name__ == "__main__":
    main()
