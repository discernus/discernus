#!/usr/bin/env node

/**
 * Stability Check Script for Narrative Gravity Research Workbench
 * Validates configuration and dependencies before proceeding with development
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🔍 NARRATIVE GRAVITY WORKBENCH - STABILITY CHECK\n');

// Test Results
const results = {
  passed: 0,
  failed: 0,
  warnings: 0,
  tests: []
};

function logTest(name, status, message = '') {
  const icon = status === 'PASS' ? '✅' : status === 'FAIL' ? '❌' : '⚠️';
  console.log(`${icon} ${name}${message ? ': ' + message : ''}`);
  
  results.tests.push({ name, status, message });
  if (status === 'PASS') results.passed++;
  else if (status === 'FAIL') results.failed++;
  else results.warnings++;
}

// Test 1: Package.json exists and is valid
try {
  const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  logTest('Package.json valid', 'PASS');
  
  // Test 1a: Required dependencies
  const requiredDeps = ['react', 'react-dom', 'vite', 'typescript', 'tailwindcss'];
  const missingDeps = requiredDeps.filter(dep => !packageJson.dependencies[dep] && !packageJson.devDependencies[dep]);
  
  if (missingDeps.length === 0) {
    logTest('Required dependencies present', 'PASS');
  } else {
    logTest('Required dependencies present', 'FAIL', `Missing: ${missingDeps.join(', ')}`);
  }
  
} catch (error) {
  logTest('Package.json valid', 'FAIL', error.message);
}

// Test 2: TypeScript Configuration
try {
  if (fs.existsSync('tsconfig.json')) {
    logTest('TypeScript config exists', 'PASS');
    
    // Check if TypeScript can parse it (more reliable than JSON.parse for .ts config)
    try {
      execSync('npx tsc --showConfig --noEmit', { stdio: 'pipe' });
      logTest('TypeScript config valid', 'PASS');
    } catch (error) {
      logTest('TypeScript config valid', 'FAIL', 'Invalid TypeScript configuration');
    }
  } else {
    logTest('TypeScript config exists', 'FAIL');
  }
} catch (error) {
  logTest('TypeScript config check', 'FAIL', error.message);
}

// Test 3: Vite Configuration
try {
  if (fs.existsSync('vite.config.ts')) {
    logTest('Vite config exists', 'PASS');
  } else {
    logTest('Vite config exists', 'FAIL');
  }
} catch (error) {
  logTest('Vite config exists', 'FAIL', error.message);
}

// Test 4: Tailwind Configuration
try {
  if (fs.existsSync('tailwind.config.js')) {
    logTest('Tailwind config exists', 'PASS');
  } else {
    logTest('Tailwind config exists', 'FAIL');
  }
} catch (error) {
  logTest('Tailwind config exists', 'FAIL', error.message);
}

// Test 5: PostCSS Configuration
try {
  if (fs.existsSync('postcss.config.cjs')) {
    logTest('PostCSS config exists', 'PASS');
  } else {
    logTest('PostCSS config exists', 'FAIL');
  }
} catch (error) {
  logTest('PostCSS config exists', 'FAIL', error.message);
}

// Test 6: Source files structure
const requiredFiles = [
  'src/App.tsx',
  'src/main.tsx',
  'src/index.css',
  'src/App.test.tsx'
];

requiredFiles.forEach(file => {
  if (fs.existsSync(file)) {
    logTest(`Source file ${file}`, 'PASS');
  } else {
    logTest(`Source file ${file}`, 'FAIL');
  }
});

// Test 7: Node modules integrity
try {
  if (fs.existsSync('node_modules')) {
    logTest('Node modules installed', 'PASS');
  } else {
    logTest('Node modules installed', 'FAIL', 'Run npm install');
  }
} catch (error) {
  logTest('Node modules installed', 'FAIL', error.message);
}

// Test 8: Build test
console.log('\n🔨 Running build test...');
try {
  execSync('npm run build', { stdio: 'pipe' });
  logTest('Build succeeds', 'PASS');
} catch (error) {
  logTest('Build succeeds', 'FAIL', 'Build command failed');
}

// Test 9: TypeScript compilation
console.log('🔍 Running TypeScript check...');
try {
  execSync('npx tsc --noEmit', { stdio: 'pipe' });
  logTest('TypeScript compilation clean', 'PASS');
} catch (error) {
  logTest('TypeScript compilation clean', 'FAIL', 'TypeScript errors found');
}

// Test 10: Unit tests (if Vitest is configured)
if (fs.existsSync('src/App.test.tsx')) {
  console.log('🧪 Running unit tests...');
  try {
    execSync('npm test -- --run', { stdio: 'pipe' });
    logTest('Unit tests pass', 'PASS');
  } catch (error) {
    logTest('Unit tests pass', 'FAIL', 'Some tests failed');
  }
}

// Test 11: Import validation
console.log('📦 Validating imports...');
try {
  const appContent = fs.readFileSync('src/App.tsx', 'utf8');
  
  if (appContent.includes("import { useState } from 'react'")) {
    logTest('React imports correct', 'PASS');
  } else {
    logTest('React imports correct', 'WARN', 'Check React import syntax');
  }
  
  if (appContent.includes("import './index.css'")) {
    logTest('CSS imports correct', 'PASS');
  } else {
    logTest('CSS imports correct', 'WARN', 'CSS import missing');
  }
  
} catch (error) {
  logTest('Import validation', 'FAIL', error.message);
}

// Test 12: CSS/Tailwind integrity
try {
  const cssContent = fs.readFileSync('src/index.css', 'utf8');
  
  if (cssContent.includes('@tailwind base') && cssContent.includes('@tailwind components') && cssContent.includes('@tailwind utilities')) {
    logTest('Tailwind CSS imports correct', 'PASS');
  } else {
    logTest('Tailwind CSS imports correct', 'FAIL', 'Tailwind directives missing');
  }
} catch (error) {
  logTest('Tailwind CSS imports correct', 'FAIL', error.message);
}

// Summary
console.log('\n📊 STABILITY CHECK SUMMARY');
console.log('='.repeat(40));
console.log(`✅ Passed: ${results.passed}`);
console.log(`❌ Failed: ${results.failed}`);
console.log(`⚠️  Warnings: ${results.warnings}`);

if (results.failed === 0) {
  console.log('\n🎉 CONFIGURATION IS STABLE');
  console.log('✅ Ready for incremental development');
  console.log('✅ All critical systems operational');
  console.log('\n📋 Next Steps:');
  console.log('  1. Test development server: npm run dev');
  console.log('  2. Run test suite: npm test');
  console.log('  3. Begin Phase 1 development');
} else {
  console.log('\n⚠️  CONFIGURATION NEEDS ATTENTION');
  console.log('❌ Fix failed tests before proceeding');
  
  const failedTests = results.tests.filter(t => t.status === 'FAIL');
  console.log('\n🔧 Failed Tests:');
  failedTests.forEach(test => {
    console.log(`  • ${test.name}: ${test.message}`);
  });
}

process.exit(results.failed > 0 ? 1 : 0); 