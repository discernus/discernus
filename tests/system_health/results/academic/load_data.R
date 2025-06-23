# Discernus Analysis Data Loader
# Load analysis results into R environment

library(readr)

# Load main analysis data
analysis_data <- read_csv("analysis_data.csv")

# Summary statistics
print("Analysis Data Summary:")
print(summary(analysis_data))

# Foundation score correlation matrix
foundation_cols <- grep("foundation_", names(analysis_data), value = TRUE)
foundation_scores <- analysis_data[foundation_cols]
correlation_matrix <- cor(foundation_scores)
print("Foundation Correlation Matrix:")
print(round(correlation_matrix, 3))

# Coordinate variance analysis
cat("\nCoordinate Variance Analysis:\n")
cat("X-coordinate variance:", var(analysis_data$x_coordinate), "\n")
cat("Y-coordinate variance:", var(analysis_data$y_coordinate), "\n")
