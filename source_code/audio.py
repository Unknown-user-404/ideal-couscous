import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import os

#UNFINISHED! Bigger works will be in the future
def grab_audio(file_name: str):
    print("-----audio grabbing-----")
    command = f"ffmpeg -i ./input/{file_name} -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    subprocess.call(command, shell=True)
    print("-----audio grabbing-----")

def insert_audio(file_extension: str):
    video_clip = VideoFileClip("result" + file_extension)
    audio_clip = AudioFileClip("audio.wav")
    start = 0
    end = video_clip.end
    audio_clip = audio_clip.subclip(start, end)
    final_audio = audio_clip
    #add audio
    final_clip = video_clip.set_audio(final_audio)
    #save
    final_clip.write_videofile("final.mp4")
    #delete files
    os.remove("./audio.wav")
    os.remove("./result" + file_extension)