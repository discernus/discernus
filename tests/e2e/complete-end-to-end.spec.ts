import { test, expect } from '@playwright/test';

test.describe('Complete End-to-End Narrative Gravity Analysis', () => {
  
  test('should load configuration and perform complete text analysis workflow', async ({ page }) => {
    // Navigate to the application (check both possible ports)
    try {
      await page.goto('http://localhost:3001');
    } catch (error) {
      await page.goto('http://localhost:3000');
    }
    
    // Verify page loads
    await expect(page).toHaveTitle(/Narrative Gravity Wells/);
    
    // Click on Experiment Designer tab
    await page.click('text=Experiment Designer');
    
    // Wait for component to load (should show loading state first)
    const loadingElement = page.locator('[data-testid="experiment-designer-loading"]');
    if (await loadingElement.isVisible()) {
      await expect(loadingElement).toBeVisible();
      await expect(page.locator('text=Loading research workbench')).toBeVisible();
    }
    
    // Wait for configuration to load
    await expect(page.locator('[data-testid="experiment-designer"]')).toBeVisible({ timeout: 10000 });
    
    // NEW WORKFLOW: Should start on Experiment Design tab
    await expect(page.locator('text=🧪 Experiment Design')).toBeVisible();
    
    // STEP 1: Create experiment configuration
    await page.fill('[data-testid="experiment-name"]', 'Test E2E Analysis');
    await page.fill('[data-testid="experiment-hypothesis"]', 'This text should show positive civic virtue themes');
    
    // Verify configuration dropdowns are populated
    const frameworkSelect = page.locator('[data-testid="framework-select"]');
    const promptSelect = page.locator('[data-testid="prompt-select"]');
    const algorithmSelect = page.locator('[data-testid="algorithm-select"]');
    
    // Check that dropdowns have options (should auto-select first option)
    await expect(frameworkSelect).not.toHaveValue('');
    await expect(promptSelect).not.toHaveValue('');
    await expect(algorithmSelect).not.toHaveValue('');
    
    // Verify configuration counts are displayed
    await expect(page.locator('text=available')).toBeVisible(); // Should see "X available" for frameworks/prompts/algorithms
    
    // Check that configuration status shows ready to create experiment
    await expect(page.locator('text=✅ Ready to create experiment')).toBeVisible();
    
    // Create the experiment
    const createButton = page.locator('[data-testid="create-experiment-button"]');
    await expect(createButton).toBeEnabled();
    await createButton.click();
    
    // Should automatically switch to Text Analysis tab
    await expect(page.locator('text=📝 Text Analysis')).toBeVisible();
    await expect(page.locator('text=🎯 Current Experiment Configuration')).toBeVisible();
    
    // STEP 2: Enter text for analysis
    const testText = 'Democracy requires active participation from all citizens to build a just and hopeful society where truth and dignity prevail over manipulation and fear.';
    await page.fill('[data-testid="text-input"]', testText);
    
    // Verify character and word count updates
    await expect(page.locator(`text=Characters: ${testText.length}`)).toBeVisible();
    const wordCount = testText.split(/\s+/).filter(w => w.length > 0).length;
    await expect(page.locator(`text=Words: ${wordCount}`)).toBeVisible();
    
    // Verify analyze button is enabled
    const analyzeButton = page.locator('[data-testid="analyze-button"]');
    await expect(analyzeButton).toBeEnabled();
    await expect(analyzeButton).toHaveText('🚀 Analyze Text');
    
    // STEP 3: Run analysis
    await analyzeButton.click();
    
    // Verify analyzing state
    await expect(analyzeButton).toBeDisabled();
    await expect(analyzeButton).toHaveText('🔄 Analyzing...');
    
    // Should automatically switch to Results tab when complete
    await expect(page.locator('text=📊 Results & Insights')).toBeVisible({ timeout: 30000 });
    
    // Wait for analysis to complete
    await expect(page.locator('[data-testid="analysis-results"]')).toBeVisible({ timeout: 30000 });
    
    // Verify analysis results are displayed
    await expect(page.locator('text=✅ Analysis Complete')).toBeVisible();
    
    // Check that key result sections are present
    await expect(page.locator('text=Gravity Well Scores')).toBeVisible();
    await expect(page.locator('text=Calculated Metrics')).toBeVisible();
    await expect(page.locator('text=Dominant Wells')).toBeVisible();
    
    // Verify specific metrics are displayed
    await expect(page.locator('text=Narrative Elevation:')).toBeVisible();
    await expect(page.locator('text=Polarity:')).toBeVisible();
    await expect(page.locator('text=Coherence:')).toBeVisible();
    await expect(page.locator('text=Directional Purity:')).toBeVisible();
    
    // Verify execution details
    await expect(page.locator('text=Model:')).toBeVisible();
    await expect(page.locator('text=Framework:')).toBeVisible();
    await expect(page.locator('text=Execution Time:')).toBeVisible();
    await expect(page.locator('text=API Cost:')).toBeVisible();
    
    // Take a screenshot of the complete results
    await page.screenshot({ path: 'test-results/complete-analysis-results.png' });
    
    console.log('✅ Complete end-to-end workflow validated successfully');
  });

  test('should handle different framework configurations', async ({ page }) => {
    // Navigate to the application
    try {
      await page.goto('http://localhost:3001');
    } catch (error) {
      await page.goto('http://localhost:3000');
    }
    
    await page.click('text=Experiment Designer');
    
    // Wait for component to load
    await expect(page.locator('[data-testid="experiment-designer"]')).toBeVisible({ timeout: 10000 });
    
    // Should be on Experiment Design tab
    await expect(page.locator('text=🧪 Experiment Design')).toBeVisible();
    
    // Test framework selection
    const frameworkSelect = page.locator('[data-testid="framework-select"]');
    const frameworkOptions = await frameworkSelect.locator('option').allTextContents();
    
    // Should have at least 3 framework options (plus the default)
    expect(frameworkOptions.length).toBeGreaterThan(2);
    
    // Test different framework selections
    for (let i = 1; i < Math.min(frameworkOptions.length, 4); i++) {
      await frameworkSelect.selectOption({ index: i });
      // Verify selection took effect
      const selectedValue = await frameworkSelect.inputValue();
      expect(selectedValue).not.toBe('');
    }
    
    console.log('✅ Framework configuration testing completed');
  });

  test('should validate experiment creation requirements', async ({ page }) => {
    // Navigate to the application
    try {
      await page.goto('http://localhost:3001');
    } catch (error) {
      await page.goto('http://localhost:3000');
    }
    
    await page.click('text=Experiment Designer');
    
    // Wait for component to load
    await expect(page.locator('[data-testid="experiment-designer"]')).toBeVisible({ timeout: 10000 });
    
    // Should be on Experiment Design tab
    await expect(page.locator('text=🧪 Experiment Design')).toBeVisible();
    
    // Verify create experiment button is disabled without experiment name
    const createButton = page.locator('[data-testid="create-experiment-button"]');
    await expect(createButton).toBeDisabled();
    
    // Add experiment name
    await page.fill('[data-testid="experiment-name"]', 'Test Experiment');
    
    // Verify create experiment button is now enabled (assuming auto-selected configs)
    await expect(createButton).toBeEnabled();
    
    console.log('✅ Experiment validation testing completed');
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // This test assumes the API might be down or return errors
    try {
      await page.goto('http://localhost:3001');
    } catch (error) {
      await page.goto('http://localhost:3000');
    }
    
    await page.click('text=Experiment Designer');
    
    // Wait a reasonable time for loading
    await page.waitForTimeout(5000);
    
    // Check if error state is displayed (if API is down)
    const errorElement = page.locator('[data-testid="experiment-designer-error"]');
    const successElement = page.locator('[data-testid="experiment-designer"]');
    
    if (await errorElement.isVisible()) {
      // API is down - verify error handling
      await expect(page.locator('text=Configuration Error:')).toBeVisible();
      await expect(page.locator('text=Make sure the API server is running')).toBeVisible();
      console.log('✅ API error handling validated');
    } else {
      // API is up - this is the expected case
      await expect(successElement).toBeVisible();
      await expect(page.locator('text=🧪 Experiment Design')).toBeVisible();
      console.log('✅ API is operational - normal flow validated');
    }
  });

  test('should support multi-model comparison mode', async ({ page }) => {
    // Navigate to the application
    try {
      await page.goto('http://localhost:3001');
    } catch (error) {
      await page.goto('http://localhost:3000');
    }
    
    await page.click('text=Experiment Designer');
    
    // Wait for component to load
    await expect(page.locator('[data-testid="experiment-designer"]')).toBeVisible({ timeout: 10000 });
    
    // Switch to multi-model mode
    const analysisModeSelect = page.locator('[data-testid="analysis-mode-select"]');
    await analysisModeSelect.selectOption('multi_model_comparison');
    
    // Verify multi-model configuration appears
    await expect(page.locator('text=Models for Comparison:')).toBeVisible();
    
    // Select some models
    await page.check('input[type="checkbox"][value="gpt-4.1"]');
    await page.check('input[type="checkbox"][value="claude-4-sonnet"]');
    
    // Create experiment
    await page.fill('[data-testid="experiment-name"]', 'Multi-Model Test');
    const createButton = page.locator('[data-testid="create-experiment-button"]');
    await createButton.click();
    
    // Should switch to text tab
    await expect(page.locator('text=📝 Text Analysis')).toBeVisible();
    await expect(page.locator('text=Multi-Model Comparison')).toBeVisible();
    
    console.log('✅ Multi-model comparison mode validated');
  });

}); 