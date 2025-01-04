
from yt_dlp import YoutubeDL

def configure_yt_dlp(output_path='downloads', 
                    format='bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    subtitle_languages=['en'],
                    write_thumbnail=True,
                    write_description=True):
    """
    Configure yt-dlp options for video downloads
    
    Args:
        output_path (str): Directory to save downloaded files
        format (str): Video format specification
        subtitle_languages (list): List of subtitle language codes
        write_thumbnail (bool): Whether to download video thumbnail
        write_description (bool): Whether to download video description
        
    Returns:
        YoutubeDL: Configured YoutubeDL instance
    """
    
    ydl_opts = {
        # Output options
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'paths': {'home': output_path},
        
        # Video format options
        'format': format,
        'merge_output_format': 'mp4',
        
        # Subtitle options
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': subtitle_languages,
        
        # Metadata options
        'writethumbnail': write_thumbnail,
        'writedescription': write_description,
        'writeinfojson': True,
        
        # Download options
        'continuedl': True,
        'retries': 3,
        'fragment_retries': 3,
        'skip_unavailable_fragments': True,
        
        # Post-processing
        'postprocessors': [
            {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
            {'key': 'FFmpegMetadata'},
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegEmbedSubtitle'},
        ],
        
        # Progress options
        'progress_hooks': [lambda d: print(f'Downloading: {d["filename"]} - {d["status"]}')],
        'verbose': True,
    }
    
    return YoutubeDL(ydl_opts)

# Example usage
def download_video(url, **kwargs):
    """
    Download a video using configured yt-dlp
    
    Args:
        url (str): Video URL to download
        **kwargs: Additional configuration options to pass to configure_yt_dlp
    """
    try:
        with configure_yt_dlp(**kwargs) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error downloading video: {str(e)}")

# Example calls
if __name__ == "__main__":
    # Basic usage
    download_video('https://www.youtube.com/watch?v=example')
    
    # Custom configuration
    download_video('https://www.youtube.com/watch?v=example',
                  output_path='custom_downloads',
                  format='bestvideo[height<=1080]+bestaudio/best',
                  subtitle_languages=['en', 'es'],
                  write_thumbnail=False)