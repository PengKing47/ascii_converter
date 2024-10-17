import keyboard
import warnings
warnings.filterwarnings("ignore")
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from time import sleep
import cv2
from blessed import Terminal 
from ascii_converter import get_ascii_art, display_image

def select_video():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Video files", "*.mp4 *.mov *.gif")]
    )
    root.destroy()
    return file_path

def save_frames_from_gif(video):
    with video as im:
        for i in range(im.n_frames):
            im.seek(i)
            im.save("images/{}.png".format(i))

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

def get_frames(num_frames):
    frames = []
    for i in range(num_frames):
        path = "images/{}.jpg".format(i)
        frames.append(Image.open(path))
    return frames

def display_video(frames, fps):
    term = Terminal()
    num_frames = len(frames)
    colors = []
    for i in range(len(frames)):
        frame = get_ascii_art(frames[i], term.height-term.height/25)
        frames[i] = frame[0]
        colors.append(frame[1])
    interval = 1 / fps
    current_frame = 0

    with term.fullscreen():
        space_pressed = False
        while True:
            if keyboard.is_pressed('space'): 
                space_pressed = True
            while space_pressed:
                sleep(0.1)
                if keyboard.is_pressed('space'):
                    space_pressed = False
                sleep(0.1)
                
            print(term.move_xy(0, 0))
            if current_frame + 1 == num_frames:
                current_frame = 0
            else:
                current_frame += 1
            display_image(frames[current_frame], colors[current_frame])
            sleep(interval)
    
if __name__ == "__main__":
    video = select_video()
    if video:
        print(f"Selected image: {video}")
    else:
        print("No image selected.")
    fps = int(input("Enter an integer for the fps of the video: "))
    print("Loading...")
    num_frames = save_frames(video)
    frames = get_frames(num_frames)
    display_video(frames, fps)