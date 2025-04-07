import os
import gc
import numpy as np



from pynoseti.process.assemble_batch_array import assemble_batch_array
from pynoseti.process.read_json_file import read_json_file
from pynoseti.process.aggregate_batch_data import aggregate_batch_data

def process_directory(directory, option):

    batch_array = assemble_batch_array(directory)

    telescope_list, quabo_address_list = read_json_file()

    pynoseti_directory = f'{directory}/pynoseti'

    data_directory = f'{directory}/pynoseti/data'

    if os.path.isdir(pynoseti_directory) is False:
        os.mkdir(pynoseti_directory)

    if os.path.isdir(data_directory) is False:
        os.mkdir(data_directory)

    batch_iterate = 0

    for batch in batch_array:

        print(f'\nProcessing batch {batch_iterate+1} of {len(batch_array)}...')

        aggregated_data = aggregate_batch_data(batch, telescope_list)

        if option == 3:

            for file in batch:

                if 'Ima_onsky' in file:

                    imaging_mode = True

                else:
                    imaging_mode = False

            if imaging_mode is True:

                np.save(f'{data_directory}/Ima_onsky_batch_{batch_iterate+1}_preprocessed_data_cube',
                        np.array(aggregated_data, dtype='object'))
                
                print(f'Data cube saved to: {data_directory}')

            else:
                np.save(f'{data_directory}/batch_{batch_iterate+1}_preprocessed_data_cube',
                        np.array(aggregated_data, dtype='object'))
                
                print(f'Data cube saved to: {data_directory}')
            
        batch_iterate +=1

        if option != 3:
            return aggregated_data

        del aggregated_data
        gc.collect()

    print('\nPreprocessing of file directory complete!\n')