import numpy as np
import matplotlib.pyplot as plt
import json
from functions import *
from pprint import pprint
from glom import glom
#file = np.load('/home/brett/Data_for_pynoseti/median_image_script_testing/pynoseti/pynoseti_Ima_onskyima2pe__20230428_050035.pcapng4test.npy', allow_pickle=True)
#file = np.load('/home/brett/Data_for_pynoseti/median_image_script_testing/pynoseti/pynoseti_full_sequence_data.npy', allow_pickle=True)
#file2 = np.load('/home/brett/Data_for_pynoseti/median_image_script_testing/pynoseti/pynoseti_full_sequence_data_TEST.npy', allow_pickle=True)
#file3 = np.load('/home/brett/Data_for_pynoseti/median_image_script_testing/pynoseti/pynoseti_full_sequence_data_SEQUENCES.npy', allow_pickle=True)
#file4 = np.load('/home/brett/Data_for_pynoseti/median_image_script_testing/pynoseti/pynoseti_full_sequence_data_FINAL_DATA.npy', allow_pickle=True)

import multiprocessing

num_cores = multiprocessing.cpu_count()
print(f"Number of available cores: {num_cores}")


#print(type(file[0][0][0]))

#print('\n')
#print(file,'\n-------------\n')
#print(file[0],'\n-------------\n')
#print(file[0][0],'\n-------------\n')
#print(file[0][0][0],'\n-------------\n')

#i=0
#for element in file:
#    print(file[i][0][0])
#    i+=1

#print(type(file2))
#print(len(file2[0][0]))




#print('\n\n\n\n----------***********---------------\n\n\n\n')
#print(type(file2[0][0]),'\n-------------\n')
#print(len(file2),'\n-------------\n')
#print(len(file2[0]),'\n-------------\n')
#print(len(file2[0][1][0].sequence),'\n-------------\n')
#print(len(file2[0][0][0]),'\n-------------\n')


'''
print(len(file3),'\n-------------\n')
print(len(file3[0]),'\n-------------\n')
print('\n\n\n\n----------***********---------------\n\n\n\n')
print(file3,'\n-------------\n')
print(file3[0],'\n-------------\n')
print(file3[0][0],'\n-------------\n')
print(file3[0][0].file_name,'\n-------------\n')
print(file3[0][1].file_name,'\n-------------\n')
'''

#print(len(file4),'\n-------------\n')
#print(len(file4[0]),'\n-------------\n')
#print('\n\n\n\n----------***********---------------\n\n\n\n')
#print(file4,'\n-------------\n')
#print(len(file4[0].sequence),'\n-------------\n')
#print(file4[0].median_frame[1].frame_selection,'\n-------------\n')
#print(len(file4[1].sequence),'\n-------------\n')
#print(len(file4[2].sequence),'\n-------------\n')
#print(file4[0][0],'\n-------------\n')
#print(file4[0][0].file_name,'\n-------------\n')
#print(file4[0][1].file_name,'\n-------------\n'


#i=0
#for element in file2:
#    print(file2[i][0][0])
#    i+=1

#print(type(file[0][0].sequence[10].data))

#plt.imshow(file[0][0][0].sequence[10].data)
#plt.show()

#first file
#first telescope
#sequence
#eleventh frame in the sequence ^^^^^^^^^

#for element in file:
    #for telescope in element:
        #print(np.info(np.stack(telescope.data)))

#print(np.stack)

#print('\ntest')


'''
import tkinter as tk
from tkinter import filedialog

def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    directory_path = filedialog.askdirectory()  # Open directory dialog
    print(f"Selected directory: {directory_path}")

select_directory()

'''


#                   file -> telescope -> 