import os
import json
import progressbar
import numpy as np
import pandas as pd
from functions import *
from scipy import ndimage
import matplotlib.pyplot as plt

#path = input('Please enter the file path for the PANOSETI recording you would like to analyze: ')
path = '/home/brett\Data_for_pynoseti\pynoseti'
path = path.replace('\\', '/')
path = path.replace('"', '')

#path = '/home/brett/Data_for_pynoseti/panoseti'

events = {
    'Pixel Locations': [],
    'Peak Count': [],
    'Time': [],
    'Threshold': [],
    'File Path': []
}

print('\nIdentifying centroids...')

with os.scandir(path) as files:
    file_count = 0
    for file in files:
        if file.is_file():
            file_count += 1

with open('config.json', 'r') as file:
    config = json.load(file)
count_threshold = config["count_threshold"]

with os.scandir(path) as files:
    j=0
    bar = progressbar.ProgressBar(max_value=file_count)

    for file in files:
        if file.is_file():
            file_name = os.path.basename(file.name)
            file_data = np.load(str(path)+'/'+str(file_name), allow_pickle=True)
            
            for sequence in file_data:
                i=0
                for frame in file_data[i]:

                    threshold_image = frame.data > count_threshold

                    labeled_array, feature_number = ndimage.label(threshold_image)
                    centroids = ndimage.center_of_mass(threshold_image, labeled_array, range(1, feature_number+1))

                    events['Pixel Locations'].append(centroids)
                    events['Peak Count'].append(len(centroids))
                    events['Time'].append(convert_unix_time(frame.timestamp))
                    events['Threshold'].append(count_threshold)
                    events['File Path'].append(path+file_name)
                    i+=1
        j+=1
        bar.update(j)

output_file = pd.DataFrame(events)
output_file.to_csv(path+'/events.csv', index=False)
print(f'\n\nEvent log written to {path}/events.csv\n')