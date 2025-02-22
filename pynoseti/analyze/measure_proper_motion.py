import numpy as np
import matplotlib.pyplot as plt

from math import sqrt

#add functionality to json file that specifies detector plane dimensions and pixel scale

def measure_proper_motion(source, pixel_scale):

    x = []
    y = []

    for element in source.motion_history:

        x.append(element[0][0])
        y.append(element[0][1])

    x = np.array(x)
    y = np.array(y)

    coefficients = np.polyfit(x, y, 1)
    slope, intercept = coefficients

    first_position_fit = [float(x[0]), float(slope*x[0]+intercept)]
    last_position_fit = [float(x[-1]), float(slope*x[-1]+intercept)]

    time_observed = float(source.last_detection_time_s-source.first_detection_time_s)

    pixel_distance_travelled = sqrt((last_position_fit[0]-first_position_fit[0])**2 + (last_position_fit[1]-first_position_fit[1])**2)

    proper_motion = pixel_distance_travelled*pixel_scale/time_observed

    print(f'Measured proper motion is {proper_motion} degrees per second.')
    print(f'Source observed for {time_observed} seconds.')

    
