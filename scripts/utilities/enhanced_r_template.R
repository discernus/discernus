# Enhanced Academic Visualization in R
# Study: lincoln_true_test
# Modern ggplot2 + plotly for publication-quality figures

library(tidyverse)
library(plotly)
library(corrplot)
library(viridis)
library(patchwork)  # For combining plots

# Load data
df <- read_csv("academic_exports/lincoln_true_test.csv")

# Modern Narrative Position Plot (replaces custom elliptical)
narrative_plot <- df %>%
  ggplot(aes(x = narrative_position_x, y = narrative_position_y)) +
  geom_point(aes(color = framework_config_id, size = framework_fit_score),
             alpha = 0.7) +
  geom_hline(yintercept = 0, linetype = "dashed", alpha = 0.5) +
  geom_vline(xintercept = 0, linetype = "dashed", alpha = 0.5) +
  scale_color_viridis_d(name = "Framework") +
  scale_size_continuous(name = "Fit Score", range = c(2, 8)) +
  theme_minimal() +
  theme(
    text = element_text(family = "Times", size = 12),
    plot.title = element_text(size = 14, hjust = 0.5)
  ) +
  labs(
    title = "Narrative Position Analysis",
    x = "Integrative Dimension →",
    y = "Elevation Dimension →",
    caption = "Source: Narrative Gravity Wells Analysis"
  )

# Save publication version
ggsave("narrative_position_publication.png", narrative_plot,
       width = 8, height = 6, dpi = 300, bg = "white")

# Interactive version
narrative_interactive <- ggplotly(narrative_plot)
htmlwidgets::saveWidget(narrative_interactive, "narrative_position_interactive.html")

# Well Scores Comparison (modern academic style)
well_cols <- df %>% select(starts_with("well_")) %>% names()

if (length(well_cols) > 0) {
  well_data <- df %>%
    select(framework_config_id, all_of(well_cols)) %>%
    pivot_longer(all_of(well_cols), names_to = "well", values_to = "score") %>%
    mutate(well = str_remove(well, "well_"))
  
  well_plot <- well_data %>%
    ggplot(aes(x = reorder(well, score, FUN = median), y = score)) +
    geom_violin(aes(fill = well), alpha = 0.7, show.legend = FALSE) +
    geom_boxplot(width = 0.2, alpha = 0.8) +
    facet_wrap(~framework_config_id, scales = "free_x") +
    coord_flip() +
    scale_fill_viridis_d() +
    theme_minimal() +
    theme(
      text = element_text(family = "Times", size = 10),
      strip.text = element_text(size = 12, face = "bold")
    ) +
    labs(
      title = "Well Scores Distribution by Framework",
      x = "Civic Virtue Wells",
      y = "Score (0-1 scale)"
    )
  
  ggsave("well_scores_comparison.png", well_plot,
         width = 12, height = 8, dpi = 300, bg = "white")
}

# Framework Performance Dashboard
performance_plot <- df %>%
  ggplot(aes(x = framework_config_id)) +
  geom_bar(aes(fill = success), position = "fill") +
  scale_fill_manual(values = c("FALSE" = "#d73027", "TRUE" = "#1a9850")) +
  scale_y_continuous(labels = scales::percent) +
  theme_minimal() +
  theme(
    text = element_text(family = "Times", size = 12),
    axis.text.x = element_text(angle = 45, hjust = 1)
  ) +
  labs(
    title = "Framework Success Rate",
    x = "Framework",
    y = "Success Rate",
    fill = "Success"
  )

ggsave("framework_performance.png", performance_plot,
       width = 10, height = 6, dpi = 300, bg = "white")

cat("✅ Enhanced R visualizations completed!\n")
cat("📁 Generated files:\n")
cat("   • narrative_position_publication.png\n")
cat("   • narrative_position_interactive.html\n") 
cat("   • well_scores_comparison.png\n")
cat("   • framework_performance.png\n")
