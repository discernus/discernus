#!/usr/bin/env python3
"""
Discernus PoC MinIO Client - Artifact Storage
Simple client for content-addressable storage using SHA256 hashing.
"""

import hashlib
import os
import tempfile
from io import BytesIO
from typing import Optional
from minio import Minio
from minio.error import S3Error
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Default MinIO configuration
DEFAULT_ENDPOINT = 'localhost:9000'
DEFAULT_ACCESS_KEY = os.getenv('MINIO_ROOT_USER', 'minio')
DEFAULT_SECRET_KEY = os.getenv('MINIO_ROOT_PASSWORD', 'minio123')
BUCKET_NAME = 'discernus-artifacts'

class ArtifactStorageError(Exception):
    """Artifact storage specific exceptions"""
    pass

class DiscernusArtifactClient:
    """Content-addressable artifact storage using MinIO/S3"""
    
    def __init__(self, 
                 endpoint: str = DEFAULT_ENDPOINT,
                 access_key: str = DEFAULT_ACCESS_KEY,
                 secret_key: str = DEFAULT_SECRET_KEY,
                 secure: bool = False):
        
        try:
            self.client = Minio(
                endpoint=endpoint,
                access_key=access_key,
                secret_key=secret_key,
                secure=secure
            )
            self.bucket = BUCKET_NAME
            self._ensure_bucket_exists()
            logger.info(f"Connected to artifact store at {endpoint}")
            
        except Exception as e:
            logger.error(f"Failed to connect to MinIO: {e}")
            raise ArtifactStorageError(f"MinIO connection failed: {e}")
    
    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
                logger.info(f"Created bucket: {self.bucket}")
            else:
                logger.debug(f"Bucket exists: {self.bucket}")
        except Exception as e:
            logger.error(f"Bucket creation failed: {e}")
            raise ArtifactStorageError(f"Bucket setup failed: {e}")
    
    def put_artifact(self, content: str) -> str:
        """
        Store content and return SHA256 hash.
        Implements content-addressable storage - same content = same hash.
        """
        try:
            # Convert to bytes
            content_bytes = content.encode('utf-8')
            
            # Calculate SHA256 hash
            hash_id = hashlib.sha256(content_bytes).hexdigest()
            
            # Check if already exists (cache hit)
            if self.artifact_exists(hash_id):
                logger.debug(f"Cache hit for hash: {hash_id}")
                return hash_id
            
            # Store new artifact
            self.client.put_object(
                bucket_name=self.bucket,
                object_name=hash_id,
                data=BytesIO(content_bytes),
                length=len(content_bytes),
                content_type='text/plain'
            )
            
            logger.info(f"Stored artifact: {hash_id} ({len(content_bytes)} bytes)")
            return hash_id
            
        except Exception as e:
            logger.error(f"Failed to store artifact: {e}")
            raise ArtifactStorageError(f"Artifact storage failed: {e}")
    
    def get_artifact(self, hash_id: str) -> str:
        """Retrieve content by SHA256 hash"""
        try:
            response = self.client.get_object(self.bucket, hash_id)
            content = response.read().decode('utf-8')
            response.close()
            response.release_conn()
            
            logger.debug(f"Retrieved artifact: {hash_id} ({len(content)} chars)")
            return content
            
        except S3Error as e:
            if e.code == 'NoSuchKey':
                logger.error(f"Artifact not found: {hash_id}")
                raise ArtifactStorageError(f"Artifact not found: {hash_id}")
            else:
                logger.error(f"S3 error retrieving artifact: {e}")
                raise ArtifactStorageError(f"Retrieval failed: {e}")
        except Exception as e:
            logger.error(f"Failed to retrieve artifact: {e}")
            raise ArtifactStorageError(f"Artifact retrieval failed: {e}")
    
    def artifact_exists(self, hash_id: str) -> bool:
        """Check if artifact exists without downloading it"""
        try:
            self.client.stat_object(self.bucket, hash_id)
            return True
        except S3Error as e:
            if e.code == 'NoSuchKey':
                return False
            else:
                logger.error(f"Error checking artifact existence: {e}")
                raise ArtifactStorageError(f"Existence check failed: {e}")
        except Exception as e:
            logger.error(f"Failed to check artifact existence: {e}")
            raise ArtifactStorageError(f"Existence check failed: {e}")
    
    def put_file(self, file_path: str) -> str:
        """Store file contents and return SHA256 hash"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.put_artifact(content)
        except Exception as e:
            logger.error(f"Failed to store file {file_path}: {e}")
            raise ArtifactStorageError(f"File storage failed: {e}")
    
    def get_to_file(self, hash_id: str, destination_path: str) -> None:
        """Retrieve artifact and save to file"""
        try:
            content = self.get_artifact(hash_id)
            with open(destination_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Saved artifact {hash_id} to {destination_path}")
        except Exception as e:
            logger.error(f"Failed to save artifact to file: {e}")
            raise ArtifactStorageError(f"File save failed: {e}")
    
    def list_artifacts(self, prefix: str = '') -> list:
        """List stored artifacts with optional prefix filter"""
        try:
            objects = self.client.list_objects(self.bucket, prefix=prefix)
            artifacts = []
            
            for obj in objects:
                artifacts.append({
                    'hash_id': obj.object_name,
                    'size': obj.size,
                    'last_modified': obj.last_modified
                })
            
            logger.debug(f"Found {len(artifacts)} artifacts")
            return artifacts
            
        except Exception as e:
            logger.error(f"Failed to list artifacts: {e}")
            raise ArtifactStorageError(f"Artifact listing failed: {e}")
    
    def delete_artifact(self, hash_id: str) -> bool:
        """Delete artifact (use carefully - breaks immutability!)"""
        try:
            self.client.remove_object(self.bucket, hash_id)
            logger.warning(f"Deleted artifact: {hash_id}")
            return True
        except S3Error as e:
            if e.code == 'NoSuchKey':
                logger.warning(f"Artifact already deleted: {hash_id}")
                return False
            else:
                logger.error(f"Failed to delete artifact: {e}")
                raise ArtifactStorageError(f"Deletion failed: {e}")
        except Exception as e:
            logger.error(f"Failed to delete artifact: {e}")
            raise ArtifactStorageError(f"Deletion failed: {e}")

# Convenience functions for backward compatibility
_default_client = None

def get_default_client() -> DiscernusArtifactClient:
    """Get default artifact client (singleton)"""
    global _default_client
    if _default_client is None:
        _default_client = DiscernusArtifactClient()
    return _default_client

def put_artifact(content: str) -> str:
    """Store content using default client"""
    return get_default_client().put_artifact(content)

def get_artifact(hash_id: str) -> str:
    """Retrieve content using default client"""
    return get_default_client().get_artifact(hash_id)

def artifact_exists(hash_id: str) -> bool:
    """Check existence using default client"""
    return get_default_client().artifact_exists(hash_id)

def main():
    """CLI entry point for testing"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: minio_client.py [put|get|exists|list] [args...]")
        sys.exit(1)
    
    command = sys.argv[1]
    client = get_default_client()
    
    try:
        if command == 'put' and len(sys.argv) >= 3:
            file_path = sys.argv[2]
            hash_id = client.put_file(file_path)
            print(f"Stored ➜ sha256:{hash_id}")
            
        elif command == 'get' and len(sys.argv) >= 4:
            hash_id = sys.argv[2]
            dest_path = sys.argv[3]
            client.get_to_file(hash_id, dest_path)
            print(f"Retrieved {hash_id} ➜ {dest_path}")
            
        elif command == 'exists' and len(sys.argv) >= 3:
            hash_id = sys.argv[2]
            exists = client.artifact_exists(hash_id)
            print(f"Artifact {hash_id}: {'EXISTS' if exists else 'NOT FOUND'}")
            
        elif command == 'list':
            artifacts = client.list_artifacts()
            print(f"Found {len(artifacts)} artifacts:")
            for artifact in artifacts:
                print(f"  {artifact['hash_id']} ({artifact['size']} bytes)")
                
        else:
            print("Invalid command or missing arguments")
            sys.exit(1)
            
    except ArtifactStorageError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 