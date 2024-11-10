import numpy as np
import matplotlib.pyplot as plt
import json
from functions import *
from pprint import pprint
#from glom import glom
#file = np.load('/home/brett/Data_for_pynoseti/median_image_script_testing/pynoseti/pynoseti_Ima_onskyima2pe__20230428_050035.pcapng4test.npy', allow_pickle=True)
#file = np.load('/home/brett/Data_for_pynoseti/median_image_script_testing/pynoseti/pynoseti_full_sequence_data.npy', allow_pickle=True)
#file2 = np.load('/home/brett/Data_for_pynoseti/median_image_script_testing/pynoseti/pynoseti_full_sequence_data_TEST.npy', allow_pickle=True)
#file3 = np.load('/home/brett/Data_for_pynoseti/median_image_script_testing/pynoseti/pynoseti_full_sequence_data_SEQUENCES.npy', allow_pickle=True)
#file4 = np.load('/home/brett/Data_for_pynoseti/median_image_script_testing/pynoseti/pynoseti_full_sequence_data_FINAL_DATA_Ima_onsky.npy', allow_pickle=True)

'''
import time
start_time = time.time()

from multiprocessing import Pool

def your_function(item):
    return item ** 2

items = list(range(100000001))

# Specify number of cores to use
num_cores = 1

with Pool(processes=num_cores) as pool:
    results = pool.map(your_function, items)

#print(results)

end_time = time.time()
print('Completed in '+str(end_time-start_time)+' seconds!')
'''

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


print(len(file4),'\n-------------\n')
print(len(file4[0]),'\n-------------\n')
#print('\n\n\n\n----------***********---------------\n\n\n\n')
print(file4,'\n-------------\n')
print(len(file4[0].sequence),'\n-------------\n')
print(file4[0].median_frame[1].frame_selection,'\n-------------\n')
print(len(file4[1].sequence),'\n-------------\n')
print(len(file4[2].sequence),'\n-------------\n')
print(file4[0][0],'\n-------------\n')
print(file4[0][0].file_name,'\n-------------\n')
print(file4[0][1].file_name,'\n-------------\n')
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Number of subplots
num_images = 4  # Adjust the number of subplots as needed

# Create separate image sequences for each subplot
# Here, we generate 100 frames of random 10x10 images for each subplot
image_sequences = [np.random.rand(100, 10, 10) for _ in range(num_images)]

# Create figure and subplots
fig, axes = plt.subplots(1, num_images, figsize=(4 * num_images, 4))
axes = np.atleast_1d(axes)  # Ensures axes is always iterable

# Initialize imshow objects for each subplot with the first frame of each sequence
ims = [ax.imshow(image_sequences[i][0], animated=True) for i, ax in enumerate(axes)]

# Update function for the animation
def update(frame):
    for i, im in enumerate(ims):
        # Update each imshow object with its corresponding image sequence
        im.set_array(image_sequences[i][frame])
    return ims

# Create the animation
ani = FuncAnimation(fig, update, frames=image_sequences[0].shape[0], blit=True)

plt.tight_layout()
plt.show()





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