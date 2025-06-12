import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import App from './App';

describe('Narrative Gravity Research Workbench - Baseline Tests', () => {
  
  // Test 1: Basic Rendering
  test('renders main application without crashing', () => {
    render(<App />);
    expect(screen.getByText('Narrative Gravity Research Workbench')).toBeInTheDocument();
  });

  // Test 2: Header Elements
  test('displays correct header information', () => {
    render(<App />);
    expect(screen.getByText('Narrative Gravity Research Workbench')).toBeInTheDocument();
    expect(screen.getByText('v2.1 Phase 1 Research Workbench')).toBeInTheDocument();
    expect(screen.getByText('Stable')).toBeInTheDocument();
  });

  // Test 3: Navigation Tabs
  test('renders all navigation tabs', () => {
    render(<App />);
    expect(screen.getByText('Experiment Designer')).toBeInTheDocument();
    expect(screen.getByText('Prompt Editor')).toBeInTheDocument();
    expect(screen.getByText('Analysis Results')).toBeInTheDocument();
    expect(screen.getByText('Compare Experiments')).toBeInTheDocument();
  });

  // Test 4: Tab Navigation
  test('tab navigation works correctly', async () => {
    render(<App />);
    
    // Initially shows loading state, then Experiment Designer loads
    await waitFor(() => {
      expect(screen.getByText('🧪 Experiment Designer')).toBeInTheDocument();
    });
    
    // Click Prompt Editor tab
    fireEvent.click(screen.getByText('Prompt Editor'));
    await waitFor(() => {
      expect(screen.getByText('Prompt Template & Framework Editor')).toBeInTheDocument();
    });
    
    // Click Analysis Results tab
    fireEvent.click(screen.getByText('Analysis Results'));
    await waitFor(() => {
      expect(screen.getByText('No analysis results yet. Run an experiment to see results here.')).toBeInTheDocument();
    });
    
    // Click Compare Experiments tab
    fireEvent.click(screen.getByText('Compare Experiments'));
    await waitFor(() => {
      expect(screen.getByText('Select 2 or more analysis results to begin comparative analysis')).toBeInTheDocument();
    });
  });

  // Test 5: CSS Classes Applied
  test('tailwind CSS classes are applied correctly', () => {
    render(<App />);
    const header = screen.getByRole('banner');
    expect(header).toHaveClass('bg-white', 'shadow-sm', 'border-b');
  });

  // Test 6: Debug Info Panel
  test('debug info panel displays correctly', () => {
    render(<App />);
    expect(screen.getByText('✅ v2.1 Phase 1 Active')).toBeInTheDocument();
    expect(screen.getByText('Features: Hierarchical prompts, Multi-model comparison, Nonlinear scoring')).toBeInTheDocument();
  });

  // Test 7: Active Tab State
  test('active tab state updates correctly', () => {
    render(<App />);
    
    const designerTab = screen.getByText('Experiment Designer');
    const promptTab = screen.getByText('Prompt Editor');
    
    // Designer tab should be active initially
    expect(designerTab.closest('button')).toHaveClass('border-blue-500', 'text-blue-600');
    
    // Click Prompt Editor
    fireEvent.click(promptTab);
    
    // Prompt tab should now be active
    expect(promptTab.closest('button')).toHaveClass('border-blue-500', 'text-blue-600');
    expect(designerTab.closest('button')).toHaveClass('border-transparent');
  });

  // Test 8: Component Structure
  test('maintains proper component structure', () => {
    render(<App />);
    
    // Check main structural elements exist
    expect(screen.getByRole('banner')).toBeInTheDocument(); // header
    expect(screen.getByRole('navigation')).toBeInTheDocument(); // nav
    expect(screen.getByRole('main')).toBeInTheDocument(); // main content
  });

  // Test 9: No Console Errors
  test('renders without console errors', () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    render(<App />);
    expect(consoleSpy).not.toHaveBeenCalled();
    consoleSpy.mockRestore();
  });

  // Test 10: Gradient Logo Element
  test('logo element renders with correct styling', () => {
    render(<App />);
    const logoElement = screen.getByText('NG');
    expect(logoElement.closest('div')).toHaveClass('bg-gradient-to-r', 'from-blue-500', 'to-purple-600');
  });
});

// Performance and Stability Tests
describe('Stability and Performance Tests', () => {
  
  test('handles rapid tab switching without errors', () => {
    render(<App />);
    
    const tabs = ['Prompt Editor', 'Analysis Results', 'Compare Experiments', 'Experiment Designer'];
    
    // Rapidly switch tabs multiple times
    for (let i = 0; i < 5; i++) {
      tabs.forEach(tabName => {
        fireEvent.click(screen.getByText(tabName));
      });
    }
    
    // Should still be functional
    expect(screen.getByText('Narrative Gravity Research Workbench')).toBeInTheDocument();
  });

  test('maintains state consistency during navigation', async () => {
    render(<App />);
    
    // Navigate to different tabs and verify content changes
    const tabs = [
      { name: 'Prompt Editor', expectedContent: 'Prompt Template & Framework Editor' },
      { name: 'Analysis Results', expectedContent: 'No analysis results yet. Run an experiment to see results here.' },
      { name: 'Compare Experiments', expectedContent: 'Select 2 or more analysis results to begin comparative analysis' },
      { name: 'Experiment Designer', expectedContent: '🧪 Experiment Designer' }
    ];
    
    for (const tab of tabs) {
      fireEvent.click(screen.getByText(tab.name));
      await waitFor(() => {
        expect(screen.getByText(tab.expectedContent)).toBeInTheDocument();
      });
    }
  });
});

// Integration Tests for Future Development
describe('Integration Readiness Tests', () => {
  
  test('app structure ready for state management integration', () => {
    render(<App />);
    
    // Verify the app has the structure needed for adding stores
    expect(document.querySelector('.min-h-screen')).toBeInTheDocument();
    expect(document.querySelector('header')).toBeInTheDocument();
    expect(document.querySelector('nav')).toBeInTheDocument();
    expect(document.querySelector('main')).toBeInTheDocument();
  });

  test('component isolation - components render independently', async () => {
    render(<App />);
    
    // Each tab should render its own content without interference
    fireEvent.click(screen.getByText('Prompt Editor'));
    await waitFor(() => {
      expect(screen.getByText('Prompt Template & Framework Editor')).toBeInTheDocument();
    });
  });
});
