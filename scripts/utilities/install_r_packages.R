# Install required R packages for academic analysis
packages <- c(
    "tidyverse",      # Data manipulation and visualization
    "arrow",          # Feather format support
    "lme4",           # Mixed-effects models
    "lmerTest",       # Statistical testing for mixed models
    "performance",    # Model assessment
    "ggplot2",        # Visualization (part of tidyverse but explicit)
    "corrplot",       # Correlation plots
    "psych",          # Psychological statistics
    "stargazer",      # Publication-ready tables
    "knitr",          # Dynamic report generation
    "car",            # Statistical analysis tools
    "effects",        # Effect displays
    "lattice",        # Lattice graphics
    "RColorBrewer",   # Color palettes
    "gridExtra"       # Grid graphics
)

# Install packages
cat("Installing R packages for academic analysis...\n")
install.packages(packages, repos="https://cloud.r-project.org", dependencies=TRUE)

# Verify installations
cat("Verifying package installations...\n")
for (pkg in packages) {
    if (require(pkg, character.only = TRUE, quietly = TRUE)) {
        cat(paste("✅", pkg, "installed successfully\n"))
    } else {
        cat(paste("❌", pkg, "installation failed\n"))
    }
}

cat("R package installation complete!\n") 