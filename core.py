import os
import time
import numpy as np
from functions import *
from reader_copy import reader_function
from playback_copy import playback_function
from analyzer import analyzer_function

print('\nWelcome to PyNOSETI!\n')
print('1: Playback Options: [Under Development]\n',
      '     -Renders an .mp4 file that compiles the continuous playback data for each telescope.')
print('2: Analyzer [Under Development]\n',
      '     -Produces a .csv file cataloguing transient centroids recognized in processed data.')
print('3: Preprocess a directory of .pcapng files.\n',
      '     -Generate a file containing preprocessed observational data for all files within a directory.\n',
      '     -WARNING: Requires disk space equal to approximately four times the size of .pcapng file directory.')
print('4: Perform all operations listed above. [Untested]\n')
option = int(input('Enter the integer corresponding to the action you would like to do: '))

#start_time = time.time()

if option == 1:

    path = input('Please enter a directory for files you want to process: ')
    path = path.replace('\\', '/')
    path = path.replace('"', '')
    path = '/home/brett/Data_for_pynoseti/median_image_script_testing'
    #path = '/home/brett/Data_for_pynoseti/ph'
    #path = str(path)+'/pynoseti'

    if os.path.isdir(path):
        
        telescope_choice = input('\nWhich telescope would you like to playback data for?\n'
                            'Skip this prompt by pressing enter and process the entire file.\n'
                            'Enter the integer corresponding to one of the telescopes: ')
        
        print('\nPreprocessed file directory recognized. Advancing to video file generation.')

        path = str(path)+'/pynoseti'

        if telescope_choice != '':
            
            #'''
            choice = int(telescope_choice)-1
            with os.scandir(path) as directory:
                file_count = 1
                for file in directory:
                    if os.path.splitext(path+os.path.basename(file.name))[1] == '.npy':
                        #if file_count == choice:
                        playback_function(file, telescope_choice, file_count, file.name)
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
                        playback_function(file, telescope_choice, file_count, file.name)
                        
                        #print('test')


    else:
        print('\nPreprocessed file directory not recognized. Generating file directory...')
        telescope_choice = input('Which telescope would you like to playback data for?\n'
                            'Skip this prompt by pressing enter and process the entire file.\n'
                            'Enter the integer corresponding to one of the telescopes: ')
        print('')
        
        #os.mkdir(str(path)+'/pynoseti')
        print('Target directory created for selected files at '+str(path)+'/panoseti\n')
        
        reader_function(path)
        
        if telescope_choice != '':
            choice = int(telescope_choice)-1
            with os.scandir(path+str('/pynoseti')) as files:
                file_count = 0
                for file in files:
                    if os.path.splitext(path+os.path.basename(file.name))[1] == '.npy':
                        if file_count == choice:
                            playback_function(file, telescope_choice)
                        choice += 1

        elif telescope_choice == '':
            print(path)
            with os.scandir(path) as files:
                file_count = 1
                for file in files:
                    file_count += 1
                    if os.path.splitext(path+os.path.basename(file.name))[1] == '.npy':
                        playback_function(path, file, telescope_choice, file_count)

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

    path = '/home/brett/Data_for_pynoseti/median_image_script_testing'
    #path = '/home/brett/Data_for_pynoseti/ph'
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