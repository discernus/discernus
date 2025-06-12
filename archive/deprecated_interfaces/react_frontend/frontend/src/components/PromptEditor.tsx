import React, { useState, useEffect } from 'react';
import { useExperimentStore } from '../store/experimentStore';

// Interface definitions for structured editing
interface PromptComponent {
  id: string;
  name: string;
  content: string;
  required: boolean;
  order: number;
}

interface PromptTemplateStructure {
  header: PromptComponent;
  role_definition: PromptComponent;
  scoring_requirements: PromptComponent;
  analysis_methodology: PromptComponent;
  hierarchical_requirements: PromptComponent;
  response_format: PromptComponent;
  instructions: PromptComponent;
  framework_fit_assessment: PromptComponent;
}

interface VersionInfo {
  version: string;
  created_at: string;
  description: string;
}

const PromptEditor: React.FC = () => {
  const { 
    prompt_templates, 
    framework_configs,
    addPromptTemplate,
    updatePromptTemplate,
    updateFrameworkConfig
  } = useExperimentStore();

  // Tab management
  const [activeTab, setActiveTab] = useState<'template' | 'framework' | 'review'>('template');
  
  // Template editing state
  const [selectedPromptId, setSelectedPromptId] = useState<string>('');
  const [selectedVersion, setSelectedVersion] = useState<string>('');
  const [promptStructure, setPromptStructure] = useState<PromptTemplateStructure | null>(null);
  
  // Framework editing state  
  const [selectedFrameworkId, setSelectedFrameworkId] = useState<string>('');
  const [editingFramework, setEditingFramework] = useState<any>(null);
  
  // UI state
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editMode, setEditMode] = useState<'view' | 'edit'>('view');
  const [newPromptForm, setNewPromptForm] = useState({
    name: '',
    version: '1.0.0', 
    description: ''
  });

  // Initialize default selections
  useEffect(() => {
    if (prompt_templates.length > 0 && !selectedPromptId) {
      setSelectedPromptId(prompt_templates[0].id);
      setSelectedVersion(prompt_templates[0].version);
    }
    if (framework_configs.length > 0 && !selectedFrameworkId) {
      setSelectedFrameworkId(framework_configs[0].id);
      setEditingFramework(JSON.parse(JSON.stringify(framework_configs[0])));
    }
  }, [prompt_templates, framework_configs]);

  // Parse content into structured components
  const parsePromptContent = (_content: string): PromptTemplateStructure => {
    // Parse the existing prompt content into discrete components
    // TODO: Implement actual parsing of existing content
    
    return {
      header: {
        id: 'header',
        name: 'Prompt Header & Version',
        content: '# Narrative Gravity Wells Analysis Prompt\n**Version:** v2.1 Phase 1 - Hierarchical Analysis Framework',
        required: true,
        order: 1
      },
      role_definition: {
        id: 'role_definition', 
        name: 'Expert Role Definition',
        content: 'You are an expert political narrative analyst specializing in narrative gravity wells analysis. Analyze the provided text using the narrative gravity wells framework with **hierarchical dominance assessment**.',
        required: true,
        order: 2
      },
      scoring_requirements: {
        id: 'scoring_requirements',
        name: 'Critical Scoring Requirements',
        content: '🚨 **MANDATORY DECIMAL SCALE: 0.0 to 1.0 ONLY** 🚨\n- Use ONLY decimal values between 0.0 and 1.0 (e.g., 0.3, 0.7, 0.9)\n- DO NOT use integers 1-10 or any other scale\n- DO NOT use percentages or any scale other than 0.0-1.0\n- Example valid scores: 0.1, 0.4, 0.6, 0.8, 1.0\n- Example INVALID scores: 1, 5, 10, 25%, 0.5/1.0',
        required: true,
        order: 3
      },
      analysis_methodology: {
        id: 'analysis_methodology',
        name: 'Analysis Approach & Methodology',
        content: '**ANALYSIS APPROACH**\n\n**PART 1: INDIVIDUAL WELL SCORING**\nScore each well from 0.0 to 1.0 based on:\n- **Conceptual strength** (not keyword frequency)\n- **Thematic centrality** to the narrative structure\n- **Semantic importance** in shaping the overall argument',
        required: true,
        order: 4
      },
      hierarchical_requirements: {
        id: 'hierarchical_requirements',
        name: 'Hierarchical Ranking Requirements (v2.1)',
        content: '**PART 2: HIERARCHICAL RANKING (CRITICAL - v2.1 FEATURE)**\nAfter scoring all wells, identify and rank the **TOP 2-3 DRIVING WELLS** that most powerfully shape this narrative:\n\n1. **PRIMARY WELL** (most dominant): [Well name] - Weight: [percentage 40-70%]\n2. **SECONDARY WELL** (significant influence): [Well name] - Weight: [percentage 20-40%]\n3. **TERTIARY WELL** (if applicable): [Well name] - Weight: [percentage 10-30%]\n\n**HIERARCHICAL REQUIREMENTS:**\n- Weights must sum to 100% across your selected driving wells\n- Provide specific textual evidence for each ranked well\n- Explain WHY each well dominates over others\n- If one well is overwhelmingly dominant (>80%), flag as "SINGLE-WELL DOMINANCE"',
        required: true,
        order: 5
      },
      framework_fit_assessment: {
        id: 'framework_fit_assessment',
        name: 'Framework Fit Assessment',
        content: '**PART 3: FRAMEWORK FIT ASSESSMENT**\nRate how well this text fits the current framework: [0.0-1.0]\n- If fit score < 0.7, identify what thematic dimensions are missing\n- Note any wells that seem inadequate for capturing the text\'s themes',
        required: true,
        order: 6
      },
      response_format: {
        id: 'response_format',
        name: 'JSON Response Format Specification',
        content: 'Provide your analysis in **JSON format** with the following structure:\n\n```json\n{\n  "individual_scores": {\n    "Well1": 0.0,\n    "Well2": 0.0,\n    [...all framework wells]\n  },\n  "hierarchical_ranking": {\n    "primary_well": {\n      "name": "WellName",\n      "weight": 0.60,\n      "evidence": "Specific textual evidence showing dominance",\n      "justification": "Why this well dominates the narrative"\n    },\n    "secondary_well": {\n      "name": "WellName",\n      "weight": 0.30,\n      "evidence": "Supporting textual evidence", \n      "justification": "Why this is the second most important well"\n    },\n    "tertiary_well": {\n      "name": "WellName",\n      "weight": 0.10,\n      "evidence": "Additional textual evidence",\n      "justification": "Supporting role explanation"\n    }\n  },\n  "framework_fit": {\n    "score": 0.0,\n    "missing_dimensions": "Any thematic elements not captured by current wells",\n    "adequacy_assessment": "How well the framework captures the text\'s themes"\n  },\n  "single_well_dominance": false,\n  "analysis_summary": "Brief explanation of the narrative\'s overall thematic structure and positioning"\n}\n```',
        required: true,
        order: 7
      },
      instructions: {
        id: 'instructions',
        name: 'Final Analysis Instructions',
        content: '## ANALYSIS QUALITY STANDARDS\n\n- **Evidence-based**: All scores must be supported by specific textual references\n- **Conceptual focus**: Prioritize thematic meaning over surface-level word matching\n- **Hierarchical clarity**: Make clear distinctions between primary, secondary, and tertiary wells\n- **Framework awareness**: Consider how well the current framework captures the text\'s themes\n- **Reproducibility**: Provide enough justification that another analyst could understand your reasoning\n\nThis prompt template is designed for **v2.1 Phase 1** hierarchical analysis with multi-model stability assessment capabilities.',
        required: true,
        order: 8
      }
    };
  };

  // Load prompt structure when selection changes
  useEffect(() => {
    if (selectedPromptId) {
      const prompt = prompt_templates.find(p => p.id === selectedPromptId);
      if (prompt) {
        setPromptStructure(parsePromptContent(prompt.content));
      }
    }
  }, [selectedPromptId, prompt_templates]);

  // Get available versions for selected prompt (simulated - expand later)
  const getAvailableVersions = (promptId: string): VersionInfo[] => {
    const prompt = prompt_templates.find(p => p.id === promptId);
    if (!prompt) return [];
    
    // For now, return current version - expand this with actual version history
    return [{
      version: prompt.version,
      created_at: prompt.created_at || new Date().toISOString(),
      description: prompt.description || 'Current version'
    }];
  };

  // Handle component content updates
  const updateComponent = (componentId: string, newContent: string) => {
    if (!promptStructure) return;
    
    setPromptStructure({
      ...promptStructure,
      [componentId]: {
        ...promptStructure[componentId as keyof PromptTemplateStructure],
        content: newContent
      }
    });
  };

  // Save structured prompt
  const saveStructuredPrompt = () => {
    if (!selectedPromptId || !promptStructure) return;
    
    // Reassemble content from components (without adding extra headers)
    const orderedComponents = Object.values(promptStructure).sort((a, b) => a.order - b.order);
    const reassembledContent = orderedComponents.map(comp => comp.content).join('\n\n');
    
    updatePromptTemplate(selectedPromptId, {
      content: reassembledContent
    });
    
    alert('Prompt template saved successfully!');
  };

  // Create new prompt template
  const handleCreatePrompt = () => {
    console.log('handleCreatePrompt called', newPromptForm);
    
    if (!newPromptForm.name.trim()) {
      alert('Please provide a prompt name');
      return;
    }

    const defaultStructure = parsePromptContent('');
    const newContent = Object.values(defaultStructure)
      .sort((a, b) => a.order - b.order)
      .map(comp => comp.content)
      .join('\n\n');

    const newTemplate = {
      name: newPromptForm.name,
      version: newPromptForm.version,
      content: newContent,
      description: newPromptForm.description,
      type: 'hierarchical' as const
    };

    console.log('Creating template:', newTemplate);
    console.log('addPromptTemplate function:', addPromptTemplate);

    try {
      addPromptTemplate(newTemplate);
      console.log('Current templates after addition:', prompt_templates.length);
      
      // Auto-select the new template
      setTimeout(() => {
        const updatedTemplates = useExperimentStore.getState().prompt_templates;
        const newTemplateInStore = updatedTemplates.find(t => t.name === newTemplate.name && t.version === newTemplate.version);
        if (newTemplateInStore) {
          setSelectedPromptId(newTemplateInStore.id);
          setSelectedVersion(newTemplateInStore.version);
          console.log('New template auto-selected:', newTemplateInStore.id);
        }
        console.log('Total templates now:', updatedTemplates.length);
      }, 100);
      
      setNewPromptForm({ name: '', version: '1.0.0', description: '' });
      setShowCreateForm(false);
      alert('New prompt template created successfully!');
      console.log('Template created successfully');
    } catch (error) {
      console.error('Error creating template:', error);
      alert('Error creating template: ' + error);
    }
  };

  // Framework editing functions (existing logic)
  const handleFrameworkSelect = (frameworkId: string) => {
    setSelectedFrameworkId(frameworkId);
    const framework = framework_configs.find(f => f.id === frameworkId);
    if (framework) {
      setEditingFramework(JSON.parse(JSON.stringify(framework)));
    }
  };

  const handleSaveFramework = () => {
    if (!selectedFrameworkId || !editingFramework) return;
    
    updateFrameworkConfig(selectedFrameworkId, editingFramework);
    alert('Framework configuration saved!');
  };



  // Tab content renderers
  const renderTemplateTab = () => (
    <div className="space-y-6">
      {/* Template Selection */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Prompt Template
          </label>
          <select
            value={selectedPromptId}
            onChange={(e) => setSelectedPromptId(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select template...</option>
            {prompt_templates.map(template => (
              <option key={template.id} value={template.id}>
                {template.name} v{template.version}
              </option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Version (Reverse Chronological)
          </label>
          <select
            value={selectedVersion}
            onChange={(e) => setSelectedVersion(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={!selectedPromptId}
          >
            {getAvailableVersions(selectedPromptId).map(version => (
              <option key={version.version} value={version.version}>
                v{version.version} - {new Date(version.created_at).toLocaleDateString()}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Create New Template Button */}
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-medium text-gray-900">Structured Template Editor</h3>
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors"
        >
          {showCreateForm ? 'Cancel' : 'Create New Template'}
        </button>
      </div>

      {/* Create New Template Form */}
      {showCreateForm && (
        <div className="bg-gray-50 p-4 rounded-md space-y-4">
          <h4 className="font-medium text-gray-900">Create New Prompt Template</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <input
              type="text"
              placeholder="Template name"
              value={newPromptForm.name}
              onChange={(e) => setNewPromptForm({...newPromptForm, name: e.target.value})}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="text"
              placeholder="Version (e.g., 1.0.0)"
              value={newPromptForm.version}
              onChange={(e) => setNewPromptForm({...newPromptForm, version: e.target.value})}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleCreatePrompt}
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
            >
              Create Template
            </button>
          </div>
          <textarea
            placeholder="Template description"
            value={newPromptForm.description}
            onChange={(e) => setNewPromptForm({...newPromptForm, description: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={2}
          />
        </div>
      )}

      {/* Structured Component Editor */}
      {promptStructure && (
        <div className="space-y-6">
                     {Object.entries(promptStructure)
             .sort(([,a], [,b]) => a.order - b.order)
             .map(([, component]) => (
              <div key={component.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-medium text-gray-900 flex items-center">
                    <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded mr-2">
                      {component.order}
                    </span>
                    {component.name}
                    {component.required && (
                      <span className="text-red-500 ml-1">*</span>
                    )}
                  </h4>
                </div>
                <textarea
                  value={component.content}
                  onChange={(e) => updateComponent(component.id, e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                  rows={Math.max(4, component.content.split('\n').length + 2)}
                />
              </div>
            ))}
          
          <div className="flex justify-end">
            <button
              onClick={saveStructuredPrompt}
              className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors"
            >
              Save Template Changes
            </button>
          </div>
        </div>
      )}
    </div>
  );

  const renderFrameworkTab = () => (
    <div className="space-y-6">
      {/* Framework Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select Framework Configuration
        </label>
        <select
          value={selectedFrameworkId}
          onChange={(e) => handleFrameworkSelect(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Select framework...</option>
          {framework_configs.map(framework => (
            <option key={framework.id} value={framework.id}>
              {framework.display_name} v{framework.version}
            </option>
          ))}
        </select>
      </div>

      {/* Edit Mode Toggle */}
      {editingFramework && (
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setEditMode('view')}
            className={`px-4 py-2 rounded-md transition-colors ${
              editMode === 'view' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            View Summary
          </button>
          <button
            onClick={() => setEditMode('edit')}
            className={`px-4 py-2 rounded-md transition-colors ${
              editMode === 'edit' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Edit Structure
          </button>
        </div>
      )}

      {/* Framework Editor Content - Using existing framework editor logic */}
      {editingFramework && editMode === 'view' && (
        <div className="bg-gray-50 p-4 rounded-md">
          <h4 className="font-medium text-gray-900 mb-3">Framework Summary</h4>
          <div className="space-y-4 text-sm">
            <div>
              <strong>Framework:</strong> {editingFramework.display_name}<br/>
              <strong>Version:</strong> {editingFramework.version}<br/>
              <strong>Description:</strong> {editingFramework.description}
            </div>
            
            <div>
              <strong>Dipoles ({editingFramework.dipoles?.length || 0}):</strong>
              <ul className="mt-2 space-y-2 ml-4">
                {editingFramework.dipoles?.map((dipole: any, i: number) => (
                  <li key={i} className="border-l-2 border-gray-300 pl-3">
                    <strong>{dipole.name}</strong>: {dipole.description}<br/>
                    <span className="text-green-700">+ {dipole.positive.name}</span> vs{' '}
                    <span className="text-red-700">- {dipole.negative.name}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {editingFramework && editMode === 'edit' && (
        <div className="space-y-6">
          {/* Framework Metadata */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Display Name</label>
              <input
                type="text"
                value={editingFramework.display_name || ''}
                onChange={(e) => setEditingFramework({
                  ...editingFramework,
                  display_name: e.target.value
                })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Version</label>
              <input
                type="text"
                value={editingFramework.version || ''}
                onChange={(e) => setEditingFramework({
                  ...editingFramework,
                  version: e.target.value
                })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              value={editingFramework.description || ''}
              onChange={(e) => setEditingFramework({
                ...editingFramework,
                description: e.target.value
              })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
            />
          </div>

          {/* Dipoles Editor */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-medium text-gray-900">Dipoles Configuration</h4>
              <button
                onClick={() => {
                  const newDipole = {
                    name: 'New Dipole',
                    description: 'Description for this dipole',
                    positive: {
                      name: 'Positive Well',
                      description: 'Description for positive orientation',
                      language_cues: ['positive cue 1', 'positive cue 2']
                    },
                    negative: {
                      name: 'Negative Well',
                      description: 'Description for negative orientation',
                      language_cues: ['negative cue 1', 'negative cue 2']
                    }
                  };
                  setEditingFramework({
                    ...editingFramework,
                    dipoles: [...(editingFramework.dipoles || []), newDipole]
                  });
                }}
                className="bg-green-600 text-white px-3 py-1 rounded-md hover:bg-green-700 transition-colors text-sm"
              >
                Add Dipole
              </button>
            </div>

            {editingFramework.dipoles?.map((dipole: any, dipoleIndex: number) => (
              <div key={dipoleIndex} className="border border-gray-200 rounded-lg p-4 mb-4">
                <div className="flex items-center justify-between mb-3">
                  <h5 className="font-medium text-gray-900">Dipole {dipoleIndex + 1}</h5>
                  <button
                    onClick={() => {
                      const newDipoles = editingFramework.dipoles.filter((_: any, i: number) => i !== dipoleIndex);
                      setEditingFramework({
                        ...editingFramework,
                        dipoles: newDipoles
                      });
                    }}
                    className="text-red-600 hover:text-red-800 text-sm"
                  >
                    Delete
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Dipole Name</label>
                    <input
                      type="text"
                      value={dipole.name || ''}
                      onChange={(e) => {
                        const newDipoles = [...editingFramework.dipoles];
                        newDipoles[dipoleIndex] = { ...dipole, name: e.target.value };
                        setEditingFramework({ ...editingFramework, dipoles: newDipoles });
                      }}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                    <input
                      type="text"
                      value={dipole.description || ''}
                      onChange={(e) => {
                        const newDipoles = [...editingFramework.dipoles];
                        newDipoles[dipoleIndex] = {
                          ...dipole,
                          description: e.target.value
                        };
                        setEditingFramework({ ...editingFramework, dipoles: newDipoles });
                      }}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                {/* Positive/Negative Wells */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Positive Well */}
                  <div className="bg-green-50 p-3 rounded-md">
                    <h6 className="font-medium text-green-800 mb-2">Positive Well</h6>
                    <div className="space-y-2">
                      <input
                        type="text"
                        placeholder="Well name"
                        value={dipole.positive?.name || ''}
                        onChange={(e) => {
                          const newDipoles = [...editingFramework.dipoles];
                          newDipoles[dipoleIndex] = {
                            ...dipole,
                            positive: { ...dipole.positive, name: e.target.value }
                          };
                          setEditingFramework({ ...editingFramework, dipoles: newDipoles });
                        }}
                        className="w-full px-2 py-1 border border-green-300 rounded-md text-sm"
                      />
                      <textarea
                        placeholder="Description"
                        value={dipole.positive?.description || ''}
                        onChange={(e) => {
                          const newDipoles = [...editingFramework.dipoles];
                          newDipoles[dipoleIndex] = {
                            ...dipole,
                            positive: { ...dipole.positive, description: e.target.value }
                          };
                          setEditingFramework({ ...editingFramework, dipoles: newDipoles });
                        }}
                        className="w-full px-2 py-1 border border-green-300 rounded-md text-sm"
                        rows={2}
                      />
                      <div>
                        <label className="block text-xs font-medium text-green-700 mb-1">Language Cues (comma-separated)</label>
                        <input
                          type="text"
                          placeholder="cue1, cue2, cue3"
                          value={dipole.positive?.language_cues?.join(', ') || ''}
                          onChange={(e) => {
                            const cues = e.target.value.split(',').map(s => s.trim()).filter(s => s);
                            const newDipoles = [...editingFramework.dipoles];
                            newDipoles[dipoleIndex] = {
                              ...dipole,
                              positive: { ...dipole.positive, language_cues: cues }
                            };
                            setEditingFramework({ ...editingFramework, dipoles: newDipoles });
                          }}
                          className="w-full px-2 py-1 border border-green-300 rounded-md text-sm"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Negative Well */}
                  <div className="bg-red-50 p-3 rounded-md">
                    <h6 className="font-medium text-red-800 mb-2">Negative Well</h6>
                    <div className="space-y-2">
                      <input
                        type="text"
                        placeholder="Well name"
                        value={dipole.negative?.name || ''}
                        onChange={(e) => {
                          const newDipoles = [...editingFramework.dipoles];
                          newDipoles[dipoleIndex] = {
                            ...dipole,
                            negative: { ...dipole.negative, name: e.target.value }
                          };
                          setEditingFramework({ ...editingFramework, dipoles: newDipoles });
                        }}
                        className="w-full px-2 py-1 border border-red-300 rounded-md text-sm"
                      />
                      <textarea
                        placeholder="Description"
                        value={dipole.negative?.description || ''}
                        onChange={(e) => {
                          const newDipoles = [...editingFramework.dipoles];
                          newDipoles[dipoleIndex] = {
                            ...dipole,
                            negative: { ...dipole.negative, description: e.target.value }
                          };
                          setEditingFramework({ ...editingFramework, dipoles: newDipoles });
                        }}
                        className="w-full px-2 py-1 border border-red-300 rounded-md text-sm"
                        rows={2}
                      />
                      <div>
                        <label className="block text-xs font-medium text-red-700 mb-1">Language Cues (comma-separated)</label>
                        <input
                          type="text"
                          placeholder="cue1, cue2, cue3"
                          value={dipole.negative?.language_cues?.join(', ') || ''}
                          onChange={(e) => {
                            const cues = e.target.value.split(',').map(s => s.trim()).filter(s => s);
                            const newDipoles = [...editingFramework.dipoles];
                            newDipoles[dipoleIndex] = {
                              ...dipole,
                              negative: { ...dipole.negative, language_cues: cues }
                            };
                            setEditingFramework({ ...editingFramework, dipoles: newDipoles });
                          }}
                          className="w-full px-2 py-1 border border-red-300 rounded-md text-sm"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="flex justify-end">
            <button
              onClick={handleSaveFramework}
              className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors"
            >
              Save Framework Changes
            </button>
          </div>
        </div>
      )}
    </div>
  );

  const renderReviewTab = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-gray-900">Integrated Prompt Review</h3>
        <div className="text-sm text-gray-500">
          Template: {prompt_templates.find(p => p.id === selectedPromptId)?.name || 'None'} + 
          Framework: {framework_configs.find(f => f.id === selectedFrameworkId)?.display_name || 'None'}
        </div>
      </div>

      {/* Version Selectors */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Prompt Template Version
          </label>
          <select
            value={selectedPromptId}
            onChange={(e) => setSelectedPromptId(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select template...</option>
            {prompt_templates.map(template => (
              <option key={template.id} value={template.id}>
                {template.name} v{template.version}
              </option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Framework Version
          </label>
          <select
            value={selectedFrameworkId}
            onChange={(e) => setSelectedFrameworkId(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select framework...</option>
            {framework_configs.map(framework => (
              <option key={framework.id} value={framework.id}>
                {framework.display_name} v{framework.version}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Combined Preview with Color Coding */}
      <div className="border border-gray-200 rounded-lg">
        <div className="bg-gray-50 px-4 py-2 border-b border-gray-200 flex items-center justify-between">
          <h4 className="font-medium text-gray-900">Final Prompt Preview</h4>
          <div className="flex items-center space-x-4 text-sm">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-blue-200 rounded mr-1"></div>
              <span>Template Content</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-200 rounded mr-1"></div>
              <span>Framework Content</span>
            </div>
          </div>
        </div>
        
        <div className="p-4 max-h-96 overflow-y-auto">
          <pre className="whitespace-pre-wrap text-sm font-mono">
            <span className="bg-blue-50 p-1 rounded">
              {prompt_templates.find(p => p.id === selectedPromptId)?.content || 'No template selected'}
            </span>
            
            {selectedFrameworkId && (
              <span className="bg-green-50 p-1 rounded">
                {(() => {
                  const framework = framework_configs.find(f => f.id === selectedFrameworkId);
                  if (!framework) return '';
                  
                  return `\n\n**FRAMEWORK WELLS FOR ANALYSIS:**\n${framework.display_name} (v${framework.version})\n\n${framework.dipoles.map((dipole: any) => {
                    return `**${dipole.name} Dimension - ${dipole.description}**\n\n${dipole.positive.name} (Integrative): ${dipole.positive.description}\nScore: ___ (0.0-1.0)\n\n${dipole.negative.name} (Disintegrative): ${dipole.negative.description}\nScore: ___ (0.0-1.0)\n\n`;
                  }).join('')}**TEXT TO ANALYZE:**\n[Text will be inserted here during analysis]`;
                })()}
              </span>
            )}
          </pre>
        </div>
        
        <div className="bg-gray-50 px-4 py-2 border-t border-gray-200">
          <p className="text-sm text-gray-600">
            ℹ️ This is exactly what will be sent to the LLM during analysis. Blue sections come from the prompt template (edit in Tab 1), green sections come from the framework configuration (edit in Tab 2).
          </p>
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Prompt Template & Framework Editor
        </h2>
        <p className="text-gray-600">
          v2.1 Structured Interface - Comprehensive editing with integrated preview
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'template', name: 'Prompt Template Editor', desc: 'Structured editing of all prompt components' },
            { id: 'framework', name: 'Framework Editor', desc: 'Configure dipoles, wells, and metadata' },
            { id: 'review', name: 'Integrated Review', desc: 'Preview final combined prompt' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div>
                <div>{tab.name}</div>
                <div className="text-xs text-gray-400 font-normal">{tab.desc}</div>
              </div>
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div>
        {activeTab === 'template' && renderTemplateTab()}
        {activeTab === 'framework' && renderFrameworkTab()}
        {activeTab === 'review' && renderReviewTab()}
      </div>
    </div>
  );
};

export default PromptEditor; 