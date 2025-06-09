# Political Spectrum Framework

**A Narrative Gravity Map for Traditional Left-Right Political Analysis**

The Political Spectrum Framework is a specialized implementation of the Narrative Gravity Map methodology, designed to evaluate political discourse through traditional left-right ideological dimensions. It maps narratives along five core dipoles—Economic (Solidarity vs. Competition), Social (Equality vs. Tradition), Authority (Democracy vs. Control), Identity (Cosmopolitan vs. Nationalist), and Change (Progressive vs. Conservative)—each representing fundamental tensions in political thought.

This framework enables analysts to assess where political narratives position themselves on the traditional political spectrum, moving beyond simple left-right labels to understand the multidimensional nature of political ideology. The framework captures the complex interplay between economic policy preferences, social values, governance approaches, identity orientations, and attitudes toward change.

By revealing a narrative's political gravity—its pull toward different ideological poles—the Political Spectrum Framework equips analysts, political scientists, strategists, and citizens with tools to map and compare political positions across actors, texts, and contexts with unprecedented precision.

## Framework Architecture

### Five Core Dipoles

**Economic Dimension: Solidarity ↔ Competition**
- **Solidarity**: Emphasizes collective economic action, wealth redistribution, and social safety nets
- **Competition**: Emphasizes market competition, individual economic achievement, and minimal government intervention

**Social Dimension: Equality ↔ Tradition**  
- **Equality**: Promotes social equality, cultural diversity, and progressive social change
- **Tradition**: Values traditional social structures, cultural continuity, and established social hierarchies

**Authority Dimension: Democracy ↔ Control**
- **Democracy**: Emphasizes participatory governance, civil liberties, and transparency
- **Control**: Accepts or promotes concentrated authority, strong leadership, and hierarchical order

**Identity Dimension: Cosmopolitan ↔ Nationalist**
- **Cosmopolitan**: Embraces global citizenship, international cooperation, and universal human values
- **Nationalist**: Prioritizes national identity, sovereignty, and domestic interests over international considerations

**Change Dimension: Progressive ↔ Conservative**
- **Progressive**: Advocates for rapid social change, reform, and transformation of existing systems
- **Conservative**: Favors gradual change, preservation of existing institutions, and caution about rapid transformation

## Overview

This framework analyzes text through traditional left-right political dimensions, examining tensions between solidarity/competition, equality/tradition, and democratic/authoritarian impulses. It is ideal for analyzing political speeches, policy documents, campaign materials, and ideological texts across the political spectrum.

## Theoretical Basis

### Core Concept
Political ideologies emerge from competing values and priorities that can be modeled as dipolar tensions. Each dipole represents a fundamental dimension of political reasoning, with integrative forces promoting social cohesion and cooperation, and disintegrative forces emphasizing competition, hierarchy, and in-group preferences.

### Dipole Structure

**Primary Tier (Weight: 1.0)**
- **Economic Dipole**: Solidarity vs Competition
- **Authority Dipole**: Democracy vs Control
  - Core dimensions that define major political divisions
  - Most predictive of overall ideological orientation

**Secondary Tier (Weight: 0.8-0.9)**  
- **Social Dipole**: Equality vs Tradition
  - Cultural and social value systems
  - Strong predictors of political alignment

**Tertiary Tier (Weight: 0.7-0.8)**
- **Identity Dipole**: Cosmopolitan vs Nationalist
- **Change Dipole**: Progressive vs Conservative
  - Contextual and strategic orientations
  - Moderate influence but important for nuanced analysis

## Mathematical Model

### Coordinate System
- **Semi-major axis**: 1.0 (horizontal)
- **Semi-minor axis**: 0.8 (vertical)  
- **Scaling factor**: 0.9 (overall system scaling)

### Well Positions (Degrees)
- **Solidarity**: 180° (left, -X axis)
- **Equality**: 135° (upper left)
- **Democracy**: 90° (top, +Y axis)
- **Cosmopolitan**: 45° (upper right)  
- **Progressive**: 225° (lower left)
- **Competition**: 0° (right, +X axis)
- **Tradition**: 315° (lower right)
- **Control**: 270° (bottom, -Y axis)
- **Nationalist**: 135° (upper left, overlapping with disintegrative positioning)
- **Conservative**: 315° (lower right, overlapping with traditional positioning)

## Usage

This framework is designed for:
- **Political campaign analysis** - Mapping ideological positioning in electoral rhetoric
- **Policy document analysis** - Understanding ideological foundations of policy proposals  
- **Comparative political analysis** - Comparing political parties and movements across contexts
- **Historical political analysis** - Tracking ideological shifts over time
- **International political comparison** - Understanding different national political spectrums

## Validation

The framework has been tested on:
- Presidential campaign speeches
- Political party manifestos
- Policy white papers
- Legislative debate transcripts
- International political documents

Results show clear differentiation between left-wing and right-wing orientations, with metrics correlating with expected ideological patterns and traditional political science classifications.

## Version History

- **v2025.06.04**: Current version - Narrative Gravity Maps methodology with Political Spectrum Framework
- **v2025.01.03**: Original version with basic political spectrum analysis

## Files

- `dipoles.json`: Conceptual framework and language cues for political spectrum analysis
- `framework.json`: Mathematical implementation and well positions
- `README.md`: This documentation 