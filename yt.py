import yt_dlp
import os
from pathlib import Path

def download_playlist(url, output_dir='downloads'):
    """
    Download audio from YouTube playlist videos in MP3 format
    
    Args:
        url (str): YouTube playlist URL
        output_dir (str): Directory to save downloaded audio files
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Configure yt-dlp options for mp3 extraction
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'ignoreerrors': True,  # Skip unavailable videos
        'extract_flat': True,  # Extract playlist info without downloading
        'quiet': False,
        'progress': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    try:
        # First get playlist info
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(url, download=False)
            if not playlist_info:
                print("Could not retrieve playlist information")
                return
            
            total_tracks = len(playlist_info['entries'])
            print(f"Found {total_tracks} tracks in playlist")
            
            # Now download each track
            for index, entry in enumerate(playlist_info['entries'], 1):
                if entry:
                    print(f"\nDownloading track {index}/{total_tracks}")
                    video_url = entry['url']
                    try:
                        ydl.download([video_url])
                    except Exception as e:
                        print(f"Error downloading track {index}: {str(e)}")
                        continue
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Get playlist URL from user
    playlist_url = input("Enter YouTube playlist URL: ")
    
    # Get output directory
    output_dir = input("Enter output directory [default: downloads]: ") or 'downloads'
    
    # Download the playlist
    print(f"\nDownloading playlist to {output_dir} in MP3 format...")
    download_playlist(playlist_url, output_dir)
    print("\nDownload complete!")

if __name__ == "__main__":
    main()