import json
import os
import re

# Define the absolute path for the input and output files
WORKSPACE_ROOT = "/Volumes/code/discernus"
INPUT_FILE = os.path.join(WORKSPACE_ROOT, "projects/2d_trump_populism/corpus/magno_news_video_urls.json")
OUTPUT_FILE = os.path.join(WORKSPACE_ROOT, "projects/2d_trump_populism/corpus/filtered_video_urls_2021-2023.json")

# Define filtering criteria
KEYWORDS = ['trump', 'rally', 'speech']
YEARS = ['2021', '2022', '2023']

def filter_videos(input_file, output_file, keywords, years):
    """
    Filters a list of YouTube video data based on keywords and years in the title.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at {input_file}")
        return

    with open(input_file, 'r') as f:
        videos = json.load(f)

    print(f"Filtering {len(videos)} videos...")

    filtered_videos = []
    for video in videos:
        title = video.get('title', '').lower()
        upload_date = video.get('upload_date', '') # YYYYMMDD format

        # Check if any of the keywords are in the title
        has_keyword = any(keyword in title for keyword in keywords)
        
        # Check if the upload year is in the target years
        has_year = False
        if upload_date and len(upload_date) == 8:
            year = upload_date[:4]
            if year in years:
                has_year = True

        if has_keyword and has_year:
            filtered_videos.append(video)

    # Save the filtered list to a new JSON file
    with open(output_file, 'w') as f:
        json.dump(filtered_videos, f, indent=4)

    print(f"Filtering complete. Found {len(filtered_videos)} relevant videos.")
    print(f"Filtered list saved to: {output_file}")

if __name__ == "__main__":
    filter_videos(INPUT_FILE, OUTPUT_FILE, KEYWORDS, YEARS)
