import os
import numpy as np
import read_json_file
from functions import Sequence

def data_cube_assembler(path):
    telescope_list, quabo_address_list = read_json_file(file)

    #for element
    
    processes = int(os.cpu_count()/2)
    
    os.mkdir(str(path)+'/pynoseti')

    with os.scandir(path) as files:

        file_count = 0

        for file in files:

            if file.is_file():
                file_count += 1

    array_data_sequence_list = []

    array_data_sequence_list = np.array(array_data_sequence_list)

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

            final_sequence_array[i].append(file[j])

        i+=1

    i=0

    final_telescope_data_array = []

    for telescope in range(len(telescope_list)):

        frame_number = 0

        temp_complete_sequence = []

        temp_median_list = []

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

    return(final_telescope_data_array)