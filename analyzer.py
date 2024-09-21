import os
import pandas
import numpy as np
from functions import *
import matplotlib.pyplot as plt
from scipy import ndimage

#path = input('Please enter the file path for the PANOSETI recording you would like to analyze: ')
path = '/home/brett\Data_for_pynoseti\pynoseti'
path = path.replace('\\', '/')
path = path.replace('"', '')

#path = '/home/brett/Data_for_pynoseti/panoseti'


events = {
    'Pixel Locations': [],
    'Time': [],
    'Peak Count': [],
    'File Path': []
}

with os.scandir(path) as files:
    for file in files:
        if file.is_file():
            file_name = os.path.basename(file.name)
            file_data = np.load(str(path)+'/'+str(file_name), allow_pickle=True)

            print(ndimage.center_of_mass(file_data[0][0].data))

file_name = '/pynoseti_Pause_onskyph0pe_ima0pe__20230426_041905.pcapng.npy'
file_data = np.load(str(path)+file_name, allow_pickle=True)
image = file_data[0][0].data

print('\n',ndimage.center_of_mass(file_data[0][0].data))

threshold = 3000
threshold_image = image >= threshold

labeled_array, feature_number = ndimage.label(threshold_image)
centroids = ndimage.center_of_mass(threshold_image, labeled_array, range(1, feature_number+1))

events['Pixel Locations'].append(centroids)
events['Time'].append(file_data.timestamp)
events['Peak Count'].append(centroids)
events['File Path'].append()