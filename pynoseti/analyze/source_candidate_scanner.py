import numpy as np
from scipy import ndimage

from pynoseti.analyze.source_relevance import source_relevance

count_threshold = 2000

def source_candidate_scanner(new_centroid, frame, persistent_sources):

    #threshold_image = np.clip(frame.data, a_min=0, a_max=None) > count_threshold

    #labeled_array, feature_number = ndimage.label(threshold_image)

    #candidate_sources = ndimage.center_of_mass(threshold_image, labeled_array, range(1, feature_number+1))




    for source in persistent_sources:


        if frame.timestamp - source.motion_history[len(source.motion_history)-1] <= 500:

            local_in_time = True













    for coordinate in candidate_sources:

        for source in persistent_sources:

            if coordinate in source.motion_history and source.first_detection_time_ms <= frame.timestamp <= source.last_detection_time_ms:




    # Plan to draw source candidate names at random from 
    # list of solar system and/or contellations
    #source_candidate = Source('Placeholder Source Name',
    #                          frame.timestamp,
    #                          None,
    #                          None,
    #                          None)