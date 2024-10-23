import keyboard
import warnings
warnings.filterwarnings("ignore")
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from time import sleep, time
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
        self.is_playing = True
        self.video = video
        self.fps = fps
        self.actual_fps = ""

    # method to be overwritten with whatever is needed
    def display_frame(self):
        display_image(self.frames[self.current_frame], self.colors[self.current_frame])

    #thread 1
    def get_frames(self):
        term = Terminal()
        cam = cv2.VideoCapture(self.video)
        current_frame = 0
        for i in range(self.num_frames):
            frame_ready, current_frame = cam.read() # get the frame
            if frame_ready:
                frame = cv2.imread(self.video, current_frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
                frame = Image.fromarray(frame) 
                frame = get_ascii_art(frame, term.height-10)
                self.frames.append(frame[0])
                self.colors.append(frame[1])

    #thread 2
    def display_video(self):
        initial_time = time()
        term = Terminal()
        interval = 1 / self.fps

        with term.fullscreen():
            space_pressed = False
            while self.is_playing:
                if keyboard.is_pressed("q") or keyboard.is_pressed("x"):
                    self.is_playing = False
                elif keyboard.is_pressed('space'): 
                    space_pressed = True
                while space_pressed:
                    sleep(0.1)
                    if keyboard.is_pressed('space'):
                        space_pressed = False
                    sleep(0.1)
                    if keyboard.is_pressed("q") or keyboard.is_pressed("x"):
                        space_pressed = False
                        self.is_playing = False
                    
                print(term.move_xy(0, 0))
                self.current_frame += 1
                if self.current_frame == len(self.frames):
                    self.current_frame = 0
                self.display_frame()
                current_time = time()
                time_difference = current_time - initial_time
                if time_difference < interval:
                    sleep(interval - time_difference)
                    self.actual_fps = self.fps
                else:
                    self.actual_fps = int(1/time_difference)
                initial_time = time()

    def start(self):
        cam = cv2.VideoCapture(self.video) 
        self.num_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
        
        get_frames_thread = Thread(target=self.get_frames)
        display_thread = Thread(target=self.display_video)

        get_frames_thread.start()
        sleep(0.5)
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
    videoPlayer = VideoPlayer(video, 60)
    videoPlayer.start()

if __name__ == "__main__":
    main()
