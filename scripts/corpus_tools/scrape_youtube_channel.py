import yt_dlp
import json
import os

# Define the channel URL and output file path
CHANNEL_URL = "https://www.youtube.com/@MAGNONEWS/videos"
WORKSPACE_ROOT = "/Volumes/code/discernus"
OUTPUT_FILE = os.path.join(WORKSPACE_ROOT, "projects/2d_trump_populism/corpus/magno_news_video_urls.json")

def scrape_channel_videos(channel_url, output_file):
    """
    Scrapes all video URLs from a YouTube channel and saves them to a JSON file.
    """
    print(f"Scraping video URLs from: {channel_url}")

    # Configure yt-dlp options to extract information without downloading
    ydl_opts = {
        'quiet': True,
        'force_generic_extractor': True,
        'get_upload_date': True,
    }

    video_data = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract channel information
            channel_info = ydl.extract_info(channel_url, download=False)
            
            if 'entries' in channel_info:
                for video in channel_info['entries']:
                    if video:
                        video_data.append({
                            'id': video.get('id'),
                            'title': video.get('title'),
                            'url': video.get('url'),
                            'upload_date': video.get('upload_date'),
                        })
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return

    # Save the data to a JSON file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(video_data, f, indent=4)

    print(f"Scraping complete. Found {len(video_data)} videos.")
    print(f"Video URLs saved to: {output_file}")

if __name__ == "__main__":
    scrape_channel_videos(CHANNEL_URL, OUTPUT_FILE)
