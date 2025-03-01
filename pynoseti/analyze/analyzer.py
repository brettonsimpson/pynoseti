import os
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy import ndimage
import matplotlib.pyplot as plt

from pynoseti.analyze.scan_bounding_box import scan_bounding_box
from pynoseti.analyze.measure_proper_motion import measure_proper_motion

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
        pixel_scale = config["detector_plane_pixel_scale"]

    scan_interval = 25

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

                        test = 1
                        
                        for frame in sequence.sequence:

                            try:

                                #print(frame.timestamp)

                                threshold_image = np.clip(frame.data, a_min=0, a_max=None) > count_threshold

                                labeled_array, feature_number = ndimage.label(threshold_image)

                                centroids = ndimage.center_of_mass(threshold_image, labeled_array, range(1, feature_number+1))

                                for centroid in centroids:

                                    candidate_source_index.append(Source_Candidate(centroid,
                                                                                   frame.timestamp,
                                                                                   motion_history=None))





                                for centroid in centroids:

                                    #if frame_iterate < len(sequence.sequence) - 25:

                                    new_centroid = scan_bounding_box(centroid, sequence.sequence[frame_iterate+scan_interval].data)

                                    if new_centroid is not None:

                                        source_match = False

                                        for source in source_index:
                                            
                                            difference_threshold = 1
                                            
                                            if frame.timestamp - source.last_detection_time_s < difference_threshold:

                                                #print(f'{frame.timestamp-source.last_detection_time_s} is < {difference_threshold}')
                                                #print(f'Source first detection time is {source.first_detection_time_s}')
                                                #print(f'Source last detection time is {source.last_detection_time_s}')
                                                #print(f'Current timestamp is {frame.timestamp}')
                                                #print(f'Interval: {test}', '\n')
                                                #test+=1



                                                source.coordinate_update(new_centroid, frame.timestamp)

                                                #print(new_centroid)
                                                #print(frame.timestamp)
                                                #print('\n')

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

                                
                            frame_iterate+=1



    print(f'\nSource index length is {len(source_index)}.\n')

    exit()
    
    #print(len(source_index[0].motion_history))

    #print(source_index[0].first_detection_time_s, source_index[0].last_detection_time_s)

    #print(len(source_index[0].motion_history))
    #print(source_index[1].motion_history)
    #test=[source_index[0].motion_history]

    #test = [item for sublist in test for item in sublist]

    #for element in source_index:

    #    print(element.motion_history)

    #print(test)


    #for element in source_index:
    #    x.append(element[0][0])
    #    y.append(element[0][1])

        #plt.scatter(x,y)
        #plt.gca().invert_yaxis()
        #plt.show()

    #for source in source_index:

    #    print(len(source.motion_history))


    #for element in x:
        
    #plt.scatter(x,y)
    #plt.gca().invert_yaxis()
    #plt.show()

    empty_frame = np.zeros((32,32))

    x=[]
    y=[]

    for source in source_index:
        #print(len(source.motion_history))
        #x=[]
        #y=[]

        for position in source.motion_history:
            
            x.append(position[0][0])
            #print(f'x is {position[0][0]}')
            y.append(position[0][1])
            #print(f'y is {position[0][1]}\n')

    x = np.array(x)
    y = np.array(y)

    coefficients = np.polyfit(x, y, 1)
    slope, intercept = coefficients
    y_fit = slope * x + intercept
    
        
    plt.plot(empty_frame)
    plt.plot(x,y_fit, color='red', label='Motion Fit Line')
    plt.scatter(x,y, c='blue', label='Coordinate History')
    plt.gca().invert_yaxis()
    plt.title('Test Source Coordinate History')
    plt.xticks([])
    plt.yticks([])
    plt.legend()
    plt.show()
    
       
    output_file = pd.DataFrame(events)
    output_file.to_csv(path+'/events.csv', index=False)
    print(f'\nEvent log written to {path}/events.csv\n')

    measure_proper_motion(source_index[0], pixel_scale)

    