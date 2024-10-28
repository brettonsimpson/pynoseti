from functions import *
def playback_function(file, choice, file_count):

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
        
        animation_list=[]
        j=0
        print('\nRendering movie files for all telescopes...')
        bar = progressbar.ProgressBar(max_value=len(array_image_list))

        bar.update(j)
        for telescope in array_image_list:
                
            fig, ax = plt.subplots()
            im = ax.imshow(array_image_list[j][0].data, cmap='viridis', vmin=0)
            cbar = fig.colorbar(im, ax=ax, orientation='vertical')
            title = ax.set_title('Frame Time: '+convert_unix_time(array_image_list[j][0].timestamp), loc='left')
            timestamp = ax.text(-0.5, 33, 'Frame 0 of '+str(len(array_image_list[j])))
            ax.set_axis_off()

            def animate(i):
                im.set_array(array_image_list[j][i].data)
                ax.set_title('Frame Time: '+convert_unix_time(array_image_list[j][i].timestamp), loc='left')
                timestamp.set_text(f'Frame {i} of '+str(len(array_image_list[j])))
                return [im, ax]

            animation_test = animation.FuncAnimation(fig, animate, frames=len(array_image_list[j]), interval=100, blit=True)
            animation_test.save(f'telescope_{j}_movie_{file_count}.mp4', writer='ffmpeg', fps=30)
            j+=1
            animation_list.append(animation_test)
            bar.update(j)