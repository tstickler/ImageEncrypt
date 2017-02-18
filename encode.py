###############################################################################
# Programmer: Tyler Stickler                                                  #
# File name: encode.py                                                        #
# Description: Encodes a user message into an image.                          #
###############################################################################

import math
import sys


###############################################################################
# This function inputs data into an image. It grabs a pixel at a certain xy   #
# coordinate, starting at the bottom right, converts its RGB value into       #
# binary, then modifies the least significant bit to hide our data. This      #
# continues until the whole message is encoded.                               #
#                                                                             #
# Function input: Image object, message to encode, output file                #
# Function returns: None                                                      #
###############################################################################
def encode_message(im, user_message, output_file):
    # User defined message to encrypt
    message = user_message

    # Determines the width and height of the image
    width, height = im.size
    pixels_in_image = width * height

    # Determines message length, zero fills it up to 33
    message_length = len(message)
    binaryMsgLength = bin(message_length)[2:].zfill(33)
    pixels_needed = math.ceil((message_length * 8) / 3)

    # Determines if their are enough pixels in the image to add the message
    if pixels_needed + 11 > pixels_in_image:
        print("Sorry, your image is too small to hold this big of a message.")
        sys.exit()

    # Creates an array to hold binary values of the letters
    messageArray = []

    # Changes each letter to binary, adds it to the message array, and converts
    # it into a string
    for letter in message:
        binaryVal = bin(ord(letter))[2:].zfill(8)
        messageArray.append(binaryVal)
    binaryMessage = "".join(messageArray)

    # The width and height modifiers are used to move us between pixels
    width_mod = 1
    height_mod = 1

    # Determines how many times we need to loop
    times_to_loop = pixels_needed + 11

    # Used as indexes
    length_counter = 32
    letter_counter = 0

    # Loop through and modify the pixels until task is complete
    while times_to_loop > 0:
        # Gets the pixel's RGB values at the current XY coordinate
        r, g, b = im.getpixel((width-width_mod, height-height_mod))

        # Converts the RGB values to their binary representation
        binary_red = list(bin(r)[2:].zfill(8))
        binary_green = list(bin(g)[2:].zfill(8))
        binary_blue = list(bin(b)[2:].zfill(8))

        # Modifies the least significant bit of the RGB value
        if length_counter > 0:
            # Modify the RGB values to insert message length
            binary_red[7] = binaryMsgLength[length_counter]
            length_counter -= 1
            binary_red = int("".join(binary_red), 2)

            binary_green[7] = binaryMsgLength[length_counter]
            length_counter -= 1
            binary_green = int("".join(binary_green), 2)

            binary_blue[7] = binaryMsgLength[length_counter]
            length_counter -= 1
            binary_blue = int("".join(binary_blue), 2)

            im.putpixel((width - width_mod, height - height_mod),
                        (binary_red, binary_green, binary_blue))
        elif times_to_loop > 0:
            # Modify the RGB values to insert our message
            if letter_counter < message_length * 8:
                binary_red[7] = binaryMessage[letter_counter]
                letter_counter += 1

            if letter_counter < message_length * 8:
                binary_green[7] = binaryMessage[letter_counter]
                letter_counter += 1

            if letter_counter < message_length * 8:
                binary_blue[7] = binaryMessage[letter_counter]
                letter_counter += 1

            binary_red = int("".join(binary_red), 2)
            binary_green = int("".join(binary_green), 2)
            binary_blue = int("".join(binary_blue), 2)

            im.putpixel((width - width_mod, height - height_mod),
                        (binary_red, binary_green, binary_blue))

        # Move us to the next pixel in the row
        width_mod += 1
        times_to_loop -= 1

        # If we hit the left side of the picture, move up a row
        if width_mod-1 == width:
            height_mod += 1
            width_mod = 1

    # Save our encoded file with the user specified name and png format
    im.save("{}.png".format(output_file))

