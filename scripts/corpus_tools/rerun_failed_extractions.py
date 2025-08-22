import json
import os
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define absolute paths for key files and directories
WORKSPACE_ROOT = "/Volumes/code/discernus"
METADATA_FILE = os.path.join(WORKSPACE_ROOT, "projects/2d_trump_populism/corpus/2024_campaign/2024_campaign_metadata.json")
EXTRACTOR_SCRIPT = os.path.join(WORKSPACE_ROOT, "scripts/corpus_tools/enhanced_transcript_extractor.py")
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "projects/2d_trump_populism/corpus/2024_campaign/primary_campaign")
LOG_FILE = os.path.join(WORKSPACE_ROOT, "projects/2d_trump_populism/corpus/2024_campaign/rerun_extraction_log.txt")

def file_is_valid(filepath):
    """Check if a file exists and is not empty."""
    return os.path.exists(filepath) and os.path.getsize(filepath) > 0

def run_extraction():
    """
    Reads metadata, checks for existing transcripts, and runs extraction for missing ones.
    """
    if not os.path.exists(METADATA_FILE):
        logging.error(f"Metadata file not found: {METADATA_FILE}")
        return

    if not os.path.exists(EXTRACTOR_SCRIPT):
        logging.error(f"Extractor script not found: {EXTRACTOR_SCRIPT}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(METADATA_FILE, 'r') as f:
        metadata_entries = json.load(f)

    logging.info(f"Loaded {len(metadata_entries)} metadata entries. Starting extraction process...")

    with open(LOG_FILE, 'w') as log:
        for entry in metadata_entries:
            doc_id = entry.get("document_id")
            youtube_url = entry.get("youtube_url")
            target_filepath = os.path.join(OUTPUT_DIR, doc_id)

            if not doc_id or not youtube_url:
                logging.warning(f"Skipping entry with missing document_id or youtube_url: {entry}")
                log.write(f"SKIPPED (missing data): {entry}\n")
                continue

            if file_is_valid(target_filepath):
                logging.info(f"SUCCESS (exists): Transcript already exists for {doc_id}")
                log.write(f"SUCCESS (exists): {doc_id}\n")
                continue

            logging.info(f"ATTEMPTING: Extracting transcript for {doc_id} from {youtube_url}")
            
            command = [
                "python3",
                EXTRACTOR_SCRIPT,
                youtube_url,
                "--output-dir",
                OUTPUT_DIR,
                "--whisper-model",
                "base"
            ]
            
            try:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                logging.info(f"SUCCESS (extracted): {doc_id}")
                log.write(f"SUCCESS (extracted): {doc_id}\n")
                log.write(result.stdout + "\n")
            except subprocess.CalledProcessError as e:
                logging.error(f"FAILED: Extraction for {doc_id}. Error: {e.stderr}")
                log.write(f"FAILED: {doc_id}\n")
                log.write(f"  URL: {youtube_url}\n")
                log.write(f"  ERROR: {e.stderr}\n")

    logging.info("Extraction process complete.")

if __name__ == "__main__":
    run_extraction()
