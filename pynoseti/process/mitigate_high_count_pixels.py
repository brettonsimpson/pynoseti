import numpy as np
from pynoseti.process.classes import High_Count_Pixel


def mitigate_high_count_pixels(sequence):

    time_series_pixel_list = []

    for i in range(len(sequence.sequence[0].data)):

        row = []

        for j in range(len(sequence.sequence[0].data)):

            row.append([])

        time_series_pixel_list.append(row)

    pixel_means_frame = time_series_pixel_list
    # 

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
    # Create a frame whose value everywhere is 1.0 except where a high count pixel mean is detected
    # so that division by the high count mask does

    i=0
    for row in high_count_mask:
        j=0
        for pixel in row:

            for high_count_pixel in high_count_pixels_list_with_means:

                if high_count_pixel.pixel == [i, j]:
                
                    ones_mask[i, j] *= high_count_pixel.local_mean

            j+=1
        i+=1


    for frame in sequence.sequence:

        frame.data = frame.data.astype(np.float32)/ones_mask


    return sequence