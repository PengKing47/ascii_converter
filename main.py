from video_player import VideoPlayer, select_video
from blessed import Terminal
import keyboard
from time import sleep
    
def initiate():
    initiate_ui()
    add_key_handler()

def initiate_ui():
    term = Terminal()
    print(term.clear() + term.move_xy(0, 0))
    display_header("", "")
    
def display_header(video, fps):
    term = Terminal()
    terminal_width = term.width
    print("\033[38;2;255;255;255m")
    print("-"*terminal_width)
    print("Open Video: O | Close Video: Q | Close Interface: X | " + f"Current Video: {video.split("/")[-1]}")
    print("-"*terminal_width)
    print("Pause/Play Video: space | FPS:", fps)
    print("-"*terminal_width)

def open_video():
    video_player = TerminalVideoPlayer(select_video(), 20)
    video_player.start()
    while video_player.is_playing:
        sleep(0.1)
    add_key_handler()

def add_key_handler():
    while True:
        if keyboard.is_pressed("o"):
            open_video()
            return
        elif keyboard.is_pressed("x"):
            exit(1)
            
class TerminalVideoPlayer(VideoPlayer):
    def display_frame(self):
        display_header(self.video, self.actual_fps)
        super().display_frame()
        
def main():
    initiate()

if __name__ == "__main__":
    main()