# Test info

- Name: Complete End-to-End Narrative Gravity Analysis >> should validate experiment creation requirements
- Location: /Users/jeffwhatcott/narrative_gravity_analysis/tests/e2e/complete-end-to-end.spec.ts:148:7

# Error details

```
Error: Timed out 5000ms waiting for expect(locator).toBeEnabled()

Locator: locator('[data-testid="create-experiment-button"]')
Expected: enabled
Received: disabled
Call log:
  - expect.toBeEnabled with timeout 5000ms
  - waiting for locator('[data-testid="create-experiment-button"]')
    9 × locator resolved to <button disabled data-testid="create-experiment-button" class="px-6 py-3 rounded-md font-semibold bg-gray-300 text-gray-500 cursor-not-allowed">💾 Save Experiment Configuration</button>
      - unexpected value "disabled"

    at /Users/jeffwhatcott/narrative_gravity_analysis/tests/e2e/complete-end-to-end.spec.ts:172:32
```

# Page snapshot

```yaml
- banner:
  - text: NG
  - heading "Narrative Gravity Research Workbench" [level=1]
  - paragraph: v2.1 Phase 1 Research Workbench
  - text: Stable
- navigation:
  - button "🧪Experiment Designer"
  - button "✏️Prompt Editor"
  - button "📊Analysis Results"
  - button "⚖️Compare Experiments"
- main:
  - heading "🧪 Research Workbench - Experiment Designer" [level=2]
  - navigation:
    - button "🧪 Experiment Design Configure hypothesis & methods"
    - button "📝 Text Analysis Run analysis on your experiment"
    - button "📊 Results & Insights View and interpret findings"
  - heading "🎯 Unified Experiment Design" [level=3]
  - text: Experiment Name *
  - textbox "e.g., Hierarchical Prompting vs Standard Analysis": Test Experiment
  - text: Research Hypothesis
  - textbox "State your hypothesis about what this configuration will reveal about narrative themes..."
  - heading "📋 Experimental Configuration" [level=3]
  - text: Framework Configuration (3 available)
  - combobox:
    - option "Select Framework..." [selected]
    - option "Civic Virtue (v2025.06.04)"
    - option "Political Spectrum (v2025.06.04)"
    - option "Moral-Rhetorical Posture (v2025.06.04)"
  - text: Prompt Template (2 available)
  - combobox:
    - option "Select Prompt..." [selected]
    - option "Hierarchical Prompt v1.0 (1.0)"
    - option "Traditional Prompt v1.0 (1.0)"
  - text: Scoring Algorithm (5 store + 4 API)
  - combobox:
    - option "Select Algorithm..." [selected]
    - option "Linear Average - Standard linear averaging approach"
    - option "Winner-Take-Most - Amplifies dominant wells while suppressing weaker ones - implements nonlinear weighting for clearer hierarchy"
    - option "Exponential Weighting - Exponential weighting that squares differences to enhance thematic distinction"
    - option "Hierarchical Dominance - Uses LLM-provided hierarchical rankings and relative weights for positioning - implements \"edge snapping\" for single-well dominance"
    - option "Nonlinear Transform - Applies nonlinear transforms to exaggerate differences near poles and compress center values"
  - text: Analysis Mode
  - combobox:
    - option "Single Model Analysis" [selected]
    - option "Multi-Model Comparison (Stability Assessment)"
  - strong: "Configuration Status:"
  - text: ⚠️ Please complete all required fields
  - button "💾 Save Experiment Configuration" [disabled]
  - text: 0 experiments created in this session
- text: "✅ v2.1 Phase 1 Active Active Tab: designer Features: Hierarchical prompts, Multi-model comparison, Nonlinear scoring Build: 10:57:28 AM"
- button "🐛 Debug"
```

# Test source

