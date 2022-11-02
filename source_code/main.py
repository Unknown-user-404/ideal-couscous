from PIL import ImageDraw,ImageFont,Image
import cv2
import numpy as np
import math
import os
import glob

cwd = os.getcwd()
try:
    os.chdir('./input')
except FileNotFoundError:
    os.mkdir('./input')
    os.chdir('./input')

fileName=input("Type in the video name in the input folder(if no .mp4 video please insert one): ")
if not '.' in fileName:
    print("Please include file extension")
    exit()
chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
charlist=list(chars)
charlen=len(charlist)
interval=charlen/256
scale_factor=0.09
charwidth=10
charheight=10
while True:
    fps=input("Type in the fps(frames per second) you want in the result video(will impact the time of the video): ")
    if fps.isdecimal():
        break

def get_char(i):
    return charlist[math.floor(i*interval)]

try:
    cap = cv2.VideoCapture(fileName)
except AttributeError:
    print(f"File {fileName} does not exist(please include file extension)")

Font=ImageFont.truetype('C:\\Windows\\Fonts\\lucon.ttf',15)
numb = 0 - 1
os.chdir(cwd)
try:
    os.chdir('./frames')
except FileNotFoundError:
    os.mkdir('./frames')
    os.chdir('./frames')
print("Generating frames(This could took a wile)...")
print("Current Frame: ", end="\r")
while True:
    try:
        numb += 1
        _, img=cap.read()
        img=Image.fromarray(img)

        width,height=img.size
        img=img.resize((int(scale_factor*width),int(scale_factor*height*(charwidth/charheight))),Image.Resampling.NEAREST)
        width,height=img.size
        pixel=img.load()
        outputImage=Image.new("RGB",(charwidth*width,charheight*height),color=(0,0,0))
        dest=ImageDraw.Draw(outputImage)

        for i in range(height):
            for j in range(width):
                r,g,b=pixel[j,i]
                h=int(0.299*r+0.587*g+0.114*b)
                pixel[j,i]=(h,h,h)
                dest.text((j*charwidth,i*charheight),get_char(h),font=Font,fill=(r,g,b))

        open_cv_image=np.array(outputImage)
        key=cv2.waitKey(1)
        if key == ord("q"):
            break
        print(f"Current Frame: {numb}", end="\r")
        cv2.imwrite(f"{numb}.png",open_cv_image)
    except AttributeError:
        break
print("Done creating frames")
cap.release()

os.chdir(cwd)

print("Making vid...")
img_array = []
for i in range(len(os.listdir('./frames'))):
    img = cv2.imread(f"./frames/{i}.png")
    height, width, layers = img.shape
    size_ = (width, height)
    img_array.append(img)
    print(f'{i}.png', end="\r")

print("Done fetching frames")
size = size_
out = cv2.VideoWriter('result.avi', cv2.VideoWriter_fourcc(*'DIVX'), int(fps), size_)
print("compiling...")

for i in range(len(img_array)):
    out.write(img_array[i])
    print(f'compiling frame {i} | {len(img_array)}', end="\r")
print("Done creating ascii video")
out.release()
