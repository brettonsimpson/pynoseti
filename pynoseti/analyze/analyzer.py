import os
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy import ndimage
import matplotlib.pyplot as plt

from pynoseti.analyze.scan_bounding_box import scan_bounding_box

from pynoseti.extract.extract_packet_data import convert_unix_time

from pynoseti.process.classes import Source, Source_Candidate

def analyzer_function(path):
    events = {
        'Pixel Locations': [],
        'Peak Count': [],
        'Telescope': [],
        'Time (PDT)': [],
        'Threshold': [],
        'File Path': []
    }

    print('\nIdentifying centroids...')

    with os.scandir(path) as files:
        file_count = 0
        for file in files:
            if file.is_file():
                if os.path.splitext(path+os.path.basename(file.name))[1] == '.npy':
                    file_count += 1

    with open('config.json', 'r') as file:
        config = json.load(file)
    count_threshold = config["count_threshold"]

    with os.scandir(path) as files:

        for file in tqdm(list(files)):
            if file.is_file():
                if os.path.splitext(path+os.path.basename(file.name))[1] == '.npy':
                    file_name = os.path.basename(file.name)
                    file_data = np.load(str(path)+'/'+str(file_name), allow_pickle=True)

                    source_index = []
                    
                    for sequence in file_data:

                        frame_iterate = 0

                        candidate_source_index = []

                        
                        
                        for frame in sequence.sequence:

                            if frame_iterate % 25 == 0 or frame_iterate == 0:
                                #print(frame_iterate)
                                #print(len(sequence.sequence))

                                threshold_image = np.clip(frame.data, a_min=0, a_max=None) > count_threshold

                                labeled_array, feature_number = ndimage.label(threshold_image)
                                centroids = ndimage.center_of_mass(threshold_image, labeled_array, range(1, feature_number+1))

                                for centroid in centroids:



                                    candidate_source_index.append(Source_Candidate(centroid, frame.timestamp, motion_history=None))

                            
                                #for candidate in candidate_source_index:

                                for centroid in centroids:

                                    if frame_iterate + 25 < len(sequence.sequence) - 1:

                                        new_centroid = scan_bounding_box(centroid, sequence.sequence[frame_iterate+25].data)
                                

                                        #if new_centroid is not None and len(source_index) == 0:

                                        #    source_index.append(Source(identifier=None,
                                        #                            first_detection_time_ms=frame.timestamp,
                                        #                            last_detection_time_ms=frame.timestamp,
                                        #                            motion_history=[new_centroid],
                                        #                            average_proper_motion=None,
                                        #                            proper_motion_direction=None))

                                        if new_centroid is not None:# and len(source_index) > 0:
                                            # If a new centroid is detected in the centroid's bounding box

                                            # fcomaopcm

                                            #print(new_centroid)
                                            #print(f'There are {len(source_index)} sources')

                                            #source_match = False
                                            source_match = False

                                            for source in source_index:

                                                if centroid in source.motion_history and frame.timestamp <= source.last_detection_time_ms + 300.0:

                                                    source.coordinate_update(new_centroid, frame.timestamp)

                                                    source_match = True
                                                    print('continuing')
                                                    continue

                                            

                                            print('test')
                                            if source_match is False:

                                                source_index.append(Source(identifier=None,
                                                                        first_detection_time_ms=frame.timestamp,
                                                                        last_detection_time_ms=frame.timestamp,
                                                                        motion_history=[new_centroid],
                                                                        average_proper_motion=None,
                                                                        proper_motion_direction=None))

                                        


                                        #elif new_centroid is None:

                                        #    candidate_source_index.append(Source_Candidate(centroid,
                                        #                                                frame.timestamp,
                                        #                                                motion_history=[centroid]))
                                        
                            frame_iterate+=1



                            #if len(centroids) > 0:

                            #    events['Pixel Locations'].append(centroids)
                            #    events['Peak Count'].append(len(centroids))
                            #    events['Telescope'].append(sequence.telescope)
                            #    events['Time (PDT)'].append(convert_unix_time(float(frame.timestamp)))
                            #    events['Threshold'].append(count_threshold)
                            #    events['File Path'].append(path+file_name)

            
    print(len(source_index[0].motion_history))
    print(source_index[1].motion_history)
    test=[source_index[0].motion_history]

    #test = [item for sublist in test for item in sublist]

    print(len(source_index))

    #print(test)

    x=[]
    y=[]

    for element in test:
        x.append(element[0][0])
        y.append(element[0][1])

        #plt.scatter(x,y)
        #plt.gca().invert_yaxis()
        #plt.show()

    #for source in source_index:

    #    print(len(source.motion_history))


    #for element in x:
        
    plt.scatter(x,y)
    plt.gca().invert_yaxis()
    plt.show()
    
       
    output_file = pd.DataFrame(events)
    output_file.to_csv(path+'/events.csv', index=False)
    print(f'\nEvent log written to {path}/events.csv\n')

    