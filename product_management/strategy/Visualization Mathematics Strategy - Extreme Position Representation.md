#Visualization Mathematics Strategy - Extreme Position Representation

11 June 2025


## Situation Analysis: Mathematical Compression Problem

### **Current Implementation Architecture**

The narrative positioning system calculates center-of-mass as a weighted average of all ten well vectors, applies tier-based moral weighting (positive for integrative, negative for disintegrative), then scales by factor 0.8 to ensure all points remain inside the ellipse boundary.

### **Mathematical Root Causes of Compression**

**Averaging Effect**: Even with perfect 1.0/0.0 scores, weighted averaging inherently pulls positions toward the geometric center. A narrative with Dignity=1.0, all others=0.0 still plots at 80% of the way toward the Dignity well, not at the boundary.

**Conservative Scaling**: The 0.8 scaling factor was chosen to guarantee all points remain inside the ellipse, but this systematically compresses the representable space and makes even maximal narratives appear moderate.

**Linear Weighting Assumptions**: Current implementation treats the relationship between well scores and positional pull as linear, but human perception of dominance may be exponential—small differences between high scores feel much more significant than identical differences between low scores.

### **Empirical Evidence of Failure**

**Synthetic Validation**: Perfect positive/negative narratives with engineered 0.9/0.1 score distributions still cluster within 40% of ellipse center rather than approaching boundaries.

**Visual User Experience**: Even domain experts report that maximally different narratives "look similar" in the current visualization, undermining interpretive confidence.

**Distance Metrics**: Calculated elliptical distances between extreme cases (0.816) are mathematically significant but visually imperceptible due to compression.

### **Perceptual Psychology Considerations**

Human visual processing treats distance differences near boundaries as more salient than identical differences near centers. The current linear mapping fights against this psychological reality, making genuine moral distinctions appear trivial.

## Mathematical Redesign Strategy

### **Approach 1: Nonlinear Dominance Amplification**

**Core Concept**: Apply exponential weighting to well scores before position calculation, amplifying differences between high scores while suppressing low scores.

**Implementation**:

```python
def exponential_weighting(score, base=2.5):
    """Convert 0.0-1.0 scores to exponentially weighted influence"""
    if score < 0.1:
        return 0.0  # Suppress noise
    return math.pow(score, base)

def calculate_nonlinear_position(well_scores, well_positions):
    weighted_positions = []
    for score, position in zip(well_scores, well_positions):
        weight = exponential_weighting(score)
        weighted_positions.append(weight * position)
    return normalize(sum(weighted_positions))
```

**Expected Behavior**: Narratives with single dominant theme (0.8+ score) will approach within 90% of boundary well position. Balanced narratives will remain near center as intended.

### **Approach 2: Adaptive Dynamic Scaling**

**Core Concept**: Adjust scaling factor based on the extremeness of the score distribution rather than using fixed 0.8 scaling.

**Implementation**:

```python
def adaptive_scaling_factor(well_scores):
    """Calculate scaling based on score extremeness"""
    max_score = max(well_scores)
    score_variance = np.var(well_scores)
    
    # High max score + high variance = very focused narrative
    extremeness = max_score * score_variance
    
    # Scale from 0.6 (very diffuse) to 0.95 (very focused)
    return 0.6 + (0.35 * min(extremeness / 0.3, 1.0))
```

**Expected Behavior**: Diffuse narratives maintain current compression for clarity, while focused narratives expand toward boundaries for visual salience.

### **Approach 3: Boundary Snapping with Hybrid Logic**

**Core Concept**: When narratives exceed dominance thresholds, allow position to "snap" toward the dominant well while maintaining mathematical rigor.

**Implementation**:

