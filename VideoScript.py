from moviepy.editor import *
import os

# Input
long_video = VideoFileClip("Long_video.mkv")
image_files = sorted(["image1.png", "image2.png", "image3.png"])  # Replace with glob or os.listdir
audio_files = sorted(["audio1.mp3", "audio2.mp3", "audio3.mp3"])


# # Process each (image, audio) pair into a short video
# top_clips = []
# for img_path, audio_path in zip(image_files, audio_files):
#     audio = AudioFileClip(audio_path)
#     duration = audio.duration

#     image_clip = ImageClip(img_path).set_duration(duration).set_audio(audio)
#     top_clips.append(image_clip)

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
