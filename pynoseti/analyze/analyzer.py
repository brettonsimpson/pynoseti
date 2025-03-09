import os
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy import ndimage
import matplotlib.pyplot as plt

from pynoseti.analyze.scan_bounding_box import scan_bounding_box
from pynoseti.analyze.measure_proper_motion import measure_proper_motion
from pynoseti.analyze.generate_summary import generate_summary

from pynoseti.extract.extract_packet_data import convert_unix_time

from pynoseti.process.classes import Source, Source_Candidate

def analyzer_function(file_data):
    events = {
        'Pixel Locations': [],
        'Peak Count': [],
        'Telescope': [],
        'Time (PDT)': [],
        'Threshold': [],
        'File Path': []
    }

    file_data = np.load(file_data, allow_pickle=True)

    scan_interval = 25

    source_index = []

    count_threshold = 2000

    for sequence in file_data:

        frame_iterate = 0

        candidate_source_index = []
        
        for frame in sequence.sequence:

            try:

                threshold_image = np.clip(frame.data, a_min=0, a_max=None) > count_threshold

                labeled_array, feature_number = ndimage.label(threshold_image)

                centroids = ndimage.center_of_mass(threshold_image, labeled_array, range(1, feature_number+1))

                for centroid in centroids:

                    candidate_source_index.append(Source_Candidate(centroid,
                                                                    frame.timestamp,
                                                                    motion_history=None))
                for centroid in centroids:

                    try:

                        new_centroid = scan_bounding_box(centroid, sequence.sequence[frame_iterate+scan_interval].data)

                        if new_centroid is not None:

                            source_match = False

                            for source in source_index:
                                
                                difference_threshold = 1
                                
                                if frame.timestamp - source.last_detection_time_s < difference_threshold:

                                    source.coordinate_update(new_centroid, frame.timestamp)

                                    source_match = True


                            if source_match is False:

                                source_index.append(Source(identifier = None,
                                                        first_detection_time_s = frame.timestamp,
                                                        last_detection_time_s = frame.timestamp,
                                                        motion_history = [new_centroid],
                                                        average_proper_motion = None,
                                                        proper_motion_direction = None))
                                
                    except IndexError as e:
                        pass
                            
            except IndexError as e:
                pass

            frame_iterate+=1