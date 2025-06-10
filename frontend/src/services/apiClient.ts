import axios from 'axios';
import { debugMonitor } from './debugMonitor';

// API Configuration - Use more robust environment variable handling
const getApiUrl = () => {
  try {
    return process.env.REACT_APP_API_URL || 'http://localhost:8000';
  } catch (e) {
    // Fallback if process.env is not available
    return 'http://localhost:8000';
  }
};

const API_BASE_URL = getApiUrl();

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 second timeout for analysis requests
  headers: {
    'Content-Type': 'application/json',
  },
});

// Track API call timing outside of interceptors
const apiCallTimings = new Map<string, number>();

// Request interceptor to add auth token if available
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - clear token and redirect to login
      localStorage.removeItem('auth_token');
      // Could dispatch logout action here
    }
    return Promise.reject(error);
  }
);

// Request interceptor for debug tracking
apiClient.interceptors.request.use((config) => {
  // Track API call start time
  const requestId = `${config.method?.toUpperCase()}_${config.url}_${Date.now()}`;
  apiCallTimings.set(requestId, performance.now());
  config.headers['X-Request-ID'] = requestId;
  
  return config;
});

// Response interceptor for debug tracking
apiClient.interceptors.response.use(
  (response) => {
    // Track successful API call
    const requestId = response.config.headers['X-Request-ID'] as string;
    const startTime = apiCallTimings.get(requestId);
    const duration = startTime ? Math.round(performance.now() - startTime) : undefined;
    
    if (requestId) apiCallTimings.delete(requestId);
    
    debugMonitor.logAPICall(
      (response.config.method || 'GET').toUpperCase(),
      response.config.url || 'unknown',
      response.status,
      duration
    );
    
    return response;
  },
  (error) => {
    // Track failed API call
    const requestId = error.config?.headers?.['X-Request-ID'] as string;
    const startTime = requestId ? apiCallTimings.get(requestId) : undefined;
    const duration = startTime ? Math.round(performance.now() - startTime) : undefined;
    
    if (requestId) apiCallTimings.delete(requestId);
    
    debugMonitor.logAPICall(
      (error.config?.method || 'GET').toUpperCase(),
      error.config?.url || 'unknown',
      error.response?.status,
      duration,
      error.message
    );
    
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Types for API responses
export interface CorpusResponse {
  id: number;
  name: string;
  description: string | null;
  upload_timestamp: string;
  record_count: number;
  uploader_id: string | null;
}

export interface DocumentResponse {
  id: number;
  corpus_id: number;
  text_id: string;
  title: string;
  document_type: string;
  author: string;
  date: string;
  publication: string | null;
  medium: string | null;
  created_at: string;
  updated_at: string;
}

export interface ChunkResponse {
  id: number;
  document_id: number;
  chunk_id: number;
  total_chunks: number;
  chunk_type: string;
  chunk_size: number;
  chunk_overlap: number | null;
  document_position: number;
  word_count: number;
  unique_words: number;
  word_density: number;
  chunk_content: string;
  framework_data: Record<string, any>;
  processing_status: string;
  created_at: string;
  updated_at: string;
}

export interface JobCreateRequest {
  corpus_id: number;
  job_name?: string;
  text_ids: string[];
  frameworks: string[];
  models: string[];
  run_count?: number;
  job_config?: Record<string, any>;
}

export interface JobResponse {
  id: number;
  corpus_id: number;
  job_name: string | null;
  text_ids: string[];
  frameworks: string[];
  models: string[];
  run_count: number;
  status: string;
  total_tasks: number;
  completed_tasks: number;
  failed_tasks: number;
  estimated_cost: number | null;
  actual_cost: number;
  created_at: string;
  updated_at: string;
  started_at: string | null;
  completed_at: string | null;
}

export interface TaskResponse {
  id: number;
  job_id: number;
  chunk_id: number;
  framework: string;
  model: string;
  run_number: number;
  status: string;
  attempts: number;
  max_attempts: number;
  result_data: Record<string, any> | null;
  last_error: string | null;
  error_count: number;
  api_cost: number | null;
  created_at: string;
  updated_at: string;
  started_at: string | null;
  finished_at: string | null;
}

// Type Definitions (Enhanced for v2.1)

export interface WellJustification {
  score: number;
  reasoning: string;
  evidence_quotes: string[];
  confidence: number;
}

export interface HierarchicalRanking {
  primary_wells: Array<{
    well: string;
    score: number;
    relative_weight: number;
  }>;
  secondary_wells: Array<{
    well: string;
    score: number;
    relative_weight: number;
  }>;
  total_weight: number;
}

export interface CalculatedMetrics {
  narrative_elevation: number;
  polarity: number;
  coherence: number;
  directional_purity: number;
}

export interface NarrativePosition {
  x: number;
  y: number;
}

export interface CompleteProvenance {
  prompt_template_hash: string;
  framework_version: string;
  scoring_algorithm_version: string;
  llm_model: string;
  timestamp: string;
  experiment_id?: number;
}

// Experiment Types
export interface ExperimentCreate {
  name: string;
  hypothesis?: string;
  description?: string;
  research_context?: string;
  prompt_template_id: string;
  framework_config_id: string;
  scoring_algorithm_id: string;
  analysis_mode: string;
  selected_models: string[];
  research_notes?: string;
  tags: string[];
}

export interface ExperimentResponse {
  id: number;
  creator_id?: number;
  name: string;
  hypothesis?: string;
  description?: string;
  research_context?: string;
  prompt_template_id: string;
  framework_config_id: string;
  scoring_algorithm_id: string;
  analysis_mode: string;
  selected_models: string[];
  status: string;
  total_runs: number;
  successful_runs: number;
  research_notes?: string;
  publication_status: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

// Analysis Request/Response Types
export interface SingleTextAnalysisRequest {
  text_content: string;
  experiment_id?: number;
  prompt_template_id: string;
  framework_config_id: string;
  scoring_algorithm_id: string;
  llm_model: string;
  model_parameters?: Record<string, any>;
  include_justifications?: boolean;
  include_hierarchical_ranking?: boolean;
}

export interface SingleTextAnalysisResponse {
  analysis_id: string;
  text_content: string;
  framework: string;
  model: string;
  raw_scores: Record<string, number>;
  hierarchical_ranking?: HierarchicalRanking;
  well_justifications?: Record<string, WellJustification>;
  calculated_metrics: CalculatedMetrics;
  narrative_position: NarrativePosition;
  framework_fit_score: number;
  dominant_wells: Array<{
    well: string;
    score: number;
    relative_weight: number;
  }>;
  execution_time: string;
  duration_seconds?: number;
  api_cost?: number;
}

export interface MultiModelAnalysisRequest {
  text_content: string;
  experiment_id?: number;
  prompt_template_id: string;
  framework_config_id: string;
  scoring_algorithm_id: string;
  selected_models: string[];
  runs_per_model?: number;
}

export interface ModelComparisonResult {
  model: string;
  runs: any[]; // RunResponse[] in full implementation
  mean_scores: Record<string, number>;
  score_variance: Record<string, number>;
  consistency_score: number;
}

export interface MultiModelAnalysisResponse {
  analysis_id: string;
  text_content: string;
  framework: string;
  scoring_algorithm: string;
  model_results: ModelComparisonResult[];
  model_agreement: Record<string, number>;
  consensus_scores: Record<string, number>;
  stability_metrics: Record<string, any>;
  total_runs: number;
  total_cost: number;
  execution_time: string;
}

// Legacy types for backward compatibility
export interface FrameworkConfig {
  id: string;
  name: string;
  version: string;
  description: string;
  dipoles: any[];
}

export interface PromptTemplate {
  id: string;
  name: string;
  version: string;
  content: string;
}

export interface ScoringAlgorithm {
  id: string;
  name: string;
  description: string;
}

// API Service Class
export const apiService = {
  // Health Check
  async healthCheck(): Promise<{ status: string; version: string; database: string }> {
    const response = await apiClient.get('/api/health');
    return response.data;
  },

  // Authentication
  async login(username: string, password: string): Promise<{ access_token: string; user: any }> {
    const response = await apiClient.post('/api/auth/login', {
      username,
      password,
    });
    
    // Store token for future requests
    if (response.data.access_token) {
      localStorage.setItem('auth_token', response.data.access_token);
    }
    
    return response.data;
  },

  async logout(): Promise<void> {
    localStorage.removeItem('auth_token');
  },

  // Experiments
  async createExperiment(experiment: ExperimentCreate): Promise<ExperimentResponse> {
    const response = await apiClient.post('/api/experiments', experiment);
    return response.data;
  },

  async listExperiments(skip = 0, limit = 100, status_filter?: string): Promise<ExperimentResponse[]> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });
    
    if (status_filter) {
      params.append('status_filter', status_filter);
    }
    
    const response = await apiClient.get(`/api/experiments?${params}`);
    return response.data;
  },

  async getExperiment(experimentId: number): Promise<ExperimentResponse> {
    const response = await apiClient.get(`/api/experiments/${experimentId}`);
    return response.data;
  },

  async updateExperiment(experimentId: number, updates: Partial<ExperimentCreate>): Promise<ExperimentResponse> {
    const response = await apiClient.put(`/api/experiments/${experimentId}`, updates);
    return response.data;
  },

  // Analysis
  async analyzeSingleText(request: SingleTextAnalysisRequest): Promise<SingleTextAnalysisResponse> {
    console.log('🔄 Sending analysis request to backend:', {
      text_length: request.text_content.length,
      model: request.llm_model,
      framework: request.framework_config_id,
      scoring_algorithm: request.scoring_algorithm_id
    });

    try {
      const response = await apiClient.post('/api/analyze/single-text', request);
      
      console.log('✅ Analysis response received:', {
        analysis_id: response.data.analysis_id,
        framework_fit_score: response.data.framework_fit_score,
        dominant_wells: response.data.dominant_wells?.length || 0,
        has_justifications: !!response.data.well_justifications,
        execution_time: response.data.execution_time
      });
      
      return response.data;
    } catch (error: any) {
      console.error('❌ Analysis request failed:', {
        status: error.response?.status,
        message: error.response?.data?.detail || error.message,
        request_config: {
          url: error.config?.url,
          method: error.config?.method
        }
      });
      
      // Re-throw with enhanced error info
      throw new Error(
        error.response?.data?.detail || 
        `Analysis failed: ${error.message}`
      );
    }
  },

  async analyzeMultiModel(request: MultiModelAnalysisRequest): Promise<MultiModelAnalysisResponse> {
    console.log('🔄 Sending multi-model analysis request:', {
      text_length: request.text_content.length,
      models: request.selected_models,
      runs_per_model: request.runs_per_model || 3
    });

    try {
      const response = await apiClient.post('/api/analyze/multi-model', request);
      
      console.log('✅ Multi-model analysis response received:', {
        analysis_id: response.data.analysis_id,
        total_runs: response.data.total_runs,
        total_cost: response.data.total_cost,
        model_count: response.data.model_results?.length || 0
      });
      
      return response.data;
    } catch (error: any) {
      console.error('❌ Multi-model analysis failed:', error);
      throw new Error(
        error.response?.data?.detail || 
        `Multi-model analysis failed: ${error.message}`
      );
    }
  },

  // Mock data for development (will be replaced by real endpoints)
  async getFrameworkConfigs(): Promise<FrameworkConfig[]> {
    // TODO: Replace with real endpoint when backend implements framework management
    return [
      {
        id: 'civic_virtue_v2025_06_04',
        name: 'Civic Virtue',
        version: 'v2025.06.04',
        description: 'Civic virtue framework for political discourse analysis',
        dipoles: []
      },
      {
        id: 'political_spectrum_v2025_06_04',
        name: 'Political Spectrum',
        version: 'v2025.06.04',
        description: 'Traditional left-right political spectrum analysis',
        dipoles: []
      },
      {
        id: 'moral_rhetorical_posture_v2025_06_04',
        name: 'Moral-Rhetorical Posture',
        version: 'v2025.06.04',
        description: 'Moral and rhetorical positioning framework',
        dipoles: []
      }
    ];
  },

  async getPromptTemplates(): Promise<PromptTemplate[]> {
    // TODO: Replace with real endpoint when backend implements template management
    return [
      {
        id: 'hierarchical_v1_0',
        name: 'Hierarchical Prompt v1.0',
        version: '1.0',
        content: 'Hierarchical analysis prompt template'
      },
      {
        id: 'traditional_v1_0',
        name: 'Traditional Prompt v1.0',
        version: '1.0',
        content: 'Traditional analysis prompt template'
      }
    ];
  },

  async getScoringAlgorithms(): Promise<ScoringAlgorithm[]> {
    // TODO: Replace with real endpoint when backend implements algorithm management
    return [
      {
        id: 'winner_take_most',
        name: 'Winner-Take-Most',
        description: 'Emphasizes dominant narrative wells'
      },
      {
        id: 'exponential_weighting',
        name: 'Exponential Weighting',
        description: 'Exponentially weights higher scores'
      },
      {
        id: 'hierarchical_dominance',
        name: 'Hierarchical Dominance',
        description: 'Hierarchical ranking with relative weights'
      },
      {
        id: 'nonlinear_transform',
        name: 'Nonlinear Transform',
        description: 'Nonlinear transformation of scores'
      }
    ];
  },

  // System info
  async getSystemInfo(): Promise<{ version: string; status: string }> {
    try {
      const health = await this.healthCheck();
      return {
        version: health.version,
        status: health.status
      };
    } catch (error) {
      return {
        version: 'unknown',
        status: 'error'
      };
    }
  },

  // Corpus Management
  async getCorpora(): Promise<CorpusResponse[]> {
    const response = await apiClient.get('/api/corpora');
    return response.data;
  },

  async getCorpusDocuments(corpusId: number): Promise<DocumentResponse[]> {
    const response = await apiClient.get(`/api/corpora/${corpusId}/documents`);
    return response.data;
  },

  async getCorpusChunks(corpusId: number): Promise<ChunkResponse[]> {
    const response = await apiClient.get(`/api/corpora/${corpusId}/chunks`);
    return response.data;
  },

  // Job Management
  async createJob(jobRequest: JobCreateRequest): Promise<JobResponse> {
    const response = await apiClient.post('/api/jobs', jobRequest);
    return response.data;
  },

  async getJobs(): Promise<JobResponse[]> {
    const response = await apiClient.get('/api/jobs');
    return response.data;
  },

  async getJob(jobId: number): Promise<JobResponse> {
    const response = await apiClient.get(`/api/jobs/${jobId}`);
    return response.data;
  },

  async getTask(taskId: number): Promise<TaskResponse> {
    const response = await apiClient.get(`/api/tasks/${taskId}`);
    return response.data;
  },

  // Framework Management (for future expansion)
  async getFrameworks(): Promise<any[]> {
    // Mock response - in production this would fetch available frameworks
    return Promise.resolve([
      {
        id: 'civic_virtue',
        name: 'Civic Virtue Framework',
        version: '1.0.0',
        description: 'Core civic virtue framework with 10 gravity wells',
        dipoles: {
          integrative: ['Dignity', 'Truth', 'Justice', 'Hope', 'Pragmatism'],
          disintegrative: ['Tribalism', 'Manipulation', 'Resentment', 'Fantasy', 'Fear']
        }
      },
      {
        id: 'moral_rhetorical_posture',
        name: 'Moral Rhetorical Posture',
        version: '1.0.0',
        description: 'Extended framework focusing on rhetorical positioning',
        dipoles: {
          integrative: ['Wisdom', 'Humility', 'Courage', 'Compassion'],
          disintegrative: ['Arrogance', 'Cowardice', 'Cruelty', 'Ignorance']
        }
      }
    ]);
  },

  // Model Management
  async getAvailableModels(): Promise<string[]> {
    // Mock response - in production this would fetch available LLM models
    return Promise.resolve([
      'claude-3-5-sonnet-20241022',
      'gpt-4-0613',
      'gpt-4-turbo-preview',
      'gemini-1.5-pro'
    ]);
  }
};

export default apiService; 