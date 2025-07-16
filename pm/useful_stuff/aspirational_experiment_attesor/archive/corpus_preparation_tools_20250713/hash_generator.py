#!/usr/bin/env python3
"""
Attesor Study Hash Generator
Generates secure, deterministic hashes for speaker content to eliminate identity bias.
"""

import hashlib
import os
import sys
from pathlib import Path

def load_hash_secret():
    """Load the hash secret from .env file"""
    env_path = Path(__file__).parent.parent.parent.parent / '.env'
    
    if not env_path.exists():
        raise FileNotFoundError("No .env file found. Please create one with ATTESOR_HASH_SECRET")
    
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('ATTESOR_HASH_SECRET='):
                secret = line.split('=', 1)[1].strip()
                if secret.startswith('"') and secret.endswith('"'):
                    secret = secret[1:-1]  # Remove quotes if present
                return secret
    
    raise ValueError("ATTESOR_HASH_SECRET not found in .env file")

def generate_hash(speaker_filename, secret):
    """
    Generate a secure, deterministic hash for a speaker filename.
    
    Args:
        speaker_filename: Original filename (e.g., "mitt_romney_2020_impeachment.txt")
        secret: Secret key from environment
    
    Returns:
        12-character hash string
    """
    # Combine filename with secret for security
    content = f"{speaker_filename}:{secret}"
    
    # Generate SHA-256 hash
    hash_obj = hashlib.sha256(content.encode('utf-8'))
    
    # Return first 12 characters for human manageable length
    return hash_obj.hexdigest()[:12]

def create_speaker_mapping():
    """Create the complete speaker mapping with secure hashes"""
    
    # Load secret
    secret = load_hash_secret()
    
    # Original speaker mapping (from sanitized file analysis)
    speakers = {
        'f9b8c2d7': {
            'speaker': 'Mitt Romney',
            'title': '2020 Impeachment Vote Speech',
            'source': 'mitt_romney_2020_impeachment.txt'
        },
        'a1c5e7d2': {
            'speaker': 'John McCain', 
            'title': '2008 Concession Speech',
            'source': 'john_mccain_2008_concession.txt'
        },
        'e2b9f5c1': {
            'speaker': 'JD Vance',
            'title': '2022 NatCon Conference Speech', 
            'source': 'jd_vance_2022_natcon_conference.txt'
        },
        'b3f7d2a6': {
            'speaker': 'Cory Booker',
            'title': '2018 First Step Act Speech',
            'source': 'cory_booker_2018_first_step_act.txt'
        },
        '7f9a2b8c': {
            'speaker': 'Alexandria Ocasio-Cortez',
            'title': '2025 Fighting Oligarchy Speech',
            'source': 'alexandria_ocasio_cortez_2025_fighting_oligarchy.txt'
        },
        'c6d4a3e8': {
            'speaker': 'John Lewis',
            'title': '1963 March on Washington Speech',
            'source': 'john_lewis_1963_march_on_washington.txt'
        },
        'd8a7b4f3': {
            'speaker': 'Steve King',
            'title': '2017 House Floor Speech',
            'source': 'steve_king_2017_house_floor.txt'
        },
        'a4c8e1d9': {
            'speaker': 'Bernie Sanders',
            'title': '2025 Fighting Oligarchy Speech',
            'source': 'bernie_sanders_2025_fighting_oligarchy.txt'
        }
    }
    
    # Generate secure hashes and create mapping
    mapping = {}
    for temp_hash, info in speakers.items():
        secure_hash = generate_hash(info['source'], secret)
        mapping[secure_hash] = {
            'temp_hash': temp_hash,  # For file operations
            'speaker': info['speaker'],
            'title': info['title'], 
            'source': info['source'],
            'processed': '2025-01-12T20:00:00Z'
        }
    
    return mapping

if __name__ == "__main__":
    try:
        mapping = create_speaker_mapping()
        
        print("Attesor Secure Hash Mapping Generated:")
        print("=" * 50)
        for secure_hash, info in mapping.items():
            print(f"Hash: {secure_hash}")
            print(f"  Speaker: {info['speaker']}")
            print(f"  Title: {info['title']}")
            print(f"  Source: {info['source']}")
            print(f"  Temp Hash: {info['temp_hash']}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 