#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


print("\n")
#path = input('Please specify the location of your Wireshark capture file: ')


# In[3]:


#print(path)


# In[4]:


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
            #timestamp_seconds = block.timestamp_high
            #timestamp_nanoseconds = block.timestamp_low
            #timestamp = timestamp_seconds + timestamp_nanoseconds/int(1e6)
            #leap_seconds = 37

            #utc_timestamp = (timestamp_seconds - leap_seconds) + timestamp_nanoseconds / 1_000_000_000

            #print(f"Packet timestamp: {utc_timestamp} seconds")


# In[5]:


#file_packet_integer_data = []

#for element in packet_array:
#    file_packet_integer_data.append(isolate_packet_pixel_data(element))


# In[6]:




class Image:
    def __init__(self, name, number, source_ip, data):
        self.name = name
        self.number = number
        self.source_ip = source_ip
        self.data = data
        #self.timestamp = timestamp





# In[7]:


from functions import *

file_packet_intensity_data = []
image_list = []
object_list = []

counter = 0


class Quabo:
    def __init__(self, telescope, quadrant, address, datastream):
        self.telescope = telescope
        self.quadrant = quadrant
        self.address = address
        self.datastream = datastream

quabo_1_1 = Quabo('telescope_1', 1, '192.168.1.4', np.array([]))
quabo_1_2 = Quabo('telescope_1', 2, '192.168.1.5', np.array([]))
quabo_1_3 = Quabo('telescope_1', 3, '192.168.1.6', np.array([]))
quabo_1_4 = Quabo('telescope_1', 4, '192.168.1.7', np.array([]))
#####
quabo_2_1 = Quabo('telescope_2', 1, '192.168.1.12', np.array([]))
quabo_2_2 = Quabo('telescope_2', 2, '192.168.1.13', np.array([]))
quabo_2_3 = Quabo('telescope_2', 3, '192.168.1.14', np.array([]))
quabo_2_4 = Quabo('telescope_2', 4, '192.168.1.15', np.array([]))
#####
quabo_3_1 = Quabo('telescope_3', 1, '192.168.3.248', np.array([]))
quabo_3_2 = Quabo('telescope_3', 2, '192.168.3.249', np.array([]))
quabo_3_3 = Quabo('telescope_3', 3, '192.168.3.250', np.array([]))
quabo_3_4 = Quabo('telescope_3', 4, '192.168.3.251', np.array([]))

class Telescope:
    def __init__(self, name, dome, quabo_array):
        self.name = name
        self.dome = dome
        self.quabo_array = quabo_array

telescope_1 = Telescope('telescope_1', 'Astrograph', [quabo_1_1, quabo_1_2, quabo_1_3, quabo_1_4])
telescope_2 = Telescope('telescope_2', 'Astrograph', [quabo_2_1, quabo_2_2, quabo_2_3, quabo_2_4])
telescope_3 = Telescope('telescope_3', 'Barnard', [quabo_3_1, quabo_3_2, quabo_3_3, quabo_3_4])

telescope_list = [telescope_1, telescope_2, telescope_3]

print("Converting hexidecimal data to photon intensity...")
print("\n")

for packet in packet_array:
    
    file_packet_intensity_data.append(row_splitter(packet))
    image_list.append('image'+str(counter))
    image_object = Image('image'+str(counter),
                         counter, get_image_source_ip(packet),
                         file_packet_intensity_data[counter],
                         #block.timestamp_high + block.timestamp_low/int(1e6),
                         )
    object_list.append(image_object)

    for telescope in telescope_list:
        for quabo in telescope.quabo_array:
            if image_object.source_ip == quabo.address:
                quabo.datastream = np.append(quabo.datastream, row_splitter(packet))


    
    list_loading(packet_array, counter)
    
    counter += 1




#for telescope in telescope_list:
#        if image_object.source_ip in telescope.quabo_addresses:
#            telescope.datastream = np.append(telescope.datastream, image_object)














# In[ ]:


#object_list = []
#
#counter = 0
#
#for image in packet_array:
#    image_object = Image('image'+str(counter), counter, get_image_source_ip(image), file_packet_intensity_data[counter])
#    object_list.append(image_object)
#    counter += 1


# In[ ]:


ip_list = []

for element in object_list:
    if element.source_ip not in ip_list:
        ip_list.append(element.source_ip)
        
print("\n")
print("Retrieving source IP addresses...")


# In[ ]:


initial_list = []

for element in ip_list:
    new_list = [element]
    initial_list.append(new_list)

address_dictionary = {key: [] for key in ip_list}

for element in object_list:
    for key in address_dictionary:
        if element.source_ip == key:
            address_dictionary[key].append(element.name)


# In[ ]:


specific_ip_list = []


for element in object_list:
    if element.source_ip == '192.168.0.4':
        specific_ip_list.append(element)






#telescope_list[0].quabo_array[0].datastream



fig, ax = plt.subplots()

matrix = np.zeros((10, 10))
im = ax.imshow(telescope_list[0].quabo_array[0].datastream[0], cmap='viridis', vmin=0)
title = ax.set_title(telescope_list[0].quabo_array[0].address)


def animate(i):

    im.set_array(telescope_list[0].quabo_array[0].datastream[i])
    title.set_text(telescope_list[0].quabo_array[0].address)

    return [im, title]

animation_test = animation.FuncAnimation(fig, animate, frames=len(telescope_list[0].quabo_array[0].datastream), interval=200, blit=False)

#plt.imshow(object_list[900].data)
plt.show()


exit()



counter = 0
for element in object_list:
    
    if element.source_ip == '192.168.3.251':
        #print(element.source_ip)
        image_plotter(element)

        time.sleep(0.0167)
        clear_output(wait=True)

        counter += 1


# In[ ]:




