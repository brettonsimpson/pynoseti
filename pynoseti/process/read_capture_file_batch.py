import os
import numpy as np
import multiprocessing
from itertools import chain
from scapy.all import rdpcap

from pynoseti.extract.read_capture_file import read_capture_file
from pynoseti.extract.extract_packet_data import *
from pynoseti.process.parallel_processing import parallel_processing

def read_capture_file_batch(batch):

    print(batch)

    packet_hex_data_list = []
    
    available_threads = os.cpu_count()

    allowed_threads = int(available_threads/4)

    packet_hex_data_list = parallel_processing(batch,
                                               read_capture_file,
                                               allowed_threads)
    
    new_list = list(chain(*packet_hex_data_list))

    packet_data_array = parallel_processing(new_list,
                                            assemble_packet_data,
                                            allowed_threads)

    return packet_data_array