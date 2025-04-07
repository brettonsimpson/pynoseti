import os
import json
import numpy as np
import six
import warnings
import pandas as pd
from itertools import chain

from tqdm import tqdm

import ray

warnings.filterwarnings("ignore")

from pynoseti.interface.downloader import downloader
from pynoseti.interface.select_file_directory import select_file_directory
from pynoseti.interface.select_file_path import select_file_path

from pynoseti.playback.playback import *
from pynoseti.playback.merge_playback_files import merge_playback_files

from pynoseti.process.aggregate_batch_data import aggregate_batch_data
from pynoseti.process.assemble_batch_array import assemble_batch_array
from pynoseti.process.read_json_file import read_json_file
from pynoseti.process.process_directory import process_directory
from pynoseti.process.parallel_processing import parallel_processing

from pynoseti.analyze.analyzer import analyzer_function
from pynoseti.analyze.frame_viewer import frame_viewer
from pynoseti.analyze.generate_summary import generate_summary

from pynoseti.extract.convert_unix_time import convert_unix_time
from pynoseti.extract.packet_diagnostic_tool import packet_diagnostic_tool

with open('config.json', 'r') as file:
    config = json.load(file)
telescope_list = []
for telescope in config['telescopes']:
    telescope_list.append(telescope['dome'])

print(f'''
   *                   *           *                                *                  *
             *
 *           
             *                   *               *           *                   *              *
                 *
         *                   *           *             *                    *               *
             *           *                                                           *           *
 *                               *           *       *   *       *
                 *           *   *       *                                           *       
     *               *              *                          *           *                 *
                 *       *               *           *                           *
       :::::::::           ::::    :::  ::::::::   ::::::::  :::::::::: ::::::::::: :::::::::::  
      :+:    :+:          :+:+:   :+: :+:    :+: :+:    :+: :+:            :+:         :+:        
     +:+    +:+ :+:  :+: :+:+:+  +:+ +:+    +:+ +:+        +:+            +:+         +:+       
    +#++:++#+   :+: :+: +#+ +:+ +#+ +#+    +:+ +#++:++#++ +#++:++#       +#+         +#+        
   +#+           +#+   +#+  +#+#+# +#+    +#+        +#+ +#+            +#+         +#+         
  #+#           #+#   #+#   #+#+# #+#    #+# #+#    #+# #+#            #+#         #+#          
 ###           ###   ###    ####  ########   ########  ##########     ###     ###########       

(1) <Playback>                         (3) <Preprocess>                     (5) <Telescopes>
    Renders an .mp4 file that compiles     Generate a file containing           List recognized
    the continuous playback data for       preprocessed observational data      telescopes and quabo
    each telescope. (This can take a       for all files within a directory.    addresses.
    while)                           

(2) <Analyzer>                         (4) <Download>                       (6) <Diagnostic Tool>
    Produces a .csv file cataloguing       Retrieve observing data from an      Inspect individual
    transient centroids recognized in      HTML page.                           .pcapng files.
    processed data.                                                             

(7) <Merge Playback Files>
    Merge multiple playback files into
    a single file.

''')

option = int(input('Enter the integer corresponding to the action you would like to do: '))

