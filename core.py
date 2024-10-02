print('\nWelcome to PyNOSETI!\n')
print('1: Playback\n',
      '    Options:\n',
      '     -Generates an .mp4 file for each telescope within each .pcapng file located within the provided directory.\n',
      '     -Select one telescope from one file to generate an .mp4 file for.\n')
print('2: Analyzer\n   -Produces a .csv file documenting transient centroids recognized in processed data.\n')
print('3: Preprocess a directory of .pcapng files.')
print('4: Perform all operations listed above.\n')
option = int(input('Enter the integer corresponding to the action you would like to do: '))

import os
import numpy as np
from functions import *
from reader import reader_function
from playback import playback_function
from analyzer import analyzer_function


if option == 1:

    #path = input('Please enter a directory for files you want to process: ')
    #path = path.replace('\\', '/')
    #path = path.replace('"', '')
    path = '/home/brett/Data_for_pynoseti'
    path = str(path)+'/pynoseti'

    if os.path.isdir(path):
        
        telescope_choice = input('\nWhich telescope would you like to playback data for?\n'
                            'Skip this prompt by pressing enter and process the entire file.\n'
                            'Enter the integer corresponding to one of the telescopes: ')
        
        print('\nPreprocessed file directory recognized. Advancing to video file generation.')

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
        reader_function(path)

        telescope_choice = input('Which telescope would you like to playback data for?\n'
                            'Skip this prompt by pressing enter and process the entire file.\n'
                            'Enter the integer corresponding to one of the telescopes: ')

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