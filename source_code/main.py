from PIL import ImageDraw,ImageFont,Image
from audio import grab_audio, insert_audio
import cv2
import numpy as np
import math
import os

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
found = False
for i in os.listdir('./'):
    if fileName == i:
        found = True
if not found:
    print(f"No file called {fileName} found")
    exit()
chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
charlist=list(chars)
charlen=len(charlist)
interval=charlen/256
scale_factor=0.09
charwidth=10
charheight=10
while True:
    try:
        print("Type in the fps(frames per second) you want in the result video(will impact the time of the video)")
        print("Press ctrl+c to use the origonal video fps")
        fps=input(": ")
        if fps.isdecimal():
            break
    except KeyboardInterrupt:
        fps="ORIGINAL"
        break

print("")

try:
    video_type=input("Please choose a video type(enter for avi, ctrl+c for mp4)\n")
    if video_type == "":
        video_type = "avi"
except KeyboardInterrupt:
    video_type = "mp4"

while True:
    start_frame=input("Enter a start frame if you want to skip frames, leave blank for no: ")
    if start_frame == "":
        start_frame = None
        break
    elif start_frame.isdecimal():
        start_frame = int(start_frame)
        break
    else:
        print("Wrong value, please try again")

def get_char(i):
    return charlist[math.floor(i*interval)]

try:
    cap = cv2.VideoCapture(fileName)
except AttributeError:
    print(f"File {fileName} does not exist(please include file extension)")

if fps == "ORIGINAL":
    fps = cap.get(cv2.CAP_PROP_FPS)

def skip_frame_create_vid(amount: int, frames_count: int):
    numb = 0 - 1
    Font=ImageFont.truetype('C:\\Windows\\Fonts\\lucon.ttf',15)
    while True:
        try:
            numb += 1
            if not numb < amount:
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
                print(f"Current Frame: {numb} | {frames_count}", end="\r")
                cv2.imwrite(f"{numb}.png",open_cv_image)
        except AttributeError:
            break

if not start_frame is None:
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
frames_count = math.floor(cap.get(cv2.CAP_PROP_FRAME_COUNT))
Font=ImageFont.truetype('C:\\Windows\\Fonts\\lucon.ttf',15)
numb = 0 - 1
frame_num = -1
os.chdir(cwd)
try:
    os.chdir('./frames')
except FileNotFoundError:
    os.mkdir('./frames')
    os.chdir('./frames')
print("Generating frames(This could took a wile)...")
print("Current Frame: ", end="\r")
if start_frame is None:
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
            print(f"Current Frame: {numb} | {frames_count - 1}", end="\r")
            cv2.imwrite(f"{numb}.png",open_cv_image)
            frame_num += 1
        except AttributeError:
            break
else:
    skip_frame_create_vid(start_frame, frames_count)

print(f"Done creating frames, total count {frame_num}")
cap.release()

os.chdir(cwd)

print(f"Making vid... | {video_type}")
img_array = []
for i in range(len(os.listdir('./frames'))):
    img = cv2.imread(f"./frames/{i}.png")
    height, width, layers = img.shape
    size_ = (width, height)
    img_array.append(img)
    print(f'{i}.png', end="\r")

print("Done fetching frames")
size = size_
if video_type == "avi":
    out = cv2.VideoWriter('result.avi', cv2.VideoWriter_fourcc(*'DIVX'), int(fps), size_)
elif video_type == "mp4":
    out = cv2.VideoWriter('result.mp4', cv2.VideoWriter_fourcc(*'mp4v'), int(fps), size_)
print("compiling...")

for i in range(len(img_array)):
    out.write(img_array[i])
    print(f'compiling frame {i} | {len(img_array)}', end="\r")
print("Done creating ascii video")
out.release()
nfile = -1
os.chdir('./frames')
for file in os.listdir('./'):
    nfile += 1
    os.remove(str(nfile) + '.png')
os.chdir(cwd)
grab_audio(fileName)
print("Audio generated")
os.rmdir('./frames')
try:
    input("Press enter to exit, or press ctrl+c to insert the audio into the result video")
except KeyboardInterrupt:
    if video_type == "avi":
        insert_audio('.avi')
    elif video_type == "mp4":
        insert_audio('.mp4')