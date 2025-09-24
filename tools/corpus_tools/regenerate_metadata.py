import os
import json
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define absolute paths
WORKSPACE_ROOT = "/Volumes/code/discernus"
CORPUS_DIR = os.path.join(WORKSPACE_ROOT, "projects/2d_trump_populism/corpus/2024_campaign/primary_campaign")
EXTRACTOR_SCRIPT = os.path.join(WORKSPACE_ROOT, "scripts/corpus_tools/enhanced_transcript_extractor.py")
LOG_FILE = os.path.join(WORKSPACE_ROOT, "projects/2d_trump_populism/corpus/2024_campaign/metadata_regeneration.log")

def get_url_from_transcript(filepath):
    """Reads the YouTube URL from the header of a transcript file."""
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith("# Video URL:"):
                return line.split(":", 1)[1].strip()
    return None

def regenerate_metadata():
    """
    Iterates through transcripts, extracts their URLs, and regenerates their metadata.
    """
    if not os.path.exists(CORPUS_DIR):
        logging.error(f"Corpus directory not found: {CORPUS_DIR}")
        return
        
    logging.info(f"Starting metadata regeneration for directory: {CORPUS_DIR}")
    
    with open(LOG_FILE, 'w') as log:
        for filename in os.listdir(CORPUS_DIR):
            if not filename.endswith(".txt"):
                continue

            transcript_path = os.path.join(CORPUS_DIR, filename)
            metadata_path = os.path.join(CORPUS_DIR, f"{Path(filename).stem}_metadata.json")
            
            youtube_url = get_url_from_transcript(transcript_path)

            if not youtube_url:
                logging.warning(f"SKIPPING: Could not find URL in {filename}")
                log.write(f"SKIPPED (no URL): {filename}\n")
                continue

            # We can re-run the extractor with --no-transcript option if it existed,
            # but for simplicity, we'll just let it re-extract.
            # A more optimized approach would be to just call a metadata generation function.
            # For now, this ensures consistency with the extractor's output.
            
            logging.info(f"REGENERATING: Metadata for {filename} from URL {youtube_url}")
            
            # Since the extractor saves based on a generated name, we will output to a temp dir
            # and then move the correct metadata file.
            # This is a workaround because the extractor controls its own output naming.
            # A better long-term solution would be to refactor the extractor.
            
            # For this pass, we will just re-run and overwrite.
            # We already have the transcripts, but this will regenerate the JSON.
            
            command = [
                "python3",
                EXTRACTOR_SCRIPT,
                youtube_url,
                "--output-dir",
                CORPUS_DIR,
                "--whisper-model", "base" # Model choice doesn't matter much as we prefer youtube_api
            ]

            try:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                logging.info(f"SUCCESS: Regenerated metadata for {filename}")
                log.write(f"SUCCESS: {filename}\n")
                log.write(result.stdout + "\n")
            except subprocess.CalledProcessError as e:
                logging.error(f"FAILED: Metadata regeneration for {filename}. Error: {e.stderr}")
                log.write(f"FAILED: {filename}\n")
                log.write(f"  URL: {youtube_url}\n")
                log.write(f"  ERROR: {e.stderr}\n")

    logging.info("Metadata regeneration complete.")

if __name__ == "__main__":
    regenerate_metadata()
