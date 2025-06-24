#!/usr/bin/env python3
"""
Automated License Monitoring for Discernus Project
Scheduled compliance monitoring with alerting and reporting

Usage:
    python3 automated_monitoring.py [--config config.json]
    
Features:
    - Scheduled compliance checks
    - Baseline comparison
    - Violation alerting
    - Automated reporting
    - CI/CD integration
"""

import argparse
import json
import sys
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart


class LicenseMonitor:
    """Automated license compliance monitoring system."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize monitor with configuration."""
        self.config = self._load_config(config_file)
        self.audit_dir = Path("monitoring_audits")
        self.audit_dir.mkdir(exist_ok=True)
        
    def _load_config(self, config_file: Optional[str]) -> Dict:
        """Load monitoring configuration."""
        default_config = {
            "policy_file": "saas_commercial_policy.json",
            "baseline_file": "baseline_audit.json",
            "monitoring_enabled": True,
            "check_frequency": "daily",
            "alert_on_violations": True,
            "alert_on_new_packages": True,
            "alert_on_license_changes": True,
            "ci_mode": False,
            "notifications": {
                "email_enabled": False,
                "slack_enabled": False,
                "github_issues_enabled": False
            },
            "retention_days": 90,
            "compliance_thresholds": {
                "max_unknown_packages": 0,
                "max_prohibited_packages": 0,
                "max_new_packages_per_day": 5
            }
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}", file=sys.stderr)
        
        return default_config
    
    def run_compliance_check(self) -> Dict:
        """Run comprehensive compliance check."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audit_file = self.audit_dir / f"automated_audit_{timestamp}.json"
        
        print(f"🔍 Running automated compliance check at {datetime.now()}")
        
        try:
            # Run license audit
            cmd = [
                "python3", "run_audit.py",
                "--policy-file", self.config["policy_file"],
                "--output-dir", str(self.audit_dir / f"audit_{timestamp}"),
                "--output-format", "json"
            ]
            
            # Add baseline comparison if available
            if os.path.exists(self.config["baseline_file"]):
                cmd.extend(["--baseline", self.config["baseline_file"]])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Audit failed: {result.stderr}")
                return {"status": "error", "message": result.stderr}
            
            # Parse results
            audit_results = self._parse_audit_results(audit_file)
            
            # Analyze changes from baseline
            changes = self._analyze_changes(audit_results)
            
            # Generate monitoring report
            report = self._generate_monitoring_report(audit_results, changes)
            
            # Check thresholds and trigger alerts
            violations = self._check_thresholds(report)
            
            if violations:
                self._send_alerts(report, violations)
            
            print(f"✅ Compliance check completed")
            print(f"📊 Status: {report['overall_status']}")
            print(f"⚠️ Issues: {len(report.get('issues', []))}")
            
            return report
            
        except Exception as e:
            print(f"❌ Monitoring failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def _parse_audit_results(self, audit_file: Path) -> Dict:
        """Parse audit results from file."""
        try:
            if audit_file.exists():
                with open(audit_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not parse audit results: {e}")
        
        return {}
    
    def _analyze_changes(self, current_results: Dict) -> Dict:
        """Analyze changes from baseline."""
        changes = {
            "new_packages": [],
            "removed_packages": [],
            "license_changes": [],
            "compliance_changes": [],
            "risk_level_changes": []
        }
        
        if not os.path.exists(self.config["baseline_file"]):
            return changes
        
        try:
            with open(self.config["baseline_file"], 'r') as f:
                baseline = json.load(f)
            
            current_packages = set(current_results.get('packages', {}).keys())
            baseline_packages = set(baseline.get('packages', {}).keys())
            
            changes["new_packages"] = list(current_packages - baseline_packages)
            changes["removed_packages"] = list(baseline_packages - current_packages)
            
            # Check for license changes
            for pkg in current_packages & baseline_packages:
                current_license = current_results['packages'][pkg].get('license', 'Unknown')
                baseline_license = baseline['packages'][pkg].get('license', 'Unknown')
                
                if current_license != baseline_license:
                    changes["license_changes"].append({
                        "package": pkg,
                        "old_license": baseline_license,
                        "new_license": current_license
                    })
        
        except Exception as e:
            print(f"Warning: Could not analyze changes: {e}")
        
        return changes
    
    def _generate_monitoring_report(self, audit_results: Dict, changes: Dict) -> Dict:
        """Generate comprehensive monitoring report."""
        return {
            "timestamp": datetime.now().isoformat(),
            "monitoring_config": self.config,
            "audit_results": audit_results,
            "changes_from_baseline": changes,
            "overall_status": audit_results.get("overall_status", "UNKNOWN"),
            "compliance_summary": audit_results.get("compliance_summary", {}),
            "issues": audit_results.get("issues", []),
            "recommendations": self._generate_recommendations(audit_results, changes)
        }
    
    def _generate_recommendations(self, audit_results: Dict, changes: Dict) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if changes["new_packages"]:
            recommendations.append(f"Review {len(changes['new_packages'])} new packages: {', '.join(changes['new_packages'][:5])}")
        
        if changes["license_changes"]:
            recommendations.append(f"Investigate {len(changes['license_changes'])} license changes")
        
        if audit_results.get("prohibited_packages"):
            recommendations.append("URGENT: Remove prohibited packages before deployment")
        
        if audit_results.get("unknown_packages"):
            recommendations.append("Research unknown package licenses")
        
        return recommendations
    
    def _check_thresholds(self, report: Dict) -> List[str]:
        """Check compliance thresholds and return violations."""
        violations = []
        thresholds = self.config["compliance_thresholds"]
        summary = report.get("compliance_summary", {})
        changes = report.get("changes_from_baseline", {})
        
        if summary.get("prohibited", 0) > thresholds["max_prohibited_packages"]:
            violations.append(f"Prohibited packages exceed threshold: {summary['prohibited']} > {thresholds['max_prohibited_packages']}")
        
        if summary.get("unknown", 0) > thresholds["max_unknown_packages"]:
            violations.append(f"Unknown packages exceed threshold: {summary['unknown']} > {thresholds['max_unknown_packages']}")
        
        if len(changes.get("new_packages", [])) > thresholds["max_new_packages_per_day"]:
            violations.append(f"New packages exceed daily threshold: {len(changes['new_packages'])} > {thresholds['max_new_packages_per_day']}")
        
        return violations
    
    def _send_alerts(self, report: Dict, violations: List[str]):
        """Send compliance violation alerts."""
        if not self.config["alert_on_violations"]:
            return
        
        print(f"🚨 COMPLIANCE VIOLATIONS DETECTED:")
        for violation in violations:
            print(f"   - {violation}")
        
        # TODO: Implement email/Slack/GitHub notifications
        # This would integrate with notification services
        
        # For now, just log to file
        alert_file = self.audit_dir / f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(alert_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "violations": violations,
                "report": report
            }, f, indent=2)
    
    def cleanup_old_audits(self):
        """Clean up old audit files based on retention policy."""
        cutoff_date = datetime.now() - timedelta(days=self.config["retention_days"])
        
        cleaned = 0
        for audit_file in self.audit_dir.glob("*"):
            if audit_file.is_file() and audit_file.stat().st_mtime < cutoff_date.timestamp():
                audit_file.unlink()
                cleaned += 1
        
        if cleaned > 0:
            print(f"🧹 Cleaned up {cleaned} old audit files")
    
    def generate_status_report(self) -> str:
        """Generate human-readable status report."""
        recent_audits = sorted(self.audit_dir.glob("automated_audit_*.json"))[-5:]
        
        report = f"""
