import os
import numpy as np

from pynoseti.extract.extract_packet_data import extract_date_from_name

def assemble_batch_array(directory):
    
    file_list = []
    date_list = []

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

                date_list.append(int(extract_date_from_name(os.path.basename(file))))
                # Create a list of dates extracted from the file names of each file in the directory.
                # This is necessary because files can have their creation dates modified when copied
                # and pasted. Also, when creating batches, this ensures the batches are formed from a
                # list sorted by date first, not the other way around.
            
                if file_count == 0:
                    file_prefix = file.name

                file_count += 1
                # Increase the file count by one and continue on to the next file.

        dictionary = {}
        for date, file in zip(date_list, file_list):
            dictionary[date] = file
        # Create a dictionary whose values are the file names and the keys are the dates extracted from
        # the file names.

        sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1]))
        # Sorting the created dictionary in ascending order according to the size of the date integer.

        files_sorted_by_date = list(sorted_dict.values())
        # Extract only the file names from the dictionary sorted by date for batch formation.

    batch_count = (len(files_sorted_by_date) + batch_size - 1) // batch_size
    # Calculate the number of data batches to process.

    batch_array = np.array_split(np.array(files_sorted_by_date), batch_count)
    # Create an array for a number of batches corresponding to the division of the file count by the batch size.

    return batch_array
    # Returns final batch array.