```ts
   72 |     await expect(analyzeButton).toBeEnabled();
   73 |     await expect(analyzeButton).toHaveText('🚀 Analyze Text');
   74 |     
   75 |     // STEP 3: Run analysis
   76 |     await analyzeButton.click();
   77 |     
   78 |     // Verify analyzing state
   79 |     await expect(analyzeButton).toBeDisabled();
   80 |     await expect(analyzeButton).toHaveText('🔄 Analyzing...');
   81 |     
   82 |     // Should automatically switch to Results tab when complete
   83 |     await expect(page.locator('text=📊 Results & Insights')).toBeVisible({ timeout: 30000 });
   84 |     
   85 |     // Wait for analysis to complete
   86 |     await expect(page.locator('[data-testid="analysis-results"]')).toBeVisible({ timeout: 30000 });
   87 |     
   88 |     // Verify analysis results are displayed
   89 |     await expect(page.locator('text=✅ Analysis Complete')).toBeVisible();
   90 |     
   91 |     // Check that key result sections are present
   92 |     await expect(page.locator('text=Gravity Well Scores')).toBeVisible();
   93 |     await expect(page.locator('text=Calculated Metrics')).toBeVisible();
   94 |     await expect(page.locator('text=Dominant Wells')).toBeVisible();
   95 |     
   96 |     // Verify specific metrics are displayed
   97 |     await expect(page.locator('text=Narrative Elevation:')).toBeVisible();
   98 |     await expect(page.locator('text=Polarity:')).toBeVisible();
   99 |     await expect(page.locator('text=Coherence:')).toBeVisible();
  100 |     await expect(page.locator('text=Directional Purity:')).toBeVisible();
  101 |     
  102 |     // Verify execution details
  103 |     await expect(page.locator('text=Model:')).toBeVisible();
  104 |     await expect(page.locator('text=Framework:')).toBeVisible();
  105 |     await expect(page.locator('text=Execution Time:')).toBeVisible();
  106 |     await expect(page.locator('text=API Cost:')).toBeVisible();
  107 |     
  108 |     // Take a screenshot of the complete results
  109 |     await page.screenshot({ path: 'test-results/complete-analysis-results.png' });
  110 |     
  111 |     console.log('✅ Complete end-to-end workflow validated successfully');
  112 |   });
  113 |
  114 |   test('should handle different framework configurations', async ({ page }) => {
  115 |     // Navigate to the application
  116 |     try {
  117 |       await page.goto('http://localhost:3001');
  118 |     } catch (error) {
  119 |       await page.goto('http://localhost:3000');
  120 |     }
  121 |     
  122 |     await page.click('text=Experiment Designer');
  123 |     
  124 |     // Wait for component to load
  125 |     await expect(page.locator('[data-testid="experiment-designer"]')).toBeVisible({ timeout: 10000 });
  126 |     
  127 |     // Should be on Experiment Design tab
  128 |     await expect(page.locator('text=🧪 Experiment Design')).toBeVisible();
  129 |     
  130 |     // Test framework selection
  131 |     const frameworkSelect = page.locator('[data-testid="framework-select"]');
  132 |     const frameworkOptions = await frameworkSelect.locator('option').allTextContents();
  133 |     
  134 |     // Should have at least 3 framework options (plus the default)
  135 |     expect(frameworkOptions.length).toBeGreaterThan(2);
  136 |     
  137 |     // Test different framework selections
  138 |     for (let i = 1; i < Math.min(frameworkOptions.length, 4); i++) {
  139 |       await frameworkSelect.selectOption({ index: i });
  140 |       // Verify selection took effect
  141 |       const selectedValue = await frameworkSelect.inputValue();
  142 |       expect(selectedValue).not.toBe('');
  143 |     }
  144 |     
  145 |     console.log('✅ Framework configuration testing completed');
  146 |   });
  147 |
  148 |   test('should validate experiment creation requirements', async ({ page }) => {
  149 |     // Navigate to the application
  150 |     try {
  151 |       await page.goto('http://localhost:3001');
  152 |     } catch (error) {
  153 |       await page.goto('http://localhost:3000');
  154 |     }
  155 |     
  156 |     await page.click('text=Experiment Designer');
  157 |     
  158 |     // Wait for component to load
  159 |     await expect(page.locator('[data-testid="experiment-designer"]')).toBeVisible({ timeout: 10000 });
  160 |     
  161 |     // Should be on Experiment Design tab
  162 |     await expect(page.locator('text=🧪 Experiment Design')).toBeVisible();
  163 |     
  164 |     // Verify create experiment button is disabled without experiment name
  165 |     const createButton = page.locator('[data-testid="create-experiment-button"]');
  166 |     await expect(createButton).toBeDisabled();
  167 |     
  168 |     // Add experiment name
  169 |     await page.fill('[data-testid="experiment-name"]', 'Test Experiment');
  170 |     
  171 |     // Verify create experiment button is now enabled (assuming auto-selected configs)
> 172 |     await expect(createButton).toBeEnabled();
      |                                ^ Error: Timed out 5000ms waiting for expect(locator).toBeEnabled()
  173 |     
  174 |     console.log('✅ Experiment validation testing completed');
  175 |   });
  176 |
  177 |   test('should handle API errors gracefully', async ({ page }) => {
  178 |     // This test assumes the API might be down or return errors
  179 |     try {
  180 |       await page.goto('http://localhost:3001');
  181 |     } catch (error) {
  182 |       await page.goto('http://localhost:3000');
  183 |     }
  184 |     
  185 |     await page.click('text=Experiment Designer');
  186 |     
  187 |     // Wait a reasonable time for loading
  188 |     await page.waitForTimeout(5000);
  189 |     
  190 |     // Check if error state is displayed (if API is down)
  191 |     const errorElement = page.locator('[data-testid="experiment-designer-error"]');
  192 |     const successElement = page.locator('[data-testid="experiment-designer"]');
  193 |     
  194 |     if (await errorElement.isVisible()) {
  195 |       // API is down - verify error handling
  196 |       await expect(page.locator('text=Configuration Error:')).toBeVisible();
  197 |       await expect(page.locator('text=Make sure the API server is running')).toBeVisible();
  198 |       console.log('✅ API error handling validated');
  199 |     } else {
  200 |       // API is up - this is the expected case
  201 |       await expect(successElement).toBeVisible();
  202 |       await expect(page.locator('text=🧪 Experiment Design')).toBeVisible();
  203 |       console.log('✅ API is operational - normal flow validated');
  204 |     }
  205 |   });
  206 |
  207 |   test('should support multi-model comparison mode', async ({ page }) => {
  208 |     // Navigate to the application
  209 |     try {
  210 |       await page.goto('http://localhost:3001');
  211 |     } catch (error) {
  212 |       await page.goto('http://localhost:3000');
  213 |     }
  214 |     
  215 |     await page.click('text=Experiment Designer');
  216 |     
  217 |     // Wait for component to load
  218 |     await expect(page.locator('[data-testid="experiment-designer"]')).toBeVisible({ timeout: 10000 });
  219 |     
  220 |     // Switch to multi-model mode
  221 |     const analysisModeSelect = page.locator('[data-testid="analysis-mode-select"]');
  222 |     await analysisModeSelect.selectOption('multi_model_comparison');
  223 |     
  224 |     // Verify multi-model configuration appears
  225 |     await expect(page.locator('text=Models for Comparison:')).toBeVisible();
  226 |     
  227 |     // Select some models
  228 |     await page.check('input[type="checkbox"][value="gpt-4.1"]');
  229 |     await page.check('input[type="checkbox"][value="claude-4-sonnet"]');
  230 |     
  231 |     // Create experiment
  232 |     await page.fill('[data-testid="experiment-name"]', 'Multi-Model Test');
  233 |     const createButton = page.locator('[data-testid="create-experiment-button"]');
  234 |     await createButton.click();
  235 |     
  236 |     // Should switch to text tab
  237 |     await expect(page.locator('text=📝 Text Analysis')).toBeVisible();
  238 |     await expect(page.locator('text=Multi-Model Comparison')).toBeVisible();
  239 |     
  240 |     console.log('✅ Multi-model comparison mode validated');
  241 |   });
  242 |
  243 | }); 
```