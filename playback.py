from functions import *
def playback_function(file, choice, file_count, file_name):

    import os
    import numpy as np
    import progressbar
    import matplotlib.pyplot as plt
    from reader import reader_function
    import matplotlib.animation as animation
    from matplotlib.offsetbox import OffsetImage, AnnotationBbox
    import matplotlib.image as mpimg
    
    telescope_choice = choice
    array_image_list = np.load(file, allow_pickle=True)
    cwd_path = os.getcwd()

    if telescope_choice != '':
        telescope_choice = int(telescope_choice)-1

        fig, ax = plt.subplots()
        if 'Ima_onsky' in file_name:
            im = ax.imshow(np.clip(array_image_list[telescope_choice].sequence[0].data-array_image_list[telescope_choice].median_frame, a_min=0, a_max=1000), cmap='viridis', vmin=0)
            cbar = fig.colorbar(im, ax=ax, orientation='vertical', label='Photoelectron Count')
            timestamp = ax.set_title(convert_unix_time(array_image_list[telescope_choice].sequence[0].timestamp), loc='left', y=-0.065)
            frame_number = ax.text(-0.5, 34.25, 'Frame 0 of '+str(len(array_image_list[telescope_choice].sequence)))
            logo = mpimg.imread(str(cwd_path)+'/assets/panoseti_logo.png')
            logo_box = OffsetImage(logo, zoom=0.5)
            annotation_box = AnnotationBbox(logo_box, (0.148, 1.081), frameon=False, xycoords='axes fraction')
            ax.add_artist(annotation_box)
            ax.set_axis_off()

            def animate(i):
                im.set_array(np.clip(array_image_list[telescope_choice].sequence[i].data-array_image_list[telescope_choice].median_frame, a_min=0, a_max=1000))
                timestamp.set_title(convert_unix_time(array_image_list[telescope_choice].sequence[i].timestamp), loc='left', y=-0.065)
                frame_number.set_text(f'Frame {i} of '+str(len(array_image_list[telescope_choice].sequence)))
                return [im, ax]

        else:
            im = ax.imshow(array_image_list[telescope_choice].sequence[0].data, cmap='viridis', vmin=0)
            cbar = fig.colorbar(im, ax=ax, orientation='vertical', label='Photoelectron Count')
            title = ax.set_title(convert_unix_time(array_image_list[telescope_choice].sequence[0].timestamp), loc='left', y=-0.065)
            frame_number = ax.text(-0.5, 34.25, 'Frame 0 of '+str(len(array_image_list[telescope_choice].sequence)))
            logo = mpimg.imread(str(cwd_path)+'/assets/panoseti_logo.png')
            logo_box = OffsetImage(logo, zoom=0.5)
            annotation_box = AnnotationBbox(logo_box, (0.148, 1.081), frameon=False, xycoords='axes fraction')
            ax.add_artist(annotation_box)
            ax.set_axis_off()

            def animate(i):
                im.set_array(array_image_list[telescope_choice].sequence[i].data)
                ax.set_title(convert_unix_time(array_image_list[telescope_choice].sequence[i].timestamp), loc='left', y=-0.065)
                frame_number.set_text(f'Frame {i} of '+str(len(array_image_list[telescope_choice].sequence)))
                return [im, ax]
            
        movie = animation.FuncAnimation(fig, animate, frames=len(array_image_list[telescope_choice].sequence), interval=100, blit=False)
        movie.save(f'telescope_{telescope_choice}_movie_{file_count}.mp4', writer='ffmpeg', fps=30)
        print('\nRendering movie file...\n')
        print('Complete!\n')

    elif telescope_choice == '':
        bar = progressbar.ProgressBar(max_value=len(array_image_list))
        print('\nRendering movie files for all telescopes...')
        bar.update(j)
        j=0
        
        for telescope in array_image_list:
            fig, ax = plt.subplots()
            if 'Ima_onsky' in file_name:
                im = ax.imshow(np.clip(array_image_list[j].sequence[0].data-array_image_list[j].median_frame, a_min=0, a_max=1000), cmap='viridis', vmin=0)
                cbar = fig.colorbar(im, ax=ax, orientation='vertical', label='Photoelectron Count')
                title = ax.set_title('Frame Time: '+convert_unix_time(array_image_list[j].sequence[0].timestamp), loc='left')
                frame_number = ax.text(-0.5, 33, 'Frame 0 of '+str(len(array_image_list[j].sequence)))
                ax.set_axis_off()

                def animate(i):
                    im.set_array(np.clip(array_image_list[j].sequence[i].data-array_image_list[j].median_frame, a_min=0, a_max=1000))
                    ax.set_title('Frame Time: '+convert_unix_time(array_image_list[j].sequence[i].timestamp), loc='left')
                    frame_number.set_text(f'Frame {i} of '+str(len(array_image_list[j].sequence)))
                    return [im, ax]

            else:
                im = ax.imshow(array_image_list[j].sequence[0].data, cmap='viridis', vmin=0)
                cbar = fig.colorbar(im, ax=ax, orientation='vertical', label='Photoelectron Count')
                title = ax.set_title('Frame Time: '+convert_unix_time(array_image_list[j].sequence[0].timestamp), loc='left')
                frame_number = ax.text(-0.5, 33, 'Frame 0 of '+str(len(array_image_list[j].sequence)))
                ax.set_axis_off()

                def animate(i):
                    im.set_array(array_image_list[j].sequence[i].data)
                    ax.set_title('Frame Time: '+convert_unix_time(array_image_list[j].sequence[i].timestamp), loc='left')
                    frame_number.set_text(f'Frame {i} of '+str(len(array_image_list[j].sequence)))
                    return [im, ax]
                
            movie = animation.FuncAnimation(fig, animate, frames=len(array_image_list[j].sequence), interval=100, blit=False)
            movie.save(f'telescope_{j}_movie_{file_count}.mp4', writer='ffmpeg', fps=30)
            j+=1
            bar.update(j)