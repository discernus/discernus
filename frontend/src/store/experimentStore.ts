import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// Types for the experimental system
export interface PromptTemplate {
  id: string;
  name: string;
  version: string;
  content: string;
  description: string;
  type?: 'standard' | 'hierarchical';
  created_at: string;
  hash: string;
}

export interface WellDefinition {
  name: string;
  description: string;
  language_cues: string[];
}

export interface Dipole {
  name: string;
  description: string;
  positive: WellDefinition;
  negative: WellDefinition;
}

export interface EllipseConfig {
  description?: string;
  semi_major_axis: number;
  semi_minor_axis: number;
  orientation: 'vertical' | 'horizontal';
}

export interface WellMathConfig {
  angle: number;
  weight: number;
  type: 'integrative' | 'disintegrative';
  tier?: 'primary' | 'secondary' | 'tertiary';
}

export interface FrameworkConfig {
  id: string;
  framework_name: string;
  display_name: string;
  version: string;
  description: string;
  dipoles: Dipole[];
  ellipse?: EllipseConfig;
  wells?: Record<string, WellMathConfig>;
  scaling_factor?: number;
  weighting_philosophy?: any;
  metrics?: any;
}

export interface ScoringAlgorithm {
  id: string;
  name: string;
  version: string;
  type: 'linear' | 'winner_take_most' | 'exponential' | 'hierarchical' | 'nonlinear_weighting';
  parameters: Record<string, any>;
  description: string;
}

export interface Experiment {
  id: string;
  name: string;
  hypothesis: string;
  prompt_template_id: string;
  framework_config_id: string;
  scoring_algorithm_id: string;
  created_at: string;
  status: 'draft' | 'running' | 'completed' | 'failed';
}

// Analysis Result Interfaces
export interface WellJustification {
  score: number;
  reasoning: string;
  evidence_quotes: string[];
  confidence: number;
}

export interface AnalysisResult {
  id: string;
  experiment_id: string;
  text_id: string;
  text_content: string;
  llm_model: string;
  llm_version: string;
  raw_scores: Record<string, number>;
  well_justifications?: Record<string, WellJustification>; // New field for detailed justifications
  calculated_metrics: {
    narrative_elevation: number;
    polarity: number;
    coherence: number;
    directional_purity: number;
  };
  execution_time: string;
  complete_provenance: {
    prompt_template_hash: string;
    framework_version: string;
    scoring_algorithm_version: string;
    llm_model: string;
    timestamp: string;
  };
  is_pinned: boolean;
}

export interface ComparisonSet {
  id: string;
  name: string;
  result_ids: string[];
  created_at: string;
}

interface ExperimentStore {
  // State
  prompt_templates: PromptTemplate[];
  framework_configs: FrameworkConfig[];
  scoring_algorithms: ScoringAlgorithm[];
  experiments: Experiment[];
  analysis_results: AnalysisResult[];
  comparison_sets: ComparisonSet[];
  
  // v2.1 additions
  available_models: string[];
  experimentForm: {
    prompt_template_id: string;
    framework_config_id: string;
    scoring_algorithm_id: string;
    analysis_mode: string;
  };
  
  // UI State
  active_experiment_id: string | null;
  pinned_result_ids: string[];
  selected_text_content: string;
  is_analyzing: boolean;
  
  // Actions - Prompt Templates
  addPromptTemplate: (template: Omit<PromptTemplate, 'id' | 'created_at' | 'hash'>) => void;
  updatePromptTemplate: (id: string, updates: Partial<PromptTemplate>) => void;
  deletePromptTemplate: (id: string) => void;
  
  // Actions - Framework Configs
  addFrameworkConfig: (config: Omit<FrameworkConfig, 'id'>) => void;
  updateFrameworkConfig: (id: string, updates: Partial<FrameworkConfig>) => void;
  
  // Actions - Scoring Algorithms
  addScoringAlgorithm: (algorithm: Omit<ScoringAlgorithm, 'id'>) => void;
  updateScoringAlgorithm: (id: string, updates: Partial<ScoringAlgorithm>) => void;
  
