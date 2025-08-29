#!/usr/bin/env python3
"""
Simple test to check if CLI hangs after completion.
"""

import subprocess
import time
import signal
import os

def test_cli_completion():
    """Test if CLI properly returns control after completion."""
    
    print("Testing CLI completion behavior...")
    
    # Run a simple command that should complete quickly
    cmd = ["python3", "-m", "discernus", "list"]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        # Start the process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for completion with timeout
        try:
            stdout, stderr = process.communicate(timeout=30)
            print(f"Process completed with return code: {process.returncode}")
            print(f"STDOUT: {stdout}")
            if stderr:
                print(f"STDERR: {stderr}")
                
        except subprocess.TimeoutExpired:
            print("❌ Process hung - killing after 30 seconds")
            process.kill()
            stdout, stderr = process.communicate()
            print(f"STDOUT: {stdout}")
            if stderr:
                print(f"STDERR: {stderr}")
            return False
            
        return process.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

if __name__ == "__main__":
    success = test_cli_completion()
    if success:
        print("✅ CLI test completed successfully")
    else:
        print("❌ CLI test failed or hung")
