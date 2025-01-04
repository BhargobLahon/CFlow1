import yt_dlp
import os
from pathlib import Path

def download_videos(url, output_dir='downloads'):
    """
    Download video(s) from YouTube URL (supports both single videos and playlists)
    
    Args:
        url (str): YouTube URL (video or playlist)
        output_dir (str): Directory to save downloaded video files
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'ignoreerrors': True,
        'quiet': False,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegMetadata',
        }],
        # Show download progress
        'progress_hooks': [
            lambda d: print(
                f"\rDownloading: {d['filename']} - "
                f"{d.get('_percent_str', '').strip() if '_percent_str' in d else d['status']}", 
                end='\n' if d['status'] == 'finished' else ''
            )
        ],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video/playlist info
            print("Extracting video information...")
            result = ydl.extract_info(url, download=False)
            
            if not result:
                print("Could not retrieve video information")
                return
                
            # Handle both single videos and playlists
            if 'entries' in result:
                # This is a playlist
                videos = list(filter(None, result['entries']))
                total_videos = len(videos)
                print(f"\nFound {total_videos} videos in playlist: {result.get('title', 'Unknown Playlist')}")
                
                for index, entry in enumerate(videos, 1):
                    print(f"\nProcessing video {index}/{total_videos}")
                    print(f"Title: {entry.get('title', 'Unknown')}")
                    try:
                        video_url = entry.get('webpage_url') or entry.get('url')
                        if video_url:
                            ydl.download([video_url])
                        else:
                            print(f"Skipping video {index}: Could not get video URL")
                    except Exception as e:
                        print(f"Error downloading video {index}: {str(e)}")
                        continue
            else:
                # This is a single video
                print(f"\nDownloading single video: {result.get('title', 'Unknown')}")
                try:
                    ydl.download([url])
                except Exception as e:
                    print(f"Error downloading video: {str(e)}")
                
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("Make sure the URL is correct and the video/playlist is accessible.")

def main():
    # Get video/playlist URL
    url = input("Enter YouTube URL (video or playlist): ").strip()
    
    # Basic URL validation
    if not url.startswith(('http://', 'https://')):
        print("Please enter a valid URL starting with http:// or https://")
        return
    
    # Get output directory
    output_dir = input("Enter output directory [default: downloads]: ").strip() or 'downloads'
    
    # Download video(s)
    print(f"\nDownloading to {output_dir} in best available quality...")
    download_videos(url, output_dir)
    print("\nProcess complete!")

if __name__ == "__main__":
    main()