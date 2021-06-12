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
from pygame.mixer import Sound, get_init, pre_init


class Note(Sound):

    def __init__(self, frequency, volume=.1):
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)
        self.chan1 = pygame.mixer.Channel(0)
        self.chan1.set_volume(1.0, 0.0)
        self.chan2 = pygame.mixer.Channel(1)
        self.chan2.set_volume(0.0, 1.0)

    def build_samples(self):
        period = int(round(get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples

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
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
real_values = []
sum_values = []

fs = int(44100)
frequences = [j for j in range(10,10*(new_width+2),10)]
max_depth = 3000

pre_init(44100, -16, 2, 1024)
pygame.init()
sound_time = int(0.03*1000/2)

try:
    while True:
        resized_depth_image = get_image(pipeline, new_width, new_height)
        # limit max depth
        resized_depth_image = max_depth-np.where((resized_depth_image>max_depth), max_depth, resized_depth_image)
        # generate sound
        l = resized_depth_image[0][0]/7
        l = int(l if l>10 else 10)
        r = resized_depth_image[0][1]/7
        r = int(r if r>10 else 10)
        left_note = Note(l)
        left_note.play(sound_time)
        right_note = Note(r)
        right_note.play(sound_time)
        #show image
        cv2.namedWindow('depth', cv2.WINDOW_NORMAL)
        cv2.imshow('depth', resized_depth_image*10)
        cv2.waitKey(1)
        
finally:
    # Stop streaming
    pipeline.stop()
