"""
AI-Generated Analysis Templates - Priority 3

Generates Cursor-assisted analysis code for academic research in multiple languages.
Supports Elena's Week 3 workflow for statistical analysis and visualization.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from src.narrative_gravity.utils.database import get_database_url


class JupyterTemplateGenerator:
    """Generate Jupyter notebook templates for narrative analysis."""
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize generator with database connection."""
        self.database_url = database_url or get_database_url()
        self.engine = create_engine(self.database_url)
    
    def generate_exploration_notebook(self, study_name: str, 
                                    output_path: str = "notebooks") -> str:
        """Generate exploratory data analysis notebook."""
        
        notebook = {
            "cells": [
                self._create_markdown_cell("# Narrative Gravity Wells - Exploratory Data Analysis", 
                                         f"Study: {study_name}"),
                self._create_code_cell(self._get_imports_code()),
                self._create_code_cell(self._get_data_loading_code(study_name)),
                self._create_markdown_cell("## Dataset Overview"),
                self._create_code_cell(self._get_overview_code()),
                self._create_markdown_cell("## Reliability Analysis"),
                self._create_code_cell(self._get_reliability_analysis_code()),
                self._create_markdown_cell("## Framework Performance"),
                self._create_code_cell(self._get_framework_analysis_code()),
                self._create_markdown_cell("## Visualization"),
                self._create_code_cell(self._get_visualization_code())
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        # Save notebook
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        notebook_path = output_dir / f"{study_name}_exploration.ipynb"
        with open(notebook_path, 'w') as f:
            json.dump(notebook, f, indent=2)
        
        return str(notebook_path)
    
    def _create_markdown_cell(self, *content):
        """Create markdown cell."""
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": list(content)
        }
    
    def _create_code_cell(self, code):
        """Create code cell."""
        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": code.split('\n')
        }
    
    def _get_imports_code(self):
        """Generate imports code."""
        return """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("📊 Narrative Gravity Wells Analysis")
print("=" * 50)"""
    
    def _get_data_loading_code(self, study_name):
        """Generate data loading code."""
        return f"""# Load dataset
print("Loading dataset...")
data = pd.read_feather('../data/{study_name}.feather')

print(f"✅ Loaded {{len(data)}} observations with {{len(data.columns)}} variables")
print(f"Date range: {{data['exp_date'].min()}} to {{data['exp_date'].max()}}")
print(f"Frameworks: {{data['framework'].unique()}}")
print(f"LLM Models: {{data['llm_model'].unique()}}")"""
    
    def _get_overview_code(self):
        """Generate dataset overview code."""
        return """# Dataset structure
print("\\nDataset Info:")
print(data.info())

# Basic statistics
print("\\nDescriptive Statistics:")
print(data.describe())

# Missing data analysis
print("\\nMissing Data Analysis:")
missing = data.isnull().sum()
missing_pct = (missing / len(data)) * 100
missing_df = pd.DataFrame({
    'Missing Count': missing,
    'Missing %': missing_pct
}).sort_values('Missing %', ascending=False)
print(missing_df[missing_df['Missing Count'] > 0])"""
    
    def _get_reliability_analysis_code(self):
        """Generate reliability analysis code."""
        return """# Reliability by framework
print("\\nReliability Analysis by Framework:")
reliability_stats = data.groupby('framework')['cv'].agg([
    'count', 'mean', 'std', 'min', 'max'
]).round(4)
print(reliability_stats)

# Reliability target analysis
target_cv = 0.20
reliable_analyses = data[data['cv'] <= target_cv]
reliability_rate = len(reliable_analyses) / len(data.dropna(subset=['cv'])) * 100

print(f"\\nReliability Rate (CV ≤ {target_cv}): {reliability_rate:.1f}%")

# Framework reliability comparison
framework_reliability = data.groupby('framework').apply(
    lambda x: (x['cv'] <= target_cv).mean() * 100
).round(1)
print("\\nReliability Rate by Framework:")
print(framework_reliability.sort_values(ascending=False))"""
    
    def _get_framework_analysis_code(self):
        """Generate framework analysis code."""
        return """# Framework performance comparison
print("\\nFramework Performance Analysis:")
framework_stats = data.groupby('framework').agg({
    'cv': ['mean', 'std', 'count'],
    'icc': ['mean', 'std'],
    'cost': ['mean', 'sum'],
    'process_time_sec': ['mean', 'sum']
}).round(4)

# Flatten column names
framework_stats.columns = ['_'.join(col).strip() for col in framework_stats.columns]
print(framework_stats)

# Statistical significance testing
from scipy import stats
frameworks = data['framework'].unique()
cv_by_framework = [data[data['framework'] == f]['cv'].dropna() for f in frameworks]

if len(cv_by_framework) > 1 and all(len(group) > 1 for group in cv_by_framework):
    f_stat, p_value = stats.f_oneway(*cv_by_framework)
    print(f"\\nFramework Effect on Reliability:")
    print(f"F-statistic: {f_stat:.4f}, p-value: {p_value:.4f}")
    
    if p_value < 0.05:
        print("✅ Significant framework effect detected")
    else:
        print("❌ No significant framework effect")"""
    
    def _get_visualization_code(self):
        """Generate visualization code."""
        return """# Comprehensive visualization suite
import matplotlib.pyplot as plt
import seaborn as sns

# Set up the plotting environment
plt.figure(figsize=(15, 12))

# 1. Reliability by Framework
plt.subplot(2, 3, 1)
if 'cv' in data.columns and data['cv'].notna().any():
    sns.boxplot(data=data, x='framework', y='cv')
    plt.axhline(y=0.20, color='red', linestyle='--', alpha=0.7, label='Target Threshold')
    plt.title('Reliability by Framework\\n(Lower CV = Better)')
    plt.xticks(rotation=45)
    plt.legend()

# 2. Model Performance
plt.subplot(2, 3, 2)
if 'llm_model' in data.columns and 'cv' in data.columns:
    sns.violinplot(data=data, x='llm_model', y='cv')
    plt.title('Model Performance Comparison')
    plt.xticks(rotation=45)

# 3. Cost vs Processing Time
plt.subplot(2, 3, 3)
if 'cost' in data.columns and 'process_time_sec' in data.columns:
    sns.scatterplot(data=data, x='process_time_sec', y='cost', hue='llm_model', alpha=0.7)
    plt.title('Cost vs Processing Time')
    plt.xlabel('Processing Time (seconds)')
    plt.ylabel('Cost (USD)')

# 4. Framework Usage Over Time
plt.subplot(2, 3, 4)
if 'exp_date' in data.columns:
    data_time = data.copy()
    data_time['month'] = pd.to_datetime(data_time['exp_date']).dt.to_period('M')
    framework_timeline = data_time.groupby(['month', 'framework']).size().reset_index(name='count')
    
    for framework in framework_timeline['framework'].unique():
        fdata = framework_timeline[framework_timeline['framework'] == framework]
        plt.plot(fdata['month'].astype(str), fdata['count'], marker='o', label=framework)
    
    plt.title('Framework Usage Timeline')
    plt.xticks(rotation=45)
    plt.legend()

# 5. Well Scores Distribution (if available)
well_columns = [col for col in data.columns if col.startswith('well_')]
if well_columns:
    plt.subplot(2, 3, 5)
    well_data = data[well_columns].melt()
    sns.boxplot(data=well_data, x='variable', y='value')
    plt.title('Well Scores Distribution')
    plt.xticks(rotation=45)
    plt.ylabel('Score')

# 6. Reliability Improvement Over Time
plt.subplot(2, 3, 6)
if 'exp_date' in data.columns and 'cv' in data.columns:
    data_time = data.copy()
    data_time['week'] = pd.to_datetime(data_time['exp_date']).dt.to_period('W')
    weekly_cv = data_time.groupby('week')['cv'].mean()
    
    plt.plot(weekly_cv.index.astype(str), weekly_cv.values, marker='o', linewidth=2)
    plt.axhline(y=0.20, color='red', linestyle='--', alpha=0.7, label='Target Threshold')
    plt.title('Reliability Improvement Over Time')
    plt.xticks(rotation=45)
    plt.ylabel('Mean CV')
    plt.legend()

plt.tight_layout()
plt.savefig('comprehensive_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print("\\n✅ Visualization suite completed!")
print("📊 Saved: comprehensive_analysis.png")"""