if option == 1:
    print('\nSelect a directory containing data you would like to process...')
    directory = select_file_directory()
    print(f'You selected: {directory}')
    
    save_directory = str(directory)+'/pynoseti'

    data_directory = str(directory)+'/pynoseti/data'

    file_count = 0

    if os.path.isdir(save_directory):
        with os.scandir(save_directory) as files:
            
            for file in files:
                if os.path.splitext(os.path.basename(file.name))[1] == '.npy':
                    file_count+=1

    if os.path.isdir(str(save_directory)+'/playback') is False:
        
        playback_folder = str(save_directory)+'/playback'
        
        os.mkdir(playback_folder)
        
        
    if file_count != 0:

        telescope_choice = input('\nWhich telescope would you like to playback data for?\n'
                            'Skip this prompt by pressing enter and process the entire file.\n'
                            'Enter the integer corresponding to one of the telescopes: ')
        
        if telescope_choice == '':
            telescope_choice = None
        
        print('\nPreprocessed file directory recognized. Advancing to video file generation.\n')


        with os.scandir(data_directory) as files:
            for file in files:
                if os.path.splitext(os.path.basename(file.name))[1] == '.npy':

                    if telescope_choice is not None:
                        choice = int(telescope_choice)-1
                        
                        playback_function(np.load(file, allow_pickle=True), telescope_choice, file.name, playback_folder)
                                    
                    elif telescope_choice is None:
                        
                        playback_function(np.load(file, allow_pickle=True), None, file.name, playback_folder)

    else:
        i=1
        print('=============================================================')
        print('Recognized Telescopes:')
        for telescope in telescope_list:
            print(f'{i}. {telescope}')
            i+=1
        print('\nThis listed can be modified by editing the config.json file.')
        print('=============================================================\n')
        telescope_choice = input('Which telescope would you like to playback data for?\n'
                            'Skip this prompt by pressing enter and process the entire file.\n'
                            'Enter the integer corresponding to one of the telescopes: ')
        print('')
        print(f'Target directory created for selected files at {save_directory}\n')

        print(directory)
        print(save_directory)
        
        if telescope_choice == '':
            telescope_choice = None

        processed_data = aggregate_batch_data(directory, telescope_list)
        
        if telescope_choice is not None:

            playback_function(processed_data[0], telescope_choice, processed_data[1], playback_folder)

        elif telescope_choice is None:

            playback_function(processed_data[0], None, processed_data[1], playback_folder)

elif option == 2:

    print('\nPlease provide the directory of the files you would like to generate an event log for: ')
    
    directory = select_file_directory()

    print(f'You selected: {directory}')

    if os.path.isdir(directory):

        file_list = []

        with os.scandir(directory) as files:
            file_count = 0
            for file in files:
                if file.is_file():
                    if os.path.splitext(directory+os.path.basename(file.name))[1] == '.npy':
                        file_list.append(f'{directory}/{os.path.basename(file.name)}')
                        file_count += 1

            observing_start = 100 #test value
    
            observing_end = 100 #test value

        with open('config.json', 'r') as file:
            config = json.load(file)
            count_threshold = config["count_threshold"]
            pixel_scale = config["detector_plane_pixel_scale"]

        ray.init(num_cpus=int(1*os.cpu_count()/4), object_store_memory=5*1024**3)

        source_list_test = [analyzer_function.remote(file) for file in file_list]

        with tqdm(total=len(file_list)) as progress:
            source_list_test2 = []
            while source_list_test:
                complete, source_list_test = ray.wait(source_list_test, num_returns=1)
                source_list_test2.append(ray.get(complete[0]))
                progress.update(1)
        
        ray.shutdown()

        print(f'\nSource list test length is {len(source_list_test2)}.\n')

        source_index = list(chain(*source_list_test2))

        print(f'\nSource index length is {len(source_index)}.\n')

        generate_summary(source_index, directory, observing_start, observing_end, None)
        print('Summary file generated!')

elif option == 3:

    print('\nPlease provide the directory of the files you would like to preprocess.')

    directory = select_file_directory()

    print(f'You selected: {directory}')

    if __name__ == '__main__':
        process_directory(directory, option)


elif option == 4:

    print('If the host webpage is password protected, verify that the username and password are correct in the config.json file.')

    url = input('Enter a URL to install data from: ')

    target_directory = input('And locate a target directory for downloaded data: ')

    downloader(url, target_directory)

    print('Download Complete!\n')
      

elif option == 5:
    print('\n=====================================================================')
    print('Recognized telescopes:\n')
    i=1
    for telescope in telescope_list:
        print(f'{i}. {telescope}')
        i+=1
    print('=====================================================================\n')


elif option == 6:

    file_path = select_file_path()
    print(f'You selected: {file_path}')

    packet_diagnostic_tool(file_path)

elif option ==7:
    print('\nPlease provide the directory of the files you would like to merge.')

    directory = select_file_directory()

    print(f'You selected: {directory}')

    merge_playback_files(directory)

    print('Merge Playback Files Complete!\n')


#end_time = time.time()
#print('Reduction completed in '+str(end_time-start_time)+' seconds!')