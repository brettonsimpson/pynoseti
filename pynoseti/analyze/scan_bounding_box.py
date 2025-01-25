import numpy as np
from scipy import ndimage

import matplotlib.pyplot as plt

from pynoseti.process.classes import Source

count_threshold = 2000
#remove later and implement reading from config file

def scan_bounding_box(centroid, frame):

    bounding_box_width = [centroid[0] - 5,
                            centroid[0] + 5]

    bounding_box_height = [centroid[1] - 5,
                            centroid[1] + 5]
    
    truncated_frame = frame[int(bounding_box_width[0]):int(bounding_box_width[1]),
                            int(bounding_box_height[0]):int(bounding_box_height[1])]
    
    threshold_image = np.clip(frame.data, a_min=0, a_max=None) > count_threshold

    labeled_array, feature_number = ndimage.label(threshold_image)

    new_centroid = ndimage.center_of_mass(threshold_image, labeled_array, range(1, feature_number+1))

    if len(new_centroid) != 0 and centroid != new_centroid:
        print(f'Centroid: {centroid}')
        print(f'New Centroid: {new_centroid}\n')
        #plt.imshow(frame.data)
        #plt.scatter(new_centroid[0], new_centroid[1])
        #plt.scatter(centroid[0], centroid[1])
        #plt.show()
        
        return new_centroid

    else:
        
        return None