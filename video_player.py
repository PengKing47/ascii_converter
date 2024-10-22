import keyboard
import warnings
warnings.filterwarnings("ignore")
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from time import sleep
import cv2
from blessed import Terminal
from threading import Thread
from ascii_converter import get_ascii_art, display_image

#global variables
frames = []
colors = []

def select_video():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Video files", "*.mp4 *.mov *.gif")]
    )
    root.destroy()
    return file_path

# thread 1
def save_frames(video):
    cam = cv2.VideoCapture(video) 
    currentframe = 0
    while(True): 
        ret,frame = cam.read() 
        if ret: 
            path = 'images/' + str(currentframe) + '.jpg'
            cv2.imwrite(path, frame) 
            currentframe += 1
        else: 
            break
    return currentframe

#thread 2
def get_frames(num_frames):
    term = Terminal()
    for i in range(num_frames):
        path = "images/{}.jpg".format(i)
        image = Image.open(path)
        frame = get_ascii_art(image, term.height-term.height/24.5)
        frames.append(frame[0])
        colors.append(frame[1])

#thread 3
def display_video(fps):
    term = Terminal()
    interval = 1 / fps
    current_frame = 0

    with term.fullscreen():
        space_pressed = False
        while True:
            if keyboard.is_pressed("q"):
                exit(1)
            elif keyboard.is_pressed('space'): 
                space_pressed = True
            while space_pressed:
                sleep(0.1)
                if keyboard.is_pressed('space'):
                    space_pressed = False
                sleep(0.1)
                if keyboard.is_pressed("q"):
                    exit(1)
                
            print(term.move_xy(0, 0))
            current_frame += 1
            if current_frame == len(frames):
                current_frame = 0
            display_image(frames[current_frame], colors[current_frame])
            sleep(interval)

def run_threads(video, fps,):
    cam = cv2.VideoCapture(video) 
    num_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))

    save_frames_thread = Thread(target=save_frames, args = (video,))
    get_frames_thread = Thread(target=get_frames, args = (num_frames,))
    display_thread = Thread(target=display_video, args = (fps,))

    save_frames_thread.start()
    sleep(0.5)
    get_frames_thread.start()
    display_thread.start()

def main():
    video = select_video()
    if video:
        print(f"Selected image: {video}")
    else:
        print("No image selected.")
    #fps = int(input("Enter an integer for the fps of the video: "))qq
    fps = 30 # this will be the standard for now
    print("Loading...")
    run_threads(video, fps)

if __name__ == "__main__":
    main()