import os
import numpy as np
import progressbar
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from src.extract.convert_unix_time import convert_unix_time


def playback_function(file, choice, file_count, file_name, path):

    telescope_choice = choice
    array_image_list = np.load(file, allow_pickle=True)
    cwd_path = os.getcwd()

    if telescope_choice != '':
        telescope_choice = int(telescope_choice)-1
        
        
        fig, ax = plt.subplots()
        if 'Ima_onsky' in file_name:
            im = ax.imshow(np.clip(array_image_list[telescope_choice].sequence[0].data-array_image_list[telescope_choice].median_data[0].median_frame, a_min=0, a_max=1000), cmap='viridis', vmin=0)
            cbar = fig.colorbar(im, ax=ax, orientation='vertical', label='Photoelectron Count')
            timestamp = ax.set_title(convert_unix_time(array_image_list[telescope_choice].sequence[0].timestamp), loc='left', y=-0.065)
            frame_number = ax.text(-0.5, 34.25, 'Frame 1 of '+str(len(array_image_list[telescope_choice].sequence)+1))
            logo = mpimg.imread(str(cwd_path)+'/assets/panoseti_logo.png')
            logo_box = OffsetImage(logo, zoom=0.5)
            annotation_box = AnnotationBbox(logo_box, (0.148, 1.081), frameon=False, xycoords='axes fraction')
            ax.add_artist(annotation_box)
            ax.set_axis_off()

            def animate(i):
                im.set_array(np.clip(array_image_list[telescope_choice].sequence[i].data-array_image_list[telescope_choice].median_data[0].median_frame, a_min=0, a_max=1000))
                ax.set_title(convert_unix_time(array_image_list[telescope_choice].sequence[i].timestamp), loc='left', y=-0.065)
                frame_number.set_text(f'Frame {i+1} of '+str(len(array_image_list[telescope_choice].sequence)+1))
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
        movie.save(f'telescope_{telescope_choice}_movie_{file_count}.mp4', writer='ffmpeg', fps=200, dpi=60)
        print('\nRendering movie file...\n')
        print('Complete!\n')

    elif telescope_choice == '':
        print('\nRendering movie file for all telescopes...')

        plot_number = len(array_image_list)
        fig, axes = plt.subplots(1, plot_number, figsize=(4*plot_number,4))
        axes = np.atleast_1d(axes)

        if 'Ima_onsky' in file_name:

            ims = [ax.imshow(array_image_list[i].sequence[0].data, animated=True, vmin=0) for i, ax in enumerate(axes)]
            frame_number = ims[0].axes.text(14, -4.58, 'Frame 1 of '+str(len(array_image_list[0].sequence)+1))
            logo = mpimg.imread(str(cwd_path)+'/assets/panoseti_logo.png')
            logo_box = OffsetImage(logo, zoom=0.3)
            annotation_box = AnnotationBbox(logo_box, (0, 1.15), frameon=False, xycoords='axes fraction')
            ims[0].axes.add_artist(annotation_box)

            for i, ax in enumerate(axes):
                ax.set_title('PDT '+convert_unix_time(array_image_list[i].sequence[0].timestamp), loc='left')
                telescope = ax.text(-0.5, 33.5, f'{str(array_image_list[i].telescope)}')
                ax.set_axis_off()

            def animate(frame):
                for i, im in enumerate(ims):
                    im.set_array(np.clip(array_image_list[i].sequence[frame].data, a_min=0, a_max=None))
                    im.axes.set_title('PDT '+convert_unix_time(array_image_list[i].sequence[frame].timestamp), loc='left')
                    frame_number.set_text(f'Frame {frame+1} of '+str(len(array_image_list[i].sequence)+1))
                return [im]
            
            movie = animation.FuncAnimation(fig, animate, frames=len(array_image_list[0].sequence), interval=100, blit=False)
            movie.save(f'{path}/telescope_{plot_number}_movie2_{file_count}.mp4', writer='ffmpeg', fps=30, dpi=60)

        else:
            ims = [ax.imshow(array_image_list[i].sequence[0].data, animated=True, vmin=0) for i, ax in enumerate(axes)]
            frame_number = ims[0].axes.text(14, -4.58, 'Frame 1 of '+str(len(array_image_list[0].sequence)+1))
            logo = mpimg.imread(str(cwd_path)+'/assets/panoseti_logo.png')
            logo_box = OffsetImage(logo, zoom=0.3)
            annotation_box = AnnotationBbox(logo_box, (0, 1.15), frameon=False, xycoords='axes fraction')
            ims[0].axes.add_artist(annotation_box)

            for i, ax in enumerate(axes):
                ax.set_title('PDT '+convert_unix_time(array_image_list[i].sequence[0].timestamp), loc='left')
                telescope = ax.text(-0.5, 33.5, f'{str(array_image_list[i].telescope)}')
                ax.set_axis_off()

            def animate(frame):
                for i, im in enumerate(ims):
                    im.set_array(np.clip(array_image_list[i].sequence[frame].data, a_min=0, a_max=None))
                    im.axes.set_title('PDT '+convert_unix_time(array_image_list[i].sequence[frame].timestamp), loc='left')
                    frame_number.set_text(f'Frame {frame+1} of '+str(len(array_image_list[i].sequence)+1))
                return [im]
            
            movie = animation.FuncAnimation(fig, animate, frames=len(array_image_list[0].sequence), interval=100, blit=False)
            movie.save(f'{path}/telescope_{plot_number}_movie2_{file_count}.mp4', writer='ffmpeg', fps=15, dpi=60)