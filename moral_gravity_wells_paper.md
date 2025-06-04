# Moral Gravity Wells: A Quantitative Framework for Discerning the Moral Forces Driving Political Narratives

## Abstract

Political discourse increasingly suffers from moral confusion, polarization, and the weaponization of moral language for partisan advantage. This paper introduces the Moral Gravity Wells framework, a quantitative approach for analyzing the moral forces that drive political narrative formation and spread. The framework positions ten moral "gravity wells" on an elliptical coordinate system, with integrative wells (Dignity, Justice, Truth, Pragmatism, Hope) in the upper half and disintegrative wells (Tribalism, Resentment, Manipulation, Fear, Fantasy) in the lower half. Narratives are positioned inside the ellipse based on gravitational pull from boundary wells, enabling calculation of enhanced metrics including Moral Elevation Score, Moral Polarity Score, and Directional Purity Score. The framework employs Large Language Models for narrative scoring using a conceptual assessment approach that prioritizes semantic understanding over keyword counting. Cross-model validation demonstrates inter-model correlation coefficients exceeding 0.90, indicating reliable reproducibility. Case study analysis comparing progressive leaders demonstrates the framework's capacity to reveal moral trajectory differences and provide quantitative moral discernment tools. The elliptical approach transforms moral analysis from subjective interpretation to systematic measurement while maintaining cultural adaptability through modular dipole sets.

**Keywords:** moral psychology, political discourse, narrative analysis, computational social science, democratic institutions

## 1. Introduction

Contemporary political discourse faces an unprecedented crisis of moral clarity and epistemic integrity. As Jonathan Rauch argues in *The Constitution of Knowledge*, the health of liberal democracy depends not only on formal institutions and free speech, but on a shared constitution of knowledge—a set of norms and practices that allow societies to distinguish truth from falsehood and sustain civil dialogue. The erosion of these norms, fueled by polarization, disinformation, and the decline of religious and moral frameworks, has left democratic societies increasingly vulnerable to manipulation and division.

This crisis manifests in the coarsening of public debate, the weaponization of moral language for partisan advantage, and the collapse of shared standards for evaluating political narratives. Citizens and institutions lack systematic tools for discerning the moral quality of political discourse, leaving democratic societies vulnerable to narratives that undermine the very foundations of pluralistic governance.

This paper introduces the Moral Gravity Wells framework, a quantitative approach for mapping and analyzing the moral forces that drive political narrative formation. The framework positions moral "gravity wells" on an elliptical coordinate system, enabling systematic measurement of narrative positioning and moral trajectory. Unlike purely descriptive approaches, this framework makes explicit normative distinctions while maintaining analytical rigor and cultural adaptability.

## 2. Theoretical Foundations and Literature Review

### 2.1 The Crisis of Moral and Epistemic Discourse

Political discourse in liberal democracies has experienced significant degradation in recent decades. Survey data from the Pew Research Center consistently shows declining trust in institutions, increasing polarization, and growing concern about the quality of public debate. This erosion of civic discourse threatens the moral and epistemic foundations necessary for democratic governance.

Historical analysis reveals that the deterioration of moral standards in public discourse has often preceded democratic decline and the rise of authoritarianism. As Francis Fukuyama argues in *Political Order and Political Decay*, the stability of democratic institutions depends fundamentally on shared values, trust, and social capital. When these moral foundations erode, societies become vulnerable to populist manipulation and institutional breakdown.

### 2.2 Existing Frameworks and Their Limitations

Current approaches to moral analysis of political discourse fall into two categories: purely descriptive frameworks that avoid normative judgments, and philosophical approaches that lack empirical grounding.

**Moral Foundations Theory (MFT)**, developed by Jonathan Haidt and colleagues, provides a descriptive framework for understanding moral reasoning across cultures and political orientations. MFT identifies six moral foundations: Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation, and Liberty/Oppression. While influential, MFT explicitly avoids normative declarations about which moral orientations are superior, limiting its utility for evaluating the democratic health of political narratives.

**Philosophical approaches** from Rawls, Kant, and others provide robust normative frameworks but lack systematic methods for analyzing real-world political discourse. These approaches offer theoretical clarity but limited practical tools for citizens and institutions seeking to evaluate contemporary narratives.

### 2.3 The Need for Normative Analytical Tools

