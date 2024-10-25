import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label, center_of_mass
from datetime import datetime

class Quabo:
    def __init__(self, address, data):
        self.address = address
        self.data = data

class Telescope:
    def __init__(self, name, dome, quabo_addresses, data):
        self.name = name
        self.dome = dome
        self.quabo_addresses = quabo_addresses
        self.data = data

class Image:
    def __init__(self, data, timestamp, dome):
        self.data = data
        self.timestamp = timestamp
        self.dome = dome

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

def hexadecimal_to_decimal(hexadecimal_array):
    '''
    This function reads the hexadecimal value list for a packet and converts each into decimal form.
    '''
    decimal_array = []
    for element in hexadecimal_array:
        decimal_array.append(int(element, 16))
    return decimal_array
# Converts the separated hexadecimal array into a decimal array.

def decimal_converted_packet(packet):
    '''
    This function performs the operations for both the 'separated_hex_values' and 'convert_hexadecimal_to_decimal'
    functions on a packet.
    '''
    return hexadecimal_to_decimal(separated_hex_values(packet))
# Performs the function of the 'separated_hex_values' function and then performs the 'convert_hexadecimal_to_decimal' 
# function on the same data.

def isolate_packet_pixel_data(packet_data):
    '''
    This function removes non-pixel data from the list of integer values. For science images, this means the first
    16 values are removed.
    '''
    converted_packet_data = decimal_converted_packet(packet_data)
    return converted_packet_data[58:]
# Returns a decimal array for the packet data excluding the first 16 elements, which do not correspond to science packet
# pixel data.

def isolate_packet_data(packet_data):
    converted_packet_data = decimal_converted_packet(packet_data)
    return converted_packet_data[42:]

# The Wireshark capture files are 570 bytes in size. The pixel data are stored in the last 528 bytes of the capture.
# Therefore, I am subtracting the first 58 bytes of the capture file because they do not correspond to pixel data.
# This must be done in combination with the subtraction of the first 16 elements of each packet.

def convert_integer_to_binary(integer):
    binary_array = []
    bit_number = 0
    quotient = integer
    
    while bit_number <= 7:
        binary_array.append(quotient%2)
        quotient = int(quotient/2)
        bit_number += 1

    return binary_array

def convert_packet_array_to_8bit_binary(packet):
    packet_binary_array_8bit = []
    for element in isolate_packet_pixel_data(packet):
        packet_binary_array_8bit.append(convert_integer_to_binary(element))
                
    return packet_binary_array_8bit

def convert_integer_to_binary(integer):
    binary_array = []
    bit_number = 0
    quotient = integer
    
    while bit_number <= 7:
        binary_array.append(quotient%2)
        quotient = int(quotient/2)
        bit_number += 1

    return binary_array

def convert_packet_array_to_8bit_binary(packet):
    packet_binary_array_8bit = []
    for element in isolate_packet_pixel_data(packet):
        packet_binary_array_8bit.append(convert_integer_to_binary(element))
                
    return packet_binary_array_8bit

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

def convert_16bit_binary_to_integer(number):
    
    i = 15
    integer = 0
    
    for element in number:
        integer += (int(element)*(2**i))
        i -= 1
    
    if integer >= 32768:
        return 0
    
    else: 
        return integer

def concatenate_streams_and_convert_to_integer(packet):
    
    concatenated_array = []
    for element in concatenate_pixel_data_streams(packet):
        concatenated_array.append(convert_16bit_binary_to_integer(element))
        
    return concatenated_array

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

def quabo_image_compiler(quabo_1, quabo_2, quabo_3, quabo_4):

    final_quadrant_1 = np.kron(np.array([[0,1],[0,0]]), quabo_1)
    final_quadrant_2 = np.kron(np.array([[0,0],[0,1]]), np.rot90(quabo_2, -1))
    final_quadrant_3 = np.kron(np.array([[0,0],[1,0]]), np.rot90(quabo_3, -2))
    final_quadrant_4 = np.kron(np.array([[1,0],[0,0]]), np.rot90(quabo_4, -3))

    return final_quadrant_1+final_quadrant_2+final_quadrant_3+final_quadrant_4


def get_image_source_ip(packet):

    return str(decimal_converted_packet(packet)[26])+'.'+str(decimal_converted_packet(packet)[27])+'.'+str(decimal_converted_packet(packet)[28])+'.'+str(decimal_converted_packet(packet)[29])

def convert_unix_time(time):

    date_object = datetime.fromtimestamp(time)
    output = date_object.strftime('%Y-%m-%d %H:%M:%S') +':'+ str(date_object.microsecond)

    return output