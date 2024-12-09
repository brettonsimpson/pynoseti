from pynoseti.process.read_capture_file_batch import read_capture_file_batch
from pynoseti.process.generate_sequence import generate_sequence
from pynoseti.process.data_cube_list_assembler import data_cube_list_assembler


def aggregate_batch_data(batch, telescope_list):

    array_data_sequence_list = []

    data = read_capture_file_batch(batch)
    #########REMEMBER TO RETURN LIST OF FILE NAMES INCLUDED IN BATCH#############

    sequence = generate_sequence(data,
                                 batch,
                                 telescope_list)

    array_data_sequence_list.append(sequence)

    final_data = data_cube_list_assembler(array_data_sequence_list,
                                          telescope_list)
    
    del data, sequence, array_data_sequence_list, telescope_list


    return final_data