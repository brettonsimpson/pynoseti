from functions import *
def playback_function():

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from reader import reader_function
    import progressbar

    array_image_list = reader_function()
    exit()
    telescope_choice = input('\nWhich telescope would you like to playback data for?\n'
                            'Skip this prompt by pressing enter and process the entire file.\n'
                            'Enter the integer corresponding to one of the telescopes: ')

    if telescope_choice != '':

        telescope_choice = int(telescope_choice)-1

        fig, ax = plt.subplots()
        im = ax.imshow(array_image_list[telescope_choice][0].data, cmap='viridis', vmin=0)
        cbar = fig.colorbar(im, ax=ax, orientation='vertical')
        title = ax.set_title('Frame Time: '+convert_unix_time(array_image_list[telescope_choice][0].timestamp), loc='left')
        timestamp = ax.text(-0.5, 33, 'Frame 0 of '+str(len(array_image_list[telescope_choice])))
        ax.set_axis_off()

        def animate(i):

            im.set_array(array_image_list[telescope_choice][i].data)

            ax.set_title('Frame Time: '+convert_unix_time(array_image_list[telescope_choice][i].timestamp), loc='left')

            timestamp.set_text(f'Frame {i} of '+str(len(array_image_list[telescope_choice])))

            return [im, ax]

        animation_test = animation.FuncAnimation(fig, animate, frames=len(array_image_list[telescope_choice]), interval=100, blit=False)

        print('\nRendering movie file...\n')
        animation_test.save('test_movie.mp4', writer='ffmpeg', fps=60)
        print('Complete!\n\n')

    elif telescope_choice == '':

        j=0
        print('\nRendering movie files for all telescopes...')
        #print(f'\nRendering movie file for telescope {j}...\n')
        bar = progressbar.ProgressBar(max_value=len(array_image_list))

        bar.update(j)
        for telescope in array_image_list:
                
            fig, ax = plt.subplots()
            im = ax.imshow(array_image_list[j][0].data, cmap='viridis', vmin=0)
            cbar = fig.colorbar(im, ax=ax, orientation='vertical')
            title = ax.set_title('Frame Time: '+convert_unix_time(array_image_list[j][0].timestamp), loc='left')
            timestamp = ax.text(-0.5, 33, 'Frame 0 of '+str(len(array_image_list[j])))
            #location = ax.text(33, -0.5, f'Dome: {array_image_list[j][0].dome}')
            ax.set_axis_off()

            def animate(i):

                im.set_array(array_image_list[j][i].data)

                ax.set_title('Frame Time: '+convert_unix_time(array_image_list[j][i].timestamp), loc='left')

                timestamp.set_text(f'Frame {i} of '+str(len(array_image_list[j])))
                #location.set_text(33, -0.5, f'Dome: {array_image_list[j][0].dome}')

                return [im, ax]

            animation_test = animation.FuncAnimation(fig, animate, frames=len(array_image_list[j]), interval=100, blit=False)

            animation_test.save(f'telescope_{j}_movie.mp4', writer='ffmpeg', fps=30)
            #print('\nComplete!\n')

            j+=1
            bar.update(j)