import React, { useState, useMemo, useCallback } from 'react';
import { useExperimentStore } from '../store/experimentStore';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const ComparisonDashboard: React.FC = () => {
  const {
    analysis_results,
    experiments,
    pinned_result_ids,
    createComparisonSet,
    comparison_sets
  } = useExperimentStore();

  const [selectedResults, setSelectedResults] = useState<string[]>([]);
  const [comparisonName, setComparisonName] = useState('');
  const [activeComparison, setActiveComparison] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'side-by-side' | 'overlay' | 'statistical'>('side-by-side');

  // Get pinned results for easy comparison
  const pinnedResults = analysis_results.filter(r => pinned_result_ids.includes(r.id));

  const getExperimentName = useCallback((experimentId: string) => {
    const experiment = experiments.find(e => e.id === experimentId);
    return experiment?.name || 'Unknown';
  }, [experiments]);

  // Calculate statistical metrics for comparison
  const comparisonStats = useMemo(() => {
    if (selectedResults.length < 2) return null;

    const results = analysis_results.filter(r => selectedResults.includes(r.id));
    
    // Calculate hierarchy sharpness metrics
    const hierarchySharpness = results.map(result => {
      const scores = Object.values(result.raw_scores);
      const mean = scores.reduce((a, b) => a + b, 0) / scores.length;
      const variance = scores.reduce((sum, score) => sum + Math.pow(score - mean, 2), 0) / scores.length;
      const coefficientOfVariation = Math.sqrt(variance) / mean;
      
      // Dominance ratio: ratio of highest to second highest score
      const sortedScores = [...scores].sort((a, b) => b - a);
      const dominanceRatio = sortedScores[0] / (sortedScores[1] || 0.01);
      
      return {
        result_id: result.id,
        coefficient_of_variation: coefficientOfVariation,
        dominance_ratio: dominanceRatio,
        max_score: Math.max(...scores),
        min_score: Math.min(...scores),
        score_range: Math.max(...scores) - Math.min(...scores)
      };
    });

    // Calculate correlations between results
    const correlations: Array<{pair: string, correlation: number}> = [];
    for (let i = 0; i < results.length; i++) {
      for (let j = i + 1; j < results.length; j++) {
        const scores1 = Object.values(results[i].raw_scores);
        const scores2 = Object.values(results[j].raw_scores);
        
        // Pearson correlation coefficient
        const n = scores1.length;
        const sum1 = scores1.reduce((a, b) => a + b, 0);
        const sum2 = scores2.reduce((a, b) => a + b, 0);
        const sum1Sq = scores1.reduce((sum, x) => sum + x * x, 0);
        const sum2Sq = scores2.reduce((sum, x) => sum + x * x, 0);
        const pSum = scores1.reduce((sum, x, idx) => sum + x * scores2[idx], 0);
        
        const num = pSum - (sum1 * sum2 / n);
        const den = Math.sqrt((sum1Sq - sum1 * sum1 / n) * (sum2Sq - sum2 * sum2 / n));
        const correlation = den === 0 ? 0 : num / den;
        
        correlations.push({
          pair: `${getExperimentName(results[i].experiment_id)} vs ${getExperimentName(results[j].experiment_id)}`,
          correlation
        });
      }
    }

         return {
       hierarchy_sharpness: hierarchySharpness,
       correlations,
       sample_size: results.length
     };
   }, [selectedResults, analysis_results, getExperimentName]);

  const handleToggleResult = (resultId: string) => {
    setSelectedResults(prev => 
      prev.includes(resultId) 
        ? prev.filter(id => id !== resultId)
        : prev.length < 4 ? [...prev, resultId] : prev // Limit to 4 for readability
    );
  };

  const handleCreateComparison = () => {
    if (!comparisonName.trim() || selectedResults.length < 2) {
      alert('Please provide a name and select at least 2 results to compare');
      return;
    }

    const comparisonId = createComparisonSet(comparisonName, selectedResults);
    setActiveComparison(comparisonId);
    setComparisonName('');
    alert('Comparison set created!');
  };

  const handleLoadComparison = (comparisonId: string) => {
    const comparison = comparison_sets.find(c => c.id === comparisonId);
    if (comparison) {
      setSelectedResults(comparison.result_ids);
      setActiveComparison(comparisonId);
    }
  };

  const prepareComparisonData = () => {
    if (selectedResults.length === 0) return [];

    const results = analysis_results.filter(r => selectedResults.includes(r.id));
    const wells = results.length > 0 ? Object.keys(results[0].raw_scores) : [];

    return wells.map(well => {
      const dataPoint: any = { well };
      results.forEach((result, index) => {
        const experimentName = getExperimentName(result.experiment_id);
        dataPoint[`exp_${index}`] = (result.raw_scores[well] * 100).toFixed(1);
        dataPoint[`exp_${index}_name`] = experimentName;
      });
      return dataPoint;
    });
  };

  const prepareMetricsComparison = () => {
    if (selectedResults.length === 0) return [];

    const results = analysis_results.filter(r => selectedResults.includes(r.id));
    
    return results.map((result, index) => ({
      experiment: getExperimentName(result.experiment_id),
      narrative_elevation: (result.calculated_metrics.narrative_elevation * 100).toFixed(1),
      polarity: result.calculated_metrics.polarity.toFixed(2),
      coherence: (result.calculated_metrics.coherence * 100).toFixed(1),
      directional_purity: (result.calculated_metrics.directional_purity * 100).toFixed(1),
      index
    }));
  };

  const selectedResultsData = analysis_results.filter(r => selectedResults.includes(r.id));

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              View Mode
            </label>
            <select
              value={viewMode}
              onChange={(e) => setViewMode(e.target.value as any)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="side-by-side">Side-by-Side</option>
              <option value="overlay">Overlay Charts</option>
              <option value="statistical">Statistical Analysis</option>
            </select>
          </div>

          <div className="text-sm text-gray-600">
            {selectedResults.length} of 4 results selected
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <input
            type="text"
            value={comparisonName}
            onChange={(e) => setComparisonName(e.target.value)}
            placeholder="Comparison set name..."
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleCreateComparison}
            disabled={selectedResults.length < 2 || !comparisonName.trim()}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
          >
            Save Comparison
          </button>
        </div>
      </div>

      {/* Saved Comparisons */}
      {comparison_sets.length > 0 && (
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="font-medium text-gray-900 mb-3">Saved Comparison Sets</h3>
          <div className="flex flex-wrap gap-2">
            {comparison_sets.map(comparison => (
              <button
                key={comparison.id}
                onClick={() => handleLoadComparison(comparison.id)}
                className={`px-3 py-1 text-sm rounded ${
                  activeComparison === comparison.id
                    ? 'bg-blue-600 text-white'
                    : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
                }`}
              >
                {comparison.name} ({comparison.result_ids.length})
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Results Selection */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pinned Results */}
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-3">
            Pinned Results ({pinnedResults.length})
          </h3>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {pinnedResults.length === 0 ? (
              <p className="text-gray-500 text-sm">No pinned results. Pin results from the Analysis Results tab.</p>
            ) : (
              pinnedResults.map(result => (
                <div
                  key={result.id}
                  className={`p-3 border rounded-md cursor-pointer transition-colors ${
                    selectedResults.includes(result.id)
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => handleToggleResult(result.id)}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-medium text-gray-900 text-sm">
                        {getExperimentName(result.experiment_id)}
                      </h4>
                      <p className="text-xs text-gray-600 mt-1">
                        {result.text_content.substring(0, 60)}...
                      </p>
                      <div className="flex items-center space-x-3 mt-1 text-xs">
                        <span className="text-green-600">
                          Elev: {(result.calculated_metrics.narrative_elevation * 100).toFixed(1)}%
                        </span>
                        <span className="text-blue-600">
                          Pol: {result.calculated_metrics.polarity.toFixed(2)}
                        </span>
                      </div>
                    </div>
                    <div className="text-xs text-gray-500">
                      {selectedResults.includes(result.id) ? '✓' : '○'}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* All Results */}
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-3">
            All Results ({analysis_results.length})
          </h3>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {analysis_results.map(result => (
              <div
                key={result.id}
                className={`p-3 border rounded-md cursor-pointer transition-colors ${
                  selectedResults.includes(result.id)
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => handleToggleResult(result.id)}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-medium text-gray-900 text-sm">
                      {getExperimentName(result.experiment_id)}
                    </h4>
                    <p className="text-xs text-gray-600 mt-1">
                      {result.text_content.substring(0, 60)}...
                    </p>
                    <div className="flex items-center space-x-3 mt-1 text-xs">
                      <span className="text-green-600">
                        Elev: {(result.calculated_metrics.narrative_elevation * 100).toFixed(1)}%
                      </span>
                      <span className="text-blue-600">
                        Pol: {result.calculated_metrics.polarity.toFixed(2)}
                      </span>
                    </div>
                  </div>
                  <div className="text-xs text-gray-500">
                    {selectedResults.includes(result.id) ? '✓' : '○'}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Comparison Visualization */}
      {selectedResults.length >= 2 && (
        <div className="border-t pt-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Comparative Analysis ({selectedResults.length} experiments)
          </h3>

          {viewMode === 'side-by-side' && (
            <div className="space-y-6">
              {/* Wells Comparison */}
              <div>
                <h4 className="font-medium text-gray-900 mb-3">Gravity Wells Scores Comparison</h4>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={prepareComparisonData()}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="well" 
                      angle={-45}
                      textAnchor="end"
                      height={80}
                      fontSize={12}
                    />
                    <YAxis 
                      domain={[0, 100]}
                      label={{ value: 'Score (%)', angle: -90, position: 'insideLeft' }}
                    />
                    <Tooltip />
                    {selectedResultsData.map((result, index) => (
                      <Bar 
                        key={result.id}
                        dataKey={`exp_${index}`}
                        name={getExperimentName(result.experiment_id)}
                        fill={`hsl(${index * 60}, 70%, 50%)`}
                      />
                    ))}
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Metrics Comparison */}
              <div>
                <h4 className="font-medium text-gray-900 mb-3">Calculated Metrics Comparison</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {prepareMetricsComparison().map((data, index) => (
                    <div key={index} className="bg-white border rounded-lg p-4">
                      <h5 className="font-medium text-gray-900 mb-3 text-sm">
                        {data.experiment}
                      </h5>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span>Elevation:</span>
                          <span className="font-medium text-green-600">{data.narrative_elevation}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Polarity:</span>
                          <span className="font-medium text-blue-600">{data.polarity}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Coherence:</span>
                          <span className="font-medium text-purple-600">{data.coherence}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Dir. Purity:</span>
                          <span className="font-medium text-orange-600">{data.directional_purity}%</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {viewMode === 'statistical' && comparisonStats && (
            <div className="space-y-6">
              {/* Hierarchy Sharpness Analysis */}
              <div>
                <h4 className="font-medium text-gray-900 mb-3">Hierarchy Sharpness Metrics</h4>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Experiment
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Coefficient of Variation
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Dominance Ratio
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Score Range
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {comparisonStats.hierarchy_sharpness.map((stat, _index) => {
                        const result = analysis_results.find(r => r.id === stat.result_id);
                        return (
                          <tr key={stat.result_id}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                              {result ? getExperimentName(result.experiment_id) : 'Unknown'}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {stat.coefficient_of_variation.toFixed(3)}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {stat.dominance_ratio.toFixed(2)}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {stat.score_range.toFixed(3)}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Correlation Analysis */}
              <div>
                <h4 className="font-medium text-gray-900 mb-3">Score Correlations</h4>
                <div className="space-y-2">
                  {comparisonStats.correlations.map((corr, index) => (
                    <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                      <span className="text-sm text-gray-700">{corr.pair}</span>
                      <span className={`text-sm font-medium ${
                        Math.abs(corr.correlation) > 0.7 ? 'text-green-600' :
                        Math.abs(corr.correlation) > 0.4 ? 'text-yellow-600' : 'text-red-600'
                      }`}>
                        r = {corr.correlation.toFixed(3)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {selectedResults.length === 0 && (
        <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <p className="text-gray-500">
            Select 2 or more analysis results to begin comparative analysis
          </p>
        </div>
      )}
    </div>
  );
};

export default ComparisonDashboard; 