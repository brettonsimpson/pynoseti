import numpy as np
import matplotlib.pyplot as plt

file = np.load('/home/brett/Data_for_pynoseti/median_image_script_testing/pynoseti/pynoseti_Ima_onskyima2pe__20230428_050035.pcapng4test.npy', allow_pickle=True)
file2 = np.load('/home/brett/Data_for_pynoseti/median_image_script_testing/pynoseti/pynoseti_Ima_onskyima2pe__20230428_050035.pcapng4.npy', allow_pickle=True)

print(file2[0].telescope)