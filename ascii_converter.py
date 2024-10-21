import warnings
warnings.filterwarnings("ignore")
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from blessed import Terminal 

def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp ")]
    )
    root.destroy()
    return file_path

def standardize_size(im, size):
    scale = im.size[1] / size
    return int(im.size[0] / scale), int(im.size[1] / scale)

def convert_rgb_to_ansi(rgb):
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    return f"\033[38;2;{r};{g};{b}m"

def convert_to_colors(im, size):
    im = im.resize(standardize_size(im, size))
    colors = []
    rgb_data = im.getdata()
    i = 0
    j = 0
    row = []
    while i < im.size[1]:
        row.append(convert_rgb_to_ansi(rgb_data[j]))
        j += 1
        if j % im.size[0] == 0:
            i += 1
            colors.append(row)
            row = []
    return colors
        
def convert_to_ascii(im, size):
    im = im.convert("L")
    im = im.resize(standardize_size(im, size))
    ascii_art = []
    image_data = im.getdata()
    i = 0
    j = 0
    row = []
    while i < im.size[1]:
        row.append(convert_pixel_to_ascii(image_data[j]))
        j += 1
        if j % im.size[0] == 0:
            i += 1
            ascii_art.append(row)

            row = []
    return ascii_art

def convert_pixel_to_ascii(pixel):
    if pixel == 0:
        return " "
    elif pixel > 0 and pixel < 36:
        return "."
    elif pixel > 36 and pixel < 72:
        return "-"
    elif pixel > 72 and pixel < 108:
        return ":"
    elif pixel > 108 and pixel < 144:
        return "o"
    elif pixel > 144 and pixel < 180:
        return "x"
    elif pixel > 180 and pixel < 216:
        return "#"
    return "@"

def write_to_outfile(ascii_art):
    file = open("outfile.txt", "w")
    
    for i in range(len(ascii_art)):
        for j in range(len(ascii_art[i])):
            file.write(ascii_art[i][j] + " ")
        file.write("\n")
    file.close()

def display_image(ascii_art, colors):
    term = Terminal()
    whitespace = int((term.width - len(ascii_art[0])*2)/2)
    print(" " * whitespace, end = "")
    for i in range(len(ascii_art)):
        for j in range(len(ascii_art[i])):
            print(colors[i][j], end = "")
            print(ascii_art[i][j] + " ", end = "")
        print("\n" + " " * whitespace, end = "")
        
def get_ascii_art(im, size):
    ascii_art = convert_to_ascii(im, size)
    colors = convert_to_colors(im, size)
    return ascii_art, colors

def main():
    image_path = select_image()
    if image_path:
        print(f"Selected image: {image_path}")
    else:
        print("No image selected.")
    im = Image.open(image_path)
    size = int(input("Enter an integer for the size of the art: "))
    ascii_art, colors = get_ascii_art(im, size)
    display_image(ascii_art, colors)

if __name__ == "__main__":
    main()