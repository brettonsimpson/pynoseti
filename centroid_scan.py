import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from scipy import ndimage

from pynoseti.interface.select_file_directory import select_file_directory

#def centroid_scan(sequence, count_threshold=2000):

file_path = "/home/brett/Data/pynoseti/airplane_batch_test/pynoseti/Ima_onsky_batch_20_preprocessed_data_cube.npy"

file = np.load(file_path, allow_pickle=True)

count_threshold = 2000


j=0



#for sequence in file:



#for frame in sequence.sequence:





for sequence in file:

    centroids = []
    masked_frame_list = []

    for frame in file[j].sequence:

        

        masked_frame = frame.data > count_threshold

        #plt.imshow(masked_frame)
        #plt.colorbar()
        #plt.show()

        labeled_array, feature_number = ndimage.label(masked_frame)

        centroids.append(ndimage.center_of_mass(masked_frame, labeled_array, range(1, feature_number+1)))

        masked_frame_list.append(masked_frame)

    #print(centroids[1000])
    #plt.scatter(centroids[0][0], centroids)
    #plt.show()
    #exit()
    new_list = []

    for detection_list in centroids:

        detections = []


        for centroid in detection_list:
            detections.append([centroid[1], centroid[0]])

        new_list.append(detections)


    #print(new_list)
    #exit()

    #centroids = np.array(centroids)
    #centroids = centroids[:, [1, 0]]

    masked_frame_list = np.array(masked_frame_list)

    fig, ax= plt.subplots()

    im = ax.imshow(np.clip(file[j].sequence[0].data, a_min=0, a_max=None))
    scatter = ax.scatter([], [], color='r', s=50)
    title = ax.set_title('0')
    fig.colorbar(im)


    def animate(i):
        
        im.set_array(np.clip(file[j].sequence[i].data, a_min=0, a_max=None))
        ax.set_title(str(i))
        if new_list[i]:
            scatter.set_offsets(new_list[i])
        
        return [im, ax]


    playback_period = (file[j].sequence[len(file[0].sequence)-1].timestamp-file[0].sequence[0].timestamp)
    fps = len(file[0].sequence)/playback_period

    movie = animation.FuncAnimation(fig, animate, frames=len(file[0].sequence), interval=100, blit=False)
    movie.save(f'/home/brett/Data/pynoseti/airplane_batch_test/pynoseti/movie_{j}.mp4', writer='ffmpeg', fps=fps, dpi=60)
#plt.show()
    j+=1