class RScriptGenerator:
    """Generate R scripts for statistical analysis and visualization."""
    
    def __init__(self):
        """Initialize R script generator."""
        self.templates = {}
    
    def generate_statistical_analysis(self, study_name: str, 
                                    output_path: str = "r_scripts") -> str:
        """Generate comprehensive R statistical analysis script."""
        
        script_content = self._build_r_analysis_script(study_name)
        
        # Save script
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        script_path = output_dir / f"{study_name}_analysis.R"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        return str(script_path)
    
    def _build_r_analysis_script(self, study_name: str) -> str:
        """Build comprehensive R analysis script."""
        
        return f"""# Narrative Gravity Wells Statistical Analysis
# Study: {study_name}
# Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# Load required libraries
library(tidyverse)
library(arrow)
library(lme4)
library(lmerTest)
library(performance)
library(ggplot2)
library(corrplot)
library(psych)

cat("📊 Narrative Gravity Wells Statistical Analysis\\n")
cat("=" %+% strrep("=", 49) %+% "\\n")

# Load data
cat("Loading dataset...\\n")
data <- read_feather("../data/{study_name}.feather")
cat("✅ Loaded", nrow(data), "observations with", ncol(data), "variables\\n")

# Data overview
cat("\\nDataset Summary:\\n")
summary(data)

# Reliability analysis
cat("\\nReliability Analysis:\\n")
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
if (sum(!is.na(data$cv)) > 10) {{
  cat("\\nMixed-effects model for reliability prediction:\\n")
  
  # Fit model
  cv_model <- lmer(cv ~ framework + llm_model + (1|text_id), 
                   data = data, REML = TRUE)
  
  # Model summary
  print(summary(cv_model))
  
  # Model performance
  cat("\\nModel Performance:\\n")
  print(performance(cv_model))
}}

# Framework comparison
cat("\\nFramework Performance Comparison:\\n")
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
cat("\\nGenerating visualizations...\\n")

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
if (length(well_columns) > 1) {{
  well_data <- data[well_columns] %>% 
    select_if(~sum(!is.na(.)) > 10)
  
  if (ncol(well_data) > 1) {{
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
  }}
}}

# 4. Timeline analysis
if ("exp_date" %in% names(data)) {{
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
}}

cat("\\n✅ Analysis complete! Check ../output/ for visualizations.\\n")
cat("📈 Statistical results saved to workspace.\\n")
"""


