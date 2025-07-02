import os
from Components.YoutubeDownloader import download_youtube_video
from Components.Edit import extractAudio, crop_video
from Components.Transcription import transcribeAudio
from Components.LanguageTasks import GetHighlight
from Components.FaceCrop import crop_to_vertical, combine_videos

video_source = input("Enter 'Y' for YouTube URL or 'L' for Local file: ").lower()
video_path_to_process = None

if video_source == 'y':
    url = input("Enter YouTube video URL: ")
    Vid = download_youtube_video(url)
    if Vid:
        video_path_to_process = Vid.replace(".webm", ".mp4") 
        print(f"Downloaded video and audio files successfully! at {video_path_to_process}")
    else:
        print("Unable to Download the video")

elif video_source == 'l':
    local_path = input("Enter the full path to your local video file: ")
    if os.path.exists(local_path):
        video_path_to_process = local_path
        print(f"Using local video file: {local_path}")
    else:
        print(f"Error: Local video file not found at '{local_path}'.")
else:
    print("Invalid choice. Exiting.")

if video_path_to_process:
    # Use video_path_to_process for all subsequent operations
    Audio = extractAudio(video_path_to_process)
    if Audio:
        transcriptions = transcribeAudio(Audio)
        if len(transcriptions) > 0:
            TransText = ""

            for text, start, end in transcriptions:
                TransText += (f"{start} - {end}: {text}")

            start , stop = GetHighlight(TransText)
            if start != 0 and stop != 0:
                print(f"Start: {start} , End: {stop}")

                Output = "Out.mp4" 
                crop_video(video_path_to_process, Output, start, stop) # Use video_path_to_process here
                
                croped = "croped.mp4"
                crop_to_vertical("Out.mp4", croped)

                combine_videos("Out.mp4", croped, "Final.mp4") 
                
                # Minimal cleanup: remove intermediate files
                if os.path.exists(Output):
                    os.remove(Output)
                if os.path.exists(croped):
                    os.remove(croped)

            else:
                print("Error in getting highlight")
        else:
            print("No transcriptions found")
    else:
        print("No audio file found")
else:
    pass

