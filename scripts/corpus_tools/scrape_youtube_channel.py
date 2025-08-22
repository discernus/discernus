import yt_dlp
import json
import os

# Define the channel URL and output file path
CHANNEL_URL = "https://www.youtube.com/@RSBN/videos"
WORKSPACE_ROOT = "/Volumes/code/discernus"
OUTPUT_FILE = os.path.join(WORKSPACE_ROOT, "projects/2d_trump_populism/corpus/rsbn_video_urls.json")

def scrape_channel_videos(channel_url, output_file):
    """
    Scrapes all video URLs from a YouTube channel and saves them to a JSON file.
    """
    log_file = output_file.replace('.json', '.log')
    print(f"Scraping video URLs from: {channel_url}. Logging to {log_file}")

    with open(log_file, 'w') as log:
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
                    for video_entry in channel_info['entries']:
                        if not video_entry:
                            continue
                        
                        video_url = video_entry.get('url')
                        if not video_url:
                            continue

                        try:
                            # Fetch detailed info for each video individually
                            video_info = ydl.extract_info(video_url, download=False)
                            video_data.append({
                                'id': video_info.get('id'),
                                'title': video_info.get('title'),
                                'url': video_info.get('webpage_url'),
                                'upload_date': video_info.get('upload_date'),
                            })
                            print(f"Successfully processed: {video_info.get('title')}")
                        except yt_dlp.utils.DownloadError as e:
                            print(f"SKIPPING video {video_url}: {e}")
                            log.write(f"SKIPPED video {video_url}: {e}\n")
                            continue

        except Exception as e:
            print(f"An error occurred during the main scraping process: {e}")
            log.write(f"FATAL ERROR: {e}\n")
        finally:
            # Save whatever data was successfully collected
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(video_data, f, indent=4)

        print(f"Scraping complete. Found {len(video_data)} videos.")
        print(f"Video URLs saved to: {output_file}")

if __name__ == "__main__":
    scrape_channel_videos(CHANNEL_URL, OUTPUT_FILE)
