#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pcapng
from pcapng import FileScanner
import os
from IPython.display import display, clear_output
import time


# In[2]:


def separated_hex_values(packet):
    '''
    This function reads in a list of hexadecimal packet data, without spaces between each pair of characters,
    and separates each hexadecimal value and assings them to a list so that they can be iterated over within
    a loop for further processing.
    '''
    separated_hexadecimal_array = []
    packet_length = len(packet)
    i = 0
    j = 1
    for character in packet:
        if j < packet_length:
            separated_hexadecimal_array.append(packet[i]+packet[j])
            i += 2
            j += 2    
    return separated_hexadecimal_array
# Reads the raw hexadecimal data string for a packet and encodes it into a list of hexadecimal values.


# In[3]:


def hexadecimal_to_decimal(hexadecimal_array):
    '''
    This function reads the hexadecimal value list for a packet and converts each into decimal form.
    '''
    decimal_array = []
    for element in hexadecimal_array:
        decimal_array.append(int(element, 16))
    return decimal_array
# Converts the separated hexadecimal array into a decimal array.


# In[4]:


def decimal_converted_packet(packet):
    '''
    This function performs the operations for both the 'separated_hex_values' and 'convert_hexadecimal_to_decimal'
    functions on a packet.
    '''
    return hexadecimal_to_decimal(separated_hex_values(packet))
# Performs the function of the 'separated_hex_values' function and then performs the 'convert_hexadecimal_to_decimal' 
# function on the same data.


# In[5]:


def isolate_packet_pixel_data(packet_data):
    '''
    This function removes non-pixel data from the list of integer values. For science images, this means the first
    16 values are removed.
    '''
    converted_packet_data = decimal_converted_packet(packet_data)
    return converted_packet_data[58:]
# Returns a decimal array for the packet data excluding the first 16 elements, which do not correspond to science packet
# pixel data.


# In[6]:


def isolate_packet_data(packet_data):
    converted_packet_data = decimal_converted_packet(packet_data)
    return converted_packet_data[42:]

# The Wireshark capture files are 570 bytes in size. The pixel data are stored in the last 528 bytes of the capture.
# Therefore, I am subtracting the first 58 bytes of the capture file because they do not correspond to pixel data.
# This must be done in combination with the subtraction of the first 16 elements of each packet.


# In[7]:


def convert_integer_to_binary(integer):
    binary_array = []
    bit_number = 0
    quotient = integer
    
    while bit_number <= 7:
        binary_array.append(quotient%2)
        quotient = int(quotient/2)
        bit_number += 1

    return binary_array


# In[8]:


def convert_packet_array_to_8bit_binary(packet):
    packet_binary_array_8bit = []
    for element in isolate_packet_pixel_data(packet):
        packet_binary_array_8bit.append(convert_integer_to_binary(element))
                
    return packet_binary_array_8bit


# In[9]:


def convert_integer_to_binary(integer):
    binary_array = []
    bit_number = 0
    quotient = integer
    
    while bit_number <= 7:
        binary_array.append(quotient%2)
        quotient = int(quotient/2)
        bit_number += 1

    return binary_array


# In[10]:


def convert_packet_array_to_8bit_binary(packet):
    packet_binary_array_8bit = []
    for element in isolate_packet_pixel_data(packet):
        packet_binary_array_8bit.append(convert_integer_to_binary(element))
                
    return packet_binary_array_8bit


# In[11]:


def concatenate_pixel_data_streams(packet):
    even_array = []
    odd_array = []
    combined_array = []
    
    i = 0
    
    for element in convert_packet_array_to_8bit_binary(packet):
    
        if i%2 == 0:
            even_array.append(element)
        if i%2 == 1:
            odd_array.append(element)

        i += 1
    i = 0
    
    #even_array = even_array[::-1]
    #odd_array = odd_array[::-1]

    for element in even_array:
        combined_array.append(odd_array[i][::-1] + even_array[i][::-1])
        #  ** * * * ** * * Flipping the arrays and concatenating them in accordance with the Quabo packet interface information ******* * ** * ** * *

        i += 1
    
    return combined_array


# In[12]:


