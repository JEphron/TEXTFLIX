import base64
from PIL import Image
from io import BytesIO
import math
import numpy as np
import sys
from colorama import init
from colorama import Fore, Back, Style
init()
# 
# print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim text')
# print(Style.RESET_ALL)

def range_map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

chars = ['M', '@', 'F', 'P', '2', 'Q', 'O', '7', 'l', ';', ',', '.', ' ']

img = Image.open('accept1.jpg')
print img.size
width, height = img.size
width, height = width/2, height/4
img = img.resize((width, height), Image.ANTIALIAS)

img_array = np.array(img)

def f(x):
    lightness = int(x[0]) + int(x[1]) + int(x[2])
    index = int(range_map(lightness, 0, 255*3, 0, len(chars)-1))
    return chars[index]

img_array = np.apply_along_axis(f, 2, img_array)


outstring = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
print outstring+'\n'.join(''.join(str(cell) for cell in row) for row in img_array)


# for y in range(0, height):
#     for x in range(0, width):
#         sys.stdout.write(img_array[x][y])
#     sys.stdout.write('\n')    
