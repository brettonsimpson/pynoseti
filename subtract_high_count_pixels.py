import numpy as np
import time
import matplotlib.pyplot as plt

file = np.load("/home/brett/Data/pynoseti/airplane_batch_test/pynoseti/Ima_onsky_batch_20_preprocessed_data_cube.npy", allow_pickle=True)
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

for pixel in pixel_means_frame[5]:
    print(float(pixel))


#j=0
#for i in range(len(pixel_means_frame[5])):
#    pixel_means_frame[5][j] += 1000
#    j+=1

#pixel_means_frame[5][19] = 0

def pixel_boundaries_mean(mean_frame, row_index, column_index):

    if row_index == 0 or 31:

        if row_index == 0 and 31 > column_index > 0:

            mean = np.mean([mean_frame[row_index+1][column_index],      # Right of pixel
                            mean_frame[row_index][column_index+1],      # Below pixel
                            mean_frame[row_index+1][column_index+1],    # Lower right of pixel
                            mean_frame[row_index][column_index-1],      # Above pixel
                            mean_frame[row_index+1][column_index-1]])   # Upper right of pixel
            return mean
            
        elif row_index == 31 and 31 > column_index > 0:

            mean = np.mean([mean_frame[row_index-1][column_index],      # Left of pixel
                            mean_frame[row_index][column_index+1],      # Below pixel
                            mean_frame[row_index-1][column_index+1],    # Lower left of pixel
                            mean_frame[row_index][column_index-1],      # Above pixel
                            mean_frame[row_index-1][column_index-1]])   # Upper left of pixel
            return mean

        elif row_index == 0 and column_index == 0:
        
            mean = np.mean([mean_frame[row_index+1][column_index],      #
                            mean_frame[row_index][column_index+1],      #
                            mean_frame[row_index+1][column_index+1]])   #
            return mean

        elif row_index == 0 and column_index == 31:
            
            mean = np.mean([mean_frame[row_index-1][column_index],      #
                            mean_frame[row_index][column_index-1],      #
                            mean_frame[row_index-1][column_index-1]])   #
            return mean
            
        elif row_index == 0 and column_index == 31:

            mean = np.mean([mean_frame[row_index+1][column_index],      #
                            mean_frame[row_index][column_index-1],      #
                            mean_frame[row_index+1][column_index-1]])   #
            return mean

        elif row_index == 31 and column_index == 0:

            mean = np.mean([mean_frame[row_index-1][column_index],      #
                            mean_frame[row_index-1][column_index+1],    #
                            mean_frame[row_index][column_index+1]])     #
            return mean

    elif column_index == 0 or 31:

        if column_index == 0 and 31 > row_index > 0:

            mean = np.mean([mean_frame[row_index+1][column_index],      # Right of pixel
                            mean_frame[row_index][column_index+1],      # Below pixel
                            mean_frame[row_index+1][column_index+1],    # Lower right of pixel
                            mean_frame[row_index-1][column_index+1],    # Lower left of pixel
                            mean_frame[row_index-1][column_index]])   # Left of pixel
            return mean
            
        elif column_index == 31 and 31 > row_index > 0:

            mean = np.mean([mean_frame[row_index-1][column_index],      # Left of pixel
                            mean_frame[row_index+1][column_index],      # Right of pixel
                            mean_frame[row_index-1][column_index-1],    # Upper left of pixel
                            mean_frame[row_index][column_index-1],      # Above pixel
                            mean_frame[row_index+1][column_index-1]])   # Upper right of pixel
            return mean

        elif row_index == 0 and column_index == 0:
        
            mean = np.mean([mean_frame[row_index+1][column_index],      #
                            mean_frame[row_index][column_index+1],      #
                            mean_frame[row_index+1][column_index+1]])   #
            return mean

        elif row_index == 31 and column_index == 31:
            
            mean = np.mean([mean_frame[row_index-1][column_index],      #
                            mean_frame[row_index][column_index-1],      #
                            mean_frame[row_index-1][column_index-1]])   #
            return mean
            
        elif row_index == 0 and column_index == 31:

            mean = np.mean([mean_frame[row_index+1][column_index],      #
                            mean_frame[row_index][column_index-1],      #
                            mean_frame[row_index+1][column_index-1]])   #
            return mean

        elif row_index == 31 and column_index == 0:

            mean = np.mean([mean_frame[row_index-1][column_index],      #
                            mean_frame[row_index-1][column_index+1],    #
                            mean_frame[row_index][column_index+1]])     #
            return mean
        
    elif 31 > row_index > 0 and 31 > column_index > 0:

        mean = np.mean([frame[row_index-1][column_index],       #
                        frame[row_index+1][column_index],       #
                        frame[row_index][column_index-1],       #
                        frame[row_index][column_index+1],       #
                        frame[row_index+1][column_index+1],     #
                        frame[row_index-1][column_index+1],     #
                        frame[row_index-1][column_index-1],     #
                        frame[row_index+1][column_index-1]])    #
        
        return mean
        
    

    #return mean





print('\n')
print(pixel_boundaries_mean(pixel_means_frame, 5, 19))

print('\n')
print(pixel_boundaries_mean(pixel_means_frame, 0, 0))
print(pixel_boundaries_mean(pixel_means_frame, 0, 31))
print(pixel_boundaries_mean(pixel_means_frame, 31, 0))
print(pixel_boundaries_mean(pixel_means_frame, 31, 31))
exit()


print('\n')
print(pixel_means_frame[5][19]/pixel_boundaries_mean(pixel_means_frame, 5, 19))


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


'''
pixel_means_frame[4][19] = 1000
pixel_means_frame[6][19] = 1000
pixel_means_frame[5][18] = 1000
pixel_means_frame[5][20] = 1000
pixel_means_frame[6][20] = 1000
pixel_means_frame[4][20] = 1000
pixel_means_frame[4][18] = 1000
pixel_means_frame[6][18] = 1000
'''



plt.imshow(pixel_means_frame)
#plt.imshow(test_frame)
plt.colorbar()
plt.show()

#19, 5 -1 from each
#17, 5 -1 rom each