import os
import gc
import numpy as np

from pynoseti.process.assemble_batch_array import assemble_batch_array
from pynoseti.process.read_json_file import read_json_file
from pynoseti.process.aggregate_batch_data import aggregate_batch_data

def process_directory(directory, option):

    batch_array = assemble_batch_array(directory)

    telescope_list, quabo_address_list = read_json_file()

    save_directory = f'{directory}/pynoseti'

    if os.path.isdir(save_directory) is False:
        os.mkdir(save_directory)

    if __name__ == '__main__':

        batch_iterate = 0

        for batch in batch_array:

            print(f'\nProcessing batch {batch_iterate+1} of {len(batch_array)}...')

            aggregated_data = aggregate_batch_data(batch, telescope_list)

            if option == 3:

                np.save(f'{save_directory}/batch_{batch_iterate+1}_preprocessed_data_cube',
                        np.array(aggregated_data, dtype='object'))
                
                print(f'Data cube saved to: {save_directory}')
        
            batch_iterate +=1

            if option != 3:
                return aggregated_data

            del aggregated_data
            gc.collect()

        print('\nPreprocessing of file directory complete!\n')