```python
def boundary_snapping_position(well_scores, well_positions, snap_threshold=0.8):
    """Snap to boundary when single well dominates"""
    max_score = max(well_scores)
    max_index = well_scores.index(max_score)
    
    if max_score >= snap_threshold:
        # Calculate how close to boundary based on dominance
        boundary_proximity = (max_score - snap_threshold) / (1.0 - snap_threshold)
        snap_position = 0.7 + (0.25 * boundary_proximity)  # Range: 0.7 to 0.95
        
        # Blend snapped position with calculated center-of-mass
        calculated_position = standard_weighted_average(well_scores, well_positions)
        return blend_positions(calculated_position, well_positions[max_index] * snap_position, boundary_proximity)
    
    return standard_weighted_average(well_scores, well_positions)
```


### **Approach 4: Multi-Modal Visualization**

**Core Concept**: Supplement elliptical positioning with additional visual encoding that makes dominance hierarchy unmistakable.

**Visual Elements**:

- **Vector Thickness**: Lines from center to wells scaled by relative weights
- **Color Intensity**: Wells colored by dominance (dominant=bright, minor=faded)
- **Radial Distance Rings**: Concentric circles showing distance from center
- **Dominance Labels**: Text annotations for wells exceeding significance thresholds


## Implementation Gameplan

### **Week 1: Mathematical Prototyping**

**Days 1-2: Algorithm Development**

- Implement all four approaches as separate functions
- Create A/B testing framework for visual comparison
- Establish synthetic test cases for systematic evaluation

**Days 3-4: Synthetic Validation**

- Apply each approach to synthetic extreme narratives
- Measure visual separation between positive/negative cases
- Document mathematical properties and edge case behavior

**Days 5-7: User Experience Testing**

- Generate comparison visualizations showing current vs. enhanced approaches
- Conduct informal feedback sessions with domain experts
- Identify most promising mathematical approach


### **Week 2: Integration and Optimization**

**Days 1-3: Best Approach Selection**

- Quantitative analysis of which approach best separates extreme cases
- Qualitative assessment of interpretability and user feedback
- Decision on primary algorithm with fallback options

**Days 4-5: System Integration**

- Integrate chosen approach into existing visualization pipeline
- Ensure backward compatibility with current analysis workflows
- Test integration with improved prompting from Track 1

**Days 6-7: Performance Optimization**

- Optimize computational efficiency for real-time visualization
- Implement caching for complex calculations
- Validate system performance with batch processing


### **Week 3: Validation and Documentation**

**Days 1-3: Comprehensive Testing**

- Apply enhanced visualization to full golden set corpus
- Validate that extreme cases now achieve visual extremeness
- Confirm that moderate cases maintain appropriate center positioning

**Days 4-5: Cross-Framework Validation**

- Test mathematical approaches with multiple framework configurations
- Ensure approaches generalize beyond Civic Virtue wells
- Document any framework-specific calibrations needed

**Days 6-7: Documentation and Handoff**

- Complete technical documentation of mathematical approaches
- Create user guides for interpreting enhanced visualizations
- Prepare training materials for human validation studies


### **Success Criteria and Validation Metrics**

**Primary Success Metrics**:

- Synthetic extreme narratives plot within 85%+ of boundary distance
- Visual separation between extreme positive/negative cases increases by 200%+
- User feedback confirms enhanced interpretability
- Mathematical properties remain stable across diverse narrative types

**Secondary Validation Targets**:

- Computational performance maintains real-time responsiveness
- Enhanced visualization integrates seamlessly with prompt improvements
- Multiple framework types benefit from mathematical enhancements
- System maintains backward compatibility for comparative analysis

**Quality Assurance Checkpoints**:

- Mathematical correctness validated through unit testing
- Visual consistency confirmed across different narrative lengths and types
- User experience improvements documented through systematic feedback
- Integration stability confirmed through stress testing

**Exit Criteria for Human Validation Readiness**:

- Extreme cases achieve visually obvious boundary positioning
- Mathematical implementation is stable and well-documented
- Integration with hierarchical prompting produces cohesive results
- User interface and interpretation guides are complete

Both tracks converge at the human validation phase, where improved prompting should surface clearer thematic hierarchies, and enhanced visualization should make those hierarchies visually unmistakable to human evaluators.

