import numpy as np
import time
import matplotlib.pyplot as plt

file = np.load("/Users/brettonsimpson/Data/PANOSETI/sample_airplane_TEST/pynoseti/Ima_onsky_batch_20_preprocessed_data_cube_TEST.npy", allow_pickle=True)

from pynoseti.process.classes import High_Count_Pixel

#file_data = file[1].sequence

for sequence in file:
    time_series_pixel_list = []
    for i in range(len(sequence.sequence[0].data)):
        row = []
        for j in range(len(sequence.sequence[0].data)):
            row.append([])
        time_series_pixel_list.append(row)
    pixel_means_frame = time_series_pixel_list
    for frame in sequence.sequence:
        i=0
        j=0
        for row in np.clip(frame.data, a_min=0, a_max=None):
            j=0
            for pixel in row:
                time_series_pixel_list[i][j].append(pixel)
                j+=1
            i+=1
    i=0
    j=0
    for row in time_series_pixel_list:
        j=0
        for pixel in row:
            pixel_means_frame[i][j] = np.mean(time_series_pixel_list[i][j])
            j+=1
        i+=1
    pixel_means_frame = np.array(pixel_means_frame)

    high_count_pixels = []
    global_mean = np.mean(pixel_means_frame)

    high_count_mask = pixel_means_frame < 5*global_mean
    i=0
    for row in high_count_mask:
        j=0
        for pixel in row:
            if pixel == 0:
                high_count_pixels.append([i, j])
            j+=1
        i+=1
    zeroed_mean_frame = pixel_means_frame.copy()

    #plt.imshow(high_count_mask)
    #plt.colorbar()
    #plt.show()

    #plt.imshow(pixel_means_frame)
    #plt.colorbar()
    #plt.show()




    high_count_pixels_list_with_means = []

    for pixel in high_count_pixels:

        zeroed_mean_frame[pixel[0]][pixel[1]] = 0
        
        x_min = max(pixel[0] - 1, 0)
        x_max = min(pixel[0] + 2, zeroed_mean_frame.shape[0])
        y_min = max(pixel[1] - 1, 0)
        y_max = min(pixel[1] + 2, zeroed_mean_frame.shape[1])
        local_pixels_frame = zeroed_mean_frame[x_min:x_max, y_min:y_max]
        
        local_mean = np.sum(local_pixels_frame) / local_pixels_frame.size-1

        zeroed_mean_frame[pixel[0]][pixel[1]] = pixel_means_frame[pixel[0]][pixel[1]]/local_mean


        high_count_pixels_list_with_means.append(High_Count_Pixel(pixel, local_mean))

    ones_mask = np.ones((32,32))
    i=0
    for row in high_count_mask:
        j=0
        for pixel in row:

            for high_count_pixel in high_count_pixels_list_with_means:

                if high_count_pixel.pixel == [i, j]:
                
                    ones_mask[i, j] *= high_count_pixel.local_mean

            j+=1
        i+=1




    print('going through sequence')

    for frame in sequence.sequence:

        #frame = frame.data.astype(np.float32)

        frame.data = frame.data.astype(np.float32) / ones_mask

    


    
            



    #save_file_list.append()

np.save("/Users/brettonsimpson/Data/PANOSETI/sample_airplane_TEST/pynoseti/Ima_onsky_batch_20_preprocessed_data_cube_TEST.npy", np.array(file, dtype='object'))











    
'''
max = 0
i=0
for row in mean_frame:
    
    
    j=0
    for column in row:

        local_pixels_frame = mean_frame[i-1:i+2,
                                        j-1:j+2]

        #try:
            #print(np.max(local_pixels_frame))
        #except ValueError:
        #    pass
        
        #plt.imshow(local_pixels_frame)
        #plt.show()
        
        try:
            local_max = np.max(local_pixels_frame)
            if local_max > max:
                max = local_max

        except ValueError:
            local_max = None

        #if column in local_pixels_frame:
        #    print(len(local_pixels_frame))


        #if column > 3*np.mean(local_pixels_frame):
        #    continue

        j+=1
    
    i+=1
'''

#print(max)
    
    
#print(np.mean(pixel_means_frame))







exit()



test_frame = np.clip(file_data[0].data, a_min=0, a_max=None)


i=0
j=0
for row in pixel_means_frame:

    j=0
    for pixel in row:

        if pixel_means_frame[i][j] > pixel_boundaries_mean(pixel_means_frame, i, j):

            pass

        j+=1

    i+=1

