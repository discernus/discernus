import json
import os
from collections import Counter

# Define the absolute path for the input file
WORKSPACE_ROOT = "/Volumes/code/discernus"
INPUT_FILE = os.path.join(WORKSPACE_ROOT, "projects/2d_trump_populism/corpus/magno_news_video_urls.json")

def analyze_video_dates(input_file):
    """
    Analyzes the distribution of videos per year from the scraped data.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at {input_file}")
        return

    with open(input_file, 'r') as f:
        videos = json.load(f)

    # Extract years from the upload_date field
    years = [video.get('upload_date', '')[:4] for video in videos if video.get('upload_date')]
    
    # Count the occurrences of each year
    year_counts = Counter(years)

    print("Video distribution by year:")
    for year, count in sorted(year_counts.items()):
        print(f"  {year}: {count} videos")

if __name__ == "__main__":
    analyze_video_dates(INPUT_FILE)
