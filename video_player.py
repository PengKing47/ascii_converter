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
images = []
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

def save_frames_from_gif(video):
    with video as im:
        for i in range(im.n_frames):
            im.seek(i)
            im.save("images/{}.png".format(i))

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
    for i in range(num_frames):
        path = "images/{}.jpg".format(i)
        images.append(Image.open(path))

# thread 3
def update_frames():
    term = Terminal()
    for i in range(len(images)):
        frame = get_ascii_art(images[i], term.height-term.height/25)
        frames.append(frame[0])
        colors.append(frame[1])
    '''
    while True:
        #adjust the frames so the video size is adjustable is adjustable
        #this causes a lot of lag 🤣
        term = Terminal()
        for i in range(len(images)):
            if keyboard.is_pressed("q"):
                exit(1)
            frame = get_ascii_art(images[i], term.height-term.height/25)
            frames[i] = frame[0]
            colors[i] = frame[1]
    '''

#thread 4
def display_video(fps):
    term = Terminal()
    num_frames = len(images)
    interval = 1 / fps
    current_frame = 0

    with term.fullscreen():
        space_pressed = False
        while True:
            if keyboard.is_pressed("q"):
                exit(1)
            if keyboard.is_pressed('space'): 
                space_pressed = True
            while space_pressed:
                sleep(0.1)
                if keyboard.is_pressed('space'):
                    space_pressed = False
                sleep(0.1)
                if keyboard.is_pressed("q"):
                    exit(1)
                
            print(term.move_xy(0, 0))
            if current_frame + 1 == num_frames:
                current_frame = 0
            else:
                current_frame += 1
            display_image(frames[current_frame], colors[current_frame])
            sleep(interval)

def run_threads(video, fps,):
    cam = cv2.VideoCapture(video) 
    num_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))

    save_frames_thread = Thread(target=save_frames, args = (video,))
    get_frames_thread = Thread(target=get_frames, args = (num_frames,))
    update_thread = Thread(target=update_frames)
    display_thread = Thread(target=display_video, args = (fps,))

    save_frames_thread.start()
    sleep(0.5)
    get_frames_thread.start()

    save_frames_thread.join()
    get_frames_thread.join()

    update_thread.start()
    update_thread.join() # if i dont wait for this to end, the begginning of the video is laggy af but the video take much longer to laod so idk
    sleep(0.01)
    display_thread.start()

if __name__ == "__main__":
    video = select_video()
    if video:
        print(f"Selected image: {video}")
    else:
        print("No image selected.")
    #fps = int(input("Enter an integer for the fps of the video: "))
    fps = 30 # this will be the standard for now
    print("Loading...")
    run_threads(video, fps)