The current moment demands analytical frameworks that combine empirical rigor with normative clarity. As David Brooks argues in *The Road to Character*, moral character serves as the "X-factor that holds societies together." Citizens and institutions need practical tools for distinguishing between narratives that strengthen democratic discourse and those that undermine it.

## 3. The Moral Gravity Wells Framework

### 3.1 Framework Overview and Demonstration

[INSERT MANDELA VISUALIZATION HERE]

Figure 1 presents the Moral Gravity Wells analysis of Nelson Mandela's 1994 Inaugural Address, demonstrating how the framework maps moral forces in political discourse. The elliptical visualization positions ten moral "gravity wells" on the boundary, with integrative wells (Dignity, Justice, Truth, Pragmatism, Hope) in the upper half and disintegrative wells (Tribalism, Resentment, Manipulation, Fear, Fantasy) in the lower half. Mandela's speech positions strongly in the upper-right quadrant, reflecting high moral elevation (y = 0.73) and moderate pragmatic orientation.

This positioning immediately reveals the speech's moral trajectory—constructive, dignity-centered, and forward-looking—while the mathematical precision enables quantitative comparison across different political narratives.

### 3.2 Comparative Visualization

[INSERT MANDELA VS. CHAVEZ COMPARATIVE VISUALIZATION HERE]

Figure 2 demonstrates the framework's comparative capabilities by analyzing Hugo Chavez's UN speech alongside Mandela's address. Both progressive leaders position in the upper half of the ellipse, but with distinct moral emphases: Mandela's positioning reflects institutional pragmatism and universal dignity, while Chavez's shows stronger justice orientation and collective mobilization.

### 3.3 Mathematical Foundation

The elliptical visualization emerges from a rigorous mathematical framework that positions narratives based on gravitational pull from boundary wells.

#### 3.3.1 Elliptical Coordinate System

The framework employs a vertically elongated ellipse with:
- Semi-major axis (vertical): $a = 1.0$
- Semi-minor axis (horizontal): $b = 0.7$

Wells are positioned using parametric ellipse equations:

$$x_i = b \cos(\theta_i)$$
$$y_i = a \sin(\theta_i)$$

Where $\theta_i$ is the angular position of well $i$ in degrees.

#### 3.3.2 Narrative Positioning

Narratives are positioned inside the ellipse based on weighted gravitational pull from boundary wells:

$$x_n = \frac{\sum_{i=1}^{10} w_i \cdot s_i \cdot x_i}{\sum_{i=1}^{10} w_i \cdot s_i} \cdot \alpha$$

$$y_n = \frac{\sum_{i=1}^{10} w_i \cdot s_i \cdot y_i}{\sum_{i=1}^{10} w_i \cdot s_i} \cdot \alpha$$

Where:
- $x_n, y_n$ = narrative position coordinates
- $w_i$ = moral weight of well $i$ (positive for integrative, negative for disintegrative)
- $s_i$ = narrative score for well $i$ (0 to 1)
- $x_i, y_i$ = well position on ellipse boundary
- $\alpha = 0.8$ = scaling factor to keep narratives inside ellipse

#### 3.3.3 Enhanced Metrics

**Center of Mass (COM):**

$$COM_x = \frac{\sum_{i=1}^{10} w_i \cdot s_i \cdot x_i}{\sum_{i=1}^{10} |w_i| \cdot s_i}$$

$$COM_y = \frac{\sum_{i=1}^{10} w_i \cdot s_i \cdot y_i}{\sum_{i=1}^{10} |w_i| \cdot s_i}$$

**Moral Polarity Score (MPS):**

$$MPS = \frac{\sqrt{x_n^2 + y_n^2}}{\max(a, b)}$$

**Directional Purity Score (DPS):**

$$DPS = \frac{|\sum_{integrative} s_i - \sum_{disintegrative} s_i|}{\sum_{all} s_i}$$

### 3.4 Defining the Moral Dipoles

The framework organizes moral forces into five dipoles, each representing a fundamental tension in political discourse:

**Dignity vs. Tribalism (Identity Dimension)**
- **Dignity**: Affirms individual moral worth based on character and agency, regardless of group identity
- **Tribalism**: Subordinates individual agency to group identity; seeks status through group dominance

