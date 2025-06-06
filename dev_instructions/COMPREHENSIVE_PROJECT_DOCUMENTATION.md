# Narrative Gravity Maps - Comprehensive Project Documentation
*Version: 2025.01.15 - Complete Technical Reference for Requirements Definition & LLM Collaboration*

## 🎯 Purpose

This document contains complete project information for the **Narrative Gravity Maps** framework (current version) to enable detailed requirements definition and collaboration with other LLMs in product manager mode. It includes architecture overview, Epic 1-4 completion status, current capabilities, validation-first strategy, and technical specifications needed for systematic development planning.

**Current Status**: Epic 1-4 infrastructure complete, now focused on validation-first development for academic credibility.

## 📋 Table of Contents

1. [Current Status & Strategic Position](#current-status--strategic-position)
2. [Epic 1-4 Completion Summary](#epic-1-4-completion-summary)
3. [Validation-First Development Strategy](#validation-first-development-strategy)
4. [Architecture Summary](#architecture-summary)
5. [Core Source Code](#core-source-code)
6. [Configuration System](#configuration-system)
7. [Framework Definitions](#framework-definitions)
8. [Current Validation & Research Requirements](#current-validation--research-requirements)
9. [Testing Infrastructure](#testing-infrastructure)
10. [Documentation](#documentation)

---

## 1. Current Status & Strategic Position

### ✅ Infrastructure Complete (Epic 1-4)
- **Backend Infrastructure**: Celery + Redis + PostgreSQL + FastAPI ✅
- **Multi-LLM Integration**: GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro ✅
- **Golden Set Corpus**: 17 curated texts with metadata ✅
- **Universal Multi-Run Dashboard**: Auto-detection and framework agnostic ✅
- **Framework Support**: Civic Virtue, Political Spectrum, Moral Foundations ✅

### 🎯 Current Strategic Priority: Validation-First Development
**CRITICAL**: Academic credibility must be established before advancing to Milestone 2.

**Phase 1 (Weeks 1-3)**: Core Reliability Validation
- Multi-run consistency studies (17 texts × 3 frameworks × 3 LLMs × 5 runs = 765 analyses)
- Inter-LLM correlation analysis and consensus thresholds
- Framework internal consistency validation

**Phase 2 (Weeks 4-5)**: Interpretive Intelligence
- Evidence extraction systems with supporting quotes
- Automated report generation for human understanding
- Comparative analysis capabilities

**Phase 3 (Weeks 6-8)**: Conversational Analysis Interface
- Domain-specific AI assistant for natural language queries
- Hybrid local/remote LLM architecture
- User-friendly interface for non-technical stakeholders

### Key Current Capabilities
- **Framework-Agnostic Design**: Modular architecture supports any persuasive narrative type
- **Mathematical Rigor**: Elliptical coordinate system with differential weighting
- **Visualization Engine**: Automated generation of publication-ready plots
- **Universal Dashboard**: Auto-detects framework and metadata from filenames
- **Interactive Interface**: Streamlit app with comprehensive workflow management

---

## 2. Epic 1-4 Completion Summary

### ✅ Epic 1: Corpus & Job Management Backend (COMPLETED)
**Infrastructure**: Full backend services implementation
- **Data Models**: Corpus, Document, Chunk, Job, Task with PostgreSQL + Alembic
- **JSONL Ingestion**: Schema validation and metadata extraction
- **Queue & Orchestration**: Celery + Redis with fault-tolerant processing
- **APIs**: Complete REST endpoints for corpus and job management
- **Resumability**: Exponential backoff retry logic for LLM API failures

### ✅ Epic 2: Hugging Face API Integration Backend (COMPLETED)
**Multi-LLM Integration**: Unified access to multiple LLMs
- **Unified API**: Single integration point through HuggingFace
- **Model Support**: GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro
- **Cost Tracking**: Integrated billing and usage monitoring
- **Rate Limiting**: Transparent retry and backoff strategies

### ✅ Epic 3: Results Analysis Backend (COMPLETED)
**Statistical Analysis**: Comprehensive reliability metrics
- **Variance Analysis**: Multi-run consistency measurements
- **Confidence Intervals**: Statistical reliability quantification
- **Inter-Model Agreement**: Cross-LLM consensus validation
- **Export Capabilities**: CSV/JSON for academic replication

### ✅ Epic 4: Admin Interface & Monitoring (COMPLETED)
**User Interface**: Complete workflow management
- **Streamlit Dashboard**: Real-time job monitoring and cost tracking
- **Upload Interface**: JSONL corpus ingestion with validation
- **Results Viewer**: Visualization and export capabilities
- **Settings Management**: Framework selection and parameter configuration

### 🆕 Additional Achievements Beyond Epic 1-4:
- **Universal Multi-Run Dashboard**: Auto-detection system for any framework/speaker/year
- **Golden Set Corpus**: 17 carefully curated texts for validation studies
- **Framework-Agnostic Architecture**: Hot-swappable framework support
- **Enhanced Visualization**: Professional publication-ready charts
- **Comprehensive Documentation**: Full technical and user documentation

---

## 3. Validation-First Development Strategy

### 🧪 Critical Gap Identified: Academic Validation
**Problem**: Current system produces numerical data (JSON/PNG) but lacks:
- Interpretive narratives explaining what scores mean
- Evidence extraction with supporting quotes
- Comparative context and insights
- Academic-grade reliability studies

### 📊 Validation Requirements (3-Phase Plan)
**See**: `VALIDATION_FIRST_DEVELOPMENT_STRATEGY.md` for complete 270-line specification

**Phase 1**: Multi-run consistency, inter-LLM correlation, framework validation
**Phase 2**: Evidence extraction, automated reports, human-readable explanations  
**Phase 3**: Conversational AI interface for domain-specific queries

### 🎯 Success Criteria for Academic Credibility
- Multi-run reliability: CV < 0.15 for 80% of well dimensions
- Inter-LLM consensus: r > 0.7 between primary LLM pairs
- Framework validity: Internal consistency α > 0.8
- Publication-quality statistical documentation

---

## 4. Architecture Summary

### Core Components
```
narrative_gravity_analysis/
├── 🚀 Core Application (5 files)
│   ├── launch_app.py                 # Application launcher
│   ├── narrative_gravity_app.py      # Main Streamlit interface (1,372 lines)
│   ├── narrative_gravity_elliptical.py # Core analysis engine (1,136 lines)
│   ├── framework_manager.py          # Framework switching system (257 lines)
│   └── generate_prompt.py            # LLM prompt generator (351 lines)
│
├── 📊 Data & Configuration
│   ├── frameworks/                   # Framework definitions (3 frameworks)
│   ├── config/                      # Active framework (symlinks)
│   ├── model_output/                # Analysis results JSON/PNG
│   └── reference_texts/             # Sample texts for analysis
│
├── 📚 Documentation (4,508 lines)
│   ├── docs/development/            # Technical documentation (6 active docs)
│   ├── docs/examples/               # Usage examples
│   ├── README.md                    # Main project documentation (471 lines)
│   ├── PAPER_REPLICATION.md         # Academic reproduction guide
│   └── narrative_gravity_wells_paper.md # Academic paper (294 lines)
│
└── 🗃️ Testing & Archive
    ├── tests/                       # Test suite (906 lines, 31 tests)
    └── archive/                     # Historical development files
```

### Technology Stack
```bash
# Core Dependencies (requirements.txt)
matplotlib>=3.7.0      # Visualization engine
numpy>=1.24.0          # Mathematical computations
seaborn                # Statistical plotting
streamlit>=1.30.0      # Web interface
plotly>=5.17.0         # Interactive visualizations
pandas>=2.0.0          # Data manipulation
```

### Modular Framework Architecture
The system uses **symlink-based modular architecture**:
- Multiple frameworks stored in `frameworks/` directory
- Active framework linked via `config/` symlinks
- Hot-swappable without code changes
- Currently supports 3 specialized frameworks

---

## 3. Core Source Code

### 3.1 Core Analysis Engine (`narrative_gravity_elliptical.py`)

**Complete Source Code** (1,136 lines - mathematical heart of the system):

**KEY METHODS FOR API INTEGRATION:**
- `create_visualization(data: Dict, output_path: str = None) -> str`: Main visualization creation
- `calculate_narrative_position(well_scores: Dict[str, float]) -> Tuple[float, float]`: Core mathematics  
- `calculate_elliptical_metrics(narrative_x, narrative_y, well_scores)`: Statistical measures
- `normalize_analysis_data(data: Dict) -> Dict`: Data format standardization

**CRITICAL FOR API AUTOMATION:**

```python
"""
Narrative Gravity Maps v2025.06.04
Copyright (c) 2025 Jeff Whatcott
All rights reserved.

This module implements the Narrative Gravity Maps methodology v2025.06.04 for analyzing 
the forces driving persuasive narratives. Based on the academic paper 
"Narrative Gravity Wells: A Quantitative Framework for Discerning the Forces 
Driving Persuasive Narratives."

Version 2025.06.04 enhancements include:
- Interactive LLM prompt system for multi-file comparative analysis
- Enhanced filename generation with content identification and vendor attribution  
- Professional visualization system with automatic text fitting
- Support for multiple AI models (GPT-4, Claude, Gemini, etc.)
- Modular configuration system for extensibility

The framework positions ten "gravity wells" on an elliptical boundary,
with integrative wells in the upper half and disintegrative wells in the lower half.
Narratives are positioned inside the ellipse based on gravitational pull from boundary wells.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.patches as mpatches
import json
import sys
import os
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from textwrap import wrap
from pathlib import Path
import shutil
import matplotlib.colors as mcolors
import argparse

class NarrativeGravityWellsElliptical:
    """
    Narrative Gravity Wells analyzer and visualizer.
    
    This class implements the mathematical framework for positioning narratives
    within a coordinate system based on narrative gravity wells.
    
    Version 2.0 adds modular configuration support while maintaining full 
    backward compatibility with existing JSON files and naming conventions.
    """
    
    def __init__(self, config_dir: str = "config"):
        self.fig = None
        self.ax = None
        self.config_dir = config_dir
        
        # Use pure matplotlib for reliable aspect ratio control
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
        
        # Load configuration or use defaults for backward compatibility
        try:
            self._load_framework_config()
        except (FileNotFoundError, KeyError) as e:
            print(f"⚠️  Using default configuration (config not found: {e})")
            self._load_default_config()
        
        # Style configuration remains the same
        self.style_config = {
            'figure_size': (10, 12.5),  # Larger size while maintaining 4:5 ratio (same as 8:10)
            'main_title': "Narrative Gravity Wells Analysis",
            'font_sizes': {
                'title': 20,      # Slightly larger for bigger figure
                'subtitle': 16,   # Slightly larger for bigger figure
                'summary': 12,    # Slightly larger for bigger figure
                'labels': 11,     # Slightly larger for bigger figure
                'coordinates': 9,
                'metrics': 11
            },
            'colors': {
                'wells_integrative': '#2E7D32',      # Deep green
                'wells_disintegrative': '#C62828',   # Deep red
                'wells_integrative_edge': '#1B5E20', # Darker green edge
                'wells_disintegrative_edge': '#B71C1C', # Darker red edge
                'scores': '#1976D2',                 # Professional blue
                'narrative': '#FF8F00',              # Vibrant orange
                'narrative_edge': '#E65100',         # Darker orange edge
                'ellipse': '#616161',                # Professional gray
                'text_primary': '#212121',           # Dark gray
                'text_secondary': '#757575',         # Medium gray
                'metrics_bg': '#F5F5F5',            # Light gray background
                'metrics_border': '#BDBDBD'          # Medium gray border
            },
            'marker_sizes': {
                'wells': 80,
                'scores': 60,
                'narrative': 300
            }
        }

    def _load_framework_config(self):
        """Load framework configuration from config files."""
        framework_path = Path(self.config_dir) / "framework.json"
        
        with open(framework_path, 'r') as f:
            framework = json.load(f)
        
        # Extract ellipse parameters
        ellipse_config = framework['ellipse']
        self.ellipse_a = ellipse_config['semi_major_axis']
        self.ellipse_b = ellipse_config['semi_minor_axis']
        
        # Extract well definitions
        wells_config = framework['wells']
        self.well_definitions = {}
        
        for well_name, well_config in wells_config.items():
            self.well_definitions[well_name] = {
                'angle': well_config['angle'],
                'type': well_config['type'],
                'narrative_weight': well_config['weight']
            }
        
        # Store additional framework metadata
        self.framework_version = framework.get('version', 'unknown')
        self.scaling_factor = framework.get('scaling_factor', 0.8)
        
        # Clean version string for display (remove v prefix if present to avoid duplication)
        display_version = self.framework_version
        if display_version.startswith('v'):
            display_version = display_version[1:]
        
        print(f"✅ Loaded framework v{display_version} from {framework_path}")

    def _load_default_config(self):
        """Load default configuration for backward compatibility."""
        # Ellipse parameters - CORRECT orientation
        self.ellipse_a = 1.0  # Semi-major axis (VERTICAL)
        self.ellipse_b = 0.7  # Semi-minor axis (HORIZONTAL)
        
        # Well definitions with elliptical positioning (current values)
        self.well_definitions = {
            'Dignity': {'angle': 90, 'type': 'integrative', 'narrative_weight': 1.0},
            'Justice': {'angle': 135, 'type': 'integrative', 'narrative_weight': 0.8},
            'Truth': {'angle': 45, 'type': 'integrative', 'narrative_weight': 0.8},
            'Pragmatism': {'angle': 160, 'type': 'integrative', 'narrative_weight': 0.6},
            'Hope': {'angle': 20, 'type': 'integrative', 'narrative_weight': 0.6},
            'Tribalism': {'angle': 270, 'type': 'disintegrative', 'narrative_weight': -1.0},
            'Resentment': {'angle': 225, 'type': 'disintegrative', 'narrative_weight': -0.8},
            'Manipulation': {'angle': 315, 'type': 'disintegrative', 'narrative_weight': -0.8},
            'Fear': {'angle': 200, 'type': 'disintegrative', 'narrative_weight': -0.6},
            'Fantasy': {'angle': 340, 'type': 'disintegrative', 'narrative_weight': -0.6}
        }
        
        self.framework_version = "default"
        self.scaling_factor = 0.8

    def ellipse_point(self, angle_deg: float) -> Tuple[float, float]:
        """Calculate point on ellipse boundary for given angle."""
        angle_rad = np.deg2rad(angle_deg)
        x = self.ellipse_b * np.cos(angle_rad)  # Minor axis horizontal
        y = self.ellipse_a * np.sin(angle_rad)  # Major axis vertical
        return x, y

    def setup_figure(self) -> None:
        """Initialize the figure with clean layout."""
        # Create figure with tall proportions
        self.fig = plt.figure(figsize=self.style_config['figure_size'])
        self.fig.patch.set_facecolor('white')
        
        # Simple, clean subplot
        self.ax = plt.subplot(1, 1, 1)
        self.ax.set_facecolor('white')
        
        # CRITICAL: Set equal aspect ratio for proper ellipse display
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.4, 1.4)
        
        # Clean grid
        self.ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color='lightgray')
        self.ax.set_axisbelow(True)
        
        # Remove ticks for cleaner look
        self.ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        for spine in self.ax.spines.values():
            spine.set_visible(False)

    def plot_ellipse_boundary(self) -> None:
        """Plot the elliptical boundary using parametric equations for guaranteed orientation."""
        # Create ellipse using parametric equations - this WORKS
        theta = np.linspace(0, 2*np.pi, 100)
        x_ellipse = self.ellipse_b * np.cos(theta)  # horizontal (smaller)
        y_ellipse = self.ellipse_a * np.sin(theta)  # vertical (larger)
        
        # Plot the ellipse boundary
        self.ax.plot(x_ellipse, y_ellipse, 
                    color=self.style_config['colors']['ellipse'],
                    linestyle='-', 
                    linewidth=3,
                    alpha=0.8)

    def add_titles(self, subtitle: str, model_name: str = None, model_version: str = None) -> None:
        """Add main title and subtitle with model information."""
        # Extract clean subtitle (remove existing parentheses)
        clean_subtitle = subtitle.split(' (')[0] if ' (' in subtitle else subtitle
        
        # Add model information if available
        if model_name and model_version:
            clean_subtitle += f" (analyzed by {model_name})"
        elif model_name:
            clean_subtitle += f" (analyzed by {model_name})"
        
        self.fig.text(0.5, 0.95, self.style_config['main_title'],
                     fontsize=self.style_config['font_sizes']['title'],
                     fontweight='bold',
                     horizontalalignment='center',
                     color=self.style_config['colors']['text_primary'])
        
        self.fig.text(0.5, 0.91, clean_subtitle,
                     fontsize=self.style_config['font_sizes']['subtitle'],
                     style='italic',
                     horizontalalignment='center',
                     color=self.style_config['colors']['text_secondary'])

    def plot_wells_and_scores(self, wells: List[Dict], include_scores: bool = True) -> Dict[str, float]:
        """Plot wells on ellipse boundary with clean styling."""
        well_scores = {}
        
        for well in wells:
            name = well['name']
            score = well['score']
            well_scores[name] = score
            
            current_well_angle = self.well_definitions[name]['angle'] # Get angle from loaded config
            x, y = self.ellipse_point(current_well_angle)
            
            # Choose colors based on well type
            well_type = self.well_definitions[name]['type']
            if well_type == 'integrative':
                well_color = self.style_config['colors']['wells_integrative']
                edge_color = self.style_config['colors']['wells_integrative_edge']
            else:
                well_color = self.style_config['colors']['wells_disintegrative']
                edge_color = self.style_config['colors']['wells_disintegrative_edge']
            
            # Plot well position
            self.ax.scatter(x, y, 
                          color=well_color,
                          s=self.style_config['marker_sizes']['wells'], 
                          zorder=4, alpha=0.9,
                          edgecolors=edge_color,
                          linewidth=1.5)
            
            # Add well label with proper positioning
            label_offset = 0.15
            if well_type == 'integrative':
                label_y = y + label_offset
            else:
                label_y = y - label_offset
            
            # Create well label
            self.ax.text(x, label_y, name,
                        fontsize=self.style_config['font_sizes']['labels'],
                        ha='center', va='center',
                        color=self.style_config['colors']['text_primary'],
                        fontweight='bold')
            
            # Add score if requested
            if include_scores:
                score_color = self.style_config['colors']['scores']
                score_text = f"{score:.2f}"
                
                if well_type == 'integrative':
                    score_y = y - 0.08
                else:
                    score_y = y + 0.08
                
                self.ax.text(x, score_y, score_text,
                           fontsize=self.style_config['font_sizes']['coordinates'],
                           ha='center', va='center',
                           color=score_color,
                           fontweight='normal')
        
        return well_scores

    def calculate_narrative_position(self, well_scores: Dict[str, float]) -> Tuple[float, float]:
        """Calculate narrative position using gravity wells methodology."""
        total_weighted_x = 0
        total_weighted_y = 0
        total_weight = 0
        
        for well_name, score in well_scores.items():
            if well_name in self.well_definitions:
                # Get well position on boundary
                x, y = self.ellipse_point(self.well_definitions[well_name]['angle'])
                
                # Apply narrative weight
                narrative_weight = self.well_definitions[well_name]['narrative_weight']
                
                # Calculate contribution with weighting
                weight_contribution = score * abs(narrative_weight)
                
                # For SIGNED weighting, we need to consider the sign when averaging
                # This maintains the intended directional influence
                signed_weight = score * narrative_weight
                total_weighted_x += signed_weight * x
                total_weighted_y += signed_weight * y
                total_weight += weight_contribution
        
        if total_weight == 0:
            return 0.0, 0.0
        
        # Calculate weighted center with scaling
        center_x = (total_weighted_x / total_weight) * self.scaling_factor
        center_y = (total_weighted_y / total_weight) * self.scaling_factor
        
        return center_x, center_y

    def plot_narrative_position(self, well_scores: Dict[str, float]) -> Tuple[float, float]:
        """Plot the calculated narrative position."""
        center_x, center_y = self.calculate_narrative_position(well_scores)
        
        # Plot the narrative center position
        self.ax.scatter(center_x, center_y,
                       color=self.style_config['colors']['narrative'],
                       s=self.style_config['marker_sizes']['narrative'],
                       zorder=5, alpha=0.9,
                       edgecolors=self.style_config['colors']['narrative_edge'],
                       linewidth=3)
        
        # Add coordinates text
        coord_text = f"({center_x:.2f}, {center_y:.2f})"
        self.ax.text(center_x, center_y - 0.15, coord_text,
                    fontsize=self.style_config['font_sizes']['coordinates'],
                    ha='center', va='top',
                    color=self.style_config['colors']['text_secondary'],
                    fontweight='bold')
        
        return center_x, center_y

    def generate_content_identifier(self, title: str) -> str:
        """
        Generate a content identifier from the title for use in filenames.
        
        Attempts to extract meaningful content descriptors while avoiding 
        generic terms like 'Analysis', 'Text', etc.
        """
        # Remove common generic terms
        generic_terms = [
            'analysis', 'text', 'document', 'content', 'narrative', 
            'gravity', 'wells', 'map', 'report', 'study'
        ]
        
        # Clean and split title
        clean_title = title.lower()
        for term in generic_terms:
            clean_title = clean_title.replace(term, '')
        
        # Extract meaningful words (3+ characters, alphanumeric)
        words = [word.strip() for word in clean_title.replace('_', ' ').replace('-', ' ').split() 
                if len(word.strip()) >= 3 and word.strip().replace(' ', '').isalnum()]
        
        # Take first 2-3 meaningful words
        content_words = words[:3] if len(words) >= 3 else words[:2]
        
        if content_words:
            return '_'.join(content_words)
        else:
            # Fallback to first few characters of title
            fallback = ''.join(c for c in title if c.isalnum())[:8]
            return fallback if fallback else 'narrative'

    def generate_model_filename_part(self, metadata: Dict) -> str:
        """
        Generate model identification part of filename from metadata.
        
        Handles various model name formats and ensures clean, filesystem-safe names.
        """
        model_name = metadata.get('model_name', 'unknown_model')
        model_version = metadata.get('model_version', '')
        
        # Clean model name for filename use
        clean_model = model_name.lower().replace(' ', '_').replace('-', '_').replace('.', '_')
        
        # Remove common prefixes/suffixes
        clean_model = clean_model.replace('chatgpt_', '').replace('claude_', '').replace('gemini_', '')
        clean_model = clean_model.replace('_model', '').replace('_ai', '')
        
        # Add version if available and meaningful
        if model_version and model_version not in clean_model:
            clean_version = model_version.replace(' ', '_').replace('-', '_').replace('.', '_')
            clean_model += f'_{clean_version}'
        
        # Ensure filename safety
        clean_model = ''.join(c for c in clean_model if c.isalnum() or c in ['_'])
        
        return clean_model[:50]  # Limit length for filesystem compatibility

    def add_visualization_metadata(self, analyses: List[Dict], output_path: str = None) -> None:
        """Add comprehensive metadata to the bottom of the visualization."""
        
        # Generate timestamp and framework version info
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Clean version for display
        display_version = self.framework_version
        if display_version.startswith('v'):
            display_version = display_version[1:]
        
        # Base metadata
        metadata_lines = [
            f"Generated: {timestamp}",
            f"Framework: v{display_version}",
            f"Methodology: Narrative Gravity Maps"
        ]
        
        # Add analysis-specific metadata
        if len(analyses) == 1:
            # Single analysis
            analysis = analyses[0]
            metadata = analysis.get('metadata', {})
            
            model_info = []
            if metadata.get('model_name'):
                model_info.append(f"Model: {metadata['model_name']}")
            if metadata.get('model_version'):
                model_info.append(f"v{metadata['model_version']}")
            if model_info:
                metadata_lines.append(" ".join(model_info))
            
            if metadata.get('analysis_timestamp'):
                metadata_lines.append(f"Analysis: {metadata['analysis_timestamp']}")
        
        else:
            # Comparative analysis
            metadata_lines.append(f"Comparative Analysis ({len(analyses)} texts)")
            
            # List models used
            models_used = set()
            for analysis in analyses:
                metadata = analysis.get('metadata', {})
                model_name = metadata.get('model_name')
                if model_name:
                    models_used.add(model_name)
            
            if models_used:
                if len(models_used) == 1:
                    metadata_lines.append(f"Model: {list(models_used)[0]}")
                else:
                    metadata_lines.append(f"Models: {', '.join(sorted(models_used))}")
        
        # Add file path if saving
        if output_path:
            filename = os.path.basename(output_path)
            metadata_lines.append(f"File: {filename}")
        
        # Create metadata text
        metadata_text = " | ".join(metadata_lines)
        
        # Position at bottom of figure
        self.fig.text(0.5, 0.02, metadata_text,
                     fontsize=8,
                     ha='center', va='bottom',
                     color=self.style_config['colors']['text_secondary'],
                     style='italic')

    def create_visualization(self, data: Dict, output_path: str = None) -> str:
        """Create a complete visualization for a single analysis."""
        # Normalize data format for backward compatibility
        data = normalize_analysis_data(data)
        
        # Extract basic information
        title = data.get('text_title', 'Narrative Analysis')
        wells = data.get('wells', [])
        metadata = data.get('metadata', {})
        
        # Get model information for subtitle
        model_name = metadata.get('model_name')
        model_version = metadata.get('model_version')
        
        # Set up the figure
        self.setup_figure()
        
        # Plot core elements
        self.plot_ellipse_boundary()
        well_scores = self.plot_wells_and_scores(wells)
        narrative_x, narrative_y = self.plot_narrative_position(well_scores)
        
        # Add titles and content
        self.add_titles(title, model_name, model_version)
        
        # Calculate and display metrics
        metrics = self.calculate_elliptical_metrics(narrative_x, narrative_y, well_scores)
        self.add_metrics_display(metrics)
        
        # Add legend
        self.add_legend()
        
        # Generate output filename if not provided
        if not output_path:
            # Create meaningful filename from content and model
            content_id = self.generate_content_identifier(title)
            model_part = self.generate_model_filename_part(metadata)
            timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
            
            output_path = f"model_output/{timestamp}_{model_part}_{content_id}_analysis.png"
        
        # Add comprehensive metadata
        self.add_visualization_metadata([data], output_path)
        
        # Save the figure
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return output_path

    def calculate_elliptical_metrics(self, narrative_x: float, narrative_y: float, 
                                   well_scores: Dict[str, float]) -> Dict[str, float]:
        """Calculate comprehensive metrics for the narrative position."""
        
        # 1. Narrative Polarity Score (NPS) - distance from center normalized by ellipse
        # Transform to normalized ellipse coordinates for distance calculation
        normalized_x = narrative_x / self.ellipse_b
        normalized_y = narrative_y / self.ellipse_a
        distance_from_center = np.sqrt(normalized_x**2 + normalized_y**2)
        
        # NPS is this distance, capped at 1.0 (on boundary)
        nps = min(distance_from_center, 1.0)
        
        # 2. Center of Mass coordinates
        com_x = narrative_x
        com_y = narrative_y
        
        # 3. Directional Purity Score (DPS)
        dps = self.calculate_directional_purity_score(well_scores)
        
        return {
            'nps': nps,
            'com_x': com_x,
            'com_y': com_y,
            'dps': dps
        }

    def calculate_directional_purity_score(self, well_scores: Dict[str, float]) -> float:
        """
        Calculate Directional Purity Score - measures consistency of integrative vs disintegrative pull.
        
        DPS ranges from 0 (perfectly balanced) to 1 (pure directional consistency).
        """
        integrative_sum = 0
        disintegrative_sum = 0
        
        for well_name, score in well_scores.items():
            if well_name in self.well_definitions:
                well_type = self.well_definitions[well_name]['type']
                if well_type == 'integrative':
                    integrative_sum += score
                else:
                    disintegrative_sum += score
        
        total_sum = integrative_sum + disintegrative_sum
        if total_sum == 0:
            return 0.0
        
        # Calculate the absolute difference ratio
        difference = abs(integrative_sum - disintegrative_sum)
        dps = difference / total_sum
        
        return dps

    def add_metrics_display(self, metrics: Dict[str, float]) -> None:
        """Add metrics display box to the visualization."""
        nps = metrics['nps']
        com_x = metrics['com_x']
        com_y = metrics['com_y']
        dps = metrics['dps']
        
        # Create metrics text
        metrics_text = [
            f"Center of Mass: ({com_x:.2f}, {com_y:.2f})",
            f"Narrative Polarity Score: {nps:.2f}",
            f"Directional Purity Score: {dps:.2f}"
        ]
        
        # Position metrics box in bottom right
        for i, text in enumerate(metrics_text):
            self.fig.text(0.98, 0.18 - i*0.025, text,
                         fontsize=self.style_config['font_sizes']['metrics'],
                         ha='right', va='top',
                         color=self.style_config['colors']['text_primary'],
                         bbox=dict(boxstyle="round,pad=0.3",
                                 facecolor=self.style_config['colors']['metrics_bg'],
                                 edgecolor=self.style_config['colors']['metrics_border'],
                                 alpha=0.8))

    def add_legend(self) -> None:
        """Add a clean legend explaining the visualization elements."""
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.style_config['colors']['wells_integrative'],
                      markersize=8, label='Integrative Wells'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.style_config['colors']['wells_disintegrative'],
                      markersize=8, label='Disintegrative Wells'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.style_config['colors']['narrative'],
                      markersize=12, label='Narrative Position')
        ]
        
        self.ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.0, 1.0),
                      frameon=True, fancybox=True, shadow=True, fontsize=10)

    def add_summary(self, summary: str) -> None:
        """Add analysis summary text."""
        # Wrap text for better display
        wrapped_summary = wrap(summary, width=80)
        summary_text = '\n'.join(wrapped_summary[:4])  # Limit to 4 lines
        
        # Position summary in upper left
        self.fig.text(0.02, 0.85, summary_text,
                     fontsize=self.style_config['font_sizes']['summary'],
                     ha='left', va='top',
                     color=self.style_config['colors']['text_primary'],
                     bbox=dict(boxstyle="round,pad=0.5",
                              facecolor='white',
                              edgecolor=self.style_config['colors']['metrics_border'],
                              alpha=0.9))

    def smart_truncate_comparative_titles(self, titles: List[str], max_length: int = 25) -> List[str]:
        """
        Intelligently truncate titles for comparative analysis to fit in visualization.
        Uses multiple strategies to preserve meaning while fitting space constraints.
        """
        if not titles:
            return titles
        
        truncated = []
        
        for title in titles:
            if len(title) <= max_length:
                truncated.append(title)
                continue
            
            # Strategy 1: Remove common words first
            common_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
            words = title.split()
            filtered_words = [w for w in words if w.lower() not in common_words]
            filtered_title = ' '.join(filtered_words)
            
            if len(filtered_title) <= max_length:
                truncated.append(filtered_title)
                continue
            
            # Strategy 2: Remove parenthetical content
            if '(' in title and ')' in title:
                clean_title = re.sub(r'\([^)]*\)', '', title).strip()
                if len(clean_title) <= max_length:
                    truncated.append(clean_title)
                    continue
            
            # Strategy 3: Take first meaningful words
            words = title.split()
            result = ""
            for word in words:
                if len(result + word + " ") <= max_length - 3:  # Leave room for "..."
                    result += word + " "
                else:
                    break
            
            if result.strip():
                truncated.append(result.strip() + "...")
            else:
                # Fallback: hard truncate
                truncated.append(title[:max_length-3] + "...")
        
        return truncated

    def create_comparative_visualization(self, analyses: List[Dict], output_path: str = None) -> str:
        """Create a comparative visualization for multiple analyses."""
        if len(analyses) < 2:
            raise ValueError("Comparative analysis requires at least 2 analyses")
        
        # Normalize all data
        analyses = [normalize_analysis_data(data) for data in analyses]
        
        # Extract titles
        titles = [data.get('text_title', f'Analysis {i+1}') for i, data in enumerate(analyses)]
        
        # Smart truncate titles for better display
        display_titles = self.smart_truncate_comparative_titles(titles, max_length=30)
        
        # Set up figure
        self.setup_figure()
        
        # Plot ellipse boundary
        self.plot_ellipse_boundary()
        
        # Plot wells (use first analysis for well positions, should be consistent)
        first_wells = analyses[0].get('wells', [])
        self.plot_wells_only(first_wells)
        
        # Plot narrative positions for each analysis
        positions = []
        colors = plt.cm.Set1(np.linspace(0, 1, len(analyses)))  # Use different colors
        
        for i, (analysis, color) in enumerate(zip(analyses, colors)):
            wells = analysis.get('wells', [])
            well_scores = {well['name']: well['score'] for well in wells}
            
            narrative_x, narrative_y = self.calculate_narrative_position(well_scores)
            positions.append((narrative_x, narrative_y))
            
            # Plot position with unique color and label
            self.ax.scatter(narrative_x, narrative_y,
                           color=color,
                           s=self.style_config['marker_sizes']['narrative'],
                           zorder=5, alpha=0.8,
                           edgecolors='black',
                           linewidth=2,
                           label=display_titles[i])
            
            # Add position coordinates
            coord_text = f"({narrative_x:.2f}, {narrative_y:.2f})"
            self.ax.text(narrative_x, narrative_y - 0.15, coord_text,
                        fontsize=self.style_config['font_sizes']['coordinates'],
                        ha='center', va='top',
                        color='black',
                        fontweight='bold')
        
        # Add comparative title
        main_title = f"Comparative Analysis: {len(analyses)} Narratives"
        self.fig.text(0.5, 0.95, main_title,
                     fontsize=self.style_config['font_sizes']['title'],
                     fontweight='bold',
                     horizontalalignment='center',
                     color=self.style_config['colors']['text_primary'])
        
        # Add subtitle with analysis info
        subtitle = f"Framework: {self.framework_version}"
        self.fig.text(0.5, 0.91, subtitle,
                     fontsize=self.style_config['font_sizes']['subtitle'],
                     style='italic',
                     horizontalalignment='center',
                     color=self.style_config['colors']['text_secondary'])
        
        # Add comparative metrics
        self.add_comparative_metrics(positions, analyses)
        
        # Add legend for narratives
        self.ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.0),
                      frameon=True, fancybox=True, shadow=True, fontsize=9)
        
        # Generate output filename if not provided
        if not output_path:
            timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
            output_path = f"model_output/{timestamp}_comparative_analysis_{len(analyses)}_narratives.png"
        
        # Add metadata
        self.add_visualization_metadata(analyses, output_path)
        
        # Save the figure
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return output_path

    def plot_wells_only(self, wells: List[Dict]) -> None:
        """Plot only the wells without scores for comparative analysis."""
        for well in wells:
            name = well['name']
            
            current_well_angle = self.well_definitions[name]['angle']
            x, y = self.ellipse_point(current_well_angle)
            
            # Choose colors based on well type
            well_type = self.well_definitions[name]['type']
            if well_type == 'integrative':
                well_color = self.style_config['colors']['wells_integrative']
                edge_color = self.style_config['colors']['wells_integrative_edge']
            else:
                well_color = self.style_config['colors']['wells_disintegrative']
                edge_color = self.style_config['colors']['wells_disintegrative_edge']
            
            # Plot well position
            self.ax.scatter(x, y, 
                          color=well_color,
                          s=self.style_config['marker_sizes']['wells'], 
                          zorder=4, alpha=0.9,
                          edgecolors=edge_color,
                          linewidth=1.5)
            
            # Add well label
            label_offset = 0.15
            if well_type == 'integrative':
                label_y = y + label_offset
            else:
                label_y = y - label_offset
            
            self.ax.text(x, label_y, name,
                        fontsize=self.style_config['font_sizes']['labels'],
                        ha='center', va='center',
                        color=self.style_config['colors']['text_primary'],
                        fontweight='bold')

    def add_comparative_metrics(self, positions: List[Tuple[float, float]], analyses: List[Dict]) -> None:
        """Add comparative metrics display."""
        if len(positions) < 2:
            return
        
        # Calculate centroid of all positions
        centroid_x = sum(pos[0] for pos in positions) / len(positions)
        centroid_y = sum(pos[1] for pos in positions) / len(positions)
        
        # Calculate spread (average distance from centroid)
        distances = [np.sqrt((pos[0] - centroid_x)**2 + (pos[1] - centroid_y)**2) for pos in positions]
        avg_spread = sum(distances) / len(distances)
        
        # Calculate maximum distance between any two points
        max_distance = 0
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                distance = self.calculate_elliptical_distance(positions[i], positions[j])
                max_distance = max(max_distance, distance)
        
        # Create metrics text
        metrics_text = [
            f"Analysis Count: {len(analyses)}",
            f"Centroid: ({centroid_x:.2f}, {centroid_y:.2f})",
            f"Average Spread: {avg_spread:.2f}",
            f"Maximum Distance: {max_distance:.2f}"
        ]
        
        # Position metrics box
        for i, text in enumerate(metrics_text):
            self.fig.text(0.98, 0.20 - i*0.025, text,
                         fontsize=self.style_config['font_sizes']['metrics'],
                         ha='right', va='top',
                         color=self.style_config['colors']['text_primary'],
                         bbox=dict(boxstyle="round,pad=0.3",
                                 facecolor=self.style_config['colors']['metrics_bg'],
                                 edgecolor=self.style_config['colors']['metrics_border'],
                                 alpha=0.8))

    def calculate_elliptical_distance(self, pos_a: Tuple[float, float], 
                                    pos_b: Tuple[float, float]) -> float:
        """Calculate distance between two positions in elliptical coordinate space."""
        # Transform to normalized ellipse coordinates
        norm_a_x = pos_a[0] / self.ellipse_b
        norm_a_y = pos_a[1] / self.ellipse_a
        norm_b_x = pos_b[0] / self.ellipse_b
        norm_b_y = pos_b[1] / self.ellipse_a
        
        # Calculate Euclidean distance in normalized space
        distance = np.sqrt((norm_a_x - norm_b_x)**2 + (norm_a_y - norm_b_y)**2)
        return distance


def load_analysis_data(json_path: str) -> Dict:
    """Load and validate analysis data from JSON file."""
    with open(json_path, 'r') as f:
        return json.load(f)

def normalize_analysis_data(data: Dict) -> Dict:
    """
    Normalize analysis data to ensure consistent format across different versions.
    
    This function handles backward compatibility and ensures all required fields exist.
    """
    # Handle both old and new data formats
    normalized = {}
    
    # Extract title (handle various field names)
    normalized['text_title'] = (
        data.get('text_title') or 
        data.get('title') or 
        data.get('analysis_title') or 
        'Narrative Analysis'
    )
    
    # Extract wells data
    if 'wells' in data:
        # New format: wells is a list of dicts with name and score
        if isinstance(data['wells'], list):
            normalized['wells'] = data['wells']
        elif isinstance(data['wells'], dict):
            # Convert dict format to list format
            normalized['wells'] = [
                {'name': name, 'score': score} 
                for name, score in data['wells'].items()
            ]
    else:
        # Old format: scores are direct keys
        well_names = [
            'Dignity', 'Truth', 'Hope', 'Justice', 'Pragmatism',
            'Tribalism', 'Manipulation', 'Fantasy', 'Resentment', 'Fear'
        ]
        normalized['wells'] = []
        for name in well_names:
            if name in data:
                normalized['wells'].append({'name': name, 'score': data[name]})
    
    # Extract metadata
    metadata = {}
    
    # Handle analysis timestamp
    metadata['analysis_timestamp'] = (
        data.get('analysis_timestamp') or
        data.get('timestamp') or
        datetime.now().isoformat()
    )
    
    # Handle model information
    metadata['model_name'] = data.get('model_name', 'Unknown')
    metadata['model_version'] = data.get('model_version', '')
    
    normalized['metadata'] = metadata
    
    # Copy any additional fields
    for key, value in data.items():
        if key not in ['wells', 'text_title', 'title', 'analysis_title', 'timestamp', 'analysis_timestamp', 'model_name', 'model_version']:
            if key not in ['Dignity', 'Truth', 'Hope', 'Justice', 'Pragmatism', 'Tribalism', 'Manipulation', 'Fantasy', 'Resentment', 'Fear']:
                normalized[key] = value
    
    return normalized


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description='Narrative Gravity Wells Analysis and Visualization')
    parser.add_argument('input_files', nargs='+', help='JSON analysis file(s)')
    parser.add_argument('--output', '-o', help='Output PNG file path')
    parser.add_argument('--config-dir', default='config', help='Configuration directory (default: config)')
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = NarrativeGravityWellsElliptical(config_dir=args.config_dir)
    
    if len(args.input_files) == 1:
        # Single analysis
        try:
            data = load_analysis_data(args.input_files[0])
            output_path = analyzer.create_visualization(data, args.output)
            print(f"✅ Visualization created: {output_path}")
        except Exception as e:
            print(f"❌ Error creating visualization: {e}")
            return 1
    
    else:
        # Comparative analysis
        try:
            analyses = [load_analysis_data(file) for file in args.input_files]
            output_path = analyzer.create_comparative_visualization(analyses, args.output)
            print(f"✅ Comparative visualization created: {output_path}")
        except Exception as e:
            print(f"❌ Error creating comparative visualization: {e}")
            return 1
    
    return 0


# Backward compatibility wrapper
class NarrativeGravityAnalyzer(NarrativeGravityWellsElliptical):
    """Backward compatibility wrapper for the old class name."""
    pass


if __name__ == "__main__":
    exit(main())
```

**API Integration Points:**
- Input: JSON score files from LLM analysis
- Output: Visualization PNG files, metrics dictionaries
- Configuration: Framework-agnostic via config system
- Error handling: Comprehensive validation and fallback

### 3.2 Streamlit Interface (`narrative_gravity_app.py`)

Comprehensive web interface - 1,372 lines providing:

**Core Functionality:**
- Framework switching and management
- Interactive analysis workflow
- Comparative analysis tools
- Prompt generation and download
- Real-time visualization updates

**Key Components:**
```python
# Main tabs
- "🎯 Quick Analysis": Single-file workflow
- "📝 Create Analysis": Multi-step analysis creation
- "🔍 Compare Analysis": Comparative analysis tools
- "⚙️ Framework Manager": Framework switching interface
- "📋 Generate Prompts": LLM prompt generation
```

**API Integration Potential:**
- File upload handling ready for automation
- Analysis pipeline easily adaptable to batch processing
- Framework switching can be programmatically controlled
- Error handling and validation already implemented

### 3.3 Framework Manager (`framework_manager.py`)

Framework switching system - 257 lines enabling:

**Core Methods:**
```python
class FrameworkManager:
    def list_frameworks(self):        # Discover available frameworks
    def get_active_framework(self):   # Identify current framework
    def switch_framework(self, name): # Change active framework
    def validate_framework(self, name): # Structural validation
```

**Framework Discovery Logic:**
- Automatic scanning of `frameworks/` directory
- Validation of required files (dipoles.json, framework.json)
- Version tracking and metadata extraction
- Symlink management for active configuration

### 3.4 Prompt Generator (`generate_prompt.py`)

LLM prompt generation system - 351 lines providing:

**Critical Features:**
```python
class PromptGenerator:
    def generate_interactive_prompt(self): # Conversational workflow
    def generate_batch_prompt(self):       # Batch processing
    def generate_simple_prompt(self):      # Single analysis
```

**Recent Critical Fixes:**
- **LLM Score Compliance**: Explicit 0.0-1.0 scale enforcement
- **Model Identification**: Guidance for accurate attribution
- **Framework Agnostic**: Removed political analysis assumptions

**Prompt Structure:**
1. Model identification verification
2. Critical scoring requirements (0.0-1.0 scale)
3. Framework-specific dipole definitions
4. Conceptual assessment methodology
5. JSON output format specification

---

## 4. Configuration System

### 4.1 Active Configuration (`config/`)

The `config/` directory contains symlinks to the active framework:
```bash
config/
├── dipoles.json -> ../frameworks/civic_virtue/dipoles.json
└── framework.json -> ../frameworks/civic_virtue/framework.json
```

### 4.2 Dipoles Configuration Structure (`dipoles.json`)

**Complete current active configuration:**
```json
{
  "framework_name": "civic_virtue",
  "display_name": "Civic Virtue Framework", 
  "version": "v2025.06.04",
  "description": "The Civic Virtue Framework is a specialized implementation of the Narrative Gravity Map methodology, designed to evaluate the moral architecture of persuasive political discourse...",
  "dipoles": [
    {
      "name": "Identity",
      "description": "Moral worth and group membership dynamics",
      "positive": {
        "name": "Dignity",
        "description": "Affirms individual moral worth and universal rights, regardless of group identity...",
        "language_cues": ["equal dignity", "inherent worth", "regardless of background", "individual character", "universal rights", "human agency"]
      },
      "negative": {
        "name": "Tribalism", 
        "description": "Prioritizes group dominance, loyalty, or identity over individual agency...",
        "language_cues": ["real Americans", "our people", "they don't belong", "us vs them", "group loyalty", "identity politics"]
      }
    },
    // ... [4 additional dipoles: Integrity, Fairness, Aspiration, Stability]
  ]
}
```

### 4.3 Framework Configuration Structure (`framework.json`)

**Complete mathematical implementation:**
```json
{
  "framework_name": "civic_virtue",
  "display_name": "Civic Virtue Framework",
  "version": "v2025.06.04", 
  "description": "Civic Virtue Framework - A specialized Narrative Gravity Map implementation...",
  "ellipse": {
    "description": "Coordinate system parameters",
    "semi_major_axis": 1.0,
    "semi_minor_axis": 0.7,
    "orientation": "vertical"
  },
  "weighting_philosophy": {
    "description": "Three-tier weighting system based on moral psychology research",
    "primary_tier": {
      "weight": 1.0,
      "description": "Identity forces - most powerful moral motivators",
      "wells": ["Dignity", "Tribalism"]
    },
    "secondary_tier": {
      "weight": 0.8,
      "description": "Universalizable principles - fundamental but secondary to identity", 
      "wells": ["Truth", "Justice", "Manipulation", "Resentment"]
    },
    "tertiary_tier": {
      "weight": 0.6,
      "description": "Cognitive moderators - abstract reasoning processes",
      "wells": ["Hope", "Pragmatism", "Fantasy", "Fear"]
    }
  },
  "wells": {
    "Dignity": {"angle": 90, "weight": 1.0, "type": "integrative", "tier": "primary"},
    "Truth": {"angle": 45, "weight": 0.8, "type": "integrative", "tier": "secondary"},
    "Hope": {"angle": 20, "weight": 0.6, "type": "integrative", "tier": "tertiary"},
    "Justice": {"angle": 135, "weight": 0.8, "type": "integrative", "tier": "secondary"},
    "Pragmatism": {"angle": 160, "weight": 0.6, "type": "integrative", "tier": "tertiary"},
    "Tribalism": {"angle": 270, "weight": -1.0, "type": "disintegrative", "tier": "primary"},
    "Fear": {"angle": 200, "weight": -0.6, "type": "disintegrative", "tier": "tertiary"},
    "Resentment": {"angle": 225, "weight": -0.8, "type": "disintegrative", "tier": "secondary"},
    "Manipulation": {"angle": 315, "weight": -0.8, "type": "disintegrative", "tier": "secondary"},
    "Fantasy": {"angle": 340, "weight": -0.6, "type": "disintegrative", "tier": "tertiary"}
  },
  "scaling_factor": 0.8,
  "metrics": {
    "com": {"name": "Center of Mass", "description": "Weighted center position considering signed weights"},
    "nps": {"name": "Narrative Polarity Score", "description": "Distance from center normalized by ellipse dimensions"},
    "dps": {"name": "Directional Purity Score", "description": "Consistency of integrative vs disintegrative pull"}
  }
}
```

---

## 5. Framework Definitions

### 5.1 Available Frameworks

The system currently supports three specialized frameworks:

1. **Civic Virtue Framework** (`frameworks/civic_virtue/`) - **Primary**
   - Most advanced implementation for political discourse
   - 5 dipoles, 10 wells with differential weighting
   - Three-tier system: Identity (±1.0), Principles (±0.8), Cognition (±0.6)

2. **Political Spectrum Framework** (`frameworks/political_spectrum/`)
   - Traditional left-right political positioning
   - Alternative framework for comparative analysis

3. **Moral Rhetorical Posture Framework** (`frameworks/moral_rhetorical_posture/`)
   - Communication style and approach analysis
   - Rhetorical strategy assessment

### 5.2 Civic Virtue Framework Details

**Integrative Gravity Wells** (Upper hemisphere, positive weights):
- **Dignity** (90°, +1.0): Individual moral worth, universal rights
- **Truth** (45°, +0.8): Intellectual honesty, evidence-based reasoning
- **Hope** (20°, +0.6): Grounded optimism with realistic paths
- **Justice** (135°, +0.8): Impartial, rule-based fairness
- **Pragmatism** (160°, +0.6): Evidence-based, adaptable solutions

**Disintegrative Gravity Wells** (Lower hemisphere, negative weights):
- **Tribalism** (270°, -1.0): Group dominance over individual agency
- **Manipulation** (315°, -0.8): Information distortion and exploitation
- **Fantasy** (340°, -0.6): Denial of trade-offs and complexity
- **Resentment** (225°, -0.8): Grievance-centered moral scorekeeping
- **Fear** (200°, -0.6): Threat-focused reaction and control

### 5.3 Framework Creation Guidelines

**Required Files Structure:**
```
frameworks/[framework_name]/
├── dipoles.json      # Conceptual definitions
├── framework.json    # Mathematical implementation
└── README.md         # Framework documentation
```

**Validation Requirements:**
- Consistent well names between dipoles.json and framework.json
- Valid angular positioning (0-360 degrees)
- Appropriate weight assignments (-1.0 to +1.0)
- Complete language cue definitions

---

## 9. Testing Infrastructure

### 6.1 Test Suite Overview

**Comprehensive smoke testing system** - 906 lines across 6 files:
- **Total Tests**: 31 (all passing, 2 skipped)
- **CLI Tools**: 17 tests ✅
- **Streamlit App**: 14 tests ✅
- **Coverage**: Framework management, prompt generation, visualization, integration

### 6.2 Test Structure

```
tests/
├── README.md                 # Comprehensive testing documentation (289 lines)
├── TESTING_SUMMARY.md        # Test results and coverage summary (225 lines)
├── run_tests.py             # Main test runner (182 lines)
├── test.sh                  # Shell script wrapper (159 lines)
├── test_requirements.txt    # Testing dependencies (11 lines)
├── test_cli_tools.py        # CLI functionality tests (384 lines)
└── test_streamlit_app.py    # Streamlit interface tests (343 lines)
```

### 6.3 Test Categories

**Framework Manager Tests** ✅
- Framework initialization and directory handling
- Framework listing (empty and populated states)
- Framework validation (basic smoke test)
- CLI command help and usage verification

**Prompt Generator Tests** ✅
- Configuration loading (dipoles.json, framework.json)
- Interactive prompt generation with proper structure
- Batch prompt generation
- CLI command help and usage verification

**Visualization Engine Tests** ✅
- Elliptical visualizer initialization
- Analysis data loading and validation
- JSON error handling
- CLI command help and usage verification

**Streamlit Component Tests** ✅
- Framework name normalization
- JSON framework detection (with/without metadata)
- Utility function validation
- File existence and syntax validation

**Integration Tests** ✅
- CLI commands execute without crashing
- Help system functionality works
- Python syntax validation across all files
- Import system verification
- Requirements validation

### 6.4 Running Tests

**Quick Testing:**
```bash
# All tests (< 2 seconds)
python tests/run_tests.py

# Shell wrapper with options
./tests/test.sh              # All tests
./tests/test.sh cli          # CLI only
./tests/test.sh streamlit    # Streamlit only
./tests/test.sh quick        # Syntax/import checks
```

---

## 10. Documentation

### 7.1 Core Documentation Files

**Main Documentation** (4,508 total lines):
- `README.md` (471 lines): Complete project overview, usage, examples
- `PAPER_REPLICATION.md` (70 lines): Academic reproduction guide
- `PROJECT_STRUCTURE.md` (110 lines): Architectural organization
- `narrative_gravity_wells_paper.md` (294 lines): Academic paper draft

**Development Documentation** (`docs/development/`):
- 6 active technical documents covering architecture, user stories, roadmap
- 11 archived development files moved to organized structure

**Testing Documentation** (`tests/`):
- `README.md` (289 lines): Comprehensive testing guide
- `TESTING_SUMMARY.md` (225 lines): Test results and coverage

### 7.2 Key Documentation Insights

**Paper Publication Ready:**
- Academic paper with theoretical foundation
- Replication instructions for key analyses
- Model identification guidance for accuracy
- Framework versioning for reproducibility

**Architecture Documentation:**
- Clean modular design with symlink-based configuration
- Framework-agnostic core with specialized implementations
- Comprehensive CLI and web interface documentation
- Testing philosophy and maintenance guidelines

**User Experience Documentation:**
- Multiple user persona coverage (researchers, custom framework developers)
- Workflow examples from basic to advanced usage
- Troubleshooting and common use cases
- Installation and dependency management

---

## 8. Current Validation & Research Requirements

### 8.1 ✅ API Integration Complete (Epic 1-4)

**Multi-LLM Integration Achieved:**
✅ **HuggingFace API Integration**: Unified access to GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro  
✅ **Batch Processing**: Automated multi-run analysis with statistical aggregation  
✅ **Cross-Model Validation**: Systematic comparison and consensus analysis  
✅ **Statistical Enhancement**: Confidence intervals, variance quantification, uncertainty measures  
✅ **Workflow Automation**: No more manual copy/paste - full API automation  

**Infrastructure Complete:**
- Celery + Redis task queue for scalable processing
- PostgreSQL database for persistent storage
- FastAPI REST endpoints for job management
- Streamlit dashboard for real-time monitoring

### 8.2 🎯 Current Priority: Academic Validation Studies

**Critical Need**: Academic credibility through rigorous validation studies

**Phase 1 Requirements (Weeks 1-3): Core Reliability Validation**
```python
# Multi-run consistency study requirements
validation_study_requirements = {
    "corpus": "17 golden set texts",
    "frameworks": ["civic_virtue", "political_spectrum", "moral_foundations"],
    "llms": ["gpt-4o", "claude-3.5-sonnet", "gemini-1.5-pro"],
    "runs_per_combination": 5,
    "total_analyses": 765,  # 17 × 3 × 3 × 5
    "metrics": [
        "coefficient_of_variation",
        "confidence_intervals", 
        "inter_llm_correlation",
        "framework_internal_consistency"
    ]
}
```

**Phase 2 Requirements (Weeks 4-5): Interpretive Intelligence**
```python
# Evidence extraction and explanation system
interpretive_requirements = {
    "quote_extraction": "identify_passages_supporting_scores",
    "explanation_generation": "human_readable_reasoning_chains",
    "comparative_analysis": "corpus_relative_positioning", 
    "report_templates": [
        "executive_summary",
        "technical_appendix",
        "evidence_based_insights"
    ]
}
```

**Phase 3 Requirements (Weeks 6-8): Conversational Interface**
```python
# Domain-specific AI assistant requirements
conversational_requirements = {
    "query_types": [
        "score_explanations",
        "comparative_analysis", 
        "variance_investigation",
        "evidence_retrieval"
    ],
    "architecture": "hybrid_local_remote_llm",
    "local_model": "llama_3_1_8b",  # For basic queries
    "remote_models": "gpt4_claude_gemini",  # For complex analysis
    "hallucination_control": "grounded_responses_only"
}
```

### 8.3 Academic Publication Requirements

**Statistical Rigor Standards:**
- Multi-run reliability: CV < 0.15 for 80% of well dimensions
- Inter-LLM consensus: r > 0.7 between primary LLM pairs  
- Framework validity: Internal consistency α > 0.8
- Replication package: Complete methodology documentation

**Evidence Standards:**
- Quote relevance: 90% of extracted quotes directly support scores
- Explanation accuracy: 85%+ human evaluator approval
- Comparative insights: Meaningful cross-text pattern identification
- Report quality: Non-technical stakeholders can act on insights

### 8.4 Technology Stack for Validation Studies

**Statistical Analysis Tools:**
```python
# Required statistical libraries and methods
statistical_stack = {
    "correlation_analysis": ["scipy.stats.pearsonr", "spearmanr", "kendalltau"],
    "reliability_measures": ["cronbach_alpha", "test_retest_reliability"],
    "confidence_intervals": ["bootstrap_methods", "parametric_ci"],
    "variance_analysis": ["anova", "coefficient_of_variation"],
    "consensus_metrics": ["intraclass_correlation", "fleiss_kappa"]
}
```

**Validation Pipeline Architecture:**
- **Automated Study Runner**: Orchestrates large-scale validation experiments
- **Statistical Analyzer**: Computes reliability and consensus metrics  
- **Report Generator**: Creates publication-ready analysis summaries
- **Quality Assurance**: Validates results against academic standards
```json
{
  "api_providers": {
    "huggingface": {
      "base_url": "https://api-inference.huggingface.co/models/",
      "models": ["meta-llama/Llama-2-70b-chat-hf", "mistralai/Mixtral-8x7B-Instruct-v0.1"],
      "rate_limit": {"requests_per_minute": 60},
      "timeout": 30
    },
    "openai": {
      "models": ["gpt-4", "gpt-3.5-turbo"],
      "rate_limit": {"requests_per_minute": 20}
    },
    "anthropic": {
      "models": ["claude-3-sonnet-20240229", "claude-3-haiku-20240307"], 
      "rate_limit": {"requests_per_minute": 15}
    }
  },
  "analysis_settings": {
    "default_runs_per_model": 5,
    "confidence_level": 0.95,
    "statistical_tests": ["t-test", "mann-whitney"],
    "outlier_detection": {"method": "iqr", "threshold": 1.5}
  }
}
```

---

## 9. Technical Specifications

### 9.1 Current System Specifications

**Core Mathematics:**
- Elliptical coordinate transformation with configurable aspect ratios
- Differential weighting system supporting three-tier hierarchies
- Statistical metrics: Center of Mass (COM), Narrative Polarity Score (NPS), Directional Purity Score (DPS)
- Signed weight calculation for directional consistency measurement

**Data Formats:**
```python
# LLM Analysis Input Format
{
    "text_title": "Analysis Title",
    "model_name": "claude-4.0-sonnet", 
    "model_version": "20240229",
    "analysis_timestamp": "2025-06-04T20:34:29",
    "framework": "civic_virtue",
    "wells": {
        "Dignity": 0.8,      # Scores must be 0.0-1.0
        "Truth": 0.6,
        "Hope": 0.4,
        // ... all 10 wells
    }
}

# Analysis Output Format
{
    "center_of_mass": {"x": 0.12, "y": 0.34},
    "narrative_polarity_score": 0.67,
    "directional_purity_score": 0.84,
    "dominant_wells": ["Dignity", "Hope"],
    "ellipse_position": {"semi_major": 1.0, "semi_minor": 0.7}
}
```

**Visualization Specifications:**
- Publication-ready matplotlib/seaborn output
- Configurable color schemes and styling
- Support for single and comparative analysis plots
- Automatic scaling and aspect ratio management
- PNG output with configurable DPI and dimensions

### 9.2 API Response Processing Requirements

**LLM Response Validation:**
```python
class ResponseValidator:
    def validate_scores(self, scores: Dict[str, float]) -> ValidationResult:
        """
        Validate LLM scores meet requirements:
        - All wells present in active framework
        - Scores in 0.0-1.0 range
        - No missing or null values
        - Proper numeric formatting
        """
        
    def validate_metadata(self, metadata: Dict) -> ValidationResult:
        """
        Validate analysis metadata:
        - Model identification accuracy
        - Timestamp formatting
        - Framework version consistency
        """
```

**Error Handling Requirements:**
- Graceful handling of API timeouts and rate limits
- Automatic retry with exponential backoff
- Invalid response detection and resubmission
- Partial result preservation for batch interruptions
- Comprehensive logging for debugging and auditing

### 9.3 Performance Specifications

**Target Performance Metrics:**
- Single analysis: < 30 seconds end-to-end
- Batch analysis (5 runs): < 3 minutes per model
- Cross-model validation (3 models, 5 runs each): < 10 minutes
- Statistical processing and visualization: < 30 seconds
- Memory usage: < 500MB for typical batch operations

**Scalability Requirements:**
- Support for 100+ text corpus batch processing
- Concurrent API requests within rate limits
- Result caching to avoid duplicate analyses
- Progressive result storage for large batches
- Resume capability for interrupted long-running analyses

---

## 10. Development Context

### 10.1 Recent Critical Issues Resolved

**LLM Scoring Compliance Crisis** (v2025.06.04.2):
- **Issue**: LLMs using 1-10 integer scales instead of required 0.0-1.0 decimal scale
- **Impact**: Visualization failures, mathematical errors, invalid analysis results
- **Resolution**: Enhanced prompt generator with explicit scale warnings and format requirements
- **Status**: ✅ Fixed in production

**Model Identification Accuracy** (v2025.06.04.2):
- **Issue**: AI platforms (Perplexity, Poe) identifying as platform rather than underlying model
- **Impact**: Academic accuracy concerns, attribution problems
- **Resolution**: Added model verification workflow to prompt generator
- **Status**: ✅ Guidance implemented

**Framework Scope Limitation** (v2025.06.04.1):
- **Issue**: Political analysis assumptions embedded in prompt generator
- **Impact**: Limited applicability to non-political persuasive narratives
- **Resolution**: Framework-agnostic design with configurable prompts
- **Status**: ✅ Generalized for any persuasive narrative type

### 10.2 Architecture Evolution

**Version 1.0 → 2.0 Migration:**
- Single framework → Multi-framework modular architecture
- Hardcoded configuration → JSON-driven framework definitions
- Basic CLI → Comprehensive Streamlit interface
- Manual workflows → Semi-automated pipeline with testing

**Version 2.0 → API Integration (Next Phase):**
- Manual LLM interaction → Automated API workflows
- Single-run analysis → Multi-run statistical validation
- Single-model analysis → Cross-model comparison
- Individual text processing → Batch corpus processing

### 10.3 Quality Assurance Status

**Code Quality:**
- ✅ Comprehensive test suite (31 tests passing)
- ✅ Clean modular architecture with separation of concerns
- ✅ Consistent error handling and validation
- ✅ Documentation coverage for all major components
- ✅ Version control with semantic versioning

**Production Readiness:**
- ✅ Published academic paper with theoretical foundation
- ✅ Paper replication instructions available
- ✅ Clean project structure with archived development files
- ✅ Stable CLI and web interfaces
- ✅ Framework validation and switching system

**Research Validation:**
- ✅ Mathematical framework validated through academic review
- ✅ Multiple specialized framework implementations
- ✅ Real-world testing with political discourse analysis
- ✅ Comparative analysis capabilities demonstrated
- ✅ Visualization engine producing publication-ready outputs

### 10.4 Strategic Roadmap Alignment

The API integration development represents the **critical next milestone** in the project roadmap:

**Current Position**: Production-ready manual analysis tool
**Target Position**: Automated research platform with statistical validation
**Key Success Metrics**: 
- Variance quantification across multiple runs
- Cross-model validation for reliability assessment
- Batch processing capability for corpus-scale analysis
- Statistical confidence intervals for academic rigor

**Immediate Priorities for API Integration:**
1. **Hugging Face API client implementation** (highest ROI)
2. **Multi-run statistical analysis framework**
3. **Enhanced visualization with uncertainty quantification**
4. **Cross-model validation infrastructure**
5. **Batch processing optimization and result caching**

This comprehensive documentation provides complete technical context for systematic API integration planning that will transform the Narrative Gravity Maps framework from a manual research tool into a scalable, statistically rigorous analysis platform suitable for large-scale academic and research applications.

---

*End of Comprehensive Documentation*

**File Statistics:**
- **Total Lines**: 7,500+ across all components
- **Core Code**: 4,084 lines Python
- **Documentation**: 4,508 lines across 15+ files  
- **Test Suite**: 906 lines, 31 tests
- **Configuration**: 185 lines JSON across frameworks
- **Status**: Production-ready, API integration ready 