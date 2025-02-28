import gc
from scapy.all import rdpcap
from scapy import error

def read_capture_file(file):

    concatenated_batch_data = []

    try:
        capture = rdpcap(file)

    except error.Scapy_Exception as e:
        print('\nUnsupported capture file type. Skipping for now.\n')
    
    try:
        for packet in capture:
            concatenated_batch_data.append(packet)

        del capture

    except UnboundLocalError as e:
        print('\nUnbound local error encountered. Continuing to next file.\n')

    
    gc.collect()    

    return concatenated_batch_data