import sys
import os
import shutil
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import static_ffmpeg

static_ffmpeg.add_paths()

def mashup_logic(singer, n_videos, duration, output_filename):
    # 1. Setup Directories
    temp_dir = "temp_downloads"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    print(f"--- Started: Downloading {n_videos} videos of '{singer}' ---")
    print("(Filtering out videos longer than 15 minutes...)")

    # CUSTOM FILTER FUNCTION
    def check_duration(info, *, incomplete=False):
        video_duration = info.get('duration')
        # 15 minutes = 900 seconds
        if video_duration and video_duration > 900:
            return "Video too long (>15 mins), skipping."
        return None

    # 2. Configure yt-dlp with Anti-Block settings
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{temp_dir}/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True,
        
        # ADDED: Filter to reject long videos
        'match_filter': check_duration,

        # FIX FOR 403 FORBIDDEN ERROR:
        'ignoreerrors': True,   
        'nocheckcertificate': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios'] 
            }
        }
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # We search for more videos (N + 5) because of the filter
            search_query = f"ytsearch{n_videos + 5}:{singer}"
            ydl.download([search_query])
    except Exception as e:
        print(f"Error downloading content: {e}")
        shutil.rmtree(temp_dir)
        sys.exit(1)

    print("\n--- Downloading complete. Processing Audio... ---")


    # 3. Audio Processing
    combined_audio = AudioSegment.empty()

    downloaded_files = [f for f in os.listdir(temp_dir) if f.endswith(".mp3")] # Get all mp3 files from the temp_downloads folder

    if not downloaded_files:    # Check if we actually got files
        print("Error: No audio files were successfully downloaded.")
        shutil.rmtree(temp_dir)
        sys.exit(1)

    downloaded_files.sort() # Sort files to ensure consistent order

    files_to_process = downloaded_files[:n_videos] # Limit to the requested number of videos
    
    print(f"Processing {len(files_to_process)} files...")

    for file_name in files_to_process:
        file_path = os.path.join(temp_dir, file_name)
        try:
            audio = AudioSegment.from_mp3(file_path)
            start_time = 21 * 1000 # Start extraction at 21st second (21000 ms)
            end_time = start_time + (duration * 1000) # End extraction at start + user duration 
            cut_audio = audio[start_time:end_time]
            combined_audio += cut_audio
        except Exception as e:
            print(f"Skipping corrupt file {file_name}: {e}")


    # 4. Export
    print(f"--- Merging and saving to {output_filename} ---")
    try:
        combined_audio.export(output_filename, format="mp3")
        print(f"Successful! Output file created: {output_filename}")
    except Exception as e:
        print(f"Error saving file: {e}")


def main():
    # 1. Validation: Correct number of parameters
    if len(sys.argv) != 5:
        print("ERROR: Incorrect number of parameters.")
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    # 2. Input Parsing
    singer_name = sys.argv[1]
    output_file = sys.argv[4]

    try:
        num_videos = int(sys.argv[2])
        audio_duration = int(sys.argv[3])
    except ValueError:
        print("ERROR: <NumberOfVideos> and <AudioDuration> must be integers.")
        sys.exit(1)

    # 3. Validation Rules
    if num_videos <= 10:
        print("ERROR: <NumberOfVideos> must be greater than 10.")
        sys.exit(1)
    
    if audio_duration <= 20:
        print("ERROR: <AudioDuration> must be greater than 20 seconds.")
        sys.exit(1)

    # Ensure output has .mp3 extension
    if not output_file.lower().endswith(".mp3"):
        output_file += ".mp3"

    # 4. Execution
    mashup_logic(singer_name, num_videos, audio_duration, output_file)

if __name__ == "__main__":
    main()