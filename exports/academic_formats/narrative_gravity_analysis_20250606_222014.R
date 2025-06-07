
# Narrative Gravity Analysis in R
# Generated: 2025-06-06T22:20:14.328529

library(tidyverse)
library(corrplot)
library(psych)

# Load data
data <- read.csv("exports/academic_formats/narrative_gravity_for_r_20250606_222014.csv")

# Basic descriptive statistics
summary(data)
describe(data)

# Variance analysis
variance_analysis <- data %>%
  group_by(speaker, model_name) %>%
  summarise(
    mean_variance = mean(total_variance, na.rm = TRUE),
    mean_cost = mean(cost_per_run, na.rm = TRUE),
    mean_civic_virtue = mean(civic_virtue_score, na.rm = TRUE),
    .groups = 'drop'
  )

print(variance_analysis)

# Correlation matrix
numeric_cols <- data %>% select_if(is.numeric)
correlation_matrix <- cor(numeric_cols, use = "complete.obs")
corrplot(correlation_matrix, method = "circle")

# Model comparison
model_comparison <- aov(total_variance ~ model_name + speaker, data = data)
summary(model_comparison)

# Save results
write.csv(variance_analysis, "variance_analysis_results.csv")
ggsave("correlation_plot.png", last_plot(), width = 10, height = 8)

print("Analysis complete! Check output files.")
