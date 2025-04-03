#from moviepy.editor import VideoFileClip, concatenate_videoclips

import ffmpeg
import os

'''
def merge_playback_files(directory):

    for file in directory.glob('*.mp4'):
        file_list = []
        file_list.append(file)

    clips = [VideoFileClip(file) for file in file_list]
    
    final_clip = concatenate_videoclips(clips, method="compose")
    
    final_clip.write_videofile('merged_playback', codec="libx264", audio_codec="aac")
'''


def merge_playback_files(directory):
    
    video_list = []
    #for file in directory.glob('*.mp4'):
    #    video_list.append(file)

    with os.scandir(directory) as files:
        for file in files:
            if file.name.endswith('.mp4'):
                video_list.append(file.path)

    input_files = [ffmpeg.input(video) for video in video_list]
    joined = ffmpeg.concat(*input_files, v=1, a=1).output('output_file.mp4', codec='libx264', audio_codec='aac')
    joined.run()

    print('Done!')