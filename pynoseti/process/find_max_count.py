import numpy as np

from pynoseti.process.classes import Image, Sequence

def find_max_count(sequence):

    max_count = 0

    for frame in sequence.sequence:

        for row in frame.data:

            if np.max(row) > max_count:

                max_count = np.max(row)
    
    return max_count