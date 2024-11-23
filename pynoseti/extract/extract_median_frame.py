import numpy as np
from pynoseti.process.classes import Median

def extract_median_frame(telescope_image_list):
#

    median_sequence = []

    for frame in telescope_image_list:
        #

        median_sequence.append(frame.data)
        #

    #print(len(median_sequence))
    #print(median_sequence[0])
    median_frame = np.median(np.stack(np.array(median_sequence)), axis=0)
    #

    return median_frame
    #


    #median_subtracted_telescope_image_list = []
    #
    #for frame in telescope_image_list:
    #
    #    median_subtracted_telescope_image_list.append(Image(frame.data-median_frame,frame.timestamp,frame.number))