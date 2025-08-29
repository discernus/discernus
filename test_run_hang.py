#!/usr/bin/env python3
"""
Test to reproduce CLI run hanging issue.
"""

import subprocess
import time
import signal
import os

def test_run_command():
    """Test if the run command hangs after completion."""
    
    print("Testing CLI run command completion behavior...")
    
    # Use a simple test experiment that should complete quickly
    cmd = ["python3", "-m", "discernus", "run", "projects/simple_test_cff", "--analysis-only"]
    
    print(f"Running: {' '.join(cmd)}")
    print("This should complete quickly with --analysis-only flag...")
    
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
            stdout, stderr = process.communicate(timeout=120)  # 2 minutes timeout
            print(f"Process completed with return code: {process.returncode}")
            print(f"STDOUT length: {len(stdout)} characters")
            if stderr:
                print(f"STDERR length: {len(stderr)} characters")
                
            # Show last few lines of output
            lines = stdout.split('\n')
            if len(lines) > 10:
                print("Last 10 lines of output:")
                for line in lines[-10:]:
                    print(f"  {line}")
            else:
                print("Full output:")
                print(stdout)
                
        except subprocess.TimeoutExpired:
            print("❌ Process hung - killing after 2 minutes")
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
    success = test_run_command()
    if success:
        print("✅ CLI run test completed successfully")
    else:
        print("❌ CLI run test failed or hung")
