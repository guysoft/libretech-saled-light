#!/usr/bin/env python3
import sys
import time
import random
import os
from pathlib import Path
from configparser import ConfigParser

FRAME_SPEED = 0.07

parser = ConfigParser()
with open(sys.argv[1]) as stream:
    parser.read_string("[top]\n" + stream.read())
    config = parser["top"]

def shift(byte_array):
    # Shift entire bytearray left by one byte
    if len(byte_array) > 1:
        first_byte = byte_array[0]
        shifted_array = byte_array[1:] + bytearray([first_byte])
    else:
        # For single-byte arrays, no shift needed
        shifted_array = byte_array
    return shifted_array

def shift_led(byte_array):
    # Shift left a led, which is three bytes
    return shift(shift(shift(byte_array)))

def random_led_colors(length, min_value=0xfe, max_value=0xff):
    # Ensure min_value is less than or equal to max_value
    if min_value > max_value:
        raise ValueError("min_value must be less than or equal to max_value")
    
    # Generate random bytes within the specified range
    return bytearray(random.randint(min_value, max_value) for _ in range(length))

frame_width =  int(config["SALED_PANEL_WIDTH"])
frame_height = 1

frame_pixel_count = frame_width * frame_height
frame_output_pixel_size = 3

# pick a pattern you want from the optoins below by uncommenting it
# frame_output_data = bytearray(b'\xff' + b'\xff' + b'\xfe') +  bytearray(b'\xff' + b'\xff' b'\xff') * (frame_pixel_count-1)
frame_output_data = random_led_colors(frame_pixel_count * frame_output_pixel_size)


while True:
    time.sleep(FRAME_SPEED)
    frame_output_data = shift_led(frame_output_data)
    sys.stdout.buffer.write(frame_output_data)
    sys.stdout.flush()


