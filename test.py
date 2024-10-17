import os
import json
import pcapng
import datetime
import progressbar
import numpy as np
from pcapng import FileScanner
from pcapng.blocks import EnhancedPacket
from functions import *
from scapy.all import rdpcap

#test = rdpcap('/home/brett/Data_for_pynoseti/ph_plane/Dual_onskyph12.5pe_ima2pe__20230428_051449.pcapng')

import pyshark

test = pyshark.FileCapture('/home/brett/Data_for_pynoseti/ph_plane/Dual_onskyph12.5pe_ima2pe__20230428_051449.pcapng', use_json=True, include_raw=True)

print(test[10].get_raw_packet().hex())
