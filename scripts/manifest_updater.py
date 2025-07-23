#!/usr/bin/env python3
"""
Manifest Updater - listens to Redis tasks.done stream and updates the manifest for a specified run
"""
import sys
import time
import json
import redis
from pathlib import Path
from scripts.discernus_cli import ArtifactManifestWriter

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
STREAM_NAME = 'tasks.done'
GROUP = None  # Not using consumer groups here


def main():
    if len(sys.argv) != 2:
        print("Usage: manifest_updater.py <run_id>")
        sys.exit(1)

    run_id = sys.argv[1]
    manifest = ArtifactManifestWriter(run_id)
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    last_id = '0-0'
    print(f"Listening for completed tasks to update manifest for run {run_id}...")
    try:
        while True:
            resp = r.xread({STREAM_NAME: last_id}, block=5000, count=10)
            if not resp:
                continue
            for stream, messages in resp:
                for msg_id, fields in messages:
                    data = json.loads(fields[b'data'])
                    result_hash = data.get('result_hash')
                    task_type = data.get('task_type', 'analysis')
                    parent_sha256 = data.get('chunk_hash') or data.get('framework_hash')

                    manifest.add_artifact(
                        sha256=result_hash,
                        uri=f"minio://discernus-artifacts/{result_hash}",
                        task_type=task_type,
                        parent_sha256=parent_sha256,
                        prompt_hash=data.get('prompt_hash')
                    )
                    print(f"Added artifact to manifest: {result_hash} ({task_type})")
                    last_id = msg_id.decode()
            # Optionally, generate markdown summary periodically
            manifest.generate_markdown_summary()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping manifest updater")
        sys.exit(0)


if __name__ == '__main__':
    main() 