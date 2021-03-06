###############################################################################
# Programmer: Tyler Stickler                                                  #
# File name: decode.py                                                        #
# Description: Decodes a user message from an image.                          #
###############################################################################

import math


###############################################################################
# This function extracts data from an image. It grabs a pixel at a certain xy #
# coordinate, starting at the bottom right, determines the length and content #
# of the message by checking the least significant bit of each RGB value and  #
# translates it into a readable string.                                       #
#                                                                             #
# Function input: Image object                                                #
# Function returns: Decoded message                                           #
###############################################################################
def decode_message(im):
    # Determines the width and height of the image
    width, height = im.size

    # The width and height modifiers are used to move us between pixels
    width_mod = 1
    height_mod = 1

    # The first 11 pixels we'll look at hold the length of our message
    times_to_loop = 11

    # Used as index
    count = 0

    # Holds the least significant bit of the RGB values for message length
    length = []

    # This while loop handles the length of the message
    while times_to_loop > 0:
        # Gets the RGB value at a given XY coordinate
        r, g, b = im.getpixel((width - width_mod, height - height_mod))

        # Converts the RGB values to binary
        binary_red = list(bin(r)[2:].zfill(8))
        count += 1

        binary_green = list(bin(g)[2:].zfill(8))
        count += 1

        if count < 32:
            binary_blue = list(bin(b)[2:].zfill(8))
            count += 1

        # Adds the value to our list
        length.append(binary_red[7])
        length.append(binary_green[7])
        if count < 32:
            length.append(binary_blue[7])

        # Move us to the next pixel in the row
        width_mod += 1
        times_to_loop -= 1

        # If we hit the left side of the picture, move up a row
        if width_mod - 1 == width:
            height_mod += 1
            width_mod = 1

    # Converts our length to an integer to perform arithmetic
    num_of_bits_in_msg = int("".join(length), 2)

    # Determine the number of pixels to look at for our message
    times_to_loop = math.ceil(num_of_bits_in_msg/3)

    # Counter to determine if we have reached our total bits
    counter = 0

    # Array to hold message bits
    bits_message = []

    # This while loop handles the contents of the message
    while times_to_loop > 0:
        # Determines which pixel we are at
        pixel_x = width - width_mod
        pixel_y = height - height_mod

        # Gets the RGB value at a given xy coordinate
        r, g, b = im.getpixel((pixel_x, pixel_y))

        # Converts the RGB values to binary
        binary_red = list(bin(r)[2:].zfill(8))
        binary_green = list(bin(g)[2:].zfill(8))
        binary_blue = list(bin(b)[2:].zfill(8))

        # Here we add the bits of the message to our list. Sometimes,
        # we'll want to stop after the red or green value in order
        # not to grab values unrelated to our message. These if
        # statements allow us to stop if our counter reaches the
        # number of bits in our message.
        if counter < num_of_bits_in_msg:
            bits_message.append(binary_red[7])
            counter += 1
        if counter < num_of_bits_in_msg:
            bits_message.append(binary_green[7])
            counter += 1
        if counter < num_of_bits_in_msg:
            bits_message.append(binary_blue[7])
            counter += 1

        # Move us to the next pixel in the row
        width_mod += 1
        times_to_loop -= 1

        # If we hit the left side of the picture, move up a row
        if width_mod - 1 == width:
            height_mod += 1
            width_mod = 1

        # If we ever the leave the image, stop trying to look for information
        if pixel_x == -1 or pixel_y == -1:
            break

    # Decoded bits are joined into groups of 8, turned into a character based
    # off of their ascii value, then added to the decoded message list
    decoded_message = []
    i = 0
    while i < num_of_bits_in_msg:
        decoded_message.append((chr(int("".join(bits_message[i:i+8]), 2))))
        i += 8

    # Joins our list so it can be displayed as a string
    decoded_message = "".join(decoded_message)
    return decoded_message
