import numpy as np
import time
import matplotlib.pyplot as plt

file = np.load("/home/brett/Data/pynoseti/sample_airplane/pynoseti/Ima_onsky_batch_20_preprocessed_data_cube.npy", allow_pickle=True)
print(len(file[0].sequence))


file_data = file[1].sequence



start_time = time.time()

time_series_pixel_list = []




for i in range(len(file_data[0].data)):
    row = []
    for j in range(len(file_data[0].data[0])):
        row.append([])
    time_series_pixel_list.append(row)

    

pixel_means_frame = time_series_pixel_list


for frame in file_data:

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


end_time = time.time()

print(f'\nTime taken to read sequence: {end_time-start_time} seconds')

#print(pixel_means_frame[0][0])
#print(np.max(pixel_means_frame))

pixel_means_frame = np.array(pixel_means_frame)

#for pixel in pixel_means_frame[5]:
#    print(float(pixel))


#j=0
#for i in range(len(pixel_means_frame[5])):
#    pixel_means_frame[5][j] += 1000
#    j+=1

#pixel_means_frame[5][19] = 0




def pixel_boundaries_mean(mean_frame, row_index, column_index):

    high_count_pixels = []

    global_mean = np.mean(mean_frame)

    print(f'Gloabl mean is {global_mean}')

    high_count_mask = mean_frame < 5*global_mean
    
    i=0
    for row in high_count_mask:
        j=0
        for pixel in row:
            if pixel == 0:
                high_count_pixels.append([i, j])
            j+=1
        i+=1

    print(len(high_count_pixels))

    #plt.imshow(mean_frame)
    #plt.show()

    

    zeroed_mean_frame = mean_frame.copy()
    
    for pixel in high_count_pixels:

        zeroed_mean_frame[pixel[0]][pixel[1]] = 0
        
        #local_pixels_frame = zeroed_mean_frame[pixel[0]-1:pixel[0]+2,
        #                                pixel[1]-1:pixel[1]+2]
        
        x_min = max(pixel[0] - 1, 0)
        x_max = min(pixel[0] + 2, zeroed_mean_frame.shape[0])
        y_min = max(pixel[1] - 1, 0)
        y_max = min(pixel[1] + 2, zeroed_mean_frame.shape[1])
        local_pixels_frame = zeroed_mean_frame[x_min:x_max, y_min:y_max]
        
        local_mean = np.sum(local_pixels_frame) / local_pixels_frame.size-1
        #print(len(local_pixels_frame))
        zeroed_mean_frame[pixel[0]][pixel[1]] = mean_frame[pixel[0]][pixel[1]]/local_mean

        print(pixel[0], pixel[1], mean_frame[pixel[0]][pixel[1]])
        print(f'Value {mean_frame[pixel[0]][pixel[1]]} changed to {mean_frame[pixel[0]][pixel[1]]/local_mean} when the local mean is {local_mean}\n')
        
    plt.imshow(zeroed_mean_frame)
    plt.colorbar()
    plt.show()



pixel_boundaries_mean(pixel_means_frame, 5, 31)




    
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

