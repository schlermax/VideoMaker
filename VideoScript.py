from moviepy.editor import *
import os
import random

PAUSE_BETWEEN_AUDIO = 0.3

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

# Validate Input
def ValidateFiles(audio, images, long, music):
    """Verifies if the input files will be sufficient for a video.
    Must pass the following Contraints:
        - None of the folders are empty
        - LongVideo folder contains one video
        - Amount of image files equals the amount of audio files
        - Long video duration is greater than or equal to cumulative audio duration
        - Check with user

    Args:
        audio (List[str]): strings representing file names for each audio
        images (List[str]): ... image
        music (List[str]): ... music
        long (List[str]): the long video
    """
    print("Validating inputs...")
    
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
    prefix = audio[0][6]
    for audio_clip in audio:
        if audio_clip[6] != prefix:
            prefix = audio_clip[6]
            cumulative_audio_duration += PAUSE_BETWEEN_AUDIO
        audio_clip = AudioFileClip(audio_clip)
        cumulative_audio_duration += audio_clip.duration + PAUSE_BETWEEN_AUDIO
    if long.duration < cumulative_audio_duration:
        print("ABORT: Long video duration is shorter than the audio duration")
        quit()

    user_input = input("$$$$$ Video duration expected to be [" + GetVerboseDuration(cumulative_audio_duration) + "] while long video duration is [" + GetVerboseDuration(long.duration) + "]\n$$$$$ Enter 'y' to proceed: ")
    if user_input != 'y':
        print("ABORT: User did not select 'y'.")
        quit()
    
    print("Input Validated.")
def GetVerboseDuration(duration):
    """Takes in a float duration of some amount of seconds 
    and returns the minutes and seconds verbosely

    Args:
        duration (float): seconds of the input

    Returns:
        String: Verbose time
    """
    minutes = int(duration/60.0)
    seconds = duration - (minutes*60)
    verbose_time = f"{minutes} minutes {seconds:.2f} seconds"
    return verbose_time

# Construct video
def ResizeInFit(clip, target_w, target_h):
    """Resize clip to fit target size while preserving aspect ratio.

    Args:
        clip (Generic video/image clip): The clip to resize
        target_w (int): desired pixel width
        target_h (int): desired pixel height

    Returns:
        clip: The same data type as the input clip except now scaled to fit within the width and height parameters.
    """
    img_w, img_h = clip.w, clip.h
    scale_w = target_w / img_w
    scale_h = target_h / img_h
    scale = min(scale_w, scale_h)  # Fit inside box
    return clip.resize(scale)
def CombineAudioImage(audio, images):
    """Takes each pair of audio and their respective image (Alphabetical order)
    and combines them into a short video. Then combines all of those short videos into one.

    Args:
        audio (List[str]): of string paths to audio
        images (List[str]): ... images
    
    Returns:
        VideoFileClip; the top half of the video
    """
    print("Creating top half video... ", end='')
    short_videos = []
    prefix = audio[0][6]

    for audio_path, image_path in zip(audio, images):
        # Longer delay between distinct sections; denoted by beginning letter of the clip
        if audio_path[6] != prefix:
            prefix = audio_path[6]
            short_videos[-1].set_duration(duration + (2*PAUSE_BETWEEN_AUDIO))
            
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration + PAUSE_BETWEEN_AUDIO

        image_clip = ImageClip(image_path).set_duration(duration)#.set_audio(audio_clip)

        # Resize image to fit target size
        image_clip = ResizeInFit(image_clip, 581, 412)
        image_clip = image_clip.set_audio(audio_clip)

        short_videos.append(image_clip)

    top_video = concatenate_videoclips(short_videos, method="compose")
    print("Complete!")
    return top_video

def CombineTopBottom(top_video, bottom_video):
    """Combines input videos with one on top and one on bottom.

    Args:
        top_video (VideoFileClip): Video on the top (image+audio video)
        bottom_video (VideoFileClip): Video on bottom (Longplay)

    Returns:
        VideoFileClip: Combined video in a top-bottom format
    """
    print("Combining the top and bottom videos and framing... ", end='')
    # Crop 30% off each side and the bottom of the bottom video (center crop)
    bottom_width = bottom_video.w
    bottom_height = bottom_video.h
    side_crop_margin = int(bottom_width * 0.3)
    bottom_crop_margin = int(bottom_height * 0.265)
    bottom_video = bottom_video.crop(x1=side_crop_margin, x2=bottom_width - side_crop_margin)
    bottom_video = bottom_video.crop(y1=0, y2=bottom_height - bottom_crop_margin)

    # Resize the bottom video
    bottom_video = ResizeInFit(bottom_video, 581, 630)

    # Stack vertically
    stacked_video = clips_array([[top_video], [bottom_video]])

    # Frame it
    frame = ImageClip("FRAME.png").set_duration(stacked_video.duration)
    frame = frame.crop(x1=side_crop_margin, x2=bottom_width - side_crop_margin)
    frame = frame.resize(newsize=(591,1080))
    
    stacked_centered = stacked_video.set_position(("center", "center"))
    final = CompositeVideoClip([frame, stacked_centered])

    print("Complete!")
    return final

def AddBackground(stacked, background):
    """Combines the stacked video with the background

    Args:
        stacked (VideoFileClip): The top-bottom video
        background (VideoFileClip): The long video again

    Returns:
        VideoFileClip: The video with a background now
    """
    print("Adding Background... ", end='')
    
    background = background.resize(3)

    background = background.crop(width=1920, height=1080, x_center=background.w//2, y_center=background.h//2.75)

    video_with_background = CompositeVideoClip([background, stacked.set_position(("center", 0))])
    
    print("Complete!")
    return video_with_background

def AddBackgroundMusic(video, music_paths, volume=0.11):
    """
    Adds quiet background music to a video from a list of music files.

    Args:
        video (VideoFileClip): The video to add music to
        music_paths (List[str]): List of paths to mp3 files
        volume (float): Volume of background music (0.0 to 1.0)

    Returns:
        VideoFileClip with background music added.
    """
    print("Adding background music... ",end='')
    duration_needed = video.duration
    music_clips = []
    
    # Start at a random point in the list
    start_index = random.randint(0, len(music_paths) - 1)
    index = start_index

    total_duration = 0
    while total_duration < duration_needed:
        clip_path = music_paths[index % len(music_paths)]
        music_clip = AudioFileClip(clip_path).volumex(volume)

        music_clips.append(music_clip)
        total_duration += music_clip.duration

        index += 1

    # Concatenate and cut to the exact video duration
    full_music = concatenate_audioclips(music_clips).subclip(0, duration_needed)

    # Mix background music with existing video audio
    final_audio = CompositeAudioClip([video.audio, full_music])
    video_with_music = video.set_audio(final_audio)

    print("Complete!")
    return video_with_music



if __name__ == "__main__":
    # Prepare for creating the video
    audio_files = GetFiles("Audio")
    image_files = GetFiles("Images")
    long_video = GetFiles("LongVideo")
    music_files = GetFiles("Music")

    ValidateFiles(audio_files, image_files, long_video, music_files)

    # Construct the video
    long_video = VideoFileClip(long_video[0])
    
    top_half = CombineAudioImage(audio_files, image_files)

    long_video = long_video.subclip(0, top_half.duration)

    stacked_video = CombineTopBottom(top_half, long_video)

    full_video = AddBackground(stacked_video, long_video)

    final_draft = AddBackgroundMusic(full_video, music_files)

    final_draft.write_videofile("output_video.mp4", fps=30, bitrate="5000k", preset="fast")

