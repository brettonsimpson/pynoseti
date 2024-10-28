from functions import *
def playback_function(path, file, choice, file_count):

    import os
    import numpy as np
    import progressbar
    import matplotlib.pyplot as plt
    from reader import reader_function
    import matplotlib.animation as animation
    
    telescope_choice = choice
    array_image_list = np.load(file, allow_pickle=True)

    if telescope_choice != '':

        telescope_choice = int(telescope_choice)-1

        fig, ax = plt.subplots()
        im = ax.imshow(array_image_list[telescope_choice][0].data, cmap='viridis', vmin=0, vmax=10000)
        cbar = fig.colorbar(im, ax=ax, orientation='vertical', label='Photoelectron Count')
        title = ax.set_title('Frame Time: '+convert_unix_time(array_image_list[telescope_choice][0].timestamp), loc='left')
        timestamp = ax.text(-0.5, 33, 'Frame 0 of '+str(len(array_image_list[telescope_choice])))
        
        ax.set_axis_off()

        def animate(i):
            im.set_array(array_image_list[telescope_choice][i].data)
            ax.set_title('Frame Time: '+convert_unix_time(array_image_list[telescope_choice][i].timestamp), loc='left')
            timestamp.set_text(f'Frame {i} of '+str(len(array_image_list[telescope_choice])))
            
            return [im, ax]

        animation_test = animation.FuncAnimation(fig, animate, frames=len(array_image_list[telescope_choice]), interval=100, blit=True)

        print('\nRendering movie file...\n')
        animation_test.save('test_movie.mp4', writer='ffmpeg', fps=60)
        print('Complete!\n\n')

    elif telescope_choice == '':
        
        print(f'{file_count} files counted!')

        subplot_count = 0
        with os.scandir(path) as files:
            for file in files:
                if file.is_file():
                    file_name = os.path.basename(file.name)
                    file_data = np.load(file, allow_pickle=True)
                    for element in file_data:
                        subplot_count +=1

        print(f'The subplot count is {subplot_count}!')


        def subplots_generator(file_count):
            column_number = int(np.ceil(np.sqrt(file_count)))
            row_number = int(np.ceil(file_count/column_number))

            fig, axes = plt.subplots(column_number, row_number, figsize = (5*column_number, 4*row_number))
            axes_list = axes.flatten()[:file_count]

            return fig, axes_list

        #fig, axes_list = subplots_generator(subplot_count)


        #print(path)
        j=0
        print('\nRendering movie files for all telescopes...')
        bar = progressbar.ProgressBar(max_value=len(array_image_list))

        bar.update(j)

        #i=0
        #for i in range(len(array_image_list)):
                                   
                
        fig, ax1 = plt.subplots()
        im = ax1.imshow(array_image_list[j][0].data, cmap='viridis', vmin=0)
        cbar = fig.colorbar(im, ax=ax1, orientation='vertical')
        title = ax1.set_title('Frame Time: '+convert_unix_time(array_image_list[j][0].timestamp), loc='left')
        timestamp = ax1.text(-0.5, 33, 'Frame 0 of '+str(len(array_image_list[j])))
        ax1.set_axis_off()

        fig, ax2 = plt.subplots()
        im = ax2.imshow(array_image_list[j][0].data, cmap='viridis', vmin=0)
        cbar = fig.colorbar(im, ax=ax2, orientation='vertical')
        title = ax2.set_title('Frame Time: '+convert_unix_time(array_image_list[j][0].timestamp), loc='left')
        timestamp = ax2.text(-0.5, 33, 'Frame 0 of '+str(len(array_image_list[j])))
        ax2.set_axis_off()
        
        fig, ax3 = plt.subplots()
        im = ax3.imshow(array_image_list[j][0].data, cmap='viridis', vmin=0)
        cbar = fig.colorbar(im, ax=ax3, orientation='vertical')
        title = ax3.set_title('Frame Time: '+convert_unix_time(array_image_list[j][0].timestamp), loc='left')
        timestamp = ax3.text(-0.5, 33, 'Frame 0 of '+str(len(array_image_list[j])))
        ax3.set_axis_off()

        #plt.tight_layout()
        #j+=1
            
        #ax1.plot()
        #plt.show()
        
       
        
        def animate(i):
       
            im.set_array(array_image_list[j][i].data)
            ax.set_title('Frame Time: '+convert_unix_time(array_image_list[j][i].timestamp), loc='left')
            timestamp.set_text(f'Frame {i} of '+str(len(array_image_list[j])))
            #plt.tight_layout()
            #j+=1
            return [im, ax]

        animation_test = animation.FuncAnimation(fig, animate, frames=len(array_image_list[k]), interval=100, blit=False)
        animation_test.save(f'telescope_{k}_movie_{file_count}.mp4', writer='ffmpeg', fps=30)
        print('animation printed!')
        k+=1
        bar.update(j)
        