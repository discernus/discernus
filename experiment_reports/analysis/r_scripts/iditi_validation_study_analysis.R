# Narrative Gravity Wells Statistical Analysis
# Study: iditi_validation_study
# Generated: 2025-06-14 22:18:55

# Load required libraries
library(tidyverse)
library(arrow)
library(lme4)
library(lmerTest)
library(performance)
library(ggplot2)
library(corrplot)
library(psych)

cat("📊 Narrative Gravity Wells Statistical Analysis\n")
cat("=" %+% strrep("=", 49) %+% "\n")

# Load data
cat("Loading dataset...\n")
data <- read_feather("../data/iditi_validation_study.feather")
cat("✅ Loaded", nrow(data), "observations with", ncol(data), "variables\n")

# Data overview
cat("\nDataset Summary:\n")
summary(data)

# Reliability analysis
cat("\nReliability Analysis:\n")
reliability_summary <- data %>%
  filter(!is.na(cv)) %>%
  group_by(framework) %>%
  summarise(
    n = n(),
    mean_cv = mean(cv, na.rm = TRUE),
    sd_cv = sd(cv, na.rm = TRUE),
    min_cv = min(cv, na.rm = TRUE),
    max_cv = max(cv, na.rm = TRUE),
    reliability_rate = mean(cv <= 0.20) * 100,
    .groups = 'drop'
  ) %>%
  arrange(mean_cv)

print(reliability_summary)

# Mixed-effects model for CV prediction
if (sum(!is.na(data$cv)) > 10) {
  cat("\nMixed-effects model for reliability prediction:\n")
  
  # Fit model
  cv_model <- lmer(cv ~ framework + llm_model + (1|text_id), 
                   data = data, REML = TRUE)
  
  # Model summary
  print(summary(cv_model))
  
  # Model performance
  cat("\nModel Performance:\n")
  print(performance(cv_model))
}

# Framework comparison
cat("\nFramework Performance Comparison:\n")
framework_comparison <- data %>%
  filter(!is.na(cv)) %>%
  group_by(framework) %>%
  summarise(
    reliability = mean(cv <= 0.20) * 100,
    consistency = 1 - mean(cv, na.rm = TRUE),
    n_analyses = n(),
    .groups = 'drop'
  ) %>%
  arrange(desc(reliability))

print(framework_comparison)

# Generate visualizations
cat("\nGenerating visualizations...\n")

# 1. Reliability by framework
p1 <- ggplot(data, aes(x = reorder(framework, cv, FUN = median, na.rm = TRUE), 
                       y = cv, fill = framework)) +
  geom_violin(alpha = 0.7) +
  geom_boxplot(width = 0.2, alpha = 0.8) +
  geom_hline(yintercept = 0.20, linetype = "dashed", color = "red") +
  theme_minimal() +
  labs(
    title = "Reliability by Framework",
    subtitle = "Coefficient of Variation (lower is better)",
    x = "Framework",
    y = "Coefficient of Variation",
    caption = "Red line: reliability threshold (0.20)"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  guides(fill = "none")

ggsave("../output/reliability_by_framework.png", p1, 
       width = 12, height = 8, dpi = 300)

# 2. Model performance comparison
p2 <- ggplot(data, aes(x = llm_model, y = cv, fill = llm_model)) +
  geom_violin(alpha = 0.7) +
  geom_boxplot(width = 0.3, alpha = 0.8) +
  facet_wrap(~framework, scales = "free_x") +
  theme_minimal() +
  labs(
    title = "Model Performance by Framework",
    x = "LLM Model",
    y = "Coefficient of Variation"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  guides(fill = "none")

ggsave("../output/model_performance_by_framework.png", p2,
       width = 15, height = 10, dpi = 300)

# 3. Well scores correlation matrix
well_columns <- names(data)[grepl("^well_", names(data))]
if (length(well_columns) > 1) {
  well_data <- data[well_columns] %>% 
    select_if(~sum(!is.na(.)) > 10)
  
  if (ncol(well_data) > 1) {
    well_correlations <- cor(well_data, use = "complete.obs")
    
    png("../output/well_correlations.png", width = 1200, height = 900)
    corrplot(well_correlations, 
             method = "color", 
             type = "upper",
             order = "hclust", 
             tl.cex = 1.2, 
             tl.col = "black",
             title = "Well Score Correlations",
             mar = c(0,0,2,0))
    dev.off()
  }
}

# 4. Timeline analysis
if ("exp_date" %in% names(data)) {
  timeline_data <- data %>%
    mutate(month = floor_date(exp_date, "month")) %>%
    group_by(month, framework) %>%
    summarise(
      n_analyses = n(),
      mean_cv = mean(cv, na.rm = TRUE),
      .groups = 'drop'
    )
  
  p4 <- ggplot(timeline_data, aes(x = month, y = mean_cv, color = framework)) +
    geom_line(size = 1.2) +
    geom_point(size = 2) +
    theme_minimal() +
    labs(
      title = "Reliability Improvement Over Time",
      x = "Month",
      y = "Mean Coefficient of Variation",
      color = "Framework"
    )
  
  ggsave("../output/reliability_timeline.png", p4,
         width = 12, height = 6, dpi = 300)
}

cat("\n✅ Analysis complete! Check ../output/ for visualizations.\n")
cat("📈 Statistical results saved to workspace.\n")
