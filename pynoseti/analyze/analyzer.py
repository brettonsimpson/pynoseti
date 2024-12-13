import os
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy import ndimage
import matplotlib.pyplot as plt

from pynoseti.extract.extract_packet_data import convert_unix_time

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
                    
                    for sequence in file_data:
                        
                        for frame in sequence.sequence:

                            threshold_image = np.clip(frame.data, a_min=0, a_max=None) > count_threshold

                            labeled_array, feature_number = ndimage.label(threshold_image)
                            centroids = ndimage.center_of_mass(threshold_image, labeled_array, range(1, feature_number+1))

                            if len(centroids) > 0:

                                events['Pixel Locations'].append(centroids)
                                events['Peak Count'].append(len(centroids))
                                events['Telescope'].append(sequence.telescope)
                                events['Time (PDT)'].append(convert_unix_time(float(frame.timestamp)))
                                events['Threshold'].append(count_threshold)
                                events['File Path'].append(path+file_name)

            
    
       
    output_file = pd.DataFrame(events)
    output_file.to_csv(path+'/events.csv', index=False)
    print(f'\nEvent log written to {path}/events.csv\n')