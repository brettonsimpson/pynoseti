import gc
from scapy.all import rdpcap
from scapy import error

def read_capture_file(file):

    concatenated_batch_data = []

    try:
        capture = rdpcap(file)

        for packet in capture:

            concatenated_batch_data.append(packet)

        del capture

    except error.Scapy_Exception as e:

        print(f'\nUnsupported capture file type. Skipping for now. Error: {e}\n')

    except UnboundLocalError as e:

        print(f'\nUnbound local error encountered. Continuing to next file. Error: {e}\n')
    
    gc.collect()    

    return concatenated_batch_data