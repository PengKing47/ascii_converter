import warnings
warnings.filterwarnings("ignore")
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    root.destroy()
    return file_path

def trim_image(im_data):
    i = 0
    while i < len(im_data):
        all_zeroes = True
        for j in range(len(im_data[i])):
            if im_data[i][j] != 0:
                all_zeroes = False
                break
        if all_zeroes:
            im_data.pop(i)
            i -= 1
        i += 1

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
        

def convert_to_pixels(im, size):
    im = im.convert("L")
    im = im.resize(standardize_size(im, size))
    pixels = []
    image_data = im.getdata()
    i = 0
    j = 0
    row = []
    while i < im.size[1]:
        row.append(image_data[j])
        j += 1
        if j % im.size[0] == 0:
            i += 1
            pixels.append(row)
            row = []
    return pixels

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
    
def convert_image_data_to_ascii(im_data):
    ascii_art = []
    for i in range(len(im_data)):
        row = []
        for j in range(len(im_data[i])):
            ascii_character = convert_pixel_to_ascii(im_data[i][j])
            row.append(ascii_character)
        ascii_art.append(row)
    return ascii_art

def write_to_outfile(ascii_art):
    file = open("outfile.txt", "w")
    
    for i in range(len(ascii_art)):
        for j in range(len(ascii_art[i])):
            file.write(ascii_art[i][j] + " ")
        file.write("\n")
    file.close()

def display_image(ascii_art, colors):
    for i in range(len(ascii_art)):
        for j in range(len(ascii_art[i])):
            print(colors[i][j], end = "")
            print(ascii_art[i][j] + " ", end = "")
        print()

def get_ascii_art(im, size):
    pixels = convert_to_pixels(im, size)
    colors = convert_to_colors(im, size)
    return convert_image_data_to_ascii(pixels), colors

if __name__ == "__main__":
    image_path = select_image()
    if image_path:
        print(f"Selected image: {image_path}")
    else:
        print("No image selected.")
    im = Image.open(image_path)
    size = int(input("Enter an integer for the size of the art: "))
    ascii_art, colors = get_ascii_art(im, size)
    display_image(ascii_art, colors)