def convert_16bit_binary_to_integer(number):
    
    i = 15
    integer = 0
    
    for element in number:
        integer += (int(element)*(2**i))
        i -= 1
    
    return integer


# In[13]:


def concatenate_streams_and_convert_to_integer(packet):
    
    concatenated_array = []
    for element in concatenate_pixel_data_streams(packet):
        concatenated_array.append(convert_16bit_binary_to_integer(element))
        
    return concatenated_array


# In[14]:


def row_splitter(packet):
    
    image = []
    full_array = []
    counter = 0
    
    for element in concatenate_pixel_data_streams(packet):
        full_array.append(convert_16bit_binary_to_integer(element))
    row_array = []
    
    for element in full_array:
        if counter == 15:
            image.append(row_array)
            row_array.append(element)
            row_array = []
            counter = 0
        else:
            row_array.append(element)
            counter += 1
            
    return image

#creates a 2D array with 16 rows of 16 elements (pixel data to be plotted)


# In[15]:


def get_image_source_ip(packet):
    return str(decimal_converted_packet(packet)[26])+'.'+str(decimal_converted_packet(packet)[27])+'.'+str(decimal_converted_packet(packet)[28])+'.'+str(decimal_converted_packet(packet)[29])


# In[16]:


def image_plotter(image):
    if len(image.data) > 0:
        plt.title(str(image.name))
        plt.imshow(image.data)
        
        plt.show()
    #plt.close()


# In[17]:


def loading_old():
    
    complete = False
    
    while True:
        print("Loading |", end = "\r")
        time.sleep(0.25)
        #clear_output(wait=True)
        print("Loading /", end = "\r")
        time.sleep(0.25)
        #clear_output(wait=True)
        print("Loading —", end = "\r")
        time.sleep(0.25)
        #clear_output(wait=True)
        print("Loading \\", end = "\r")
        time.sleep(0.25)
        #clear_output(wait=True)
        
        if complete == True:
            return


# In[18]:


def loading_complete():
    return


# In[ ]:


def list_loading(list_input, counter):
    
    if counter == 0:
        print("Loading [....................]", end = "\r")
    if counter == len(list_input)/20:
        print("Loading [|...................]", end = "\r")
    if counter == 2*len(list_input)/20:
        print("Loading [||..................]", end = "\r")
    if counter == 3*len(list_input)/20:
        print("Loading [|||.................]", end = "\r")
    if counter == 4*len(list_input)/20:
        print("Loading [||||................]", end = "\r")
    if counter == 5*len(list_input)/20:
        print("Loading [|||||...............]", end = "\r")
    if counter == 6*len(list_input)/20:
        print("Loading [||||||..............]", end = "\r")
    if counter == 7*len(list_input)/20:
        print("Loading [|||||||.............]", end = "\r")
    if counter == 8*len(list_input)/20:
        print("Loading [||||||||............]", end = "\r")
    if counter == 9*len(list_input)/20:
        print("Loading [|||||||||...........]", end = "\r")
    if counter == 10*len(list_input)/20:
        print("Loading [||||||||||..........]", end = "\r")
    if counter == 11*len(list_input)/20:
        print("Loading [|||||||||||.........]", end = "\r")
    if counter == 12*len(list_input)/20:
        print("Loading [||||||||||||........]", end = "\r")
    if counter == 13*len(list_input)/20:
        print("Loading [|||||||||||||.......]", end = "\r")
    if counter == 14*len(list_input)/20:
        print("Loading [||||||||||||||......]", end = "\r")
    if counter == 15*len(list_input)/20:
        print("Loading [|||||||||||||||.....]", end = "\r")
    if counter == 16*len(list_input)/20:
        print("Loading [||||||||||||||||....]", end = "\r")
    if counter == 17*len(list_input)/20:
        print("Loading [|||||||||||||||||...]", end = "\r")
    if counter == 18*len(list_input)/20:
        print("Loading [||||||||||||||||||..]", end = "\r")
    if counter == 19*len(list_input)/20:
        print("Loading [|||||||||||||||||||.]", end = "\r")
    if counter == 20*len(list_input)/20-1:
        print("Loading Complete!", end = "\r")

