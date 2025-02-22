import numpy as np

from pynoseti.process.classes import Image, Sequence

def find_max_count(sequence):

    max_count = 0

    i=0

    #print(i)

    for frame in sequence.sequence:

        for row in frame.data:

            #for element in row:


            if np.max(row) > max_count:

                max_count = np.max(row)
                print(np.max(row))

        
        i+=1

    return max_count