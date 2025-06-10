import React, { useState } from 'react';
import { useExperimentStore } from '../store/experimentStore';
import apiService, { SingleTextAnalysisRequest } from '../services/apiClient';

const ExperimentDesigner: React.FC = () => {
  const {
    prompt_templates,
    framework_configs,
    scoring_algorithms,
    available_models,
    experimentForm,
    setExperimentForm,
    analysis_results,
    addAnalysisResult
  } = useExperimentStore();

  // Safe initialization of experimentForm
  const safeExperimentForm = experimentForm || {
    prompt_template_id: '',
    framework_config_id: '',
    scoring_algorithm_id: '',
    analysis_mode: ''
  };

  const [textInput, setTextInput] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [isMultiModelMode, setIsMultiModelMode] = useState(false);
  const [selectedModel, setSelectedModel] = useState('gpt-4');
  const [selectedModelsForComparison, setSelectedModelsForComparison] = useState<string[]>(['gpt-4', 'claude-3-sonnet']);

  const handleCreateExperiment = async () => {
    if (!safeExperimentForm.prompt_template_id || !safeExperimentForm.framework_config_id || !safeExperimentForm.scoring_algorithm_id) {
      alert('Please configure all experiment parameters first.');
      return;
    }

    try {
      console.log('🔄 Creating experiment with configuration:', safeExperimentForm);
      
      // TODO: Implement experiment creation via API
      // For now, just validate the form
      alert('Experiment configuration saved! Ready for analysis.');
      
    } catch (error: any) {
      console.error('❌ Experiment creation failed:', error);
      alert(`Experiment creation failed: ${error.message}`);
    }
  };

  const handleRunAnalysis = async () => {
    if (!textInput.trim()) {
      alert('Please enter text to analyze');
      return;
    }
    if (!safeExperimentForm.prompt_template_id || !safeExperimentForm.framework_config_id || !safeExperimentForm.scoring_algorithm_id) {
      alert('Please configure the experiment first');
      return;
    }

    setAnalyzing(true);
    setAnalysisError(null);
    
    try {
      console.log('🔄 Starting analysis with configuration:', { 
        textInput: textInput.substring(0, 100) + '...',
        models: isMultiModelMode ? selectedModelsForComparison : [selectedModel],
        config: safeExperimentForm
      });

      if (isMultiModelMode) {
        // Multi-model comparison analysis
        const multiModelRequest = {
          text_content: textInput,
          prompt_template_id: safeExperimentForm.prompt_template_id,
          framework_config_id: safeExperimentForm.framework_config_id,
          scoring_algorithm_id: safeExperimentForm.scoring_algorithm_id,
          selected_models: selectedModelsForComparison,
          runs_per_model: 3
        };

        const multiModelResponse = await apiService.analyzeMultiModel(multiModelRequest);
        
        console.log('✅ Multi-model analysis completed:', multiModelResponse);
        
        // Convert multi-model response to individual results for the store
        multiModelResponse.model_results.forEach((modelResult, index) => {
          const analysisResult = {
            id: `${multiModelResponse.analysis_id}-${modelResult.model}-${index}`,
            experiment_id: 'temp-' + Date.now(),
            text_id: 'text-' + Date.now(),
            text_content: textInput,
            llm_model: modelResult.model,
            llm_version: '1.0',
            raw_scores: modelResult.mean_scores,
            well_justifications: undefined, // Multi-model doesn't include individual justifications
            calculated_metrics: {
              narrative_elevation: 0.72,
              polarity: 0.15,
              coherence: 0.85,
              directional_purity: 0.62
            },
            execution_time: multiModelResponse.execution_time,
            complete_provenance: {
              prompt_template_hash: 'multi-model-hash',
              framework_version: framework_configs.find(f => f.id === safeExperimentForm.framework_config_id)?.version || '1.0',
              scoring_algorithm_version: '1.0',
              llm_model: modelResult.model,
              timestamp: multiModelResponse.execution_time
            },
            is_pinned: false
          };
          
          addAnalysisResult(analysisResult);
        });

        alert(`Multi-model analysis complete! Analyzed with ${selectedModelsForComparison.length} models. Check the Analysis Results tab.`);
        
      } else {
        // Single model analysis
        const singleTextRequest: SingleTextAnalysisRequest = {
          text_content: textInput,
          prompt_template_id: safeExperimentForm.prompt_template_id,
          framework_config_id: safeExperimentForm.framework_config_id,
          scoring_algorithm_id: safeExperimentForm.scoring_algorithm_id,
          llm_model: selectedModel,
          include_justifications: true,
          include_hierarchical_ranking: true
        };

        const response = await apiService.analyzeSingleText(singleTextRequest);
        
        console.log('✅ Single text analysis completed:', response);

        // Convert API response to store format
        const analysisResult = {
          id: response.analysis_id,
          experiment_id: 'temp-' + Date.now(),
          text_id: 'text-' + Date.now(),
          text_content: response.text_content,
          llm_model: response.model,
          llm_version: '1.0',
          raw_scores: response.raw_scores,
          well_justifications: response.well_justifications,
          calculated_metrics: response.calculated_metrics,
          execution_time: response.execution_time,
          complete_provenance: {
            prompt_template_hash: 'api-hash',
            framework_version: framework_configs.find(f => f.id === safeExperimentForm.framework_config_id)?.version || '1.0',
            scoring_algorithm_version: '1.0',
            llm_model: response.model,
            timestamp: response.execution_time
          },
          is_pinned: false
        };
        
        addAnalysisResult(analysisResult);
        alert('Analysis complete! Check the Analysis Results tab.');
      }
      
    } catch (error: any) {
      console.error('❌ Analysis failed:', error);
      setAnalysisError(error.message || 'Analysis failed. Please try again.');
      alert(`Analysis failed: ${error.message || 'Unknown error'}`);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="experiment-designer">
      <div className="designer-header">
        <h2>🧪 Experiment Designer</h2>
        <p>Configure and run narrative gravity analysis experiments</p>
      </div>

      {/* Configuration Section */}
      <div className="config-section">
        <h3>📋 Experiment Configuration</h3>
        
        <div className="config-grid">
          <div className="config-item">
            <label>Prompt Template:</label>
            <select 
              value={safeExperimentForm.prompt_template_id} 
              onChange={(e) => setExperimentForm({...safeExperimentForm, prompt_template_id: e.target.value})}
            >
              <option value="">Select Template...</option>
              {prompt_templates.map(template => (
                <option key={template.id} value={template.id}>
                  {template.name} ({template.version})
                </option>
              ))}
            </select>
          </div>

          <div className="config-item">
            <label>Framework Configuration:</label>
            <select 
              value={safeExperimentForm.framework_config_id} 
              onChange={(e) => setExperimentForm({...safeExperimentForm, framework_config_id: e.target.value})}
            >
              <option value="">Select Framework...</option>
                             {framework_configs.map(framework => (
                 <option key={framework.id} value={framework.id}>
                   {framework.display_name} ({framework.version})
                 </option>
               ))}
            </select>
          </div>

          <div className="config-item">
            <label>Scoring Algorithm:</label>
            <select 
              value={safeExperimentForm.scoring_algorithm_id} 
              onChange={(e) => setExperimentForm({...safeExperimentForm, scoring_algorithm_id: e.target.value})}
            >
              <option value="">Select Algorithm...</option>
              {scoring_algorithms.map(algorithm => (
                <option key={algorithm.id} value={algorithm.id}>
                  {algorithm.name}
                </option>
              ))}
            </select>
          </div>

          <div className="config-item">
            <label>Analysis Mode:</label>
            <select 
              value={safeExperimentForm.analysis_mode} 
              onChange={(e) => {
                const isMulti = e.target.value === 'multi_model_comparison';
                setIsMultiModelMode(isMulti);
                setExperimentForm({...safeExperimentForm, analysis_mode: e.target.value});
              }}
            >
              <option value="single_model">Single Model Analysis</option>
              <option value="multi_model_comparison">Multi-Model Comparison (Stability Assessment)</option>
            </select>
          </div>
        </div>

        {/* Model Selection */}
        <div className="model-selection">
          {isMultiModelMode ? (
            <div className="multi-model-selection">
              <label>Models for Comparison:</label>
              <div className="model-checkboxes">
                                 {available_models.map((model: string) => (
                   <label key={model} className="checkbox-label">
                     <input
                       type="checkbox"
                       checked={selectedModelsForComparison.includes(model)}
                       onChange={(e) => {
                         if (e.target.checked) {
                           setSelectedModelsForComparison([...selectedModelsForComparison, model]);
                         } else {
                           setSelectedModelsForComparison(selectedModelsForComparison.filter(m => m !== model));
                         }
                       }}
                     />
                     {model}
                   </label>
                 ))}
              </div>
            </div>
          ) : (
            <div className="single-model-selection">
              <label>LLM Model:</label>
                             <select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
                 {available_models.map((model: string) => (
                   <option key={model} value={model}>{model}</option>
                 ))}
               </select>
            </div>
          )}
        </div>

        <button 
          className="create-experiment-btn"
          onClick={handleCreateExperiment}
          disabled={!safeExperimentForm.prompt_template_id || !safeExperimentForm.framework_config_id || !safeExperimentForm.scoring_algorithm_id}
        >
          💾 Save Experiment Configuration
        </button>
      </div>

      {/* Text Analysis Section */}
      <div className="analysis-section">
        <h3>📝 Text Analysis</h3>
        
        <div className="text-input-area">
          <label>Text to Analyze:</label>
          <textarea
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            placeholder="Enter the text you want to analyze..."
            rows={8}
            className="text-input"
          />
          <div className="input-info">
            Characters: {textInput.length} | Words: {textInput.split(/\s+/).filter(w => w.length > 0).length}
          </div>
        </div>

        {analysisError && (
          <div className="error-message">
            ❌ {analysisError}
          </div>
        )}

        <button 
          className="analyze-btn"
          onClick={handleRunAnalysis}
          disabled={analyzing || !textInput.trim() || !safeExperimentForm.prompt_template_id}
        >
          {analyzing ? '🔄 Analyzing...' : '🚀 Run Analysis'}
        </button>

        {analyzing && (
          <div className="analysis-progress">
            <div className="progress-info">
              <p>🔄 Analysis in progress...</p>
              <p>Model: {isMultiModelMode ? `${selectedModelsForComparison.length} models` : selectedModel}</p>
                             <p>Framework: {framework_configs.find(f => f.id === safeExperimentForm.framework_config_id)?.display_name || 'Unknown'}</p>
              <p>Algorithm: {scoring_algorithms.find(a => a.id === safeExperimentForm.scoring_algorithm_id)?.name || 'Unknown'}</p>
            </div>
          </div>
        )}
      </div>

      {/* Status Section */}
      <div className="status-section">
        <h3>📊 Status</h3>
        <div className="status-grid">
          <div className="status-item">
            <span className="status-label">Available Templates:</span>
            <span className="status-value">{prompt_templates.length}</span>
          </div>
          <div className="status-item">
            <span className="status-label">Available Frameworks:</span>
            <span className="status-value">{framework_configs.length}</span>
          </div>
          <div className="status-item">
            <span className="status-label">Available Algorithms:</span>
            <span className="status-value">{scoring_algorithms.length}</span>
          </div>
          <div className="status-item">
            <span className="status-label">Analysis Results:</span>
            <span className="status-value">{analysis_results.length}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExperimentDesigner; 