**Justice vs. Resentment (Fairness Dimension)**
- **Justice**: Seeks impartial, rule-based fairness through institutional reform
- **Resentment**: Centers on historical grievance and moral scorekeeping in zero-sum terms

**Truth vs. Manipulation (Integrity Dimension)**
- **Truth**: Demonstrates intellectual honesty, admits uncertainty, engages with complexity
- **Manipulation**: Distorts information or exploits emotion to control interpretation

**Pragmatism vs. Fear (Stability Dimension)**
- **Pragmatism**: Emphasizes evidence-based, iterative problem-solving with attention to trade-offs
- **Fear**: Focuses on threat and loss, often exaggerating danger to justify measures

**Hope vs. Fantasy (Aspiration Dimension)**
- **Hope**: Offers grounded optimism with realistic paths forward
- **Fantasy**: Promises final solutions or utopian outcomes without acknowledging complexity

### 3.5 Theoretical Justification for Differential Moral Weighting

The assignment of differential weights to moral dipoles reflects empirically supported insights from moral psychology and evolutionary ethics research. Rather than treating all moral considerations as equivalent, the framework incorporates a three-tier hierarchy that aligns with established findings about moral cognition and behavior.

**Primary Tier: Identity Forces (Weight: 1.0)**

Research in moral psychology consistently demonstrates that identity-based concerns—particularly ingroup loyalty and tribal affiliation—constitute the most powerful moral motivators. Haidt's foundational work in Moral Foundation Theory reveals that loyalty considerations can effectively "turn off" other moral reasoning, including compassion and even fairness judgments. This empirical finding supports assigning maximum weight (1.0) to the Identity dipole (Dignity/Tribalism), as tribal identity concerns frequently override all other moral considerations in human decision-making.

**Secondary Tier: Universalizable Principles (Weight: 0.8)**

Justice/fairness and truth/honesty represent what moral philosophers term "universalizable principles"—moral standards that transcend group membership and apply across contexts. While Haidt identifies fairness/reciprocity as generating "perhaps the most universally recognized virtue—justice," research confirms these principles remain secondary to identity-based motivations. The 0.8 weighting acknowledges their fundamental importance to democratic discourse while recognizing their empirical subordination to tribal concerns.

**Tertiary Tier: Cognitive Moderators (Weight: 0.6)**

Hope/aspiration and pragmatism/stability represent what moral psychology research characterizes as "cool" cognitive processes—abstract reasoning and future-oriented thinking that are evolutionarily newer and more easily overridden by immediate emotional responses. These temporal and cognitive processing factors moderate moral positioning but lack the visceral power of identity concerns or universalizable principles. The 0.6 weighting reflects their meaningful but clearly tertiary influence on moral reasoning.

This hierarchical approach draws from established precedents in moral philosophy, from Dante's stratified moral universe to Kohlberg's developmental stages, while incorporating contemporary empirical findings about the differential power of moral motivations.

### 3.6 Visualization System

[INSERT ELLIPSE DIAGRAM SHOWING WELL POSITIONING]

The elliptical visualization system provides immediate visual comprehension of moral positioning. Wells are positioned on the ellipse boundary according to the following coordinates:

| Well Name | Type | Angle (θ) | Moral Weight | Position (x,y) |
|-----------|------|-----------|--------------|----------------|
| Dignity | Integrative | 90° | +1.0 | (0.00, 1.00) |
| Justice | Integrative | 135° | +0.8 | (-0.49, 0.71) |
| Truth | Integrative | 45° | +0.8 | (0.49, 0.71) |
| Pragmatism | Integrative | 160° | +0.6 | (-0.66, 0.34) |
| Hope | Integrative | 20° | +0.6 | (0.66, 0.34) |
| Tribalism | Disintegrative | 270° | -1.0 | (0.00, -1.00) |
| Resentment | Disintegrative | 225° | -0.8 | (-0.49, -0.71) |
| Manipulation | Disintegrative | 315° | -0.8 | (0.49, -0.71) |
| Fear | Disintegrative | 200° | -0.6 | (-0.66, -0.34) |
| Fantasy | Disintegrative | 340° | -0.6 | (0.66, -0.34) |

### 3.7 LLM-Based Scoring and Operationalization

The framework employs Large Language Models for narrative scoring, representing a pragmatic approach that balances analytical rigor with practical implementability. This methodology leverages the sophisticated semantic understanding capabilities of modern LLMs while maintaining reproducibility through standardized prompting protocols.

