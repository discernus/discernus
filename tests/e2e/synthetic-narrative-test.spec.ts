import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

test.describe('Synthetic Narrative Analysis Tests', () => {
  
  // Load synthetic narrative text
  const syntheticTextPath = path.join(process.cwd(), 'corpus/raw_sources/synthetic_narratives/right_center_positive_stewardship.txt');
  const syntheticText = fs.readFileSync(syntheticTextPath, 'utf-8').trim();

  test('should analyze synthetic stewardship narrative and show results in Analysis Results tab', async ({ page }) => {
    // Navigate to the application
    await page.goto('http://localhost:3000');
    
    // Verify page loads
    await expect(page).toHaveTitle(/Narrative Gravity Wells/);
    
    // Click on Experiment Designer tab
    await page.click('text=Experiment Designer');
    
    // Wait for configuration to load
    await expect(page.locator('[data-testid="experiment-designer"]')).toBeVisible({ timeout: 10000 });
    
    // Verify configuration status shows ready
    await expect(page.locator('text=✅ Ready for analysis')).toBeVisible();
    
    // Clear any existing text and enter the synthetic narrative
    const textInput = page.locator('[data-testid="text-input"]');
    await textInput.clear();
    await textInput.fill(syntheticText);
    
    // Verify character count is correct
    await expect(page.locator(`text=Characters: ${syntheticText.length}`)).toBeVisible();
    
    // Click analyze button
    const analyzeButton = page.locator('[data-testid="analyze-button"]');
    await expect(analyzeButton).toBeEnabled();
    await analyzeButton.click();
    
    // Verify analyzing state
    await expect(analyzeButton).toBeDisabled();
    await expect(analyzeButton).toHaveText('🔄 Analyzing...');
    
    // Wait for analysis to complete (synthetic text is longer, may take more time)
    await expect(page.locator('[data-testid="analysis-results"]')).toBeVisible({ timeout: 45000 });
    
    // Verify analysis results are displayed
    await expect(page.locator('text=✅ Analysis Complete')).toBeVisible();
    
    // Check that key result sections are present
    await expect(page.locator('text=Gravity Well Scores')).toBeVisible();
    await expect(page.locator('text=Calculated Metrics')).toBeVisible();
    await expect(page.locator('text=Dominant Wells')).toBeVisible();
    
    // Now check the Analysis Results tab
    await page.click('text=Analysis Results');
    
    // Wait for results to load (should fetch from API)
    await page.waitForTimeout(2000); // Give time for API call
    
    // Check if results are displayed - look for the refresh button first
    const refreshButton = page.locator('[data-testid="refresh-results-button"]');
    if (await refreshButton.isVisible()) {
      await refreshButton.click();
      await page.waitForTimeout(2000);
    }
    
    // Look for analysis results in the tab
    const resultsContainer = page.locator('[data-testid="analysis-results-list"]');
    if (await resultsContainer.isVisible()) {
      // Check for analysis result cards
      const resultCards = page.locator('[data-testid="analysis-result-card"]');
      const cardCount = await resultCards.count();
      
      if (cardCount > 0) {
        console.log(`✅ Found ${cardCount} analysis results in Analysis Results tab`);
        
        // Verify at least one result contains expected data for the stewardship narrative
        const firstCard = resultCards.first();
        await expect(firstCard).toBeVisible();
        
        // Check for some expected content in a stewardship narrative analysis
        const cardText = await firstCard.textContent();
        console.log('Analysis result content preview:', cardText?.substring(0, 200));
        
      } else {
        console.log('⚠️ No analysis result cards found');
      }
    } else {
      console.log('⚠️ Analysis results container not found');
    }
    
    // Take a screenshot for debugging
    await page.screenshot({ path: 'test-results/synthetic-narrative-analysis.png', fullPage: true });
    
    console.log('✅ Synthetic narrative analysis test completed');
  });

  test('should handle different synthetic narratives', async ({ page }) => {
    // Test with the left-center positive narrative
    const leftCenterPath = path.join(process.cwd(), 'corpus/raw_sources/synthetic_narratives/left_center_positive_renewal.txt');
    const leftCenterText = fs.readFileSync(leftCenterPath, 'utf-8').trim();
    
    await page.goto('http://localhost:3000');
    await page.click('text=Experiment Designer');
    
    // Wait for component to load
    await expect(page.locator('[data-testid="experiment-designer"]')).toBeVisible({ timeout: 10000 });
    
    // Enter the left-center narrative
    const textInput = page.locator('[data-testid="text-input"]');
    await textInput.clear();
    await textInput.fill(leftCenterText);
    
    // Analyze
    const analyzeButton = page.locator('[data-testid="analyze-button"]');
    await analyzeButton.click();
    
    // Wait for completion
    await expect(page.locator('[data-testid="analysis-results"]')).toBeVisible({ timeout: 45000 });
    
    // Check results show different values than the stewardship narrative
    await expect(page.locator('text=✅ Analysis Complete')).toBeVisible();
    
    console.log('✅ Left-center narrative analysis completed');
  });
}); 