class StataIntegration:
    """Generate Stata scripts for publication-grade statistical analysis."""
    
    def __init__(self):
        """Initialize Stata integration."""
        pass
    
    def generate_publication_analysis(self, study_name: str, 
                                    output_path: str = "stata_scripts") -> str:
        """Generate Stata script for publication-quality analysis."""
        
        script_content = self._build_stata_script(study_name)
        
        # Save script
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        script_path = output_dir / f"{study_name}_publication.do"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        return str(script_path)
    
    def _build_stata_script(self, study_name: str) -> str:
        """Build publication-quality Stata analysis script."""
        
        return f"""// Narrative Gravity Wells Publication Analysis
// Study: {study_name}
// Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

clear all
set more off
set scheme s1color

// Load dataset
display "📊 Loading {study_name} dataset..."
use "../data/{study_name}.dta", clear

// Dataset overview
describe
summarize

// Framework reliability analysis
display "Framework Reliability Analysis:"
display "=" + _dup(60)

bysort framework: summarize cv, detail
bysort framework: display "Framework: " framework[1] ///
    ", Mean CV: " %6.4f r(mean) ", Reliability Rate: " ///
    %5.1f (r(mean) <= 0.20)*100 "%"

// Mixed-effects regression for CV prediction
display ""
display "Mixed-effects model for reliability prediction:"
mixed cv i.framework i.llm_model || text_id:, reml

// Store model for later use
estimates store cv_model

// Test framework differences
testparm i.framework
display "Framework effect p-value: " %6.4f r(p)

// Generate framework reliability table
preserve
collapse (mean) mean_cv=cv (count) n_obs=cv ///
    (sd) sd_cv=cv, by(framework)
generate reliability_rate = (mean_cv <= 0.20) * 100

// Format for publication
format mean_cv sd_cv %6.4f
format reliability_rate %5.1f

list framework mean_cv sd_cv reliability_rate n_obs, ///
    separator(0) abbreviate(15)

// Export to LaTeX
estpost tabstat mean_cv sd_cv reliability_rate n_obs, ///
    by(framework) statistics(mean) columns(statistics)
esttab using "../output/framework_reliability.tex", ///
    cells("mean_cv(fmt(4)) sd_cv(fmt(4)) reliability_rate(fmt(1)) n_obs(fmt(0))") ///
    replace booktabs ///
    title("Framework Reliability Analysis") ///
    mtitles("Mean CV" "SD CV" "Reliability Rate (%)" "N Observations")

restore

// Model comparison analysis
display ""
display "Model Performance Analysis:"
display "=" + _dup(50)

// Two-way ANOVA for CV by framework and model
anova cv framework##llm_model

// Store ANOVA results
estimates store anova_model

// Export model results
esttab cv_model using "../output/cv_regression.tex", ///
    replace booktabs ///
    title("Mixed-Effects Model: Coefficient of Variation") ///
    label nonumbers ///
    stats(N ll chi2 p aic bic, ///
        labels("Observations" "Log-likelihood" "Chi-square" "p-value" "AIC" "BIC"))

// Cost analysis (if cost data available)
capture confirm variable cost
if !_rc {{
    display ""
    display "Cost Analysis:"
    
    // Cost regression
    regress cost process_time_sec i.llm_model
    estimates store cost_model
    
    // Export cost analysis
    esttab cost_model using "../output/cost_analysis.tex", ///
        replace booktabs ///
        title("Cost Analysis Model") ///
        label
}}

// Well scores analysis (if available)
quietly: describe well_*
if r(k) > 0 {{
    display ""
    display "Well Scores Correlation Analysis:"
    
    // Correlation matrix
    pwcorr well_*, sig star(0.05) print(0.05)
    
    // Principal component analysis
    pca well_*, components(3)
    
    // Export PCA results
    esttab using "../output/pca_results.tex", ///
        replace booktabs ///
        title("Principal Component Analysis: Well Scores")
}}

// Generate summary statistics table
estpost summarize cv icc cost process_time_sec
esttab using "../output/summary_statistics.tex", ///
    cells("mean(fmt(4)) sd(fmt(4)) min(fmt(4)) max(fmt(4)) count(fmt(0))") ///
    replace booktabs ///
    title("Summary Statistics") ///
    nomtitles

display ""
display "✅ Publication analysis complete!"
display "📊 Results exported to ../output/ directory"
display "📋 LaTeX tables ready for manuscript inclusion"
"""


# Convenience functions for CLI integration
def generate_jupyter_notebook(study_name: str, output_path: str = "notebooks") -> str:
    """Quick Jupyter notebook generation."""
    generator = JupyterTemplateGenerator()
    return generator.generate_exploration_notebook(study_name, output_path)


def generate_r_analysis(study_name: str, output_path: str = "r_scripts") -> str:
    """Quick R script generation."""
    generator = RScriptGenerator()
    return generator.generate_statistical_analysis(study_name, output_path)


def generate_stata_analysis(study_name: str, output_path: str = "stata_scripts") -> str:
    """Quick Stata script generation."""
    integration = StataIntegration()
    return integration.generate_publication_analysis(study_name, output_path) 