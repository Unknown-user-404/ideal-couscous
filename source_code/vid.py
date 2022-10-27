import glob
import cv2
import numpy as np
import time
import os

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
out = cv2.VideoWriter('result.avi', cv2.VideoWriter_fourcc(*'DIVX'), 25, size_)
print("compiling...")

for i in range(len(img_array)):
    out.write(img_array[i])
    print(f"{i} | {len(img_array)}", end="\r")
print("Done")
out.release()