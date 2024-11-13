import os
import time
import json
import numpy as np
from functions import *
from reader import reader_function
from playback_copy import playback_function
from analyzer import analyzer_function

with open('config.json', 'r') as file:
    config = json.load(file)
telescope_list = []
for telescope in config['telescopes']:
    telescope_list.append(telescope['dome'])

print(f'''
    *                   *           *                           *                       *
            *
*           
            *       *            *               *           *                   *              *
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

(1) Playback                            (3) Preprocess                          Recognized Telescopes:
    Renders an .mp4 file that compiles      Generate a file containing          1. {telescope_list[0]}
    the continuous playback data for        preprocessed observational data     2. {telescope_list[1]}
    each telescope. (This can take a        for all files within a directory.   3. {telescope_list[2]}
    while)                           

(2) Analyzer                            (4) All of the Above [Untested]
    Produces a .csv file cataloguing        Perform all operations listed
    transient centroids recognized in       previously.
    processed data.
''')

option = int(input('Enter the integer corresponding to the action you would like to do: '))

if option == 1:
    print('\nSelect a directory containing data you would like to process.')
    path = select_directory()
    target_path = str(path)+'/pynoseti'

    if os.path.isdir(target_path):
        
        telescope_choice = input('\nWhich telescope would you like to playback data for?\n'
                            'Skip this prompt by pressing enter and process the entire file.\n'
                            'Enter the integer corresponding to one of the telescopes: ')
        
        print('\nPreprocessed file directory recognized. Advancing to video file generation.')

        if telescope_choice != '':
            
            #'''
            choice = int(telescope_choice)-1
            with os.scandir(path) as directory:
                file_count = 1
                for file in directory:
                    if os.path.splitext(path+os.path.basename(file.name))[1] == '.npy':
                        #if file_count == choice:
                        playback_function(file, telescope_choice, file_count, file.name, path)
                        #choice += 1
            #'''
            #choice = int(telescope_choice)-1
            #with os.scandir(path) as files:
        elif telescope_choice == '':
            with os.scandir(path) as files:
                file_count = 1
                for file in files:
                    if os.path.splitext(path+os.path.basename(file.name))[1] == '.npy':
                        file_count+=1
                        playback_function(file, telescope_choice, file_count, file.name, path)

    else:
        i=1
        print('=============================================================')
        print('Recognized Telescopes:')
        for telescope in telescope_list:
            print(f'{i}. {telescope}')
            i+=1
        print('\nThis listed can be modified by editing the config.json file.')
        print('=============================================================')
        telescope_choice = input('Which telescope would you like to playback data for?\n'
                            'Skip this prompt by pressing enter and process the entire file.\n'
                            'Enter the integer corresponding to one of the telescopes: ')
        print('')
        print(f'Target directory created for selected files at {target_path}\n')
        
        processed_data = reader_function(path)
        
        if telescope_choice != '':
            choice = int(telescope_choice)-1
            with os.scandir(path) as files:
                file_count = 0
                for file in files:
                    if os.path.splitext(path+os.path.basename(file.name))[1] == '.npy':
                        if file_count == choice:
                            playback_function(processed_data, telescope_choice)
                        choice += 1

        elif telescope_choice == '':
            print(path)
            with os.scandir(path) as files:
                file_count = 1
                for file in files:
                    file_count += 1
                    if os.path.splitext(path+os.path.basename(file.name))[1] == '.npy':
                        playback_function(path, processed_data, telescope_choice, file_count)

elif option == 2:
    path = input('\nPlease provide the directory of the files you would like to generate an event log for: ')
    path = path.replace('\\', '/')
    path = path.replace('"', '')

    if os.path.isdir(path):
        analyzer_function(path)
    else:
        print('\nPreprocessed file directory not recognized. Generating file directory...')
        reader_function(path)
        analyzer_function(path)

elif option == 3:
    path = input('\nPlease provide the directory of the files you would like to preprocess: ')
    path = path.replace('\\', '/')
    path = path.replace('"', '')
    reader_function(path)
    print('Preprocessing of file directory complete!\n')

elif option == 4:
    path = input('\nPlease provide the directory of the files you would like to preprocess: ')
    path = path.replace('\\', '/')
    path = path.replace('"', '')
    target_path = str(path)+'/pynoseti'
    if os.path.isdir(target_path):
        telescope_choice = input('Which telescope would you like to playback data for?\n'
                            'Skip this prompt by pressing enter and process the entire file.\n'
                            'Enter the integer corresponding to one of the telescopes: ')
        
        print('\nPreprocessed file directory recognized. Advancing to video file generation.\n')

        if telescope_choice != '':
            choice = int(telescope_choice)-1
            with os.scandir(path) as files:
                file_count = 1
                for file in files:
                    if os.path.splitext(path+os.path.basename(file.name))[1] == '.npy':
                        if file_count == choice:
                            playback_function(file, telescope_choice)
                        choice += 1

        elif telescope_choice == '':
            with os.scandir(path) as files:
                for file in files:
                    if os.path.splitext(path+os.path.basename(file.name))[1] == '.npy':
                        playback_function(file, telescope_choice)
    else:
        print('\nPreprocessed file directory not recognized. Generating file directory...')
        
        os.mkdir(str(path)+'/pynoseti')
        print('Target directory created for selected files at '+str(path)+'/panoseti\n')
        
        reader_function(path)

        telescope_choice = input('Which telescope would you like to playback data for?\n'
                            'Skip this prompt by pressing enter and process the entire file.\n'
                            'Enter the integer corresponding to one of the telescopes: ')

        if os.path.isdir(path):
            print('\nPreprocessed file directory recognized. Advancing to video file generation.\n')

            if telescope_choice != '':
                choice = int(telescope_choice)-1
                with os.scandir(path) as files:
                    file_count = 1
                    for file in files:
                        if os.path.splitext(path+os.path.basename(file.name))[1] == '.npy':
                            if file_count == choice:
                                playback_function(file, telescope_choice)
                            choice += 1

            elif telescope_choice == '':
                with os.scandir(path) as files:
                    for file in files:
                        if os.path.splitext(path+os.path.basename(file.name))[1] == '.npy':
                            playback_function(file, telescope_choice)

    analyzer_function(target_path)
#end_time = time.time()
#print('Reduction completed in '+str(end_time-start_time)+' seconds!')