#!/usr/bin/env python3
"""
CI Status Checker for Discernus
Monitors GitHub Actions CI/CD pipeline status and provides local feedback.
"""

import sys
import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional


class CIStatusChecker:
    """Check and display CI status for the Discernus project"""
    
    def __init__(self, repo_owner: str = None, repo_name: str = None):
        # Try to detect repository from git remote
        if not repo_owner or not repo_name:
            try:
                import subprocess
                result = subprocess.run(["git", "remote", "get-url", "origin"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    remote_url = result.stdout.strip()
                    # Parse GitHub URLs
                    if "github.com" in remote_url:
                        # Handle both SSH and HTTPS formats
                        if remote_url.startswith("git@"):
                            # SSH format: git@github.com:owner/repo.git
                            parts = remote_url.split(":")[-1].replace(".git", "").split("/")
                        else:
                            # HTTPS format: https://github.com/owner/repo.git
                            parts = remote_url.split("/")[-2:]
                            parts[-1] = parts[-1].replace(".git", "")
                        
                        if len(parts) >= 2:
                            repo_owner = parts[0]
                            repo_name = parts[1]
            except Exception:
                pass
        
        self.repo_owner = repo_owner or "unknown"
        self.repo_name = repo_name or "unknown"
        self.api_base = "https://api.github.com"
        
    def get_latest_workflow_runs(self) -> Optional[Dict[str, Any]]:
        """Get the latest workflow runs from GitHub Actions"""
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/actions/runs"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Failed to fetch CI status: {e}")
            return None
    
    def format_duration(self, created_at: str, updated_at: str) -> str:
        """Calculate and format the duration of a workflow run"""
        try:
            start = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            end = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            duration = end - start
            
            total_seconds = int(duration.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            
            if minutes > 0:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"
        except Exception:
            return "Unknown"
    
    def get_status_emoji(self, status: str, conclusion: Optional[str]) -> str:
        """Get emoji representation of workflow status"""
        if status == "in_progress":
            return "🔄"
        elif status == "queued":
            return "⏳"
        elif conclusion == "success":
            return "✅"
        elif conclusion == "failure":
            return "❌"
        elif conclusion == "cancelled":
            return "⚠️"
        else:
            return "❓"
    
    def display_status(self) -> bool:
        """Display CI status and return True if all is well"""
        print("🔍 Checking Discernus CI/CD Status...")
        print("=" * 50)
        
        runs_data = self.get_latest_workflow_runs()
        if not runs_data:
            print("❌ Unable to fetch CI status")
            return False
        
        workflow_runs = runs_data.get("workflow_runs", [])
        if not workflow_runs:
            print("📭 No workflow runs found")
            return False
        
        # Show the latest 5 runs
        print(f"📊 Latest workflow runs:")
        print()
        
        all_good = True
        for i, run in enumerate(workflow_runs[:5]):
            status = run.get("status", "unknown")
            conclusion = run.get("conclusion")
            emoji = self.get_status_emoji(status, conclusion)
            
            branch = run.get("head_branch", "unknown")
            commit_sha = run.get("head_sha", "")[:7]
            commit_msg = run.get("display_title", "No message")
            
            # Truncate long commit messages
            if len(commit_msg) > 60:
                commit_msg = commit_msg[:57] + "..."
            
            created_at = run.get("created_at", "")
            updated_at = run.get("updated_at", "")
            duration = self.format_duration(created_at, updated_at)
            
            print(f"{emoji} {branch} ({commit_sha}) - {duration}")
            print(f"   {commit_msg}")
            
            if status == "completed" and conclusion != "success":
                all_good = False
                print(f"   🔗 {run.get('html_url', '')}")
            
            print()
        
        # Overall status
        latest_run = workflow_runs[0]
        latest_status = latest_run.get("status")
        latest_conclusion = latest_run.get("conclusion")
        
        print("=" * 50)
        if latest_status == "completed" and latest_conclusion == "success":
            print("🎉 Latest CI run: SUCCESS")
            print("✅ All systems operational")
        elif latest_status == "in_progress":
            print("🔄 Latest CI run: IN PROGRESS")
            print("⏳ Waiting for completion...")
        elif latest_status == "completed" and latest_conclusion == "failure":
            print("💥 Latest CI run: FAILED")
            print("❌ Action required")
            all_good = False
        else:
            print(f"❓ Latest CI run: {latest_status} ({latest_conclusion})")
            all_good = False
        
        return all_good
    
    def check_local_changes(self) -> bool:
        """Check if there are uncommitted local changes"""
        import subprocess
        
        try:
            # Check if we're in a git repository
            subprocess.run(["git", "status"], capture_output=True, check=True)
            
            # Check for uncommitted changes
            result = subprocess.run(["git", "status", "--porcelain"], 
                                  capture_output=True, text=True)
            
            if result.stdout.strip():
                print("⚠️  You have uncommitted changes:")
                print(result.stdout)
                return False
            else:
                print("✅ Working directory clean")
                return True
                
        except subprocess.CalledProcessError:
            print("ℹ️  Not in a git repository or git not available")
            return True
        except FileNotFoundError:
            print("ℹ️  Git not found")
            return True


def main():
    """Main function to check CI status"""
    checker = CIStatusChecker()
    
    # Check CI status
    ci_good = checker.display_status()
    
    print()
    
    # Check local changes
    local_clean = checker.check_local_changes()
    
    print()
    print("=" * 50)
    
    if ci_good and local_clean:
        print("🚀 Ready to ship! CI passing and working directory clean.")
        sys.exit(0)
    elif ci_good:
        print("✅ CI is passing, but you have uncommitted changes.")
        sys.exit(0)
    else:
        print("⚠️  CI issues detected. Please review before deploying.")
        sys.exit(1)


if __name__ == "__main__":
    main() 