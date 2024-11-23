import os
import json
import numpy as np
from pathlib import Path
from pcapng import FileScanner
from pcapng.blocks import EnhancedPacket
from pynoseti.playback.playback import *
from pynoseti.process.aggregate_data import aggregate_data
from pynoseti.interface.select_file_directory import select_file_directory

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

(1) Playback                           (3) Preprocess                       (5) Telescopes
    Renders an .mp4 file that compiles     Generate a file containing           List recognized
    the continuous playback data for       preprocessed observational data      telescopes and quabo
    each telescope. (This can take a       for all files within a directory.    addresses.
    while)                           

(2) Analyzer                           (4) All of the Above [Untested]
    Produces a .csv file cataloguing       Perform all operations listed
    transient centroids recognized in      previously.
    processed data.
''')

option = int(input('Enter the integer corresponding to the action you would like to do: '))

if option == 1:
    print('\nSelect a directory containing data you would like to process...')
    directory = select_file_directory()
    print(f'You selected: {directory}')

    save_directory = str(directory)+'/pynoseti'

    file_count = 0

    if os.path.isdir(save_directory):
        with os.scandir(save_directory) as files:
            
            for file in files:
                if os.path.splitext(os.path.basename(file.name))[1] == '.npy':
                    file_count+=1
        
    if file_count != 0:

        telescope_choice = input('\nWhich telescope would you like to playback data for?\n'
                            'Skip this prompt by pressing enter and process the entire file.\n'
                            'Enter the integer corresponding to one of the telescopes: ')
        
        if telescope_choice == '':
            telescope_choice = None
        
        print('\nPreprocessed file directory recognized. Advancing to video file generation.\n')

        #file = np.load(f'{save_directory}/')

        if telescope_choice is not None:
            choice = int(telescope_choice)-1
            with os.scandir(save_directory) as files:
            
                for file in files:
                    if os.path.splitext(os.path.basename(file.name))[1] == '.npy':
                        
                        playback_function(np.load(file, allow_pickle=True), telescope_choice, file.name, save_directory)
                        
        elif telescope_choice is None:
            with os.scandir(save_directory) as files:
                
                for file in files:
                    if os.path.splitext(os.path.basename(file.name))[1] == '.npy':
                        
                        playback_function(np.load(file, allow_pickle=True), None, file.name, save_directory)

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
        
        processed_data = aggregate_data(directory)
        
        if telescope_choice is not None:

            playback_function(processed_data[0], telescope_choice, processed_data[1], save_directory)

        elif telescope_choice is None:

            playback_function(processed_data[0], None, processed_data[1], save_directory)

elif option == 2:
    exit()
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

    print('\nPlease provide the directory of the files you would like to preprocess.')

    directory = select_file_directory()

    print(f'You selected: {directory}')

    save_directory = f'{directory}/pynoseti'

    if __name__ == '__main__':
        aggregated_data = aggregate_data(directory)

    file_prefix = Path(aggregated_data[1]).stem[:-6]

    np.save(f'{save_directory}/{file_prefix}preprocessed_data_cube', np.array(aggregated_data[0], dtype='object'))

    print(f'Data cube saved to: {save_directory}')
    print('Preprocessing of file directory complete!\n')

elif option == 4:
    exit()
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

elif option == 5:
    print('\n=====================================================================')
    print('Recognized telescopes:\n')
    i=1
    for telescope in telescope_list:
        print(f'{i}. {telescope}')
        i+=1
    print('=====================================================================\n')


#end_time = time.time()
#print('Reduction completed in '+str(end_time-start_time)+' seconds!')