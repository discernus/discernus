const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  // Capture console messages
  page.on('console', msg => {
    console.log(`🔍 Console ${msg.type()}: ${msg.text()}`);
  });
  
  // Capture errors
  page.on('pageerror', error => {
    console.log(`❌ Page Error: ${error.message}`);
  });
  
  console.log('🔄 Navigating to http://localhost:3000...');
  await page.goto('http://localhost:3000');
  
  // Wait for page to load
  await page.waitForTimeout(3000);
  
  console.log('📸 Screenshot saved as frontend-debug.png');
  await page.screenshot({ path: 'frontend-debug.png' });
  
  console.log('📄 Page title:', await page.title());
  
  // Check for content
  const bodyText = await page.textContent('body');
  console.log('📝 Page content length:', bodyText.length);
  
  // Check for specific elements
  const header = await page.locator('header').isVisible();
  console.log('📋 Header visible:', header);
  
  const nav = await page.locator('nav').isVisible();
  console.log('🧭 Navigation visible:', nav);
  
  const main = await page.locator('main').isVisible();
  console.log('📄 Main content visible:', main);
  
  // Check for the experiment designer tab specifically
  const experimentTab = await page.locator('button:has-text("Experiment Designer")').isVisible();
  console.log('🧪 Experiment Designer tab visible:', experimentTab);
  
  console.log('📸 Second screenshot saved as frontend-debug-after.png');
  await page.screenshot({ path: 'frontend-debug-after.png' });
  
  console.log('🔄 Keeping browser open for 5 seconds for manual inspection...');
  await page.waitForTimeout(5000);
  
  await browser.close();
})(); 