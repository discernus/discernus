import { useState, Suspense, lazy } from 'react';
import './index.css';
import DebugConsole from './components/DebugConsole';
import { debugMonitor } from './services/debugMonitor';

// Lazy load components with error boundaries
const ExperimentDesigner = lazy(() => import('./components/ExperimentDesigner').catch(() => ({
  default: () => <div className="p-6"><h2 className="text-xl font-semibold text-gray-900 mb-4">🧪 Experiment Designer</h2><p className="text-red-600">Component failed to load</p></div>
})));

const PromptEditor = lazy(() => import('./components/PromptEditor').catch(() => ({
  default: () => <div className="p-6"><h2 className="text-xl font-semibold text-gray-900 mb-4">✏️ Prompt Editor</h2><p className="text-red-600">Component failed to load</p></div>
})));

const AnalysisResults = lazy(() => import('./components/AnalysisResults').catch(() => ({
  default: () => <div className="p-6"><h2 className="text-xl font-semibold text-gray-900 mb-4">📊 Analysis Results</h2><p className="text-red-600">Component failed to load</p></div>
})));

const ComparisonDashboard = lazy(() => import('./components/ComparisonDashboard').catch(() => ({
  default: () => <div className="p-6"><h2 className="text-xl font-semibold text-gray-900 mb-4">⚖️ Compare Experiments</h2><p className="text-red-600">Component failed to load</p></div>
})));

function App() {
  const [activeTab, setActiveTab] = useState('designer');

  // Track user actions for debugging
  const handleTabChange = (tabId: string) => {
    debugMonitor.logUserAction(`Tab changed to ${tabId}`, { tabId, previousTab: activeTab });
    setActiveTab(tabId);
  };

  const tabs = [
    { id: 'designer', name: 'Experiment Designer', icon: '🧪' },
    { id: 'prompts', name: 'Prompt Editor', icon: '✏️' },
    { id: 'results', name:'Analysis Results', icon: '📊' },
    { id: 'comparison', name: 'Compare Experiments', icon: '⚖️' }
  ];

  const renderTabContent = () => {
    const LoadingFallback = () => (
      <div className="p-6 text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading component...</p>
      </div>
    );

    return (
      <Suspense fallback={<LoadingFallback />}>
        <div>
          {activeTab === 'designer' && <ExperimentDesigner />}
          {activeTab === 'prompts' && <PromptEditor />}
          {activeTab === 'results' && <AnalysisResults />}
          {activeTab === 'comparison' && <ComparisonDashboard />}
        </div>
      </Suspense>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">NG</span>
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">Narrative Gravity Research Workbench</h1>
                <p className="text-sm text-gray-500">v2.1 Phase 1 Research Workbench</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">
                <span className="font-medium">Stable</span>
              </div>
              <div className="w-2 h-2 bg-green-400 rounded-full" title="Connected"></div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => handleTabChange(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.name}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-sm border">
          {renderTabContent()}
        </div>
      </main>

      {/* Debug Info */}
      <div className="fixed bottom-4 right-4 bg-black bg-opacity-75 text-white p-3 rounded-lg text-xs">
        <div>✅ v2.1 Phase 1 Active</div>
        <div>Active Tab: {activeTab}</div>
        <div>Features: Hierarchical prompts, Multi-model comparison, Nonlinear scoring</div>
        <div>Build: {new Date().toLocaleTimeString()}</div>
      </div>

      {/* Debug Console */}
      <DebugConsole />
    </div>
  );
}

export default App;
