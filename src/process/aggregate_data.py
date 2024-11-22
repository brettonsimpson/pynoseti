import os
import numpy as np
import progressbar
import src

from src.process.classes import Sequence, Median
from src.process.read_capture_file import read_capture_file
from src.process.read_json_file import read_json_file
from src.process.generate_sequence import generate_sequence
from src.process.data_cube_list_assembler import data_cube_list_assembler

def aggregate_data(directory):

    telescope_list, quabo_address_list = read_json_file()

    save_directory = f'{directory}/pynoseti'

    if os.path.isdir(save_directory) is False:
        os.mkdir(save_directory)
    
    with os.scandir(directory) as files:

        file_count = 0
        file_iterate = 1

        for file in files:

            if file.is_file():

                if file_count == 0:
                    file_prefix = file.name

                file_count += 1

    with os.scandir(directory) as files:

        array_data_sequence_list = []

        for file in files:
            if file.is_file():

                print(f'Processing file {file_iterate} of {file_count}...')

                data, file_name = read_capture_file(file)

                sequence = generate_sequence(data, file_name, telescope_list)

                array_data_sequence_list.append(sequence)

                print('Complete!\n')

                file_iterate +=1

    return data_cube_list_assembler(array_data_sequence_list, telescope_list), file_prefix