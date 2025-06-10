import { test, expect } from '@playwright/test';

// Test configuration
const FRONTEND_URL = 'http://localhost:3000';
const API_URL = 'http://localhost:8000';
const TEST_TEXT = `
In these challenging times, we must choose between hope and despair, between unity and division. 
Our democracy depends on the active participation of all citizens. We have the power to build 
a more just and equitable society for everyone. The path forward requires courage, truth, and 
a commitment to justice. We cannot allow fear and manipulation to divide us. Instead, we must 
embrace our shared dignity and work together toward a better future for all.
`;

test.describe('UI-Driven End-to-End Test', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the frontend
    await page.goto(FRONTEND_URL);
    
    // Wait for the app to load
    await expect(page.locator('h1, h2').first()).toContainText('Narrative Gravity Wells');
  });

  test('Complete experiment workflow through UI', async ({ page }) => {
    console.log('🚀 Starting UI-driven end-to-end test...');

    // Step 1: Configure the experiment in the UI
    console.log('📋 Step 1: Configuring experiment...');
    
    // Select prompt template
    await page.locator('select').filter({ hasText: 'Select Template' }).first().selectOption('civic_virtue_v2_1');
    await expect(page.locator('select').first()).not.toHaveValue('');
    console.log('   ✅ Selected prompt template');

    // Select framework configuration
    await page.locator('select').nth(1).selectOption('civic_virtue');
    await expect(page.locator('select').nth(1)).not.toHaveValue('');
    console.log('   ✅ Selected framework configuration');

    // Select scoring algorithm
    await page.locator('select').nth(2).selectOption('hierarchical_v2_1');
    await expect(page.locator('select').nth(2)).not.toHaveValue('');
    console.log('   ✅ Selected scoring algorithm');

    // Step 2: Enter text for analysis
    console.log('📝 Step 2: Entering text for analysis...');
    
    const textArea = page.locator('textarea').first();
    await textArea.fill(TEST_TEXT);
    await expect(textArea).toHaveValue(TEST_TEXT);
    console.log('   ✅ Entered test text');

    // Step 3: Run the analysis
    console.log('🔍 Step 3: Running analysis...');
    
    const runButton = page.locator('button').filter({ hasText: /Run Analysis|Analyze/ }).first();
    await runButton.click();
    console.log('   ✅ Clicked run analysis button');

    // Wait for analysis to complete (look for success message or results)
    await expect(page.locator('text=Analysis complete')).toBeVisible({ timeout: 30000 });
    console.log('   ✅ Analysis completed successfully');

    // Step 4: Navigate to Analysis Results tab
    console.log('📊 Step 4: Viewing analysis results...');
    
    const resultsTab = page.locator('button, a').filter({ hasText: /Analysis Results|Results/ }).first();
    await resultsTab.click();
    console.log('   ✅ Navigated to Analysis Results tab');

    // Step 5: Verify results are displayed in the UI
    console.log('🔍 Step 5: Verifying results in UI...');
    
    // Check for analysis result cards
    await expect(page.locator('text=Analysis Result #')).toBeVisible({ timeout: 10000 });
    console.log('   ✅ Analysis results are displayed');

    // Check for well scores
    const wellScores = page.locator('[class*="well"], [class*="score"]').first();
    await expect(wellScores).toBeVisible();
    console.log('   ✅ Well scores are visible');

    // Check for calculated metrics
    await expect(page.locator('text=Elevation')).toBeVisible();
    await expect(page.locator('text=Polarity')).toBeVisible();
    await expect(page.locator('text=Coherence')).toBeVisible();
    console.log('   ✅ Calculated metrics are displayed');

    // Step 6: Verify data in database via API
    console.log('🗄️  Step 6: Verifying data in database...');
    
    // Get experiments from API
    const apiResponse = await page.request.get(`${API_URL}/api/experiments`);
    expect(apiResponse.ok()).toBeTruthy();
    const experiments = await apiResponse.json();
    expect(experiments.length).toBeGreaterThan(0);
    console.log(`   ✅ Found ${experiments.length} experiments in database`);

    // Get the most recent experiment
    const recentExperiment = experiments[experiments.length - 1];
    expect(recentExperiment.prompt_template_id).toBeTruthy();
    expect(recentExperiment.framework_config_id).toBeTruthy();
    expect(recentExperiment.scoring_algorithm_id).toBeTruthy();
    console.log(`   ✅ Recent experiment has proper configuration`);

    // Get runs for the recent experiment
    const runsResponse = await page.request.get(`${API_URL}/api/experiments/${recentExperiment.id}/runs`);
    expect(runsResponse.ok()).toBeTruthy();
    const runs = await runsResponse.json();
    expect(runs.length).toBeGreaterThan(0);
    console.log(`   ✅ Found ${runs.length} runs for experiment ${recentExperiment.id}`);

    // Verify run data
    const recentRun = runs[runs.length - 1];
    expect(recentRun.text_content).toBeTruthy();
    expect(recentRun.raw_scores).toBeTruthy();
    expect(Object.keys(recentRun.raw_scores).length).toBeGreaterThan(0);
    expect(recentRun.status).toBe('completed');
    expect(recentRun.success).toBe(true);
    console.log(`   ✅ Run ${recentRun.id} has complete analysis data`);

    // Step 7: Verify specific analysis results
    console.log('🔬 Step 7: Verifying analysis quality...');
    
    // Check that we have expected wells
    const expectedWells = ['Dignity', 'Truth', 'Justice', 'Hope', 'Pragmatism'];
    for (const well of expectedWells) {
      expect(recentRun.raw_scores[well]).toBeDefined();
      expect(typeof recentRun.raw_scores[well]).toBe('number');
      expect(recentRun.raw_scores[well]).toBeGreaterThanOrEqual(0);
      expect(recentRun.raw_scores[well]).toBeLessThanOrEqual(1);
    }
    console.log('   ✅ All expected wells have valid scores');

    // Check hierarchical ranking if present
    if (recentRun.hierarchical_ranking) {
      expect(recentRun.hierarchical_ranking.primary_wells).toBeDefined();
      expect(recentRun.hierarchical_ranking.primary_wells.length).toBeGreaterThan(0);
      console.log('   ✅ Hierarchical ranking data is present');
    }

    // Check calculated metrics
    expect(recentRun.narrative_elevation).toBeDefined();
    expect(recentRun.polarity).toBeDefined();
    expect(recentRun.coherence).toBeDefined();
    expect(recentRun.directional_purity).toBeDefined();
    console.log('   ✅ Calculated metrics are present');

    console.log('\n🎉 UI-driven end-to-end test PASSED!');
    console.log('✅ Complete workflow verified:');
    console.log('   • UI experiment configuration');
    console.log('   • Text input and analysis execution');
    console.log('   • Results display in Analysis Results tab');
    console.log('   • Data persistence in database');
    console.log('   • Analysis quality and completeness');
  });

  test('Multi-model analysis workflow', async ({ page }) => {
    console.log('🚀 Starting multi-model analysis test...');

    // Configure experiment (similar to above)
    await page.locator('select').first().selectOption('civic_virtue_v2_1');
    await page.locator('select').nth(1).selectOption('civic_virtue');
    await page.locator('select').nth(2).selectOption('hierarchical_v2_1');

    // Enter text
    await page.locator('textarea').first().fill(TEST_TEXT);

    // Switch to multi-model mode
    const multiModelToggle = page.locator('input[type="checkbox"]').filter({ hasText: /Multi.*Model|Compare.*Models/ }).first();
    if (await multiModelToggle.isVisible()) {
      await multiModelToggle.check();
      console.log('   ✅ Enabled multi-model mode');
    }

    // Run analysis
    await page.locator('button').filter({ hasText: /Run Analysis|Analyze/ }).first().click();
    
    // Wait for completion
    await expect(page.locator('text=Multi-model analysis complete')).toBeVisible({ timeout: 60000 });
    console.log('   ✅ Multi-model analysis completed');

    // Verify results
    await page.locator('button, a').filter({ hasText: /Analysis Results|Results/ }).first().click();
    
    // Should have multiple results (one per model)
    const resultCards = page.locator('[class*="result"], [class*="analysis"]').filter({ hasText: 'Analysis Result' });
    expect(await resultCards.count()).toBeGreaterThan(1);
    console.log('   ✅ Multiple model results displayed');
  });

  test('Results visualization and interaction', async ({ page }) => {
    console.log('🚀 Testing results visualization...');

    // First run a quick analysis to have data
    await page.locator('select').first().selectOption('civic_virtue_v2_1');
    await page.locator('select').nth(1).selectOption('civic_virtue');
    await page.locator('select').nth(2).selectOption('hierarchical_v2_1');
    await page.locator('textarea').first().fill('Short test text for visualization.');
    await page.locator('button').filter({ hasText: /Run Analysis|Analyze/ }).first().click();
    await expect(page.locator('text=Analysis complete')).toBeVisible({ timeout: 30000 });

    // Navigate to results
    await page.locator('button, a').filter({ hasText: /Analysis Results|Results/ }).first().click();

    // Test result interactions
    const pinButton = page.locator('button').filter({ hasText: /Pin/ }).first();
    if (await pinButton.isVisible()) {
      await pinButton.click();
      console.log('   ✅ Result pinning works');
    }

    // Test expandable sections (if present)
    const expandButton = page.locator('button').filter({ hasText: /Show|Expand|Details/ }).first();
    if (await expandButton.isVisible()) {
      await expandButton.click();
      console.log('   ✅ Expandable sections work');
    }

    // Verify visualization elements
    await expect(page.locator('[class*="chart"], [class*="graph"], [class*="visualization"]')).toBeVisible();
    console.log('   ✅ Visualization elements are displayed');
  });
}); 