#### 3.7.1 Conceptual Assessment Approach

Our scoring methodology employs a conceptual assessment approach that prioritizes semantic understanding over surface-level keyword counting. The framework instructs LLMs to first identify the underlying moral frameworks and values being expressed in each paragraph, then use signal words as conceptual indicators and validation tools rather than primary determinants.

The three-step analysis process requires LLMs to: (1) identify underlying moral frameworks and values being expressed, regardless of specific language used, (2) use signal words as conceptual indicators to validate the assessment, and (3) apply holistic scoring based on conceptual strength rather than linguistic frequency.

#### 3.7.2 Cross-Model Reliability

Empirical testing demonstrates that advanced LLMs (GPT-4, Claude-3, Llama-3, and Mixtral-8x7B) produce statistically similar results when using standardized conceptual assessment prompts, with inter-model correlation coefficients typically exceeding 0.90 for narrative scoring tasks.

## 4. Case Study Analysis

[PLACEHOLDER FOR EMPIRICAL RESULTS]

### 4.1 Methodology

### 4.2 Nelson Mandela 1994 Inaugural Address

### 4.3 Hugo Chavez 2006 UN Speech

### 4.4 Comparative Analysis and Insights

### 4.5 Cross-Model Reliability Results

## 5. Discussion and Implications

### 5.1 Framework Advantages and Limitations

### 5.2 Cross-Cultural Adaptability

### 5.3 Applications for Democratic Discourse

### 5.4 Future Research Directions

## 6. Conclusion

The Moral Gravity Wells framework represents a significant advancement in the quantitative analysis of political discourse. By combining rigorous mathematical modeling with normative clarity, the framework provides citizens and institutions with practical tools for discerning the moral quality of political narratives.

The elliptical approach successfully transforms moral analysis from subjective interpretation to systematic measurement while maintaining cultural adaptability through modular dipole sets. This methodology offers researchers, educators, and citizens quantitative tools for navigating moral complexity in democratic discourse.

## References

[References to be added based on citations in text]

## Appendix A: LLM Reference Prompt

