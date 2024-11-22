import os
import numpy as np
from src.process.classes import Median, Sequence

def data_cube_list_assembler(array_data_sequence_list, telescope_list):

    array_data_sequence_list = np.array(array_data_sequence_list, dtype='object')

    i=0

    final_sequence_array = []

    semifinal_telescope_data_array = []

    for telescope in range(len(telescope_list)):

        semifinal_telescope_data_array.append([])
        final_sequence_array.append([])

        for file in array_data_sequence_list:

            semifinal_telescope_data_array[i].append(file[i])
        
        i+=1

    i=0

    for telescope in semifinal_telescope_data_array:

        j=0

        for file in telescope:

            final_sequence_array[i].append(file)#[j])

        i+=1

    i=0

    final_telescope_data_array = []

    for telescope in range(len(telescope_list)):

        frame_number = 0

        temp_complete_sequence = []

        temp_median_list = []

        temp_telescope_identifier = ''

        temp_file_name = ''
        
        for file in final_sequence_array[i]:

            frame_selection = [frame_number]

            for frame in file.sequence:

                temp_complete_sequence.append(frame)
                frame_number+=1

            temp_complete_sequence = sorted(temp_complete_sequence, key=lambda obj: obj.timestamp)

            frame_selection.append(frame_number)

            temp_median_list.append(Median(file.median_data, frame_selection))

            temp_telescope_identifier = file.telescope

            temp_file_name = file.file_name
            
        final_telescope_data_array.append(Sequence(temp_complete_sequence,
                                                temp_median_list,
                                                temp_telescope_identifier,
                                                temp_file_name))
        
        i+=1

    return final_telescope_data_array