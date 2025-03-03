import numpy as np

import matplotlib.pyplot as plt

from pynoseti.process.classes import Sequence, Image

def frame_viewer(file, telescope_choice, time_choice):

    timestamp_list = []

    

    for frame in file[telescope_choice-1].sequence:

        timestamp_list.append(float(frame.timestamp))

    #timestamp_list = np.asarray(timestamp_list)

    #approximate_frame = timestamp_list[(np.abs(timestamp_list - time_choice)).argmin()]


    #idx = (np.abs(timestamp_list - time_choice)).argmin()



    #print(timestamp_list)

    #print(f'\n{approximate_frame}')

    plt.imshow(file[telescope_choice-1].sequence[0].data)
    plt.colorbar()
    plt.show()
    