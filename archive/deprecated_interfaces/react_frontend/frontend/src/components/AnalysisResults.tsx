import React, { useState, useEffect } from 'react';
import { useExperimentStore, AnalysisResult } from '../store/experimentStore';
import apiService from '../services/apiClient';

const AnalysisResults: React.FC = () => {
  const {
    analysis_results,
    pinned_result_ids,
    togglePinResult,
    setAnalysisResults
  } = useExperimentStore();

  // Enhanced filtering for multi-model and hierarchical results
  const [filterMode, setFilterMode] = useState<'all' | 'hierarchical' | 'multi_model'>('all');
  const [showStabilityMetrics, setShowStabilityMetrics] = useState(false);
  const [expandedJustifications, setExpandedJustifications] = useState<Record<string, boolean>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch analysis results when component mounts
  useEffect(() => {
    const fetchAnalysisResults = async () => {
      try {
        setLoading(true);
        setError(null);
        console.log('🔄 Fetching analysis results from API...');
        
        const results = await apiService.getAnalysisResults();
        console.log('✅ Fetched', results.length, 'analysis results');
        
        // Convert API results to store format
        const convertedResults: AnalysisResult[] = results.map((result) => ({
          id: result.analysis_id,
          experiment_id: 'single-text-analysis', // Since these are single text analyses
          text_id: result.analysis_id,
          text_content: result.text_content,
          llm_model: result.model,
          llm_version: 'latest',
          raw_scores: result.raw_scores,
          well_justifications: result.well_justifications,
          calculated_metrics: result.calculated_metrics,
          execution_time: result.execution_time,
          complete_provenance: {
            prompt_template_hash: 'api-result',
            framework_version: result.framework,
            scoring_algorithm_version: 'api-result',
            llm_model: result.model,
            timestamp: result.execution_time
          },
          is_pinned: false
        }));
        
        // Update store with fetched results
        setAnalysisResults(convertedResults);
        
      } catch (err: any) {
        console.error('❌ Failed to fetch analysis results:', err);
        setError(err.message || 'Failed to load analysis results');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysisResults();
  }, []); // Empty dependency array means this runs once when component mounts

  // Group multi-model results for comparison (temporarily disabled)
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const groupedResults = {} as Record<string, typeof analysis_results>;

  const filteredResults = analysis_results.filter((_result) => {
    // All filters temporarily disabled due to interface mismatch
    return true;
  });

  // Toggle justification expansion
  const toggleJustification = (resultId: string, wellName: string) => {
    const key = `${resultId}-${wellName}`;
    setExpandedJustifications(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  // Bar Chart Component
  const BarChart: React.FC<{ scores: Record<string, number> }> = ({ scores }) => {
    const maxScore = Math.max(...Object.values(scores));
    const sortedScores = Object.entries(scores).sort(([,a], [,b]) => b - a);

    return (
      <div className="space-y-2">
        {sortedScores.map(([well, score]) => (
          <div key={well} className="flex items-center space-x-3">
            <div className="w-20 text-sm font-medium text-gray-700 text-right">
              {well}
            </div>
            <div className="flex-1 h-6 bg-gray-200 rounded-full overflow-hidden">
              <div 
                className={`h-full rounded-full transition-all duration-300 ${
                  score > 0.6 ? 'bg-green-500' :
                  score > 0.4 ? 'bg-yellow-500' : 'bg-red-500'
                }`}
                style={{ width: `${(score / maxScore) * 100}%` }}
              />
            </div>
            <div className="w-12 text-sm font-mono text-gray-600">
              {score.toFixed(2)}
            </div>
          </div>
        ))}
      </div>
    );
  };

  // Justification Display Component
  const JustificationDisplay: React.FC<{ 
    resultId: string;
    wellName: string; 
    justification: any; 
    expanded: boolean; 
  }> = ({ resultId, wellName, justification, expanded }) => {
    if (!justification) return null;

    return (
      <div className="mt-2 p-3 bg-gray-50 rounded-md border-l-4 border-blue-200">
        <div className="flex items-center justify-between mb-2">
          <h5 className="text-sm font-medium text-gray-800">{wellName}</h5>
          <div className="flex items-center space-x-2">
            <span className="text-xs text-gray-500">
              Confidence: {(justification.confidence * 100).toFixed(0)}%
            </span>
            <button
              onClick={() => toggleJustification(resultId, wellName)}
              className="text-xs text-blue-600 hover:text-blue-800"
            >
              {expanded ? 'Hide' : 'Show'} Details
            </button>
          </div>
        </div>
        
        {expanded && (
          <div className="space-y-3">
            <div>
              <p className="text-sm text-gray-700 mb-2">
                <strong>Reasoning:</strong> {justification.reasoning}
              </p>
            </div>
            
            {justification.evidence_quotes && justification.evidence_quotes.length > 0 && (
              <div>
                <p className="text-xs font-medium text-gray-600 mb-2">Evidence Quotes:</p>
                <ul className="space-y-1">
                  {justification.evidence_quotes.map((quote: string, idx: number) => (
                    <li key={idx} className="text-xs text-gray-600 pl-3 border-l-2 border-gray-300">
                      "{quote}"
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  // Enhanced result rendering
  const renderAnalysisResult = (result: AnalysisResult, index: number) => {
    const isHierarchical = false; // result.complete_provenance.prompt_type === 'hierarchical';
    const isMultiModel = false; // result.complete_provenance.is_multi_model;
    
    // Get top 3 scoring wells for summary
    const topWells = Object.entries(result.raw_scores)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3);
    
    return (
      <div key={result.id} className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm" data-testid="analysis-result-card">
        {/* Header with basic metadata */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-2">
              <h3 className="text-lg font-medium text-gray-900">
                Analysis Result #{index + 1}
              </h3>
              
              {/* Basic badges */}
              {isHierarchical && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                  Hierarchical
                </span>
              )}
              
              {isMultiModel && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  Multi-Model
                </span>
              )}
            </div>
            
            <p className="text-sm text-gray-600 mb-2">
              Model: <span className="font-medium">{result.llm_model}</span> • 
              Time: {new Date(result.execution_time).toLocaleString()}
            </p>

            {/* Top 3 Wells Summary */}
            <div className="flex items-center space-x-4 text-sm">
              <span className="text-gray-500">Top scoring wells:</span>
              {topWells.map(([well, score], idx) => (
                <span key={well} className="font-medium">
                  {well} ({score.toFixed(2)})
                  {idx < topWells.length - 1 && ', '}
                </span>
              ))}
            </div>
          </div>
          
          <button
            onClick={() => togglePinResult(result.id)}
            className={`px-3 py-1 rounded-md text-sm ${
              pinned_result_ids.includes(result.id)
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {pinned_result_ids.includes(result.id) ? 'Pinned' : 'Pin'}
          </button>
        </div>

        {/* Basic metrics display */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div>
            <dt className="text-sm font-medium text-gray-500">Elevation</dt>
            <dd className="mt-1 text-lg font-semibold text-gray-900">
              {result.calculated_metrics.narrative_elevation.toFixed(3)}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Polarity</dt>
            <dd className="mt-1 text-lg font-semibold text-gray-900">
              {result.calculated_metrics.polarity.toFixed(3)}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Coherence</dt>
            <dd className="mt-1 text-lg font-semibold text-gray-900">
              {result.calculated_metrics.coherence.toFixed(3)}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Purity</dt>
            <dd className="mt-1 text-lg font-semibold text-gray-900">
              {result.calculated_metrics.directional_purity.toFixed(3)}
            </dd>
          </div>
        </div>

        {/* Enhanced scores display with bar chart */}
        <div className="mb-6">
          <h4 className="text-md font-medium text-gray-900 mb-4">All Well Scores</h4>
          <BarChart scores={result.raw_scores} />
        </div>

        {/* Justification Display */}
        {result.well_justifications && (
          <div className="mb-6">
            <h4 className="text-md font-medium text-gray-900 mb-3">
              LLM Justifications ({Object.keys(result.well_justifications).length} wells)
            </h4>
            <div className="space-y-2">
              {Object.entries(result.well_justifications).map(([wellName, justification]) => (
                <JustificationDisplay
                  key={wellName}
                  resultId={result.id}
                  wellName={wellName}
                  justification={justification}
                  expanded={expandedJustifications[`${result.id}-${wellName}`] || false}
                />
              ))}
            </div>
          </div>
        )}

        {/* Text content preview */}
        <div className="border-t pt-4">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Text Content</h4>
          <p className="text-sm text-gray-600 bg-gray-50 p-3 rounded-md">
            {result.text_content.substring(0, 300)}
            {result.text_content.length > 300 && '...'}
          </p>
        </div>
      </div>
    );
  };

  // Loading state
  if (loading) {
    return (
      <div className="p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Analysis Results</h2>
        <div className="flex items-center justify-center p-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <span className="ml-4 text-gray-600">Loading analysis results...</span>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Analysis Results</h2>
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <strong>Error:</strong> {error}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6" data-testid="analysis-results-container">
      {/* Basic filter controls */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h2 className="text-xl font-semibold text-gray-900">Analysis Results</h2>
          
          <div className="flex items-center space-x-2">
            <select
              value={filterMode}
              onChange={(e) => setFilterMode(e.target.value as any)}
              className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Results</option>
              <option value="hierarchical">Hierarchical Only (Coming Soon)</option>
              <option value="multi_model">Multi-Model Only (Coming Soon)</option>
            </select>
            
            {Object.keys(groupedResults).length > 0 && (
              <button
                onClick={() => setShowStabilityMetrics(!showStabilityMetrics)}
                className="px-3 py-1 bg-blue-100 text-blue-800 rounded-md text-sm hover:bg-blue-200"
              >
                {showStabilityMetrics ? 'Hide' : 'Show'} Stability Metrics
              </button>
            )}
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <button
            onClick={() => {
              setLoading(true);
              setError(null);
              apiService.getAnalysisResults().then(results => {
                const convertedResults: AnalysisResult[] = results.map((result) => ({
                  id: result.analysis_id,
                  experiment_id: 'single-text-analysis',
                  text_id: result.analysis_id,
                  text_content: result.text_content,
                  llm_model: result.model,
                  llm_version: 'latest',
                  raw_scores: result.raw_scores,
                  well_justifications: result.well_justifications,
                  calculated_metrics: result.calculated_metrics,
                  execution_time: result.execution_time,
                  complete_provenance: {
                    prompt_template_hash: 'api-result',
                    framework_version: result.framework,
                    scoring_algorithm_version: 'api-result',
                    llm_model: result.model,
                    timestamp: result.execution_time
                  },
                  is_pinned: false
                }));
                setAnalysisResults(convertedResults);
                setLoading(false);
              }).catch(err => {
                setError(err.message);
                setLoading(false);
              });
            }}
            className="px-3 py-1 bg-blue-100 text-blue-800 rounded-md text-sm hover:bg-blue-200"
            data-testid="refresh-results-button"
          >
            🔄 Refresh
          </button>
          <div className="text-sm text-gray-600">
            {filteredResults.length} results • {pinned_result_ids.length} pinned
          </div>
        </div>
      </div>

      {/* Multi-model stability metrics (simplified) */}
      {showStabilityMetrics && Object.keys(groupedResults).length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="text-md font-medium text-blue-900 mb-3">Multi-Model Stability Assessment</h3>
          <p className="text-sm text-blue-700">Coming soon - interface updates in progress</p>
        </div>
      )}

      {/* Results display */}
      {filteredResults.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No analysis results yet. Run an experiment to see results here.</p>
        </div>
      ) : (
        <div className="space-y-6" data-testid="analysis-results-list">
          {filteredResults.map(renderAnalysisResult)}
        </div>
      )}
    </div>
  );
};

export default AnalysisResults; 