<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

## Summary Document: Why the Polar/Cartesian Hybrid is Superior, and Why Scaling Should Be Dynamic


---

### Key Insights

- The polar/Cartesian hybrid approach is mathematically and interpretively superior for narrative gravity mapping.
- Fixed scaling factors (e.g., 0.8) ensure no narrative position falls outside the boundary, but may mute differences.
- Dynamic scaling at runtime maximizes visual space and preserves analytical clarity.
- The Narrative Gravity Maps architecture is fully compatible with this enhancement.

---

## 1. Why the Polar/Cartesian Hybrid is Superior

### **A. Mathematical and Interpretive Strengths**

- **Well Positioning (Polar/Elliptical):**
    - Gravity wells (thematic poles) are placed at fixed angles around a circle or ellipse using polar or elliptical parametric equations, directly reflecting theoretical structure and symmetry[^1][^2].
    - This allows for intuitive, theory-driven arrangement of conceptual poles, supporting frameworks with any number of wells, arbitrary angular spacing, and elliptical distortion.
- **Narrative Positioning (Cartesian):**
    - The position of a narrative is calculated as the weighted center of mass (COM) of the wells, using their (x, y) coordinates and the narrative’s scores[^1][^2].
    - Cartesian averaging is mathematically straightforward, visually interpretable, and compatible with standard metrics (distance, clustering, etc.).
- **Why Not Pure Polar?**
    - Summing or averaging in polar coordinates is mathematically awkward and less intuitive for multidimensional, weighted systems.
    - Most geometric and statistical analyses (distance, clustering, etc.) are easier and more meaningful in Cartesian space[^1][^2].


### **B. System and Framework Flexibility**

- The hybrid approach supports:
    - Elliptical and circular frameworks.
    - Arbitrary well weighting and non-uniform angular spacing.
    - Extension to new frameworks without breaking compatibility or interpretive clarity[^1][^3].

---

## 2. The Limitation of Fixed Scaling

### **A. Why Scaling Is Used**

- The weighted COM can fall outside the circle/ellipse if scores are highly imbalanced.
- A fixed scaling factor (e.g., 0.8) is applied to keep all narrative positions inside the boundary[^1][^2].


### **B. Drawbacks of Fixed Scaling**

- **Muted Differences:**
All data points are proportionally shrunk toward the center, reducing the absolute spread and potentially muting distinctions between narratives, especially for those that would otherwise be near the edge[^1][^2].
- **Wasted Visual Space:**
In datasets where no narrative is near the boundary, much of the visual space remains unused.

---

## 3. Recommendation: Dynamic Scaling at Runtime

### **A. Rationale and Benefits**

- **Maximizes Use of Space:**
Dynamically scaling so the furthest narrative position just touches the boundary ensures all available visual space is utilized, making distinctions between narratives clearer.
- **Preserves Relative Differences:**
All positions are scaled by the same factor, so relative distances and analytical relationships are preserved.
- **Adapts to Data:**
Works equally well for datasets with tightly clustered or widely spread narratives.
- **Avoids Out-of-Bounds Artifacts:**
No narrative will ever be plotted outside the conceptual space, maintaining interpretive integrity.


### **B. Implementation Steps**

1. **Compute Raw Narrative Positions:**
Calculate the (x, y) positions for all narratives using the standard weighted COM formula.
2. **Determine Maximum Distance:**
For each narrative, compute its normalized distance from the center to the ellipse/circle boundary.
3. **Calculate Scaling Factor:**
Set the scaling factor to \$ min(1, 1 / max observed distance) \$, or slightly less (e.g., 0.99) for a margin.
4. **Apply Scaling:**
Multiply all narrative (x, y) positions by the scaling factor before plotting.
5. **Document Scaling:**
Store and display the scaling factor used for each visualization to ensure transparency and reproducibility.

### **C. System Compatibility**

- The Narrative Gravity Maps architecture already supports runtime framework selection and dynamic configuration[^3].
- Scaling can be implemented as:
    - A runtime parameter in the visualization module.
    - A configurable option in framework.json or as a visualization override.
    - An experimental variable in systematic methodological research.

---

## 4. Benefits of Dynamic Scaling

| Benefit | Description |
| :-- | :-- |
| Maximized Visual Spread | Ensures the most extreme narrative fills the available space, improving interpretability |
| Preserved Analytical Clarity | Maintains proportional relationships between narratives |
| Adaptability | Automatically adjusts to the distribution of each dataset |
| Transparency | Scaling factor can be logged for reproducibility and cross-dataset comparison |
| Methodological Rigor | Compatible with systematic experimental design and comparative research |


---

## 5. Conclusion

**The polar/Cartesian hybrid approach is mathematically optimal and interpretively robust for narrative gravity mapping.** Fixed scaling, while safe, can mute differences and waste visual space. **Dynamic scaling at runtime is a recommended enhancement:** it maximizes visual and analytical clarity without sacrificing rigor or compatibility. The Narrative Gravity Maps system is fully capable of supporting this improvement, and its adoption will further strengthen both research quality and practical utility[^1][^3][^2].

---

> “The computational procedures work identically across all framework implementations, ensuring mathematical consistency while supporting diverse theoretical commitments and experimental comparisons... Wells are positioned using parametric ellipse equations... Narrative positions are calculated as weighted averages of well positions... Where 0.8 scaling factor to keep narratives inside ellipse.”
> — Narrative Gravity Maps v1.3.0[^1]

---

**Implementation of dynamic scaling should be prioritized as a core upgrade for all future framework releases.**

<div style="text-align: center">⁂</div>

[^1]: narrative_gravity_maps_v1.3.0.md

[^2]: narrative_gravity_maps_v1.0.1.md

[^3]: FRAMEWORK_ARCHITECTURE.md

[^4]: if-you-were-to-develop-a-compl-5KHQ_w5ARS6NumH6P0fHvA.md

[^5]: strategic_pivot.md

[^6]: Human_Thematic_Perception_and_Computational_Replication_A_Literature_Review.md

[^7]: research_input_workflow.md

[^8]: user_journey_arc.md

[^9]: user_stories.md

[^10]: process_architecture.md

[^11]: README.md