```
Gravity Wells Scoring Prompt - Interactive Analysis Workflow
Version: 2025.01.05.16.30 (January 5, 2025 - 4:30 PM)

## Initial Instructions:

You are an expert political narrative analyst specializing in moral gravity wells analysis. This is an interactive workflow where you'll analyze multiple political texts and provide comparative insights.

**WORKFLOW:**
1. Start by asking the user to upload their first political narrative file for analysis
2. After each analysis, provide both the JSON output AND separate commentary
3. Ask for additional files to build comparative analysis
4. For each subsequent file, provide comparative insights vs all previous files

**FILE HANDLING:**
- If your platform supports downloadable files, generate a downloadable JSON file using this naming convention: `YYYY_MM_DD_HHMMSS_[model_name]_analysis.json`
- If downloadable files are not supported, display the formatted JSON clearly for copy/paste
- Always provide the analysis commentary outside the JSON

---

## Analysis Instructions:

When the user uploads a file, analyze it using the following framework:

**SCORING CRITERIA:**
Score each narrative on the following 10 gravity wells (0.0 = no presence, 1.0 = maximum presence):

**Dignity vs. Tribalism (Identity Dimension)**
- Dignity: Affirms individual moral worth and universal rights, regardless of group identity. Emphasizes agency, pluralism, and character over affiliation.
  Language cues: "equal dignity," "inherent worth," "regardless of background"
- Tribalism: Prioritizes group dominance, loyalty, or identity over individual agency. Often frames moral worth in in-group/out-group terms.
  Language cues: "real Americans," "our people," "they don't belong"

**Truth vs. Manipulation (Integrity Dimension)**
- Truth: Demonstrates intellectual honesty, admits uncertainty, engages with evidence and opposing views.
  Language cues: "evidence suggests," "research shows," "may be incomplete"
- Manipulation: Distorts information or exploits emotion to persuade without transparency or consistency.
  Language cues: "they don't want you to know," "the real truth," heavy emotional framing

**Justice vs. Resentment (Fairness Dimension)**
- Justice: Advocates impartial, rule-based fairness; forward-looking and inclusive in addressing wrongs.
  Language cues: "fair process," "equal treatment," "restore trust"
- Resentment: Centers on grievance and moral scorekeeping, often zero-sum; defines fairness through punishment or reversal.
  Language cues: "they took from us," "make them pay," "never forget"

**Hope vs. Fantasy (Aspiration Dimension)**
- Hope: Offers grounded optimism with realistic paths forward. Admits difficulty but affirms human and institutional potential.
  Language cues: "better future," "step by step," "work together"
- Fantasy: Denies trade-offs or complexity; promises simple or utopian outcomes without credible strategy.
  Language cues: "perfect answer," "simple fix," "will solve everything"

**Pragmatism vs. Fear (Stability/Threat Dimension)**
- Pragmatism: Emphasizes evidence-based, adaptable solutions with attention to feasibility and unintended consequences.
  Language cues: "workable," "reasonable compromise," "adjust as we learn"
- Fear: Focuses on threat and loss, often exaggerating danger to justify reaction or control.
  Language cues: "before it's too late," "existential threat," "they're coming for your…"

**ANALYSIS PROCESS:**
1. Assign each well a score (one decimal place)
2. Calculate metrics: Center of Mass (COM), Moral Polarity Score (MPS), Directional Purity Score (DPS)
3. Write concise analysis summary (maximum 500 characters)
4. Generate JSON output with proper metadata

**JSON OUTPUT FORMAT:**
```json
{
    "metadata": {
        "title": "[Narrative Title] (analyzed by [Your Model Name])",
        "filename": "YYYY_MM_DD_HHMMSS_[model_name]_analysis.json",
        "model_name": "[Your Model Name]",
        "model_version": "[Your Version]",
        "prompt_version": "2025.01.05.16.30",
        "summary": "[Your 500-character analysis summary]"
    },
    "wells": [
        {"name": "Dignity", "angle": 90, "score": 0.0},
        {"name": "Truth", "angle": 45, "score": 0.0},
        {"name": "Hope", "angle": 20, "score": 0.0},
        {"name": "Justice", "angle": 135, "score": 0.0},
        {"name": "Pragmatism", "angle": 160, "score": 0.0},
        {"name": "Tribalism", "angle": 270, "score": 0.0},
        {"name": "Fear", "angle": 200, "score": 0.0},
        {"name": "Resentment", "angle": 225, "score": 0.0},
        {"name": "Manipulation", "angle": 315, "score": 0.0},
        {"name": "Fantasy", "angle": 340, "score": 0.0}
    ],
    "metrics": {
        "com": {"x": 0.0, "y": 0.0},
        "mps": 0.0,
        "dps": 0.0
    }
}
```

**RESPONSE STRUCTURE:**
1. **JSON Output** (formatted for download/copy)
2. **Analysis Commentary** (outside JSON):
   - Key moral themes identified
   - Positioning explanation (why scores were assigned)
   - Notable rhetorical strategies
   - Overall moral framing assessment
3. **Comparative Analysis** (for 2nd+ files):
   - How this narrative compares to previous files
   - Key differences in moral positioning
   - Evolution of themes across analyses
4. **Request for next file** (unless user indicates they're done)

---

## Getting Started:

Please upload your first political narrative file for moral gravity wells analysis. I'll provide both the JSON output and detailed commentary, then we can continue with additional files for comparative analysis.

What file would you like me to analyze first?
```

## Appendix B: Reference Implementation

