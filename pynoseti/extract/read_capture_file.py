import gc
from scapy.all import rdpcap

def read_capture_file(file):

    concatenated_batch_data = []

    capture = rdpcap(file)
    
    for packet in capture:
        concatenated_batch_data.append(packet)

    del capture
    gc.collect()    

    return concatenated_batch_data