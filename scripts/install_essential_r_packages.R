# Install Essential R Packages for Academic Analysis
# Focused installation with compiler compatibility

# Essential packages only
essential_packages <- c(
    "ggplot2",        # Core visualization
    "dplyr",          # Data manipulation  
    "readr",          # Data reading
    "knitr",          # Report generation
    "corrplot"        # Correlation plots (already installed)
)

# Try installing with better error handling
cat("Installing essential R packages with compiler fix...\n")

for (pkg in essential_packages) {
    cat(paste("Attempting to install:", pkg, "\n"))
    
    tryCatch({
        if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
            install.packages(pkg, repos="https://cloud.r-project.org", dependencies=TRUE)
            
            # Verify installation
            if (require(pkg, character.only = TRUE, quietly = TRUE)) {
                cat(paste("✅", pkg, "installed successfully\n"))
            } else {
                cat(paste("❌", pkg, "installation failed\n"))
            }
        } else {
            cat(paste("✅", pkg, "already installed\n"))
        }
    }, error = function(e) {
        cat(paste("❌", pkg, "error:", e$message, "\n"))
    })
}

cat("Essential R packages installation attempt complete!\n") 