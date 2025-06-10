import React, { useState, useEffect } from 'react';
import apiService from '../services/apiClient';

interface ConfigData {
  frameworks: Array<{id: string; name: string; version: string}>;
  prompts: Array<{id: string; name: string; version: string}>;
  algorithms: Array<{id: string; name: string}>;
}

const ExperimentDesigner: React.FC = () => {
  // API Configuration State
  const [configData, setConfigData] = useState<ConfigData>({
    frameworks: [], prompts: [], algorithms: []
  });
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  // Experiment Configuration State
  const [selectedFramework, setSelectedFramework] = useState('');
  const [selectedPrompt, setSelectedPrompt] = useState('');
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('');
  const [selectedModel, setSelectedModel] = useState('gpt-4.1');

  // Text Analysis State
  const [textInput, setTextInput] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

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
        
        // Auto-select first options
        if (frameworks.length > 0) setSelectedFramework(frameworks[0].id);
        if (prompts.length > 0) setSelectedPrompt(prompts[0].id);
        if (algorithms.length > 0) setSelectedAlgorithm(algorithms[0].id);

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

  // Handle text analysis
  const handleAnalyze = async () => {
    if (!textInput.trim()) {
      alert('Please enter text to analyze');
      return;
    }
    if (!selectedFramework || !selectedPrompt || !selectedAlgorithm) {
      alert('Please select all configuration options');
      return;
    }

    setAnalyzing(true);
    setAnalysisError(null);
    setAnalysisResult(null);

    try {
      console.log('🔄 Starting analysis...', { 
        text: textInput.substring(0, 50) + '...',
        framework: selectedFramework,
        prompt: selectedPrompt,
        algorithm: selectedAlgorithm,
        model: selectedModel
      });

      const result = await apiService.analyzeSingleText({
        text_content: textInput,
        prompt_template_id: selectedPrompt,
        framework_config_id: selectedFramework,
        scoring_algorithm_id: selectedAlgorithm,
        llm_model: selectedModel,
        include_justifications: true,
        include_hierarchical_ranking: true
      });

      console.log('✅ Analysis completed:', result);
      setAnalysisResult(result);
      
    } catch (error: any) {
      console.error('❌ Analysis failed:', error);
      setAnalysisError(error.message || 'Analysis failed');
    } finally {
      setAnalyzing(false);
    }
  };

  // Loading state
  if (loading) {
    return (
      <div className="p-6" data-testid="experiment-designer-loading">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">🧪 Experiment Designer</h2>
        <div className="flex items-center justify-center p-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <span className="ml-4 text-gray-600">Loading configuration...</span>
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
      <h2 className="text-2xl font-bold text-gray-900 mb-6">🧪 Experiment Designer</h2>
      
      {/* Configuration Section */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-4">📋 Analysis Configuration</h3>
        
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Framework ({configData.frameworks.length} available)
            </label>
            <select 
              value={selectedFramework}
              onChange={(e) => setSelectedFramework(e.target.value)}
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
              value={selectedPrompt}
              onChange={(e) => setSelectedPrompt(e.target.value)}
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
              Scoring Algorithm ({configData.algorithms.length} available)
            </label>
            <select 
              value={selectedAlgorithm}
              onChange={(e) => setSelectedAlgorithm(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2"
              data-testid="algorithm-select"
            >
              <option value="">Select Algorithm...</option>
              {configData.algorithms.map(alg => (
                <option key={alg.id} value={alg.id}>
                  {alg.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              LLM Model
            </label>
            <select 
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2"
              data-testid="model-select"
            >
              <optgroup label="🔵 OpenAI (2025 Models)">
                <option value="gpt-4.1">GPT-4.1 (Latest - Recommended)</option>
                <option value="gpt-4.1-mini">GPT-4.1 Mini</option>
                <option value="o1">o1 (Reasoning)</option>
                <option value="o3">o3 (Advanced Reasoning)</option>
                <option value="gpt-4o">GPT-4o (Current)</option>
                <option value="gpt-4o-mini">GPT-4o Mini</option>
              </optgroup>
              
              <optgroup label="🟠 Anthropic (Claude 4 Series)">
                <option value="claude-4-opus">Claude 4 Opus (Latest - Premium)</option>
                <option value="claude-4-sonnet">Claude 4 Sonnet (Latest - Recommended)</option>
                <option value="claude-3.7-sonnet">Claude 3.7 Sonnet</option>
                <option value="claude-3.5-sonnet">Claude 3.5 Sonnet</option>
                <option value="claude-3.5-haiku">Claude 3.5 Haiku (Fast)</option>
              </optgroup>
              
              <optgroup label="🔴 Mistral AI (2025 Models)">
                <option value="mistral-large-2411">Mistral Large (November 2024 - Recommended)</option>
                <option value="mistral-small-2409">Mistral Small (Efficient)</option>
              </optgroup>
              
              <optgroup label="🟢 Google AI (Gemini 2.5 Series)">
                <option value="gemini-2.5-pro">Gemini 2.5 Pro (Latest - Deep Think)</option>
                <option value="gemini-2.5-flash">Gemini 2.5 Flash (Latest - Adaptive)</option>
                <option value="gemini-2.0-flash">Gemini 2.0 Flash</option>
                <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
              </optgroup>
              
              <optgroup label="🌟 Open Source (Latest)">
                <option value="deepseek-r1">DeepSeek R1 (Reasoning)</option>
                <option value="qwen3-235b">Qwen3 235B (Latest)</option>
                <option value="llama-4-scout">Llama 4 Scout (10M Context)</option>
                <option value="llama-3.3-70b">Llama 3.3 70B</option>
              </optgroup>
              
              <optgroup label="📖 Legacy Models">
                <option value="gpt-4">GPT-4 (Legacy)</option>
                <option value="gpt-3.5-turbo">GPT-3.5 Turbo (Legacy)</option>
                <option value="claude-3-sonnet">Claude 3 Sonnet (Legacy)</option>
                <option value="claude-3-haiku">Claude 3 Haiku (Legacy)</option>
              </optgroup>
            </select>
            <div className="text-xs text-gray-500 mt-1">
              💡 Recommended: GPT-4.1, Claude 4 Sonnet, or Mistral Large for narrative analysis
            </div>
          </div>
        </div>

        <div className="bg-blue-50 p-3 rounded text-sm">
          <strong>Configuration Status:</strong> {
            selectedFramework && selectedPrompt && selectedAlgorithm 
              ? '✅ Ready for analysis'
              : '⚠️ Please select all options'
          }
        </div>
      </div>

      {/* Text Input Section */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-4">📝 Text Analysis</h3>
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Text to Analyze
          </label>
          <textarea
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            placeholder="Enter the text you want to analyze for narrative gravity wells..."
            rows={6}
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
          disabled={analyzing || !textInput.trim() || !selectedFramework}
          className={`px-6 py-3 rounded-md font-semibold ${
            analyzing || !textInput.trim() || !selectedFramework
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }`}
          data-testid="analyze-button"
        >
          {analyzing ? '🔄 Analyzing...' : '🚀 Analyze Text'}
        </button>
      </div>

      {/* Results Section */}
      {analysisResult && (
        <div className="mb-8" data-testid="analysis-results">
          <h3 className="text-lg font-semibold mb-4">📊 Analysis Results</h3>
          
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
            <h4 className="font-semibold text-green-900 mb-2">✅ Analysis Complete</h4>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <strong>Model:</strong> {analysisResult.model}
              </div>
              <div>
                <strong>Framework:</strong> {analysisResult.framework}
              </div>
              <div>
                <strong>Execution Time:</strong> {analysisResult.duration_seconds?.toFixed(2)}s
              </div>
              <div>
                <strong>API Cost:</strong> ${analysisResult.api_cost?.toFixed(4)}
              </div>
            </div>
          </div>

          {/* Raw Scores */}
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

          {/* Calculated Metrics */}
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

          {/* Dominant Wells */}
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
        </div>
      )}
    </div>
  );
};

export default ExperimentDesigner; 