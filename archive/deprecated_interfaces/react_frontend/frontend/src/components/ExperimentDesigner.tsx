import React, { useState, useEffect } from 'react';
import { useExperimentStore } from '../store/experimentStore';
import apiService from '../services/apiClient';

interface ConfigData {
  frameworks: Array<{id: string; name: string; version: string}>;
  prompts: Array<{id: string; name: string; version: string}>;
  algorithms: Array<{id: string; name: string}>;
}

const ExperimentDesigner: React.FC = () => {
  // Store integration
  const {
    prompt_templates,
    framework_configs, 
    scoring_algorithms,
    experiments,
    experimentForm,
    setExperimentForm,
    createExperiment,
    addAnalysisResult,
    setAnalyzing,
    is_analyzing
  } = useExperimentStore();

  // API Configuration State  
  const [configData, setConfigData] = useState<ConfigData>({
    frameworks: [], prompts: [], algorithms: []
  });
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  // Experiment Design State
  const [experimentName, setExperimentName] = useState('');
  const [experimentHypothesis, setExperimentHypothesis] = useState('');
  const [analysisMode, setAnalysisMode] = useState('single_model');
  const [selectedModels, setSelectedModels] = useState<string[]>(['gpt-4.1']);
  const [runsPerModel, setRunsPerModel] = useState(3);

  // Text Analysis State
  const [textInput, setTextInput] = useState('');
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  // UI State
  const [activeTab, setActiveTab] = useState<'design' | 'text' | 'results'>('design');

  // Load configuration on mount
  useEffect(() => {
    const loadConfiguration = async () => {
      try {
        console.log('🔄 Loading API configuration...');
        const [frameworks, prompts, algorithms] = await Promise.all([
          apiService.getFrameworkConfigs(),
          apiService.getPromptTemplates(), 
          apiService.getScoringAlgorithms()
        ]);

        setConfigData({ frameworks, prompts, algorithms });
        
        // Auto-select first options if not already set
        if (!experimentForm.framework_config_id && frameworks.length > 0) {
          setExperimentForm({
            ...experimentForm,
            framework_config_id: frameworks[0].id
          });
        }
        if (!experimentForm.prompt_template_id && prompts.length > 0) {
          setExperimentForm({
            ...experimentForm,
            prompt_template_id: prompts[0].id
          });
        }
        if (!experimentForm.scoring_algorithm_id && algorithms.length > 0) {
          setExperimentForm({
            ...experimentForm,
            scoring_algorithm_id: algorithms[0].id
          });
        }

        console.log('✅ Configuration loaded successfully');
      } catch (error: any) {
        console.error('❌ Configuration loading failed:', error);
        setLoadError(error.message || 'Failed to load configuration');
      } finally {
        setLoading(false);
      }
    };

    loadConfiguration();
  }, []);

  // Handle experiment creation
  const handleCreateExperiment = () => {
    if (!experimentName.trim()) {
      alert('Please enter an experiment name');
      return;
    }
    if (!experimentForm.framework_config_id || !experimentForm.prompt_template_id || !experimentForm.scoring_algorithm_id) {
      alert('Please select all configuration options');
      return;
    }

    const experimentId = createExperiment({
      name: experimentName,
      hypothesis: experimentHypothesis,
      prompt_template_id: experimentForm.prompt_template_id,
      framework_config_id: experimentForm.framework_config_id,
      scoring_algorithm_id: experimentForm.scoring_algorithm_id
    });

    console.log('✅ Experiment created:', experimentId);
    setExperimentHypothesis('');
    setActiveTab('text');
  };

  // Handle text analysis
  const handleAnalyze = async () => {
    if (!textInput.trim()) {
      alert('Please enter text to analyze');
      return;
    }
    if (!experimentForm.framework_config_id || !experimentForm.prompt_template_id || !experimentForm.scoring_algorithm_id) {
      alert('Please complete experiment configuration first');
      return;
    }

    setAnalyzing(true);
    setAnalysisError(null);
    setAnalysisResult(null);

    try {
      if (analysisMode === 'single_model') {
        // Single model analysis
        const result = await apiService.analyzeSingleText({
          text_content: textInput,
          prompt_template_id: experimentForm.prompt_template_id,
          framework_config_id: experimentForm.framework_config_id,
          scoring_algorithm_id: experimentForm.scoring_algorithm_id,
          llm_model: selectedModels[0],
          include_justifications: true,
          include_hierarchical_ranking: true
        });

        setAnalysisResult(result);
        
        // Add to store
        addAnalysisResult({
          experiment_id: experiments[experiments.length - 1]?.id || 'single-text',
          text_id: result.analysis_id,
          text_content: textInput,
          llm_model: result.model,
          llm_version: 'latest',
          raw_scores: result.raw_scores,
          well_justifications: result.well_justifications,
          calculated_metrics: result.calculated_metrics,
          execution_time: result.execution_time,
          complete_provenance: {
            prompt_template_hash: `hash_${experimentForm.prompt_template_id}`,
            framework_version: experimentForm.framework_config_id,
            scoring_algorithm_version: experimentForm.scoring_algorithm_id,
            llm_model: result.model,
            timestamp: new Date().toISOString()
          }
        });

      } else {
        // Multi-model analysis
        const result = await apiService.analyzeMultiModel({
          text_content: textInput,
          prompt_template_id: experimentForm.prompt_template_id,
          framework_config_id: experimentForm.framework_config_id,
          scoring_algorithm_id: experimentForm.scoring_algorithm_id,
          selected_models: selectedModels,
          runs_per_model: runsPerModel
        });

        setAnalysisResult(result);
      }
      
      setActiveTab('results');
      
    } catch (error: any) {
      console.error('❌ Analysis failed:', error);
      setAnalysisError(error.message || 'Analysis failed');
    } finally {
      setAnalyzing(false);
    }
  };

  // Handle model selection for multi-model mode
  const handleModelToggle = (model: string) => {
    setSelectedModels(prev => 
      prev.includes(model) 
        ? prev.filter(m => m !== model)
        : [...prev, model]
    );
  };

  // Validation
  const isExperimentValid = experimentName.trim() && 
                           experimentForm.framework_config_id && 
                           experimentForm.prompt_template_id && 
                           experimentForm.scoring_algorithm_id;

  const isAnalysisReady = textInput.trim() && isExperimentValid;

  // Loading state
  if (loading) {
    return (
      <div className="p-6" data-testid="experiment-designer-loading">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">🧪 Experiment Designer</h2>
        <div className="flex items-center justify-center p-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <span className="ml-4 text-gray-600">Loading research workbench...</span>
        </div>
      </div>
    );
  }

  // Error state
  if (loadError) {
    return (
      <div className="p-6" data-testid="experiment-designer-error">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">🧪 Experiment Designer</h2>
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <strong>Configuration Error:</strong> {loadError}
          <br />
          <small>Make sure the API server is running on http://localhost:8000</small>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6" data-testid="experiment-designer">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">🧪 Research Workbench - Experiment Designer</h2>
      
      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'design', label: '🧪 Experiment Design', desc: 'Configure hypothesis & methods' },
            { id: 'text', label: '📝 Text Analysis', desc: 'Run analysis on your experiment' },
            { id: 'results', label: '📊 Results & Insights', desc: 'View and interpret findings' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div>{tab.label}</div>
              <div className="text-xs text-gray-400">{tab.desc}</div>
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'design' && (
        <div className="space-y-8">
          {/* Experiment Definition */}
          <div>
            <h3 className="text-lg font-semibold mb-4">🎯 Unified Experiment Design</h3>
            
            <div className="grid grid-cols-1 gap-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Experiment Name *
                </label>
                <input
                  type="text"
                  value={experimentName}
                  onChange={(e) => setExperimentName(e.target.value)}
                  placeholder="e.g., Hierarchical Prompting vs Standard Analysis"
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  data-testid="experiment-name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Research Hypothesis
                </label>
                <textarea
                  value={experimentHypothesis}
                  onChange={(e) => setExperimentHypothesis(e.target.value)}
                  placeholder="State your hypothesis about what this configuration will reveal about narrative themes..."
                  rows={3}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  data-testid="experiment-hypothesis"
                />
              </div>
            </div>
          </div>

          {/* Configuration Section */}
          <div>
            <h3 className="text-lg font-semibold mb-4">📋 Experimental Configuration</h3>
            
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Framework Configuration ({configData.frameworks.length} available)
                </label>
                <select 
                  value={experimentForm.framework_config_id}
                  onChange={(e) => setExperimentForm({...experimentForm, framework_config_id: e.target.value})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  data-testid="framework-select"
                >
                  <option value="">Select Framework...</option>
                  {configData.frameworks.map(fw => (
                    <option key={fw.id} value={fw.id}>
                      {fw.name} ({fw.version})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Prompt Template ({configData.prompts.length} available)
                </label>
                <select 
                  value={experimentForm.prompt_template_id}
                  onChange={(e) => setExperimentForm({...experimentForm, prompt_template_id: e.target.value})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  data-testid="prompt-select"
                >
                  <option value="">Select Prompt...</option>
                  {configData.prompts.map(pt => (
                    <option key={pt.id} value={pt.id}>
                      {pt.name} ({pt.version})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Scoring Algorithm ({scoring_algorithms.length} store + {configData.algorithms.length} API)
                </label>
                <select 
                  value={experimentForm.scoring_algorithm_id}
                  onChange={(e) => setExperimentForm({...experimentForm, scoring_algorithm_id: e.target.value})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  data-testid="algorithm-select"
                >
                  <option value="">Select Algorithm...</option>
                  {scoring_algorithms.map(alg => (
                    <option key={alg.id} value={alg.id}>
                      {alg.name} - {alg.description}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Analysis Mode
                </label>
                <select 
                  value={analysisMode}
                  onChange={(e) => setAnalysisMode(e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  data-testid="analysis-mode-select"
                >
                  <option value="single_model">Single Model Analysis</option>
                  <option value="multi_model_comparison">Multi-Model Comparison (Stability Assessment)</option>
                </select>
              </div>
            </div>

            {/* Multi-model configuration */}
            {analysisMode === 'multi_model_comparison' && (
              <div className="bg-blue-50 p-4 rounded-lg mb-4">
                <h4 className="font-semibold mb-3">Models for Comparison:</h4>
                <div className="grid grid-cols-3 gap-2 mb-4">
                  {[
                    { id: 'gpt-4.1', name: 'GPT-4.1', group: 'OpenAI' },
                    { id: 'claude-4-sonnet', name: 'Claude 4 Sonnet', group: 'Anthropic' },
                    { id: 'mistral-large-2411', name: 'Mistral Large', group: 'Mistral' },
                    { id: 'gemini-2.5-pro', name: 'Gemini 2.5 Pro', group: 'Google' },
                    { id: 'gpt-4o', name: 'GPT-4o', group: 'OpenAI' },
                    { id: 'claude-3.5-sonnet', name: 'Claude 3.5', group: 'Anthropic' }
                  ].map(model => (
                    <label key={model.id} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={selectedModels.includes(model.id)}
                        onChange={() => handleModelToggle(model.id)}
                        className="rounded"
                      />
                      <span className="text-sm">{model.name}</span>
                    </label>
                  ))}
                </div>
                
                <div className="flex items-center space-x-4">
                  <label className="text-sm font-medium">Runs per model:</label>
                  <select 
                    value={runsPerModel}
                    onChange={(e) => setRunsPerModel(Number(e.target.value))}
                    className="border border-gray-300 rounded px-2 py-1"
                  >
                    <option value={1}>1 run</option>
                    <option value={3}>3 runs</option>
                    <option value={5}>5 runs</option>
                    <option value={10}>10 runs</option>
                  </select>
                </div>
                
                {selectedModels.length < 2 && (
                  <div className="text-amber-600 text-sm mt-2">
                    ⚠️ Select at least 2 models for meaningful comparison
                  </div>
                )}
              </div>
            )}

            <div className={`p-3 rounded text-sm ${
              isExperimentValid 
                ? 'bg-green-50 text-green-700' 
                : 'bg-amber-50 text-amber-700'
            }`}>
              <strong>Configuration Status:</strong> {
                isExperimentValid
                  ? '✅ Ready to create experiment'
                  : '⚠️ Please complete all required fields'
              }
            </div>
          </div>

          {/* Experiment Actions */}
          <div className="flex items-center space-x-4">
            <button
              onClick={handleCreateExperiment}
              disabled={!isExperimentValid}
              className={`px-6 py-3 rounded-md font-semibold ${
                isExperimentValid
                  ? 'bg-blue-600 text-white hover:bg-blue-700'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
              data-testid="create-experiment-button"
            >
              💾 Save Experiment Configuration
            </button>
            
            <div className="text-sm text-gray-600">
              {experiments.length} experiments created in this session
            </div>
          </div>
        </div>
      )}

      {activeTab === 'text' && (
        <div className="space-y-6">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h3 className="font-semibold mb-2">🎯 Current Experiment Configuration</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div><strong>Framework:</strong> {experimentForm.framework_config_id || 'Not selected'}</div>
              <div><strong>Prompt:</strong> {experimentForm.prompt_template_id || 'Not selected'}</div>
              <div><strong>Algorithm:</strong> {experimentForm.scoring_algorithm_id || 'Not selected'}</div>
              <div><strong>Mode:</strong> {analysisMode === 'single_model' ? 'Single Model' : 'Multi-Model Comparison'}</div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">📝 Text Analysis</h3>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Text to Analyze
              </label>
              <textarea
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                placeholder="Enter the text you want to analyze using your experimental configuration..."
                rows={8}
                className="w-full border border-gray-300 rounded-md px-3 py-2"
                data-testid="text-input"
              />
              <div className="text-sm text-gray-500 mt-1">
                Characters: {textInput.length} | Words: {textInput.split(/\s+/).filter(w => w.length > 0).length}
              </div>
            </div>

            {analysisError && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                <strong>Analysis Error:</strong> {analysisError}
              </div>
            )}

            <button
              onClick={handleAnalyze}
              disabled={is_analyzing || !isAnalysisReady}
              className={`px-6 py-3 rounded-md font-semibold ${
                is_analyzing || !isAnalysisReady
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
              data-testid="analyze-button"
            >
              {is_analyzing ? '🔄 Analyzing...' : 
               analysisMode === 'single_model' ? '🚀 Analyze Text' : '🚀 Run Multi-Model Analysis'}
            </button>
          </div>
        </div>
      )}

      {activeTab === 'results' && (
        <div className="space-y-6">
          {analysisResult ? (
            <div data-testid="analysis-results">
              <h3 className="text-lg font-semibold mb-4">📊 Analysis Results</h3>
              
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                <h4 className="font-semibold text-green-900 mb-2">✅ Analysis Complete</h4>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div><strong>Model:</strong> {analysisResult.model || 'Multi-model'}</div>
                  <div><strong>Framework:</strong> {analysisResult.framework || experimentForm.framework_config_id}</div>
                  <div><strong>Execution Time:</strong> {analysisResult.duration_seconds?.toFixed(2)}s</div>
                  <div><strong>API Cost:</strong> ${analysisResult.api_cost?.toFixed(4) || analysisResult.total_cost?.toFixed(4)}</div>
                </div>
              </div>

              {/* Single model results */}
              {analysisResult.raw_scores && (
                <>
                  <div className="bg-white border border-gray-200 rounded-lg p-4 mb-4">
                    <h4 className="font-semibold mb-3">Gravity Well Scores</h4>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      {Object.entries(analysisResult.raw_scores || {}).map(([well, score]) => (
                        <div key={well} className="flex justify-between">
                          <span>{well}:</span>
                          <span className="font-mono">{(score as number).toFixed(3)}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="bg-white border border-gray-200 rounded-lg p-4 mb-4">
                    <h4 className="font-semibold mb-3">Calculated Metrics</h4>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div className="flex justify-between">
                        <span>Narrative Elevation:</span>
                        <span className="font-mono">{analysisResult.calculated_metrics?.narrative_elevation?.toFixed(3)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Polarity:</span>
                        <span className="font-mono">{analysisResult.calculated_metrics?.polarity?.toFixed(3)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Coherence:</span>
                        <span className="font-mono">{analysisResult.calculated_metrics?.coherence?.toFixed(3)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Directional Purity:</span>
                        <span className="font-mono">{analysisResult.calculated_metrics?.directional_purity?.toFixed(3)}</span>
                      </div>
                    </div>
                  </div>

                  {analysisResult.dominant_wells && (
                    <div className="bg-white border border-gray-200 rounded-lg p-4">
                      <h4 className="font-semibold mb-3">Dominant Wells</h4>
                      <div className="space-y-2">
                        {analysisResult.dominant_wells.map((well: any, index: number) => (
                          <div key={index} className="flex justify-between items-center">
                            <span className="font-medium">{well.well}</span>
                            <div className="flex items-center space-x-2">
                              <span className="text-sm text-gray-600">{well.relative_weight}%</span>
                              <span className="font-mono text-sm">{well.score?.toFixed(3)}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </>
              )}

              {/* Multi-model results */}
              {analysisResult.model_results && (
                <div className="bg-white border border-gray-200 rounded-lg p-4">
                  <h4 className="font-semibold mb-3">Multi-Model Comparison</h4>
                  <div className="space-y-4">
                    {analysisResult.model_results.map((modelResult: any, index: number) => (
                      <div key={index} className="border-l-4 border-blue-200 pl-4">
                        <h5 className="font-medium">{modelResult.model}</h5>
                        <div className="grid grid-cols-3 gap-2 text-sm mt-2">
                          {Object.entries(modelResult.mean_scores || {}).map(([well, score]) => (
                            <div key={well} className="flex justify-between">
                              <span>{well}:</span>
                              <span className="font-mono">{(score as number).toFixed(3)}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <p>Run an analysis to see results here.</p>
              <button
                onClick={() => setActiveTab('text')}
                className="mt-2 text-blue-600 hover:text-blue-800"
              >
                → Go to Text Analysis
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ExperimentDesigner; 