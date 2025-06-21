
# Figma Spec — Discernus Visual Analytics

## Canvas: Elliptical Gravity Map
- Ellipse Diameter: 600px
- Pole Dots: 10 evenly spaced on perimeter
  - Label Position: Radial offset 25px outward
  - Label Font: Bold, 12pt, gray/black
- Score Rays:
  - Stroke: 2px dashed
  - Color: #3399ff (with 60% opacity)
- Narrative Center:
  - Circle: 12px radius
  - Fill: #ff9933 with subtle glow
  - Tooltip on hover: coordinates, coherence, purity
- Contradiction Ribbon:
  - Red arc overlay connecting opposing poles if contradiction_index > 0.5

## Bar Chart: Integrative vs Disintegrative
- Two groups:
  - Left: Green wells (Dignity, Hope, etc.)
  - Right: Red wells (Fear, Tribalism, etc.)
- Bar Width: 40px, Spacing: 20px
- Error Bars: ±1σ, capped lines
- Label Below Bar: Well name and exact score

## Correlation Grid
- Grid Cell: 80x80px
- Fill: Gradient (blue-red), intensity = Pearson r
- Diagonal Labels: Human ↔ Model
- Tooltip: “Model X vs Human on [Well]: r = 0.82”

## Export / Embeds
- Button set: [Download SVG], [Download PNG], [Copy Markdown Card]
- Accessibility: Colorblind-safe palette toggle

## Prototype Notes
- Link visuals to side panel summary dynamically
- Group per-speech dashboards in carousel or tab mode
