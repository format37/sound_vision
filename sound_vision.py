# opencv install ubuntu:
# https://stackoverflow.com/questions/37188623/ubuntu-how-to-install-opencv-for-python3
import cv2
# pip install pyrealsense2
import pyrealsense2 as rs
import numpy as np

width = 640
height = 480
new_width = 7
new_height = 7

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, width, height, rs.format.z16, 30)
profile = pipeline.start(config)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
real_values = []
sum_values = []

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        depth_data = depth.get_data()
        depth_image = 1-np.asanyarray(depth_data)
        resized_depth_image = cv2.resize(depth_image, (new_width, new_height), interpolation=cv2.INTER_AREA)        
        cv2.namedWindow('depth', cv2.WINDOW_NORMAL)
        cv2.imshow('depth', resized_depth_image)
        cv2.waitKey(1)    
        
finally:
    # Stop streaming
    pipeline.stop()
