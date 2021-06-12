# opencv install ubuntu:
# https://stackoverflow.com/questions/37188623/ubuntu-how-to-install-opencv-for-python3
import cv2
# pip install pyrealsense2
import pyrealsense2 as rs
import numpy as np
import math
from array import array
from time import sleep
# pip install pygame
import pygame
#from pygame.mixer import Sound, get_init, pre_init
import pysine

def get_image(pipeline, new_width, new_height):
    frames = pipeline.wait_for_frames()
    depth = frames.get_depth_frame()
    depth_data = depth.get_data()
    depth_image = np.asanyarray(depth_data)[:,30:]
    return cv2.resize(depth_image, (new_width, new_height), interpolation=cv2.INTER_AREA)

width = 640
height = 480
#new_width = 7
#new_height = 7
new_width = 2
new_height = 1
sound_mask_left = np.array([list(reversed([(x+1)/new_width for x in range(new_width)])) for y in range(new_height)])/2
sound_mask_right = np.array([[(x+1)/new_width for x in range(new_width)] for y in range(new_height)])/2

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, width, height, rs.format.z16, 30)
profile = pipeline.start(config)
max_depth = 3000

sampleRate = 44100
freq = 440
pygame.mixer.init(44100,-16,2,512)

try:
    while True:
        resized_depth_image = get_image(pipeline, new_width, new_height)
        # limit max depth
        #resized_depth_image = max_depth-np.where((resized_depth_image>max_depth), max_depth, resized_depth_image)
        # generate sound
        l = resized_depth_image[0][0]/1100
        r = resized_depth_image[0][1]/1100
        arr2 = np.array([[
            4096 * np.sin(2.0 * np.pi * freq * x / sampleRate / l ),
            4096 * np.sin(2.0 * np.pi * freq * x / sampleRate / r ),
        ] for x in range(0, sampleRate)]).astype(np.int16)

        try:
            sound.stop()
        except:
            pass
        sound = pygame.sndarray.make_sound(arr2)
        sound.play(-1)
        #show image
        cv2.namedWindow('depth', cv2.WINDOW_NORMAL)
        cv2.imshow('depth', resized_depth_image*10)
        cv2.waitKey(1)
        
finally:
    # Stop streaming
    pipeline.stop()
