from moviepy.editor import *
import os

PAUSE_BETWEEN_AUDIO = 0.5

# Gather input
def GetFiles(path):
    """Gathers file names

    Args:
        path (string): representing path to a local folder

    Returns:
        List: of strings; paths to files in the folder
    """
    try:
        files = os.listdir(path)
        for i in range(len(files)):
            files[i] = path+"\\"+files[i]
        return files
    except Exception as error:
        print("ABORT:",error,"\nAdd the folder to the local directory of VideoScript.py")
        quit()

# Verify Input
def VerifyFiles(audio, images, long, music):
    """Verifies if the input files will be sufficient for a video.
    Must pass the following Contraints:
        - None of the folders are empty
        - LongVideo folder contains one video
        - Amount of image files equals the amount of audio files
        - Long video duration is greater than or equal to cumulative audio duration
        - Check with user

    Args:
        audio (List): strings representing file names for each audio
        images (List): ... image
        music (List): ... music
        long (List): the long video
    """
    print("Verifying inputs...")
    
    folders = {"Audio":audio, "Images":images, "LongVideo":long, "Music":music}
    for folder in folders:
        print(folders[folder])
        if len(folders[folder]) == 0:
            print("ABORT:",folder,"folder is empty.")
            quit()


    if len(images) != len(audio):
        print("ABORT: Amount of images is not equal to the amount of audio.")
        quit()
    

    if len(long_video) > 1:
        print("ABORT: Too many files in the LongVideo folder.")
    

    cumulative_audio_duration = 0.0
    long = VideoFileClip(long[0])
    for audio_clip in audio:
        audio_clip = AudioFileClip(audio_clip)
        cumulative_audio_duration += audio_clip.duration + PAUSE_BETWEEN_AUDIO
    if long.duration < cumulative_audio_duration:
        print("ABORT: Long video duration is shorter than the audio duration")
        quit()

    user_input = input("$$$$$ Video duration expected to be [" + GetVerboseDuration(cumulative_audio_duration) + "] while long video duration is [" + GetVerboseDuration(long.duration) + "]\n$$$$$ Enter 'y' to proceed: ")
    if user_input != 'y':
        print("ABORT: User did not select 'y'.")
        quit()
    
    print("Input Verified.")
def GetVerboseDuration(duration):
    """Takes in a float duration of some amount of seconds 
    and returns the minutes and seconds verbosely

    Args:
        duration (float): seconds of the input

    Returns:
        String
    """
    minutes = int(duration/60.0)
    seconds = duration - (minutes*60)
    verbose_time = str(minutes)+" minutes "+str(seconds)+" seconds"
    return verbose_time

# Construct video
def CombineAudioImage(audio, images):
    """Takes each pair of audio and their respective image (Alphabetical order)
    and combines them into a short video. Then combines all of those short videos into one.

    Args:
        audio (List): of string paths to audio
        images (List): ... images
    
    Returns:
        VideoFileClip; the top half of the video
    """
    print("Creating top half video...")
    short_videos = []

    for audio_path, image_path in zip(audio, images):
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration + PAUSE_BETWEEN_AUDIO

        image_clip = ImageClip(image_path).set_duration(duration).set_audio(audio_clip)
        short_videos.append(image_clip)

    top_video = concatenate_videoclips(short_videos)
    print("Top half complete.")
    return top_video

# # Concatenate all image/audio clips for the top half
# top_video = concatenate_videoclips(top_clips)

# # Resize both videos to stack vertically
# height = min(top_video.h, long_video.h)
# width = max(top_video.w, long_video.w)

# top_video_resized = top_video.resize(height=height//2).resize(width=width)
# long_video_resized = long_video.resize(height=height//2).resize(width=width)

# # Stack vertically
# final_video = clips_array([[top_video_resized], [long_video_resized]])

# # Output
# final_video.write_videofile("output_video.mp4", fps=24)


if __name__ == "__main__":
    audio_files = GetFiles("Audio")
    image_files = GetFiles("Images")
    long_video = GetFiles("LongVideo")
    music_files = GetFiles("Music")

    VerifyFiles(audio_files, image_files, long_video, music_files)

    top_half = CombineAudioImage(audio_files, image_files)

