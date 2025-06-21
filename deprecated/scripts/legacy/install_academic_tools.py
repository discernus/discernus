#!/usr/bin/env python3
"""
Academic Tools Installation Script - Narrative Gravity Analysis

Installs and configures academic analysis tools for the complete research pipeline:
- Anaconda (Python scientific stack + Jupyter)
- RStudio Desktop
- Required Python packages for data analysis
- Required R packages for statistical analysis
- Stata integration setup (if license available)

Usage:
    python install_academic_tools.py --install-all
    python install_academic_tools.py --install-python-only
    python install_academic_tools.py --install-r-only
    python install_academic_tools.py --verify-installation
"""

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json
import requests
from datetime import datetime


class AcademicToolsInstaller:
    """Comprehensive academic tools installation and configuration."""
    
    def __init__(self):
        """Initialize installer with system detection."""
        self.system = platform.system().lower()
        self.arch = platform.machine().lower()
        self.python_packages = [
            "pandas>=2.0.0",
            "numpy>=1.24.0", 
            "scipy>=1.10.0",
            "statsmodels>=0.14.0",
            "scikit-learn>=1.3.0",
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0",
            "plotly>=5.15.0",
            "jupyter>=1.0.0",
            "jupyterlab>=4.0.0",
            "notebook>=6.5.0",
            "psycopg2-binary>=2.9.0",
            "sqlalchemy>=2.0.0",
            "pyarrow>=12.0.0",  # For feather format
            "pyreadstat>=1.2.0",  # For Stata .dta files
            "openpyxl>=3.1.0",  # For Excel export
            "xlsxwriter>=3.1.0"  # For advanced Excel formatting
        ]
        self.r_packages = [
            "tidyverse",
            "arrow",  # For feather files
            "lme4",  # Mixed-effects models
            "lmerTest",  # Tests for mixed-effects models
            "performance",  # Model evaluation
            "ggplot2",
            "dplyr", 
            "corrplot",
            "psych",
            "stargazer",  # Publication tables
            "RPostgreSQL",  # PostgreSQL connection
            "DBI",  # Database interface
            "knitr",  # Dynamic documents
            "rmarkdown",  # R Markdown
            "plotly",  # Interactive plots
            "shiny"  # Interactive web apps
        ]
        
    def install_all(self) -> bool:
        """Install all academic tools and packages."""
        print("🚀 Installing Academic Analysis Pipeline...")
        print("=" * 60)
        
        success = True
        
        # Step 1: Install Anaconda
        if not self.verify_anaconda():
            print("\n📦 Installing Anaconda...")
            if not self.install_anaconda():
                print("❌ Anaconda installation failed")
                success = False
            else:
                print("✅ Anaconda installed successfully")
        else:
            print("✅ Anaconda already installed")
            
        # Step 2: Install Python packages
        print("\n🐍 Installing Python packages...")
        if not self.install_python_packages():
            print("❌ Python packages installation failed")
            success = False
        else:
            print("✅ Python packages installed successfully")
            
        # Step 3: Install R and RStudio
        if not self.verify_r():
            print("\n📊 Installing R...")
            if not self.install_r():
                print("❌ R installation failed")
                success = False
            else:
                print("✅ R installed successfully")
        else:
            print("✅ R already installed")
            
        # Step 4: Install RStudio Desktop
        if not self.verify_rstudio():
            print("\n🔧 Installing RStudio Desktop...")
            if not self.install_rstudio():
                print("❌ RStudio installation failed")
                success = False
            else:
                print("✅ RStudio installed successfully")
        else:
            print("✅ RStudio already installed")
            
        # Step 5: Install R packages
        print("\n📈 Installing R packages...")
        if not self.install_r_packages():
            print("❌ R packages installation failed")
            success = False
        else:
            print("✅ R packages installed successfully")
            
        # Step 6: Configure Stata integration (optional)
        print("\n📋 Configuring Stata integration...")
        stata_configured = self.configure_stata_integration()
        if stata_configured:
            print("✅ Stata integration configured")
        else:
            print("⚠️  Stata not available - skipping integration")
            
        # Step 7: Create configuration files
        print("\n⚙️  Creating configuration files...")
        self.create_configuration_files()
        print("✅ Configuration files created")
        
        # Step 8: Verify installation
        print("\n🔍 Verifying installation...")
        verification_results = self.verify_installation()
        self.print_verification_results(verification_results)
        
        if success and verification_results['overall_success']:
            print("\n🎉 Academic tools installation completed successfully!")
            print("📚 Ready for publication-quality analysis workflow")
            return True
        else:
            print("\n❌ Installation completed with some issues")
            print("📝 Check the verification results above for details")
            return False
    
    def install_anaconda(self) -> bool:
        """Install Anaconda distribution."""
        try:
            if self.system == "darwin":  # macOS
                if "arm" in self.arch or "aarch64" in self.arch:
                    download_url = "https://repo.anaconda.com/archive/Anaconda3-2023.09-0-MacOSX-arm64.sh"
                else:
                    download_url = "https://repo.anaconda.com/archive/Anaconda3-2023.09-0-MacOSX-x86_64.sh"
                installer_name = "anaconda_installer.sh"
            elif self.system == "linux":
                download_url = "https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh"
                installer_name = "anaconda_installer.sh"
            else:  # Windows
                download_url = "https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Windows-x86_64.exe"
                installer_name = "anaconda_installer.exe"
            
            # Download installer
            print(f"📥 Downloading Anaconda from {download_url}")
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            with open(installer_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Install
            if self.system in ["darwin", "linux"]:
                subprocess.run(["chmod", "+x", installer_name], check=True)
                subprocess.run(["bash", installer_name, "-b"], check=True)
            else:  # Windows
                subprocess.run([installer_name, "/S"], check=True)
            
            # Cleanup
            os.remove(installer_name)
            
            return True
            
        except Exception as e:
            print(f"❌ Anaconda installation failed: {e}")
            return False
    
    def install_python_packages(self) -> bool:
        """Install required Python packages."""
        try:
            # Use pip from current environment
            pip_cmd = ["pip3", "install", "--upgrade"] + self.python_packages
            
            print(f"Installing packages: {', '.join(self.python_packages)}")
            result = subprocess.run(pip_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ pip install failed: {result.stderr}")
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Python packages installation failed: {e}")
            return False
    
    def install_r(self) -> bool:
        """Install R statistical software."""
        try:
            if self.system == "darwin":  # macOS
                # Install via Homebrew
                subprocess.run(["brew", "install", "r"], check=True)
            elif self.system == "linux":
                # Install via apt (Ubuntu/Debian)
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "r-base", "r-base-dev"], check=True)
            else:  # Windows
                print("⚠️  Windows R installation requires manual download from https://cran.r-project.org/")
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ R installation failed: {e}")
            return False
    
    def install_rstudio(self) -> bool:
        """Install RStudio Desktop."""
        try:
            if self.system == "darwin":  # macOS
                # Install via Homebrew Cask
                subprocess.run(["brew", "install", "--cask", "rstudio"], check=True)
            elif self.system == "linux":
                # Download and install deb package
                download_url = "https://download1.rstudio.org/electron/jammy/amd64/rstudio-2023.09.1-494-amd64.deb"
                subprocess.run(["wget", download_url, "-O", "rstudio.deb"], check=True)
                subprocess.run(["sudo", "dpkg", "-i", "rstudio.deb"], check=True)
                subprocess.run(["sudo", "apt", "install", "-f"], check=True)  # Fix dependencies
                os.remove("rstudio.deb")
            else:  # Windows
                print("⚠️  Windows RStudio installation requires manual download from https://posit.co/download/rstudio-desktop/")
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ RStudio installation failed: {e}")
            return False
    
    def install_r_packages(self) -> bool:
        """Install required R packages."""
        try:
            # Create R script to install packages
            r_script = f"""# Install required R packages
packages <- c({', '.join([f'"{pkg}"' for pkg in self.r_packages])})

install_packages <- function(packages) {{
    for (pkg in packages) {{
        if (!require(pkg, character.only = TRUE)) {{
            cat("Installing package:", pkg, "\\n")
            install.packages(pkg, dependencies = TRUE, repos = "https://cran.rstudio.com/")
            library(pkg, character.only = TRUE)
        }} else {{
            cat("Package already installed:", pkg, "\\n")
        }}
    }}
}}

install_packages(packages)
cat("✅ R packages installation completed\\n")
"""
            
            # Write and execute R script
            with open("install_r_packages.R", "w") as f:
                f.write(r_script)
            
            result = subprocess.run(["Rscript", "install_r_packages.R"], 
                                  capture_output=True, text=True)
            
            # Cleanup
            os.remove("install_r_packages.R")
            
            if result.returncode != 0:
                print(f"❌ R packages installation failed: {result.stderr}")
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ R packages installation failed: {e}")
            return False
    
    def configure_stata_integration(self) -> bool:
        """Configure Stata integration if available."""
        try:
            # Check if Stata is available
            stata_paths = [
                "/Applications/Stata/StataMP.app/Contents/MacOS/stata",
                "/Applications/Stata/StataSE.app/Contents/MacOS/stata", 
                "/usr/local/stata/stata",
                "C:\\Program Files\\Stata17\\StataMP-64.exe",
                "C:\\Program Files\\Stata16\\StataMP-64.exe"
            ]
            
            stata_path = None
            for path in stata_paths:
                if os.path.exists(path):
                    stata_path = path
                    break
            
            if not stata_path:
                # Try to find in PATH
                try:
                    result = subprocess.run(["which", "stata"], capture_output=True, text=True)
                    if result.returncode == 0:
                        stata_path = result.stdout.strip()
                except:
                    pass
            
            if stata_path:
                # Install PyStata for Python-Stata integration
                try:
                    subprocess.run(["pip3", "install", "pystata"], check=True)
                    print(f"✅ Stata found at: {stata_path}")
                    print("✅ PyStata installed for Python-Stata integration")
                    return True
                except:
                    print("⚠️  Stata found but PyStata installation failed")
                    return False
            else:
                print("⚠️  Stata not found - skipping integration")
                return False
                
        except Exception as e:
            print(f"⚠️  Stata configuration failed: {e}")
            return False
    
    def create_configuration_files(self):
        """Create configuration files for academic tools."""
        
        # Create academic tools configuration
        config = {
            "installation_date": datetime.now().isoformat(),
            "system_info": {
                "platform": self.system,
                "architecture": self.arch
            },
            "python_packages": self.python_packages,
            "r_packages": self.r_packages,
            "paths": {
                "exports": "exports/academic_formats",
                "notebooks": "notebooks",
                "r_scripts": "r_scripts", 
                "stata_scripts": "stata_scripts",
                "output": "output/academic_analysis"
            }
        }
        
        # Save configuration
        with open("config/academic_tools.json", "w") as f:
            json.dump(config, f, indent=2)
        
        # Create directories
        directories = [
            "notebooks",
            "r_scripts", 
            "stata_scripts",
            "output/academic_analysis"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def verify_anaconda(self) -> bool:
        """Verify Anaconda installation."""
        try:
            result = subprocess.run(["conda", "--version"], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def verify_r(self) -> bool:
        """Verify R installation."""
        try:
            result = subprocess.run(["R", "--version"], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def verify_rstudio(self) -> bool:
        """Verify RStudio installation."""
        if self.system == "darwin":
            return os.path.exists("/Applications/RStudio.app")
        elif self.system == "linux":
            try:
                result = subprocess.run(["which", "rstudio"], capture_output=True, text=True)
                return result.returncode == 0
            except:
                return False
        else:
            return False  # Windows check would be more complex
    
    def verify_installation(self) -> Dict[str, bool]:
        """Comprehensive installation verification."""
        results = {
            "python_packages": {},
            "r_packages": {},
            "tools": {},
            "overall_success": True
        }
        
        # Verify Python packages
        for package in self.python_packages:
            package_name = package.split(">=")[0].split("==")[0]
            try:
                __import__(package_name.replace("-", "_"))
                results["python_packages"][package_name] = True
            except ImportError:
                results["python_packages"][package_name] = False
                results["overall_success"] = False
        
        # Verify R packages
        for package in self.r_packages:
            try:
                r_script = f'if (require("{package}", quietly = TRUE)) cat("TRUE") else cat("FALSE")'
                result = subprocess.run(["Rscript", "-e", r_script], 
                                      capture_output=True, text=True)
                results["r_packages"][package] = "TRUE" in result.stdout
                if not results["r_packages"][package]:
                    results["overall_success"] = False
            except:
                results["r_packages"][package] = False
                results["overall_success"] = False
        
        # Verify tools
        results["tools"]["anaconda"] = self.verify_anaconda()
        results["tools"]["r"] = self.verify_r()
        results["tools"]["rstudio"] = self.verify_rstudio()
        
        for tool, status in results["tools"].items():
            if not status:
                results["overall_success"] = False
        
        return results
    
    def print_verification_results(self, results: Dict[str, bool]):
        """Print verification results in a formatted way."""
        print("\n📋 Installation Verification Results:")
        print("=" * 50)
        
        # Tools verification
        print("\n🔧 Academic Tools:")
        for tool, status in results["tools"].items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {tool.upper()}")
        
        # Python packages verification
        print("\n🐍 Python Packages:")
        python_success = sum(results["python_packages"].values())
        python_total = len(results["python_packages"])
        print(f"  📦 {python_success}/{python_total} packages installed")
        
        failed_python = [pkg for pkg, status in results["python_packages"].items() if not status]
        if failed_python:
            print(f"  ❌ Failed: {', '.join(failed_python)}")
        
        # R packages verification
        print("\n📈 R Packages:")
        r_success = sum(results["r_packages"].values())
        r_total = len(results["r_packages"])
        print(f"  📦 {r_success}/{r_total} packages installed")
        
        failed_r = [pkg for pkg, status in results["r_packages"].items() if not status]
        if failed_r:
            print(f"  ❌ Failed: {', '.join(failed_r)}")
        
        # Overall status
        print(f"\n🎯 Overall Status: {'✅ SUCCESS' if results['overall_success'] else '❌ ISSUES DETECTED'}")


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="Install academic analysis tools")
    parser.add_argument("--install-all", action="store_true", 
                       help="Install all academic tools")
    parser.add_argument("--install-python-only", action="store_true",
                       help="Install only Python packages")
    parser.add_argument("--install-r-only", action="store_true",
                       help="Install only R and R packages")
    parser.add_argument("--verify-installation", action="store_true",
                       help="Verify existing installation")
    
    args = parser.parse_args()
    
    installer = AcademicToolsInstaller()
    
    if args.install_all:
        success = installer.install_all()
        sys.exit(0 if success else 1)
    elif args.install_python_only:
        success = installer.install_python_packages()
        sys.exit(0 if success else 1)
    elif args.install_r_only:
        r_success = installer.install_r() if not installer.verify_r() else True
        rstudio_success = installer.install_rstudio() if not installer.verify_rstudio() else True
        packages_success = installer.install_r_packages()
        success = r_success and rstudio_success and packages_success
        sys.exit(0 if success else 1)
    elif args.verify_installation:
        results = installer.verify_installation()
        installer.print_verification_results(results)
        sys.exit(0 if results['overall_success'] else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main() 