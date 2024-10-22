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

class VideoPlayer():
    def __init__(self, video, fps):
        self.frames = []
        self.colors = []
        self.num_frames = 0
        self.current_frame = 0
        self.video = video
        self.fps = fps

    # method to be overwritten with whatever is needed
    def display_frame(self):
        display_image(self.frames[self.current_frame], self.colors[self.current_frame])

    # thread 1
    def save_frames(self):
        print("Loading...")
        cam = cv2.VideoCapture(self.video) 
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
    def get_frames(self):
        term = Terminal()
        for i in range(self.num_frames):
            path = "images/{}.jpg".format(i)
            image = Image.open(path)
            frame = get_ascii_art(image, term.height-term.height/24.5)
            self.frames.append(frame[0])
            self.colors.append(frame[1])

    #thread 3
    def display_video(self):
        term = Terminal()
        interval = 1 / self.fps

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
                self.current_frame += 1
                if self.current_frame == len(self.frames):
                    self.current_frame = 0
                self.display_frame()
                sleep(interval)

    def start(self):
        cam = cv2.VideoCapture(self.video) 
        self.num_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
        
        save_frames_thread = Thread(target=self.save_frames)
        get_frames_thread = Thread(target=self.get_frames)
        display_thread = Thread(target=self.display_video)

        save_frames_thread.start()
        sleep(0.5)
        get_frames_thread.start()
        display_thread.start()

def select_video():
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Video files", "*.mp4 *.mov *.gif")]
        )
        root.destroy()
        return file_path

def main():
    video = select_video()
    if video:
        print(f"Selected image: {video}")
    else:
        print("No image selected.")
    videoPlayer = VideoPlayer(video, 20)
    videoPlayer.start()

if __name__ == "__main__":
    main()
