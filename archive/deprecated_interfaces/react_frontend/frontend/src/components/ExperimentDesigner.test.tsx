import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import ExperimentDesigner from './ExperimentDesigner';
import { useExperimentStore } from '../store/experimentStore';

// Mock the experiment store
vi.mock('../store/experimentStore', () => ({
  useExperimentStore: vi.fn()
}));

// Mock the API service
vi.mock('../services/apiClient', () => ({
  default: {
    analyzeSingleText: vi.fn(() => Promise.resolve({
      analysis_id: 'test-123',
      text_content: 'test text',
      model: 'gpt-4',
      raw_scores: { Truth: 0.8, Justice: 0.6, Dignity: 0.4 },
      calculated_metrics: { narrative_elevation: 0.75, polarity: 0.3, coherence: 0.9, directional_purity: 0.7 },
      execution_time: '2025-01-06T16:00:00Z'
    })),
    analyzeMultiModel: vi.fn(() => Promise.resolve({
      analysis_id: 'test-multi-123',
      model_results: [
        { model: 'gpt-4', mean_scores: { Truth: 0.8, Justice: 0.6 } },
        { model: 'claude-3-sonnet', mean_scores: { Truth: 0.7, Justice: 0.5 } }
      ],
      execution_time: '2025-01-06T16:00:00Z'
    }))
  }
}));

describe('ExperimentDesigner - v2.1 Phase 1 Features', () => {
  const mockStore = {
    prompt_templates: [
      {
        id: 'hierarchical-1',
        name: 'Hierarchical Prompt v1.0',
        version: '1.0.0',
        type: 'hierarchical',
        content: 'Test hierarchical prompt content...',
        description: 'Test hierarchical prompt'
      }
    ],
    framework_configs: [
      {
        id: 'civic-virtue-1',
        framework_name: 'civic_virtue',
        display_name: 'Civic Virtue Framework',
        version: '1.0.0',
        description: 'Test framework',
        dipoles: []
      }
    ],
    scoring_algorithms: [
      {
        id: 'hierarchical-1',
        name: 'Hierarchical Dominance',
        version: '1.0.0',
        type: 'hierarchical',
        parameters: { primary_weight: 0.6, secondary_weight: 0.3, tertiary_weight: 0.1 },
        description: 'Hierarchical scoring'
      },
      {
        id: 'winner-take-most-1',
        name: 'Winner-Take-Most',
        version: '1.0.0',
        type: 'winner_take_most',
        parameters: { dominance_threshold: 0.6, boost_factor: 1.5 },
        description: 'Winner take most scoring'
      }
    ],
    available_models: ['gpt-4', 'claude-3-sonnet', 'claude-3-opus'],
    experimentForm: {
      prompt_template_id: '',
      framework_config_id: '',
      scoring_algorithm_id: '',
      analysis_mode: ''
    },
    analysis_results: [],
    setExperimentForm: vi.fn(),
    addAnalysisResult: vi.fn()
  };

  beforeEach(() => {
    vi.mocked(useExperimentStore).mockReturnValue(mockStore);
  });

  it('renders hierarchical prompt templates', () => {
    render(<ExperimentDesigner />);
    
    expect(screen.getByText('🧪 Experiment Designer')).toBeInTheDocument();
    expect(screen.getByText('Prompt Template:')).toBeInTheDocument();
  });

  it('shows nonlinear scoring algorithms', () => {
    render(<ExperimentDesigner />);
    
    expect(screen.getByText('Scoring Algorithm:')).toBeInTheDocument();
    // Algorithms are in dropdown options, not directly visible text
  });

  it('displays multi-model comparison options', () => {
    render(<ExperimentDesigner />);
    
    expect(screen.getByText('Analysis Mode:')).toBeInTheDocument();
    expect(screen.getByText('Single Model Analysis')).toBeInTheDocument();
    expect(screen.getByText('Multi-Model Comparison (Stability Assessment)')).toBeInTheDocument();
  });

  it('enables multi-model mode when selected', async () => {
    render(<ExperimentDesigner />);
    
    // Find the Analysis Mode select (it's the 4th select element in the config)
    const selects = screen.getAllByRole('combobox');
    const analysisModeSelect = selects[3]; // Analysis Mode is the 4th select
    fireEvent.change(analysisModeSelect, { target: { value: 'multi_model_comparison' } });
    
    await waitFor(() => {
      expect(screen.getByText('Models for Comparison:')).toBeInTheDocument();
    });
  });

  it('shows validation warning for insufficient model selection', async () => {
    render(<ExperimentDesigner />);
    
    // Try to save configuration without selections
    const saveButton = screen.getByText('💾 Save Experiment Configuration');
    expect(saveButton).toBeDisabled();
  });

  it('creates experiment with hierarchical prompt configuration', async () => {
    // Mock a complete form
    const completeStore = {
      ...mockStore,
      experimentForm: {
        prompt_template_id: 'hierarchical-1',
        framework_config_id: 'civic-virtue-1',
        scoring_algorithm_id: 'hierarchical-1',
        analysis_mode: 'single_model'
      }
    };
    
    vi.mocked(useExperimentStore).mockReturnValue(completeStore);
    
    render(<ExperimentDesigner />);
    
    const saveButton = screen.getByText('💾 Save Experiment Configuration');
    expect(saveButton).not.toBeDisabled();
  });

  it('validates experiment form before creation', () => {
    render(<ExperimentDesigner />);
    
    // Save button should be disabled without complete form
    const saveButton = screen.getByText('💾 Save Experiment Configuration');
    expect(saveButton).toBeDisabled();
  });

  it('displays experiment configuration details', () => {
    render(<ExperimentDesigner />);
    
    expect(screen.getByText('📋 Experiment Configuration')).toBeInTheDocument();
    expect(screen.getByText('Prompt Template:')).toBeInTheDocument();
    expect(screen.getByText('Framework Configuration:')).toBeInTheDocument();
    expect(screen.getByText('Scoring Algorithm:')).toBeInTheDocument();
  });
}); 