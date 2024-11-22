import numpy as np

data = np.load('')

def mean_sequence_deviation(sequence):

    frame_sequence = []    

    for frame in sequence.sequence:
        frame_sequence.append(frame.data)
    
    mean_frame = np.mean(np.stack(np.array(frame_sequence, dtype='object')))

print(mean_sequence_deviation(data[0]))