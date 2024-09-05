import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pcapng
from pcapng import FileScanner
from pcapng.blocks import EnhancedPacket
import os
from IPython.display import display, clear_output
import time
import json
import progressbar

start_time = time.time()

print("\n")
#path = input('Please specify the location of your Wireshark capture file: ')

# Declares the list that will hold the hexadecimal data for each packet.

###########################################################
path = "C:/Pause_onskyph0pe_ima0pe__20230426_040905.pcapng"
#path = "/home/brett/Data_for_pynoseti/Pause_onskyph0pe_ima0pe__20230426_040905.pcapng"
# Specifies the path to the file to be used in processing.
# Don't forget to change when using a new file.
###########################################################

packet_array = []
# Declares the list that will hold the hexadecimal data for each packet.

import datetime
print("Reading selected file...")
print("\n")

with open(path, 'rb') as file:
    scanner = FileScanner(file)
    for block in scanner:
        if isinstance(block, pcapng.blocks.EnhancedPacket):
            # Checks, while iterating over each block, if it is of the EnchancedPacket data type. If so,
            # its hexadecimal packet data is stored in 'packet_array'.
            packet = block.packet_data
            hex_data = packet.hex()
            packet_array.append(hex_data)

class Quabo:
    def __init__(self, address, data):
        self.address = address
        self.data = data

class Telescope:
    def __init__(self, name, dome, quabo_array, data):
        self.name = name
        self.dome = dome
        self.quabo_array = quabo_array
        self.data = data

with open('config.json', 'r') as file:
    config = json.load(file)
telescope_list = []
quabo_list = []
for setting in config['telescopes']:
    telescope = Telescope(name = setting['identifier'],
                          dome = setting['dome'], 
                          quabo_array = setting['quabo_array'],
                          data = [[],[],[],[]]
                          )
    telescope_list.append(telescope)
    for address in telescope.quabo_array:
        if address not in quabo_list:
            quabo_list.append(Quabo(address, []))


print("Converting hexidecimal data to photon intensity...")
print("\n")

class Packet:
    def __init__(self, name, number, source_ip, data):
        self.name = name
        self.number = number
        self.source_ip = source_ip
        self.data = data

from functions import *

print('Recognized telescopes:', '\n')
for telescope in telescope_list:
    print(telescope.name+', ')
print('\n')
telescope_choice = input('Which telescope would you like to playback data for?\nSkip this prompt by pressing enter and process the entire file.\nEnter the integer corresponding to one of the telescopes: ')

if telescope_choice == '1':
    i=0
    bar = progressbar.ProgressBar(max_value=len(packet_array))
    for packet in packet_array:
        j=0
        for address in telescope_list[0].quabo_array:
            if get_image_source_ip(packet) == address:
                quabo_list[j].data.append(packet)
        bar.update(i)
        i+=1

elif telescope_choice == '2':
    i=0
    bar = progressbar.ProgressBar(max_value=len(packet_array))
    for packet in packet_array:
        j=0
        for address in telescope_list[1].quabo_array:
            if get_image_source_ip(packet) == address:
                quabo_list[j].data.append(packet)
        bar.update(i)
        i+=1

elif telescope_choice == '3':
    i=0
    bar = progressbar.ProgressBar(max_value=len(packet_array))
    for packet in packet_array:
        j=0
        for address in telescope_list[2].quabo_array:
            if get_image_source_ip(packet) == address:
                quabo_list[j].data.append(packet)
        bar.update(i)
        i+=1

else:
    print('\n***under construction***\n')


exit()

image_list = []
i=0
for element in range(len(telescope_list[0].quabo_array[0].datastream)-1):
    image_list.append(quabo_image_compiler(
        telescope_list[0].quabo_array[0].datastream[i],
        telescope_list[0].quabo_array[1].datastream[i],
        telescope_list[0].quabo_array[2].datastream[i],
        telescope_list[0].quabo_array[3].datastream[i]
    ))
    i+=1





end_time = time.time()
print(end_time-start_time)

fig, ax = plt.subplots()

matrix = np.zeros((10, 10))
im = ax.imshow(image_list[0], cmap='viridis', vmin=0)
title = ax.set_title(telescope_list[0].quabo_array[0].address)


def animate(i):
    im.set_array(image_list[i])
    title.set_text(telescope_list[0].quabo_array[0].address)

    return [im, title]

animation_test = animation.FuncAnimation(fig, animate, frames=len(telescope_list[0].quabo_array[0].datastream), interval=5, blit=False)


plt.show()