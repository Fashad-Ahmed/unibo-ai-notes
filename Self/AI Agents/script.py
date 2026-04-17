from moviepy import VideoFileClip, AudioFileClip
import random

AUDIO_PATH = "/Users/fashad/fashad/projects/unibo-ai-notes/Self/AI Agents/story_audio.mp3"
BACKGROUND_VIDEO_PATH = "/Users/fashad/fashad/projects/unibo-ai-notes/Self/AI Agents/background_footage.mp4"
OUTPUT_PATH = "/Users/fashad/fashad/projects/unibo-ai-notes/Self/AI Agents/ready_to_caption.mp4"

def assemble_video():
    print("Loading media files...")
    # Load the generated TTS audio
    audio_clip = AudioFileClip(AUDIO_PATH)
    audio_duration = audio_clip.duration

    video_clip = VideoFileClip(BACKGROUND_VIDEO_PATH)

    max_start_time = video_clip.duration - audio_duration
    start_time = random.uniform(0, max_start_time)
    end_time = start_time + audio_duration

    print(f"Slicing video from {start_time:.2f}s to {end_time:.2f}s...")
    
    sliced_video = video_clip.subclipped(start_time, end_time).without_audio()

    final_video = sliced_video.with_audio(audio_clip)

    print("Exporting final MP4... this might take a minute.")
    final_video.write_videofile(
        OUTPUT_PATH, 
        fps=30, 
        codec="libx264", 
        audio_codec="aac",
        preset="ultrafast" # Speeds up the rendering process
    )
    
    audio_clip.close()
    video_clip.close()
    
    print(f"Done! Saved as {OUTPUT_PATH}")

if __name__ == "__main__":
    assemble_video()