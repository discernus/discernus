import { test, expect } from '@playwright/test';

test.describe('Complete End-to-End Narrative Gravity Analysis', () => {
  
  test('should load configuration and perform complete text analysis workflow', async ({ page }) => {
    // Navigate to the application
    await page.goto('http://localhost:3000');
    
    // Verify page loads
    await expect(page).toHaveTitle(/Narrative Gravity Wells/);
    
    // Click on Experiment Designer tab
    await page.click('text=Experiment Designer');
    
    // Wait for component to load (should show loading state first)
    const loadingElement = page.locator('[data-testid="experiment-designer-loading"]');
    if (await loadingElement.isVisible()) {
      await expect(loadingElement).toBeVisible();
      await expect(page.locator('text=Loading configuration')).toBeVisible();
    }
    
    // Wait for configuration to load
    await expect(page.locator('[data-testid="experiment-designer"]')).toBeVisible({ timeout: 10000 });
    
    // Verify configuration dropdowns are populated
    const frameworkSelect = page.locator('[data-testid="framework-select"]');
    const promptSelect = page.locator('[data-testid="prompt-select"]');
    const algorithmSelect = page.locator('[data-testid="algorithm-select"]');
    
    // Check that dropdowns have options (should auto-select first option)
    await expect(frameworkSelect).not.toHaveValue('');
    await expect(promptSelect).not.toHaveValue('');
    await expect(algorithmSelect).not.toHaveValue('');
    
    // Verify configuration counts are displayed
    await expect(page.locator('text=3 available')).toBeVisible(); // frameworks
    await expect(page.locator('text=4 available')).toBeVisible(); // prompts or algorithms
    
    // Check that configuration status shows ready
    await expect(page.locator('text=✅ Ready for analysis')).toBeVisible();
    
    // Enter text for analysis
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
    
    // Click analyze button
    await analyzeButton.click();
    
    // Verify analyzing state
    await expect(analyzeButton).toBeDisabled();
    await expect(analyzeButton).toHaveText('🔄 Analyzing...');
    
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
    
    // Verify analyze button is re-enabled after completion
    await expect(analyzeButton).toBeEnabled();
    await expect(analyzeButton).toHaveText('🚀 Analyze Text');
    
    // Take a screenshot of the complete results
    await page.screenshot({ path: 'test-results/complete-analysis-results.png' });
    
    console.log('✅ Complete end-to-end workflow validated successfully');
  });

  test('should handle different framework configurations', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('text=Experiment Designer');
    
    // Wait for component to load
    await expect(page.locator('[data-testid="experiment-designer"]')).toBeVisible({ timeout: 10000 });
    
    // Test framework selection
    const frameworkSelect = page.locator('[data-testid="framework-select"]');
    const frameworkOptions = await frameworkSelect.locator('option').allTextContents();
    
    // Should have at least 3 framework options (plus the default)
    expect(frameworkOptions.length).toBeGreaterThan(3);
    
    // Test different framework selections
    for (let i = 1; i < Math.min(frameworkOptions.length, 4); i++) {
      await frameworkSelect.selectOption({ index: i });
      // Verify selection took effect
      const selectedValue = await frameworkSelect.inputValue();
      expect(selectedValue).not.toBe('');
    }
    
    console.log('✅ Framework configuration testing completed');
  });

  test('should validate input requirements', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('text=Experiment Designer');
    
    // Wait for component to load
    await expect(page.locator('[data-testid="experiment-designer"]')).toBeVisible({ timeout: 10000 });
    
    // Clear the text input
    await page.fill('[data-testid="text-input"]', '');
    
    // Verify analyze button is disabled with empty text
    const analyzeButton = page.locator('[data-testid="analyze-button"]');
    await expect(analyzeButton).toBeDisabled();
    
    // Add some text
    await page.fill('[data-testid="text-input"]', 'Short test text');
    
    // Verify analyze button is now enabled
    await expect(analyzeButton).toBeEnabled();
    
    console.log('✅ Input validation testing completed');
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // This test assumes the API might be down or return errors
    await page.goto('http://localhost:3000');
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
      console.log('✅ API is operational - normal flow validated');
    }
  });

  test('should verify data persistence through multiple analyses', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('text=Experiment Designer');
    
    // Wait for component to load
    await expect(page.locator('[data-testid="experiment-designer"]')).toBeVisible({ timeout: 10000 });
    
    // Perform first analysis
    await page.fill('[data-testid="text-input"]', 'First analysis: Building hope and dignity in our communities.');
    await page.click('[data-testid="analyze-button"]');
    await expect(page.locator('[data-testid="analysis-results"]')).toBeVisible({ timeout: 30000 });
    
    const firstResults = await page.locator('[data-testid="analysis-results"]').textContent();
    
    // Perform second analysis with different text
    await page.fill('[data-testid="text-input"]', 'Second analysis: Fear and manipulation undermine democratic values.');
    await page.click('[data-testid="analyze-button"]');
    await expect(page.locator('[data-testid="analysis-results"]')).toBeVisible({ timeout: 30000 });
    
    const secondResults = await page.locator('[data-testid="analysis-results"]').textContent();
    
    // Verify results are different (indicating proper analysis)
    expect(firstResults).not.toBe(secondResults);
    
    console.log('✅ Multiple analysis workflow validated');
  });

}); 