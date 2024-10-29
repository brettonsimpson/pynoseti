import numpy as np
import matplotlib.pyplot as plt




file = np.load('/home/brett/Data_for_pynoseti/median_image_script_testing/pynoseti/pynoseti_Ima_onskyima2pe__20230428_050009.pcapng1.npy', allow_pickle=True)

plt.imshow(file[0].data[0].data)
plt.show()

print('test')

exit()
for telescope in file:
    frame_sequence = []
    for frame in telescope:
        frame_sequence.append(frame.data)
    stacked_sequence = np.stack(frame_sequence)
    print(stacked_sequence.shape)



    #print(len(telescope.data))
    #image_sequence = np.stack(telescope.data)
    #print(telescope.shape)




exit()


for frame in file[0]:
    new_array.append(frame.data)

new_array = np.stack(np.array(new_array))

print(new_array.shape)

median_frame = np.median(new_array, axis=0)


plt.imshow(np.clip(new_array[0]-median_frame, a_min=0, a_max=None))
#plt.imshow(median_frame)
#plt.imshow(new_array[0])
cbar = plt.colorbar()
plt.show()

exit()

plt.scatter(random_data_1[0], random_data_1[1])
plt.show()