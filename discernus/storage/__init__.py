"""
Discernus Storage Module
========================

Content-addressable artifact storage for research provenance.
"""

from .minio_client import DiscernusArtifactClient, get_artifact, put_artifact, ArtifactStorageError

__all__ = ['DiscernusArtifactClient', 'get_artifact', 'put_artifact', 'ArtifactStorageError'] 