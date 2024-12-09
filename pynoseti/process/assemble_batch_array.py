import os
import numpy as np

def assemble_batch_array(directory):
    
    file_list = []

    batch_size = 5
    # Define the number of files that are contained within one batch.

    with os.scandir(directory) as files:
    # Create a list of files to be iterated over from the provided directory.

        file_count = 0
        file_iterate = 1
        # Specify iterable variables to be used in the following for loops.

        for file in files:

            if file.is_file():
            # Clarifies that the current element in the for loop is a file and not a directory.

                file_list.append(os.path.abspath(file))
                # Adds the absolute path for each file to a list for later reference.
            
                if file_count == 0:
                    file_prefix = file.name

                file_count += 1
                # Increase the file count by one and continue on to the next file.

    batch_count = (len(file_list) + batch_size - 1) // batch_size
    # Calculate the number of data batches to process.

    batch_array = np.array_split(np.array(file_list), batch_count)
    # Create an array for a number of batches corresponding to the division of the file count by the batch size.

    return batch_array
    # Returns final batch array.