# License Monitoring Status Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Policy:** {self.config['policy_file']}
**Monitoring:** {'✅ Enabled' if self.config['monitoring_enabled'] else '❌ Disabled'}

## Recent Activity
"""
        
        for audit_file in recent_audits:
            try:
                with open(audit_file, 'r') as f:
                    data = json.load(f)
                timestamp = audit_file.stem.replace('automated_audit_', '')
                status = data.get('overall_status', 'Unknown')
                issues = len(data.get('issues', []))
                report += f"- **{timestamp}**: {status} ({issues} issues)\n"
            except:
                continue
        
        return report


def main():
    """Main monitoring function."""
    parser = argparse.ArgumentParser(description='Automated license monitoring')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--ci-mode', action='store_true', help='Run in CI mode')
    parser.add_argument('--cleanup', action='store_true', help='Clean up old files')
    parser.add_argument('--status', action='store_true', help='Show status report')
    
    args = parser.parse_args()
    
    monitor = LicenseMonitor(args.config)
    
    if args.ci_mode:
        monitor.config["ci_mode"] = True
    
    if args.cleanup:
        monitor.cleanup_old_audits()
        return
    
    if args.status:
        print(monitor.generate_status_report())
        return
    
    # Run compliance check
    result = monitor.run_compliance_check()
    
    if result.get("status") == "error":
        sys.exit(1)
    
    # Exit with error code if non-compliant
    if result.get("overall_status") == "NON_COMPLIANT":
        print("🚨 License compliance check failed!")
        sys.exit(1)
    
    print("✅ License monitoring completed successfully")


if __name__ == "__main__":
    main() 