  // Actions - Experiments
  createExperiment: (experiment: Omit<Experiment, 'id' | 'created_at' | 'status'>) => string;
  updateExperiment: (id: string, updates: Partial<Experiment>) => void;
  setActiveExperiment: (id: string | null) => void;
  
  // v2.1 actions
  setExperimentForm: (form: { prompt_template_id: string; framework_config_id: string; scoring_algorithm_id: string; analysis_mode: string; }) => void;
  
  // Actions - Analysis Results
  addAnalysisResult: (result: Omit<AnalysisResult, 'id' | 'is_pinned'>) => void;
  togglePinResult: (id: string) => void;
  clearPinnedResults: () => void;
  
  // Actions - Comparisons
  createComparisonSet: (name: string, result_ids: string[]) => string;
  
  // Actions - Text Analysis
  setSelectedText: (content: string) => void;
  setAnalyzing: (analyzing: boolean) => void;
}

const generateId = () => Math.random().toString(36).substr(2, 9);
const generateHash = (content: string) => {
  // Simple hash function that works with Unicode
  let hash = 0;
  for (let i = 0; i < content.length; i++) {
    const char = content.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash).toString(36).substr(0, 12);
};

export const useExperimentStore = create<ExperimentStore>()(
  persist(
    (set, _get) => ({
      // Initial state
      prompt_templates: [
        {
          id: 'default-v1',
          name: 'Standard Scoring v1.0',
          version: '1.0.0',
          content: `# Narrative Gravity Wells Analysis Prompt
**Version:** v2.1 Phase 1 - Hierarchical Analysis Framework

## Analysis Instructions

You are an expert political narrative analyst specializing in narrative gravity wells analysis. Analyze the provided text using the narrative gravity wells framework with **hierarchical dominance assessment**.

## CRITICAL SCORING REQUIREMENTS

🚨 **MANDATORY DECIMAL SCALE: 0.0 to 1.0 ONLY** 🚨
- Use ONLY decimal values between 0.0 and 1.0 (e.g., 0.3, 0.7, 0.9)
- DO NOT use integers 1-10 or any other scale
- DO NOT use percentages or any scale other than 0.0-1.0
- Example valid scores: 0.1, 0.4, 0.6, 0.8, 1.0
- Example INVALID scores: 1, 5, 10, 25%, 0.5/1.0

## ANALYSIS APPROACH

**PART 1: INDIVIDUAL WELL SCORING**
Score each well from 0.0 to 1.0 based on:
- **Conceptual strength** (not keyword frequency)
- **Thematic centrality** to the narrative structure
- **Semantic importance** in shaping the overall argument

**PART 2: HIERARCHICAL RANKING (CRITICAL - v2.1 FEATURE)**
After scoring all wells, identify and rank the **TOP 2-3 DRIVING WELLS** that most powerfully shape this narrative:

1. **PRIMARY WELL** (most dominant): [Well name] - Weight: [percentage 40-70%]
2. **SECONDARY WELL** (significant influence): [Well name] - Weight: [percentage 20-40%] 
3. **TERTIARY WELL** (if applicable): [Well name] - Weight: [percentage 10-30%]

**HIERARCHICAL REQUIREMENTS:**
- Weights must sum to 100% across your selected driving wells
- Provide specific textual evidence for each ranked well
- Explain WHY each well dominates over others
- If one well is overwhelmingly dominant (>80%), flag as "SINGLE-WELL DOMINANCE"

**PART 3: FRAMEWORK FIT ASSESSMENT**
Rate how well this text fits the current framework: [0.0-1.0]
- If fit score < 0.7, identify what thematic dimensions are missing
- Note any wells that seem inadequate for capturing the text's themes

## RESPONSE FORMAT

Provide your analysis in **JSON format** with the following structure:

\`\`\`json
{
  "individual_scores": {
    "Well1": 0.0,
    "Well2": 0.0,
    [... all framework wells]
  },
  "hierarchical_ranking": {
    "primary_well": {
      "name": "WellName",
      "weight": 0.60,
      "evidence": "Specific textual evidence showing dominance",
      "justification": "Why this well dominates the narrative"
    },
    "secondary_well": {
      "name": "WellName", 
      "weight": 0.30,
      "evidence": "Supporting textual evidence",
      "justification": "Why this is the second most important well"
    },
    "tertiary_well": {
      "name": "WellName",
      "weight": 0.10,
      "evidence": "Additional textual evidence",
      "justification": "Supporting role explanation"
    }
  },
  "framework_fit": {
    "score": 0.0,
    "missing_dimensions": "Any thematic elements not captured by current wells",
    "adequacy_assessment": "How well the framework captures the text's themes"
  },
  "single_well_dominance": false,
  "analysis_summary": "Brief explanation of the narrative's overall thematic structure and positioning"
}
\`\`\`

## ANALYSIS QUALITY STANDARDS

- **Evidence-based**: All scores must be supported by specific textual references
- **Conceptual focus**: Prioritize thematic meaning over surface-level word matching
- **Hierarchical clarity**: Make clear distinctions between primary, secondary, and tertiary wells
- **Framework awareness**: Consider how well the current framework captures the text's themes
- **Reproducibility**: Provide enough justification that another analyst could understand your reasoning

This prompt template is designed for **v2.1 Phase 1** hierarchical analysis with multi-model stability assessment capabilities.`,
          description: 'Enhanced v2.1 hierarchical prompt template with dominance ranking, evidence requirements, and framework fit assessment',
          type: 'hierarchical',
          created_at: new Date().toISOString(),
          hash: generateHash('hierarchical-v2.1-default')
        }
      ],
      framework_configs: [
        // Multiple versions of Civic Virtue Framework
        {
          id: 'civic-virtue-v1',
          framework_name: 'civic_virtue',
          display_name: 'Civic Virtue Framework',
          version: '2025.06.04',
          description: 'Civic Virtue Framework - A specialized Narrative Gravity Map implementation for moral analysis of persuasive political discourse. Uses three-tier weighting system based on moral psychology research.',
          dipoles: [
            {
              name: 'Identity',
              description: 'Moral worth and group membership dynamics',
              positive: {
                name: 'Dignity',
                description: 'Affirms individual moral worth and universal rights, regardless of group identity. Emphasizes agency, pluralism, and character over affiliation.',
                language_cues: ['equal dignity', 'inherent worth', 'regardless of background', 'individual character', 'universal rights', 'human agency']
              },
              negative: {
                name: 'Tribalism',
                description: 'Prioritizes group dominance, loyalty, or identity over individual agency. Often frames moral worth in in-group/out-group terms.',
                language_cues: ['real Americans', 'our people', 'they don\'t belong', 'us vs them', 'group loyalty', 'identity politics']
              }
            },
            {
              name: 'Integrity',
              description: 'Relationship between truth and information',
              positive: {
                name: 'Truth',
                description: 'Commitment to accuracy, evidence-based reasoning, and intellectual honesty. Values facts over convenience.',
                language_cues: ['based on evidence', 'facts show', 'research indicates', 'honest assessment', 'intellectual integrity', 'objective analysis']
              },
              negative: {
                name: 'Manipulation',
                description: 'Uses selective information, distortion, or deception to advance goals. Prioritizes persuasion over accuracy.',
                language_cues: ['cherry-picking', 'spin', 'misleading', 'distorted facts', 'propaganda', 'convenient omissions']
              }
            },
            {
              name: 'Fairness',
              description: 'Approach to justice and moral rules',
              positive: {
                name: 'Justice',
                description: 'Emphasizes impartial, rule-based fairness and equal treatment. Seeks systematic solutions to moral problems.',
                language_cues: ['equal treatment', 'fair process', 'rule of law', 'impartial justice', 'systematic approach', 'due process']
              },
              negative: {
                name: 'Resentment',
                description: 'Frames justice as grievance-based moral scorekeeping. Often personalizes systemic issues or seeks retribution.',
                language_cues: ['they owe us', 'payback time', 'moral debt', 'getting even', 'victimized by', 'unfair advantage']
              }
            },
            {
              name: 'Aspiration',
              description: 'Orientation toward future possibilities',
              positive: {
                name: 'Hope',
                description: 'Presents grounded optimism with realistic pathways forward. Balances idealism with practical steps.',
                language_cues: ['we can build', 'path forward', 'realistic solutions', 'achievable goals', 'step by step', 'evidence-based optimism']
              },
              negative: {
                name: 'Fantasy',
                description: 'Promotes unrealistic solutions or denies trade-offs and complexity. Often promises simple fixes to complex problems.',
                language_cues: ['easy solutions', 'no trade-offs', 'simple fix', 'magic bullet', 'ignore complexity', 'wishful thinking']
              }
            },
            {
              name: 'Stability',
              description: 'Approach to change and governance',
              positive: {
                name: 'Pragmatism',
                description: 'Emphasizes evidence-based, adaptable solutions. Values what works over ideological purity.',
                language_cues: ['what works', 'evidence-based', 'practical solutions', 'flexible approach', 'learn and adapt', 'pragmatic compromise']
              },
              negative: {
                name: 'Fear',
                description: 'Emphasizes threats, dangers, and need for control. Often frames change as dangerous and promotes reactive responses.',
                language_cues: ['dangerous times', 'under threat', 'need control', 'risky change', 'protect ourselves', 'fear-based reasoning']
              }
            }
          ],
          ellipse_config: {
            semi_major_axis: 1.0,
            semi_minor_axis: 0.7,
            orientation: 'vertical'
          },
          well_math_config: {
            scaling_factor: 0.8,
            primary_tier_weight: 1.0,
            secondary_tier_weight: 0.8,
            tertiary_tier_weight: 0.6
          }
        },
        {
          id: 'civic-virtue-v2',
          framework_name: 'civic_virtue',
          display_name: 'Civic Virtue Framework',
          version: '2025.01.03',
          description: 'Civic Virtue Framework - Earlier version with simplified weighting system.',
          dipoles: [
            {
              name: 'Identity',
              description: 'Moral worth and group membership dynamics',
              positive: {
                name: 'Dignity',
                description: 'Affirms individual moral worth and universal rights.',
                language_cues: ['equal dignity', 'inherent worth', 'individual character']
              },
              negative: {
                name: 'Tribalism',
                description: 'Prioritizes group dominance over individual agency.',
                language_cues: ['real Americans', 'our people', 'us vs them']
              }
            },
            {
              name: 'Integrity',
              description: 'Relationship between truth and information',
              positive: {
                name: 'Truth',
                description: 'Commitment to accuracy and evidence-based reasoning.',
                language_cues: ['based on evidence', 'facts show', 'honest assessment']
              },
              negative: {
                name: 'Manipulation',
                description: 'Uses selective information or deception to advance goals.',
                language_cues: ['cherry-picking', 'spin', 'misleading']
              }
            },
            {
              name: 'Fairness',
              description: 'Approach to justice and moral rules',
              positive: {
                name: 'Justice',
                description: 'Emphasizes impartial, rule-based fairness.',
                language_cues: ['equal treatment', 'fair process', 'rule of law']
              },
              negative: {
                name: 'Resentment',
                description: 'Frames justice as grievance-based scorekeeping.',
                language_cues: ['they owe us', 'payback time', 'moral debt']
              }
            },
            {
              name: 'Aspiration',
              description: 'Orientation toward future possibilities',
              positive: {
                name: 'Hope',
                description: 'Presents grounded optimism with realistic pathways.',
                language_cues: ['we can build', 'path forward', 'realistic solutions']
              },
              negative: {
                name: 'Fantasy',
                description: 'Promotes unrealistic solutions or denies complexity.',
                language_cues: ['easy solutions', 'no trade-offs', 'simple fix']
              }
            },
            {
              name: 'Stability',
              description: 'Approach to change and governance',
              positive: {
                name: 'Pragmatism',
                description: 'Emphasizes evidence-based, adaptable solutions.',
                language_cues: ['what works', 'evidence-based', 'practical solutions']
              },
              negative: {
                name: 'Fear',
                description: 'Emphasizes threats and need for control.',
                language_cues: ['dangerous times', 'under threat', 'need control']
              }
            }
          ],
          ellipse_config: {
            semi_major_axis: 1.0,
            semi_minor_axis: 0.7,
            orientation: 'vertical'
          },
          well_math_config: {
            scaling_factor: 0.8,
            primary_tier_weight: 1.0,
            secondary_tier_weight: 1.0,
            tertiary_tier_weight: 1.0
          }
        },
        // Political Spectrum Framework - Multiple Versions
        {
          id: 'political-spectrum-v1',
          framework_name: 'political_spectrum',
          display_name: 'Political Spectrum Framework',
          version: '2025.06.04',
          description: 'Political Spectrum Analysis - Traditional left-right positioning with enhanced dipole structure.',
          dipoles: [
            {
              name: 'Economic',
              description: 'Economic policy orientation',
              positive: {
                name: 'Solidarity',
                description: 'Emphasizes collective action and shared responsibility.',
                language_cues: ['working together', 'collective good', 'shared responsibility']
              },
              negative: {
                name: 'Competition',
                description: 'Emphasizes individual competition and market solutions.',
                language_cues: ['free market', 'individual responsibility', 'competitive advantage']
              }
            },
            {
              name: 'Social',
              description: 'Social policy orientation',
              positive: {
                name: 'Equality',
                description: 'Emphasizes equal outcomes and social justice.',
                language_cues: ['equal outcomes', 'social justice', 'systemic change']
              },
              negative: {
                name: 'Tradition',
                description: 'Emphasizes traditional values and established norms.',
                language_cues: ['traditional values', 'established norms', 'cultural heritage']
              }
            },
            {
              name: 'Political',
              description: 'Political authority orientation',
              positive: {
                name: 'Democracy',
                description: 'Emphasizes democratic participation and representation.',
                language_cues: ['democratic process', 'popular will', 'representation']
              },
              negative: {
                name: 'Control',
                description: 'Emphasizes centralized control and authority.',
                language_cues: ['strong leadership', 'centralized control', 'order and stability']
              }
            },
            {
              name: 'Cultural',
              description: 'Cultural orientation',
              positive: {
                name: 'Cosmopolitan',
                description: 'Emphasizes global perspective and cultural diversity.',
                language_cues: ['global perspective', 'cultural diversity', 'international cooperation']
              },
              negative: {
                name: 'Nationalist',
                description: 'Emphasizes national identity and sovereignty.',
                language_cues: ['national identity', 'sovereignty', 'cultural preservation']
              }
            },
            {
              name: 'Change',
              description: 'Approach to change',
              positive: {
                name: 'Progressive',
                description: 'Emphasizes progressive change and reform.',
                language_cues: ['progressive change', 'reform', 'innovation']
              },
              negative: {
                name: 'Conservative',
                description: 'Emphasizes conservation and gradual change.',
                language_cues: ['preserve tradition', 'gradual change', 'proven methods']
              }
            }
          ],
          ellipse_config: {
            semi_major_axis: 1.0,
            semi_minor_axis: 0.8,
            orientation: 'horizontal'
          },
          well_math_config: {
            scaling_factor: 0.9,
            primary_tier_weight: 1.0,
            secondary_tier_weight: 0.8,
            tertiary_tier_weight: 0.6
          }
        },
        {
          id: 'political-spectrum-v2',
          framework_name: 'political_spectrum',
          display_name: 'Political Spectrum Framework',
          version: '2025.01.03',
          description: 'Political Spectrum Analysis - Earlier version with basic left-right positioning.',
          dipoles: [
            {
              name: 'Economic',
              description: 'Economic policy orientation',
              positive: {
                name: 'Solidarity',
                description: 'Collective action and shared responsibility.',
                language_cues: ['working together', 'collective good']
              },
              negative: {
                name: 'Competition',
                description: 'Individual competition and market solutions.',
                language_cues: ['free market', 'individual responsibility']
              }
            },
            {
              name: 'Social',
              description: 'Social policy orientation',
              positive: {
                name: 'Equality',
                description: 'Equal outcomes and social justice.',
                language_cues: ['equal outcomes', 'social justice']
              },
              negative: {
                name: 'Tradition',
                description: 'Traditional values and established norms.',
                language_cues: ['traditional values', 'established norms']
              }
            },
            {
              name: 'Authority',
              description: 'Political authority orientation',
              positive: {
                name: 'Democracy',
                description: 'Democratic participation and representation.',
                language_cues: ['democratic process', 'popular will']
              },
              negative: {
                name: 'Control',
                description: 'Centralized control and authority.',
                language_cues: ['strong leadership', 'centralized control']
              }
            }
          ],
          ellipse_config: {
            semi_major_axis: 1.0,
            semi_minor_axis: 0.8,
            orientation: 'horizontal'
          },
          well_math_config: {
            scaling_factor: 0.9,
            primary_tier_weight: 1.0,
            secondary_tier_weight: 1.0,
            tertiary_tier_weight: 1.0
          }
        },
        // Moral-Rhetorical Posture Framework - Multiple Versions
        {
          id: 'moral-rhetorical-v1',
          framework_name: 'moral_rhetorical_posture',
          display_name: 'Moral-Rhetorical Posture Framework',
          version: '2025.06.04',
          description: 'Moral-Rhetorical Posture - Assesses communication style and rhetorical strategy.',
          dipoles: [
            {
              name: 'Justice',
              description: 'Approach to justice and conflict resolution',
              positive: {
                name: 'Restorative',
                description: 'Focuses on healing and rebuilding relationships.',
                language_cues: ['healing', 'rebuilding', 'restoration', 'reconciliation']
              },
              negative: {
                name: 'Retributive',
                description: 'Focuses on punishment and consequences.',
                language_cues: ['punishment', 'consequences', 'accountability', 'justice served']
              }
            },
            {
              name: 'Perspective',
              description: 'Scope of moral consideration',
              positive: {
                name: 'Universalist',
                description: 'Applies moral principles broadly across groups.',
                language_cues: ['universal principles', 'all people', 'human rights', 'global perspective']
              },
              negative: {
                name: 'Partisan',
                description: 'Prioritizes particular group interests.',
                language_cues: ['our side', 'group interests', 'partisan advantage', 'tribal loyalty']
              }
            },
            {
              name: 'Attitude',
              description: 'Rhetorical posture and tone',
              positive: {
                name: 'Humility',
                description: 'Acknowledges limitations and uncertainty.',
                language_cues: ['acknowledge limits', 'uncertain', 'room for error', 'learning']
              },
              negative: {
                name: 'Triumph',
                description: 'Projects certainty and dominance.',
                language_cues: ['absolute certainty', 'complete victory', 'total dominance', 'no doubt']
              }
            },
            {
              name: 'Reflection',
              description: 'Level of moral self-examination',
              positive: {
                name: 'Moral Reflection',
                description: 'Engages in moral self-examination and critique.',
                language_cues: ['self-examination', 'moral critique', 'ethical reflection', 'introspection']
              },
              negative: {
                name: 'Operational Will',
                description: 'Focuses on action without moral reflection.',
                language_cues: ['just do it', 'action over reflection', 'operational focus', 'get things done']
              }
            },
            {
              name: 'Change',
              description: 'Approach to systemic change',
              positive: {
                name: 'Reformist',
                description: 'Seeks gradual, systematic reform.',
                language_cues: ['gradual reform', 'systematic change', 'step by step', 'institutional improvement']
              },
              negative: {
                name: 'Revolutionary',
                description: 'Seeks radical, transformative change.',
                language_cues: ['radical change', 'transformation', 'revolutionary', 'complete overhaul']
              }
            }
          ],
          ellipse_config: {
            semi_major_axis: 1.0,
            semi_minor_axis: 0.7,
            orientation: 'vertical'
          },
          well_math_config: {
            scaling_factor: 0.8,
            primary_tier_weight: 1.0,
            secondary_tier_weight: 1.0,
            tertiary_tier_weight: 1.0
          }
        },
        {
          id: 'moral-rhetorical-v2',
          framework_name: 'moral_rhetorical_posture',
          display_name: 'Moral-Rhetorical Posture Framework',
          version: '2025.01.03',
          description: 'Moral-Rhetorical Posture - Earlier version with basic rhetorical analysis.',
          dipoles: [
            {
              name: 'Justice',
              description: 'Approach to justice',
              positive: {
                name: 'Restorative',
                description: 'Focuses on healing and rebuilding.',
                language_cues: ['healing', 'rebuilding', 'restoration']
              },
              negative: {
                name: 'Retributive',
                description: 'Focuses on punishment and consequences.',
                language_cues: ['punishment', 'consequences', 'accountability']
              }
            },
            {
              name: 'Perspective',
              description: 'Scope of moral consideration',
              positive: {
                name: 'Universalist',
                description: 'Applies principles broadly.',
                language_cues: ['universal principles', 'all people']
              },
              negative: {
                name: 'Partisan',
                description: 'Prioritizes group interests.',
                language_cues: ['our side', 'group interests']
              }
            },
            {
              name: 'Attitude',
              description: 'Rhetorical posture',
              positive: {
                name: 'Humility',
                description: 'Acknowledges limitations.',
                language_cues: ['acknowledge limits', 'uncertain']
              },
              negative: {
                name: 'Triumph',
                description: 'Projects certainty and dominance.',
                language_cues: ['absolute certainty', 'complete victory']
              }
            }
          ],
          ellipse_config: {
            semi_major_axis: 1.0,
            semi_minor_axis: 0.7,
            orientation: 'vertical'
          },
          well_math_config: {
            scaling_factor: 0.8,
            primary_tier_weight: 1.0,
            secondary_tier_weight: 1.0,
            tertiary_tier_weight: 1.0
          }
        }
      ],
      scoring_algorithms: [
        {
          id: 'linear-v1',
          name: 'Linear Average',
          version: '1.0.0',
          type: 'linear',
          parameters: { scaling_factor: 0.8 },
          description: 'Standard linear averaging approach'
        },
        {
          id: 'winner-take-most-v1',
          name: 'Winner-Take-Most',
          version: '1.0.0',
          type: 'winner_take_most',
          parameters: { 
            dominance_threshold: 0.6,
            boost_factor: 1.5,
            suppress_factor: 0.3
          },
          description: 'Amplifies dominant wells while suppressing weaker ones - implements nonlinear weighting for clearer hierarchy'
        },
        {
          id: 'exponential-v1',
          name: 'Exponential Weighting',
          version: '1.0.0',
          type: 'exponential',
          parameters: { 
            exponent: 2.0,
            normalization: true 
          },
          description: 'Exponential weighting that squares differences to enhance thematic distinction'
        },
        {
          id: 'hierarchical-v1',
          name: 'Hierarchical Dominance',
          version: '1.0.0',
          type: 'hierarchical',
          parameters: { 
            primary_weight: 0.6,
            secondary_weight: 0.3,
            tertiary_weight: 0.1,
            edge_snap_threshold: 0.8
          },
          description: 'Uses LLM-provided hierarchical rankings and relative weights for positioning - implements "edge snapping" for single-well dominance'
        },
        {
          id: 'nonlinear-v1',
          name: 'Nonlinear Transform',
          version: '1.0.0',
          type: 'nonlinear_weighting',
          parameters: { 
            transform_function: 'sigmoid',
            steepness: 3.0,
            center_point: 0.5
          },
          description: 'Applies nonlinear transforms to exaggerate differences near poles and compress center values'
        }
      ],
      experiments: [],
      analysis_results: [],
      comparison_sets: [],
      
      // UI State
      active_experiment_id: null,
      pinned_result_ids: [],
      selected_text_content: '',
      is_analyzing: false,
      
      // Actions
      addPromptTemplate: (template) => set((state) => ({
        prompt_templates: [
          ...state.prompt_templates,
          {
            ...template,
            id: generateId(),
            created_at: new Date().toISOString(),
            hash: generateHash(template.content)
          }
        ]
      })),
      
      updatePromptTemplate: (id, updates) => set((state) => ({
        prompt_templates: state.prompt_templates.map(t => 
          t.id === id 
            ? { 
                ...t, 
                ...updates, 
                hash: updates.content ? generateHash(updates.content) : t.hash 
              }
            : t
        )
      })),
      
      deletePromptTemplate: (id) => set((state) => ({
        prompt_templates: state.prompt_templates.filter(t => t.id !== id)
      })),
      
      addFrameworkConfig: (config) => set((state) => ({
        framework_configs: [
          ...state.framework_configs,
          { ...config, id: generateId() }
        ]
      })),
      
      updateFrameworkConfig: (id, updates) => set((state) => ({
        framework_configs: state.framework_configs.map(c => 
          c.id === id ? { ...c, ...updates } : c
        )
      })),
      
      addScoringAlgorithm: (algorithm) => set((state) => ({
        scoring_algorithms: [
          ...state.scoring_algorithms,
          { ...algorithm, id: generateId() }
        ]
      })),
      
      updateScoringAlgorithm: (id, updates) => set((state) => ({
        scoring_algorithms: state.scoring_algorithms.map(a => 
          a.id === id ? { ...a, ...updates } : a
        )
      })),
      
      createExperiment: (experiment) => {
        const id = generateId();
        set((state) => ({
          experiments: [
            ...state.experiments,
            {
              ...experiment,
              id,
              created_at: new Date().toISOString(),
              status: 'draft' as const
            }
          ]
        }));
        return id;
      },
      
      updateExperiment: (id, updates) => set((state) => ({
        experiments: state.experiments.map(e => 
          e.id === id ? { ...e, ...updates } : e
        )
      })),
      
      setActiveExperiment: (id) => set({ active_experiment_id: id }),
      
      addAnalysisResult: (result) => set((state) => ({
        analysis_results: [
          ...state.analysis_results,
          { ...result, id: generateId(), is_pinned: false }
        ]
      })),
      
      togglePinResult: (id) => set((state) => {
        const isPinned = state.pinned_result_ids.includes(id);
        return {
          pinned_result_ids: isPinned 
            ? state.pinned_result_ids.filter(pid => pid !== id)
            : [...state.pinned_result_ids, id],
          analysis_results: state.analysis_results.map(r => 
            r.id === id ? { ...r, is_pinned: !isPinned } : r
          )
        };
      }),
      
      clearPinnedResults: () => set((state) => ({
        pinned_result_ids: [],
        analysis_results: state.analysis_results.map(r => ({ ...r, is_pinned: false }))
      })),
      
      createComparisonSet: (name, result_ids) => {
        const id = generateId();
        set((state) => ({
          comparison_sets: [
            ...state.comparison_sets,
            {
              id,
              name,
              result_ids,
              created_at: new Date().toISOString()
            }
          ]
        }));
        return id;
      },
      
      setSelectedText: (content) => set({ selected_text_content: content }),
      
      setAnalyzing: (analyzing) => set({ is_analyzing: analyzing }),
      
             // v2.1 additions
       available_models: ['gpt-4', 'gpt-4-turbo', 'claude-3-sonnet', 'claude-3-opus', 'claude-3-haiku'],
      experimentForm: {
        prompt_template_id: '',
        framework_config_id: '',
        scoring_algorithm_id: '',
        analysis_mode: '',
      },
      
      // v2.1 actions
      setExperimentForm: (form) => set({ experimentForm: form })
    }),
    {
      name: 'narrative-gravity-experiment-store',
      version: 1,
    }
  )
); 