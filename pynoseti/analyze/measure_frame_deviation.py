import numpy as np

def mean_sequence_deviation(sequence):

    frame_sequence = []    

    for frame in sequence.sequence:
        frame_sequence.append(frame.data)
        #print(frame.data)
    
    mean_frame = np.mean(np.stack(np.array(frame_sequence)), axis=0)
    standard_deviation = np.std(np.array(frame_sequence), axis=0)
    variance = np.var(np.array(frame_sequence), axis=0)
    #print(mean_frame)

    return mean_frame, standard_deviation, variance