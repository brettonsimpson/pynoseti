from moviepy.editor import VideoFileClip, concatenate_videoclips

def merege_playback_files(directory):

    for file in directory.glob('*.mp4'):
        file_list = []
        file_list.append(file)

    clips = [VideoFileClip(file) for file in file_list]
    
    final_clip = concatenate_videoclips(clips, method="compose")
    
    final_clip.write_videofile('merged_playback', codec="libx264", audio_codec="aac")