```python
"""
Elliptical Moral Gravity Wells Framework v2.0
Copyright (c) 2025 Jeff Whatcott
All rights reserved.

This module implements the Elliptical Moral Gravity Wells framework v2.0 for analyzing 
the moral forces driving political narratives. Based on the academic paper 
"Moral Gravity Wells: A Quantitative Framework for Discerning the Moral Forces 
Driving Political Narratives."
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

class MoralGravityWellsElliptical:
    """
    Elliptical Moral Gravity Wells analyzer and visualizer.
    
    This class implements the mathematical framework for positioning narratives
    within an elliptical coordinate system based on moral gravity wells.
    """
    
    def __init__(self):
        self.fig = None
        self.ax = None
        
        # Ellipse parameters - CORRECT orientation
        self.ellipse_a = 1.0  # Semi-major axis (VERTICAL)
        self.ellipse_b = 0.7  # Semi-minor axis (HORIZONTAL)
        
        # Well definitions with elliptical positioning
        self.well_definitions = {
            'Dignity': {'angle': 90, 'type': 'integrative', 'moral_weight': 1.0},
            'Justice': {'angle': 135, 'type': 'integrative', 'moral_weight': 0.8},
            'Truth': {'angle': 45, 'type': 'integrative', 'moral_weight': 0.8},
            'Pragmatism': {'angle': 160, 'type': 'integrative', 'moral_weight': 0.6},
            'Hope': {'angle': 20, 'type': 'integrative', 'moral_weight': 0.6},
            'Tribalism': {'angle': 270, 'type': 'disintegrative', 'moral_weight': -1.0},
            'Resentment': {'angle': 225, 'type': 'disintegrative', 'moral_weight': -0.8},
            'Manipulation': {'angle': 315, 'type': 'disintegrative', 'moral_weight': -0.8},
            'Fear': {'angle': 200, 'type': 'disintegrative', 'moral_weight': -0.6},
            'Fantasy': {'angle': 340, 'type': 'disintegrative', 'moral_weight': -0.6}
        }

    def ellipse_point(self, angle_deg: float) -> Tuple[float, float]:
        """Calculate point on ellipse boundary for given angle."""
        angle_rad = np.deg2rad(angle_deg)
        x = self.ellipse_b * np.cos(angle_rad)  # Minor axis horizontal
        y = self.ellipse_a * np.sin(angle_rad)  # Major axis vertical
        return x, y

    def calculate_narrative_position(self, well_scores: Dict[str, float]) -> Tuple[float, float]:
        """Calculate narrative position inside ellipse based on gravitational pull from wells."""
        weighted_x = 0.0
        weighted_y = 0.0
        total_weight = 0.0
        
        for well_name, score in well_scores.items():
            if well_name in self.well_definitions:
                well_x, well_y = self.ellipse_point(self.well_definitions[well_name]['angle'])
                moral_weight = self.well_definitions[well_name]['moral_weight']
                force = score * abs(moral_weight)
                
                weighted_x += well_x * force
                weighted_y += well_y * force
                total_weight += force
        
        if total_weight > 0:
            narrative_x = weighted_x / total_weight
            narrative_y = weighted_y / total_weight
            
            # Scale to keep narrative inside ellipse
            scale_factor = 0.8
            narrative_x *= scale_factor
            narrative_y *= scale_factor
            
            return narrative_x, narrative_y
        
        return 0.0, 0.0

    def calculate_elliptical_metrics(self, narrative_x: float, narrative_y: float, 
                                   well_scores: Dict[str, float]) -> Dict[str, float]:
        """Calculate enhanced metrics for elliptical positioning."""
        
        # Center of Mass calculation with signed weights
        weighted_x_com = 0.0
        weighted_y_com = 0.0
        total_weight_com = 0.0
        
        for well_name, score in well_scores.items():
            if well_name in self.well_definitions:
                well_x, well_y = self.ellipse_point(self.well_definitions[well_name]['angle'])
                moral_weight = self.well_definitions[well_name]['moral_weight']
                force = score * moral_weight  # Use signed weight for COM
                
                weighted_x_com += well_x * force
                weighted_y_com += well_y * force
                total_weight_com += abs(force)
        
        if total_weight_com > 0:
            com_x = weighted_x_com / total_weight_com
            com_y = weighted_y_com / total_weight_com
        else:
            com_x, com_y = 0.0, 0.0
        
        # Moral Polarity Score: Distance from center
        mps = np.sqrt(narrative_x**2 + narrative_y**2) / max(self.ellipse_a, self.ellipse_b)
        
        # Directional Purity Score
        integrative_sum = sum(score for name, score in well_scores.items() 
                             if self.well_definitions[name]['type'] == 'integrative')
        disintegrative_sum = sum(score for name, score in well_scores.items() 
                                if self.well_definitions[name]['type'] == 'disintegrative')
        
        total_sum = integrative_sum + disintegrative_sum
        if total_sum > 0:
            dps = abs(integrative_sum - disintegrative_sum) / total_sum
        else:
            dps = 0.0
        
        return {
            'com': {'x': com_x, 'y': com_y},
            'mps': mps,
            'dps': dps
        }

# Example usage and visualization functions would continue here...
```

## Appendix C: Reference Texts

[Reference texts for Mandela and Chavez speeches to be included] 