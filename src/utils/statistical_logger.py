"""
Enhanced Statistical Logger with PostgreSQL Backend
Designed for academic research workflows and enterprise analytics
"""

import json
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
from pathlib import Path
import pandas as pd

try:
    import psycopg2
    import psycopg2.extras
    HAS_POSTGRESQL = True
except ImportError:
    HAS_POSTGRESQL = False

try:
    import sqlite3
    HAS_SQLITE = True
except ImportError:
    HAS_SQLITE = False

@dataclass
class RunData:
    """Individual run data structure - enhanced to capture full LLM interaction"""
    run_id: str
    job_id: str
    run_number: int
    well_scores: Dict[str, float]
    narrative_position: Dict[str, float]  # x, y coordinates
    analysis_text: str
    model_name: str
    framework: str
    timestamp: str
    cost: float
    duration_seconds: float
    success: bool
    error_message: Optional[str] = None
    # Enhanced fields for full LLM capture
    raw_prompt: str = ""  # The complete prompt sent to LLM
    raw_response: str = ""  # The complete raw response from LLM
    input_text: str = ""  # The source text being analyzed
    model_parameters: Dict[str, Any] = None  # Temperature, max_tokens, etc.
    api_metadata: Dict[str, Any] = None  # Request/response metadata

@dataclass
class JobData:
    """Multi-run job data structure"""
    job_id: str
    speaker: str
    speech_type: str
    text_length: int
    framework: str
    model_name: str
    total_runs: int
    successful_runs: int
    total_cost: float
    total_duration_seconds: float
    timestamp: str
    mean_scores: Dict[str, float]
    variance_stats: Dict[str, Any]  # variance analysis results
    threshold_category: str  # perfect, near_perfect, minimal, normal
    
class StatisticalLogger:
    """
    Enterprise-grade logging system for narrative gravity analysis
    Supports PostgreSQL (preferred) and SQLite (fallback)
    Designed for academic research and business intelligence tools
    """
    
    def __init__(self, 
                 pg_config: Dict[str, str] = None,
                 db_path: str = "logs/discernus_stats.db",
                 prefer_postgresql: bool = True):
        """
        Initialize logger with PostgreSQL preference
        
        Args:
            pg_config: PostgreSQL connection config
            db_path: SQLite fallback path
            prefer_postgresql: Use PostgreSQL if available
        """
        self.pg_config = pg_config or self._get_default_pg_config()
        self.db_path = Path(db_path)
        self.use_postgresql = prefer_postgresql and HAS_POSTGRESQL
        
        if self.use_postgresql:
            try:
                self._init_postgresql()
                print("✅ Using PostgreSQL for enhanced analytics compatibility")
            except Exception as e:
                print(f"⚠️ PostgreSQL unavailable ({e}), falling back to SQLite")
                self.use_postgresql = False
                
        if not self.use_postgresql:
            if not HAS_SQLITE:
                raise ImportError("Neither PostgreSQL nor SQLite available")
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._init_sqlite()
            print("📁 Using SQLite (limited analytics compatibility)")
    
    def _get_default_pg_config(self) -> Dict[str, str]:
        """Get default PostgreSQL configuration"""
        import os
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'discernus'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '')
        }
    
    def _get_connection(self):
        """Get database connection"""
        if self.use_postgresql:
            return psycopg2.connect(**self.pg_config)
        else:
            return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = None) -> List[tuple]:
        """Execute query and return results"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            print(f"Database query error: {e}")
            return []
    
    def _init_postgresql(self):
        """Initialize PostgreSQL with enhanced schema"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Enable JSON support
        cursor.execute("CREATE EXTENSION IF NOT EXISTS btree_gin;")
        
        # Jobs table with JSONB for better querying
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            speaker TEXT NOT NULL,
            speech_type TEXT NOT NULL,
            text_length INTEGER NOT NULL,
            framework TEXT NOT NULL,
            model_name TEXT NOT NULL,
            total_runs INTEGER NOT NULL,
            successful_runs INTEGER NOT NULL,
            total_cost DECIMAL(10,4) NOT NULL,
            total_duration_seconds DECIMAL(8,2) NOT NULL,
            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            mean_scores JSONB NOT NULL,
            variance_stats JSONB NOT NULL,
            threshold_category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        
        # Runs table with full LLM corpus
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            job_id TEXT NOT NULL REFERENCES jobs(job_id),
            run_number INTEGER NOT NULL,
            well_scores JSONB NOT NULL,
            narrative_position JSONB NOT NULL,
            analysis_text TEXT NOT NULL,
            model_name TEXT NOT NULL,
            framework TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            cost DECIMAL(8,4) NOT NULL,
            duration_seconds DECIMAL(6,2) NOT NULL,
            success BOOLEAN NOT NULL,
            error_message TEXT,
            raw_prompt TEXT,
            raw_response TEXT,
            input_text TEXT,
            model_parameters JSONB,
            api_metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        
        # Create indexes for analytics performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_runs_job_id ON runs(job_id);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_runs_model_name ON runs(model_name);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_runs_timestamp ON runs(timestamp);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_jobs_speaker ON jobs(speaker);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_jobs_model_name ON jobs(model_name);')
        
        # Variance statistics table for academic analysis
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS variance_stats (
            id SERIAL PRIMARY KEY,
            job_id TEXT NOT NULL REFERENCES jobs(job_id),
            well_name TEXT NOT NULL,
            mean_score DECIMAL(6,4) NOT NULL,
            std_deviation DECIMAL(6,4) NOT NULL,
            variance DECIMAL(8,6) NOT NULL,
            score_category TEXT NOT NULL,
            well_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        
        # Also create the variance_statistics table that dashboard queries expect
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS variance_statistics (
            job_id TEXT PRIMARY KEY,
            well_statistics JSONB NOT NULL,
            narrative_statistics JSONB NOT NULL,
            framework_info JSONB NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        
        # Performance metrics for business intelligence
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id SERIAL PRIMARY KEY,
            job_id TEXT NOT NULL REFERENCES jobs(job_id),
            model_name TEXT NOT NULL,
            framework TEXT NOT NULL,
            success_rate DECIMAL(5,4) NOT NULL,
            avg_cost_per_run DECIMAL(8,4) NOT NULL,
            avg_duration_per_run DECIMAL(6,2) NOT NULL,
            total_variance_sum DECIMAL(8,6) NOT NULL,
            max_individual_variance DECIMAL(8,6) NOT NULL,
            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        
        conn.commit()
        conn.close()
    
    def _init_sqlite(self):
        """Initialize SQLite with enhanced schema (fallback)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Jobs table - multi-run job metadata
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            speaker TEXT NOT NULL,
            speech_type TEXT NOT NULL,
            text_length INTEGER NOT NULL,
            framework TEXT NOT NULL,
            model_name TEXT NOT NULL,
            total_runs INTEGER NOT NULL,
            successful_runs INTEGER NOT NULL,
            total_cost REAL NOT NULL,
            total_duration_seconds REAL NOT NULL,
            timestamp TEXT NOT NULL,
            mean_scores TEXT NOT NULL,  -- JSON
            variance_stats TEXT NOT NULL,  -- JSON
            threshold_category TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Runs table - individual run data with enhanced logging
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            job_id TEXT NOT NULL,
            run_number INTEGER NOT NULL,
            well_scores TEXT NOT NULL,  -- JSON
            narrative_position TEXT NOT NULL,  -- JSON
            analysis_text TEXT NOT NULL,
            model_name TEXT NOT NULL,
            framework TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            cost REAL NOT NULL,
            duration_seconds REAL NOT NULL,
            success BOOLEAN NOT NULL,
            error_message TEXT,
            raw_prompt TEXT,  -- Complete prompt sent to LLM
            raw_response TEXT,  -- Complete raw response from LLM
            input_text TEXT,  -- Source text being analyzed
            model_parameters TEXT,  -- JSON: temperature, max_tokens, etc.
            api_metadata TEXT,  -- JSON: request/response metadata
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES jobs (job_id)
        )
        ''')
        
        # Variance statistics table for academic analysis
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS variance_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL,
            well_name TEXT NOT NULL,
            mean_score REAL NOT NULL,
            std_deviation REAL NOT NULL,
            variance REAL NOT NULL,
            score_category TEXT NOT NULL,
            well_type TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES jobs (job_id)
        )
        ''')
        
        # Performance metrics for business intelligence
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL,
            model_name TEXT NOT NULL,
            framework TEXT NOT NULL,
            success_rate REAL NOT NULL,
            avg_cost_per_run REAL NOT NULL,
            avg_duration_per_run REAL NOT NULL,
            total_variance_sum REAL NOT NULL,
            max_individual_variance REAL NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (job_id) REFERENCES jobs (job_id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_run(self, run_data: RunData):
        """Log individual run data"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.use_postgresql:
            cursor.execute('''
            INSERT INTO runs (
                run_id, job_id, run_number, well_scores, narrative_position, 
                analysis_text, model_name, framework, timestamp, cost, 
                duration_seconds, success, error_message, raw_prompt, raw_response,
                input_text, model_parameters, api_metadata
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (run_id) DO UPDATE SET
                well_scores = EXCLUDED.well_scores,
                narrative_position = EXCLUDED.narrative_position,
                analysis_text = EXCLUDED.analysis_text,
                cost = EXCLUDED.cost,
                duration_seconds = EXCLUDED.duration_seconds,
                raw_prompt = EXCLUDED.raw_prompt,
                raw_response = EXCLUDED.raw_response,
                input_text = EXCLUDED.input_text,
                model_parameters = EXCLUDED.model_parameters,
                api_metadata = EXCLUDED.api_metadata
            ''', [
            run_data.run_id,
            run_data.job_id,
            run_data.run_number,
            json.dumps(run_data.well_scores) if run_data.well_scores else '{}',
            json.dumps(run_data.narrative_position) if run_data.narrative_position else '{}',
            run_data.analysis_text,
            run_data.model_name,
            run_data.framework,
            run_data.timestamp,
            run_data.cost,
            run_data.duration_seconds,
            run_data.success,
            run_data.error_message,
            run_data.raw_prompt,
            run_data.raw_response,
            run_data.input_text,
            json.dumps(run_data.model_parameters) if run_data.model_parameters else '{}',
            json.dumps(run_data.api_metadata) if run_data.api_metadata else '{}'
        ])
        else:
            cursor.execute('''
            INSERT OR REPLACE INTO runs (
                run_id, job_id, run_number, well_scores, narrative_position, 
                analysis_text, model_name, framework, timestamp, cost, 
                duration_seconds, success, error_message, raw_prompt, raw_response,
                input_text, model_parameters, api_metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                run_data.run_id,
                run_data.job_id,
                run_data.run_number,
                json.dumps(run_data.well_scores) if run_data.well_scores else '{}',
                json.dumps(run_data.narrative_position) if run_data.narrative_position else '{}',
                run_data.analysis_text,
                run_data.model_name,
                run_data.framework,
                run_data.timestamp,
                run_data.cost,
                run_data.duration_seconds,
                run_data.success,
                run_data.error_message,
                run_data.raw_prompt,
                run_data.raw_response,
                run_data.input_text,
                json.dumps(run_data.model_parameters) if run_data.model_parameters else '{}',
                json.dumps(run_data.api_metadata) if run_data.api_metadata else '{}'
            ))
        
        conn.commit()
        conn.close()
    
    def log_job(self, job_data: JobData):
        """Log multi-run job data"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.use_postgresql:
            cursor.execute('''
            INSERT INTO jobs (
                job_id, speaker, speech_type, text_length, framework, model_name,
                total_runs, successful_runs, total_cost, total_duration_seconds,
                timestamp, mean_scores, variance_stats, threshold_category
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (job_id) DO UPDATE SET
                successful_runs = EXCLUDED.successful_runs,
                total_cost = EXCLUDED.total_cost,
                total_duration_seconds = EXCLUDED.total_duration_seconds,
                mean_scores = EXCLUDED.mean_scores,
                variance_stats = EXCLUDED.variance_stats,
                threshold_category = EXCLUDED.threshold_category
            ''', [
            job_data.job_id,
            job_data.speaker,
            job_data.speech_type,
            job_data.text_length,
            job_data.framework,
            job_data.model_name,
            job_data.total_runs,
            job_data.successful_runs,
            job_data.total_cost,
            job_data.total_duration_seconds,
            job_data.timestamp,
            json.dumps(job_data.mean_scores),
            json.dumps(job_data.variance_stats),
            job_data.threshold_category
        ])
        else:
            cursor.execute('''
            INSERT OR REPLACE INTO jobs (
                job_id, speaker, speech_type, text_length, framework, model_name,
                total_runs, successful_runs, total_cost, total_duration_seconds,
                timestamp, mean_scores, variance_stats, threshold_category
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job_data.job_id,
                job_data.speaker,
                job_data.speech_type,
                job_data.text_length,
                job_data.framework,
                job_data.model_name,
                job_data.total_runs,
                job_data.successful_runs,
                job_data.total_cost,
                job_data.total_duration_seconds,
                job_data.timestamp,
                json.dumps(job_data.mean_scores),
                json.dumps(job_data.variance_stats),
                job_data.threshold_category
            ))
        
        conn.commit()
        conn.close()
    
    def log_variance_statistics(self, job_id: str, well_stats: Dict[str, Dict], 
                              framework_info: Dict[str, Any]):
        """Log detailed variance statistics for threshold analysis"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        integrative_wells = framework_info.get('integrative_wells', [])
        disintegrative_wells = framework_info.get('disintegrative_wells', [])
        
        for well_name, stats in well_stats.items():
            # Categorize score level
            mean_score = stats['mean']
            if mean_score < 0.3:
                score_category = 'low'
            elif mean_score > 0.7:
                score_category = 'high'
            else:
                score_category = 'medium'
            
            # Categorize well type
            if well_name in integrative_wells:
                well_type = 'integrative'
            elif well_name in disintegrative_wells:
                well_type = 'disintegrative'
            else:
                well_type = 'unknown'
            
            if self.use_postgresql:
                cursor.execute('''
                INSERT INTO variance_stats (
                    job_id, well_name, mean_score, std_deviation, variance,
                    score_category, well_type
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', [
                    job_id,
                    well_name,
                    float(stats['mean']),  # Convert numpy types to Python types
                    float(stats['std']),
                    float(stats['variance']),
                    score_category,
                    well_type
                ])
            else:
                cursor.execute('''
                INSERT INTO variance_stats (
                    job_id, well_name, mean_score, std_deviation, variance,
                    score_category, well_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                                ''', (
                job_id,
                well_name,
                float(stats['mean']),  # Convert numpy types to Python types
                float(stats['std']),
                float(stats['variance']),
                score_category,
                well_type
            ))
        
        conn.commit()
        conn.close()
    
    def log_performance_metrics(self, job_id: str, model_name: str, framework: str,
                              success_rate: float, avg_cost: float, avg_duration: float,
                              total_variance: float, max_variance: float):
        """Log performance metrics"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.use_postgresql:
            cursor.execute('''
            INSERT INTO performance_metrics (
                job_id, model_name, framework, success_rate, avg_cost_per_run,
                avg_duration_per_run, total_variance_sum, max_individual_variance,
                timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', [
                job_id, model_name, framework, float(success_rate), float(avg_cost), float(avg_duration),
                float(total_variance), float(max_variance), datetime.now().isoformat()
            ])
        else:
            cursor.execute('''
            INSERT INTO performance_metrics (
                job_id, model_name, framework, success_rate, avg_cost_per_run,
                avg_duration_per_run, total_variance_sum, max_individual_variance,
                timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
            job_id, model_name, framework, float(success_rate), float(avg_cost), float(avg_duration),
            float(total_variance), float(max_variance), datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def get_variance_threshold_analysis(self) -> Dict[str, Any]:
        """Analyze variance patterns to suggest empirical thresholds"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get all variance data
        cursor.execute('''
        SELECT std_deviation, mean_score, score_category, well_type 
        FROM variance_stats
        ''')
        
        data = cursor.fetchall()
        conn.close()
        
        if not data:
            return {"error": "No variance data available"}
        
        variances = [row[0] for row in data]
        
        # Calculate statistics
        analysis = {
            "total_samples": len(variances),
            "variance_stats": {
                "min": min(variances),
                "max": max(variances),
                "mean": np.mean(variances),
                "median": np.median(variances),
                "std": np.std(variances),
                "percentiles": {
                    "5th": np.percentile(variances, 5),
                    "10th": np.percentile(variances, 10),
                    "25th": np.percentile(variances, 25),
                    "75th": np.percentile(variances, 75),
                    "90th": np.percentile(variances, 90),
                    "95th": np.percentile(variances, 95),
                }
            },
            "suggested_thresholds": {
                "individual_minimal": np.percentile(variances, 10),  # 10th percentile
                "individual_low": np.percentile(variances, 25),      # 25th percentile
                "sum_minimal": np.percentile(variances, 10) * 10,    # Scaled for 10 wells
            }
        }
        
        return analysis
    
    def get_model_performance_comparison(self) -> Dict[str, Any]:
        """Compare performance across different models and frameworks"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT model_name, framework, 
               AVG(success_rate) as avg_success_rate,
               AVG(avg_cost_per_run) as avg_cost,
               AVG(avg_duration_per_run) as avg_duration,
               AVG(total_variance_sum) as avg_variance,
               COUNT(*) as job_count
        FROM performance_metrics
        GROUP BY model_name, framework
        ORDER BY avg_success_rate DESC, avg_cost ASC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        comparison = {
            'models': []
        }
        
        for row in results:
            comparison['models'].append({
                'model_name': row[0],
                'framework': row[1],
                'avg_success_rate': row[2],
                'avg_cost': row[3],
                'avg_duration': row[4],
                'avg_variance': row[5],
                'job_count': row[6]
            })
        
        return comparison
    
    def get_full_response_corpus(self, filters: Dict[str, Any] = None) -> List[Dict]:
        """Retrieve full raw response corpus for analysis
        
        Args:
            filters: Dict with optional filters like:
                - model_name: str
                - framework: str
                - speaker: str
                - min_cost: float
                - max_variance: float
                - date_range: tuple of (start_date, end_date)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Build query with filters (handle boolean types)
        success_condition = 'r.success = true' if self.use_postgresql else 'r.success = 1'
        
        base_query = f'''
        SELECT r.run_id, r.job_id, r.run_number, r.well_scores, r.narrative_position,
               r.analysis_text, r.model_name, r.framework, r.timestamp, r.cost,
               r.duration_seconds, r.success, r.error_message, r.raw_prompt,
               r.raw_response, r.input_text, r.model_parameters, r.api_metadata,
               j.speaker, j.speech_type, j.text_length
        FROM runs r
        JOIN jobs j ON r.job_id = j.job_id
        WHERE {success_condition}
        '''
        params = []
        
        if filters:
            placeholder = '%s' if self.use_postgresql else '?'
            if 'model_name' in filters:
                base_query += f' AND r.model_name = {placeholder}'
                params.append(filters['model_name'])
            if 'framework' in filters:
                base_query += f' AND r.framework = {placeholder}'
                params.append(filters['framework'])
            if 'speaker' in filters:
                base_query += f' AND j.speaker = {placeholder}'
                params.append(filters['speaker'])
            if 'min_cost' in filters:
                base_query += f' AND r.cost >= {placeholder}'
                params.append(filters['min_cost'])
            if 'date_range' in filters:
                base_query += f' AND r.timestamp >= {placeholder} AND r.timestamp <= {placeholder}'
                params.extend(filters['date_range'])
        
        base_query += ' ORDER BY r.timestamp DESC'
        
        cursor.execute(base_query, params)
        results = cursor.fetchall()
        conn.close()
        
        # Convert to structured format
        corpus = []
        for row in results:
            # Handle JSON parsing for different database backends
            if self.use_postgresql:
                # PostgreSQL JSONB is already parsed
                well_scores = row[3] if isinstance(row[3], dict) else json.loads(row[3])
                narrative_position = row[4] if isinstance(row[4], dict) else json.loads(row[4])
                model_parameters = row[16] if isinstance(row[16], dict) else (json.loads(row[16]) if row[16] else {})
                api_metadata = row[17] if isinstance(row[17], dict) else (json.loads(row[17]) if row[17] else {})
            else:
                # SQLite stores as JSON strings
                well_scores = json.loads(row[3])
                narrative_position = json.loads(row[4])
                model_parameters = json.loads(row[16]) if row[16] else {}
                api_metadata = json.loads(row[17]) if row[17] else {}
            
            corpus.append({
                'run_id': row[0],
                'job_id': row[1],
                'run_number': row[2],
                'well_scores': well_scores,
                'narrative_position': narrative_position,
                'analysis_text': row[5],
                'model_name': row[6],
                'framework': row[7],
                'timestamp': row[8],
                'cost': row[9],
                'duration_seconds': row[10],
                'success': row[11],
                'error_message': row[12],
                'raw_prompt': row[13],
                'raw_response': row[14],
                'input_text': row[15],
                'model_parameters': model_parameters,
                'api_metadata': api_metadata,
                'speaker': row[18],
                'speech_type': row[19],
                'text_length': row[20]
            })
        
        return corpus
    
    def get_corpus_stats(self) -> Dict[str, Any]:
        """Get summary statistics of the full response corpus"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Basic stats (handle both PostgreSQL and SQLite boolean types)
        success_condition = 'success = true' if self.use_postgresql else 'success = 1'
        
        cursor.execute(f'SELECT COUNT(*) FROM runs WHERE {success_condition}')
        total_runs = cursor.fetchone()[0]
        
        cursor.execute(f'SELECT COUNT(DISTINCT job_id) FROM runs WHERE {success_condition}')
        total_jobs = cursor.fetchone()[0]
        
        cursor.execute(f'SELECT COUNT(DISTINCT model_name) FROM runs WHERE {success_condition}')
        unique_models = cursor.fetchone()[0]
        
        cursor.execute(f'SELECT SUM(cost) FROM runs WHERE {success_condition}')
        total_cost = cursor.fetchone()[0] or 0
        
        cursor.execute(f'''
        SELECT model_name, COUNT(*) as count 
        FROM runs WHERE {success_condition}
        GROUP BY model_name 
        ORDER BY count DESC
        ''')
        model_distribution = cursor.fetchall()
        
        cursor.execute(f'''
        SELECT speaker, COUNT(*) as count 
        FROM runs r JOIN jobs j ON r.job_id = j.job_id 
        WHERE r.{success_condition}
        GROUP BY speaker 
        ORDER BY count DESC
        ''')
        speaker_distribution = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_runs': total_runs,
            'total_jobs': total_jobs,
            'unique_models': unique_models,
            'total_cost': total_cost,
            'model_distribution': [{'model': row[0], 'count': row[1]} for row in model_distribution],
            'speaker_distribution': [{'speaker': row[0], 'count': row[1]} for row in speaker_distribution]
        }
    
    def export_for_academics(self, 
                            export_format: str = "csv",
                            output_dir: str = "exports/",
                            include_raw_responses: bool = False) -> Dict[str, str]:
        """
        Export data in formats suitable for academic statistical analysis
        
        Args:
            export_format: 'csv', 'spss', 'stata', 'r', 'parquet', 'all'
            output_dir: Directory for export files
            include_raw_responses: Include full text responses
            
        Returns:
            Dict mapping format to file path
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exported_files = {}
        
        # Get comprehensive dataset
        df_runs = self._get_runs_dataframe(include_raw_responses)
        df_jobs = self._get_jobs_dataframe()
        df_variance = self._get_variance_dataframe()
        
        formats_to_export = [export_format] if export_format != 'all' else ['csv', 'spss', 'parquet', 'r']
        
        for fmt in formats_to_export:
            if fmt == 'csv':
                # CSV for general use
                runs_file = output_path / f"discernus_runs_{timestamp}.csv"
                jobs_file = output_path / f"discernus_jobs_{timestamp}.csv"
                variance_file = output_path / f"discernus_variance_{timestamp}.csv"
                
                df_runs.to_csv(runs_file, index=False)
                df_jobs.to_csv(jobs_file, index=False)  
                df_variance.to_csv(variance_file, index=False)
                
                exported_files['csv'] = {
                    'runs': str(runs_file),
                    'jobs': str(jobs_file),
                    'variance': str(variance_file)
                }
                
            elif fmt == 'spss':
                try:
                    import pyreadstat
                    
                    # SPSS with proper variable labels
                    spss_file = output_path / f"discernus_analysis_{timestamp}.sav"
                    
                    # Combine key data for SPSS analysis
                    spss_df = self._prepare_spss_dataset(df_runs, df_jobs, df_variance)
                    
                    # Variable labels for SPSS
                    variable_labels = {
                        'job_id': 'Multi-run Job Identifier',
                        'speaker': 'Political Speaker',
                        'model_name': 'AI Model Used',
                        'civic_virtue_score': 'Net Civic Virtue Score',
                        'total_variance': 'Total Variance Across Wells',
                        'success_rate': 'Analysis Success Rate',
                        'cost_per_run': 'Cost per Analysis Run',
                        'text_length': 'Input Text Length (characters)'
                    }
                    
                    pyreadstat.write_sav(spss_df, str(spss_file), variable_labels=variable_labels)
                    exported_files['spss'] = str(spss_file)
                    
                except ImportError:
                    print("⚠️ pyreadstat not available for SPSS export")
                    
            elif fmt == 'parquet':
                # Parquet for data lakes and big data analytics
                parquet_file = output_path / f"discernus_corpus_{timestamp}.parquet"
                df_runs.to_parquet(parquet_file, index=False, compression='snappy')
                exported_files['parquet'] = str(parquet_file)
                
            elif fmt == 'r':
                # R-specific export with analysis script
                r_file = output_path / f"discernus_data_{timestamp}.RData"
                r_script = output_path / f"discernus_analysis_{timestamp}.R"
                
                # Save as CSV for R import (most reliable)
                csv_file = output_path / f"discernus_for_r_{timestamp}.csv"
                combined_df = self._prepare_r_dataset(df_runs, df_jobs, df_variance)
                combined_df.to_csv(csv_file, index=False)
                
                # Generate R analysis script
                self._generate_r_script(str(csv_file), str(r_script))
                
                exported_files['r'] = {
                    'data': str(csv_file),
                    'script': str(r_script)
                }
        
        return exported_files
    
    def _get_runs_dataframe(self, include_raw_responses: bool = False) -> pd.DataFrame:
        """Convert runs table to pandas DataFrame"""
        conn = self._get_connection()
        
        # Handle boolean queries for different databases
        success_condition = 'success = true' if self.use_postgresql else 'success = 1'
        
        if include_raw_responses:
            query = f"SELECT * FROM runs WHERE {success_condition} ORDER BY timestamp DESC"
        else:
            query = f"""
            SELECT run_id, job_id, run_number, well_scores, narrative_position,
                   analysis_text, model_name, framework, timestamp, cost,
                   duration_seconds, success, model_parameters
            FROM runs WHERE {success_condition} ORDER BY timestamp DESC
            """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Expand JSON columns for analysis
        if not df.empty:
            # Handle JSON parsing for different database backends
            if self.use_postgresql:
                # PostgreSQL JSONB is already parsed as dict
                well_scores_df = pd.json_normalize(df['well_scores'].tolist())
                narrative_df = pd.json_normalize(df['narrative_position'].tolist())
            else:
                # SQLite stores as JSON strings
                well_scores_df = pd.json_normalize(df['well_scores'].apply(json.loads))
                narrative_df = pd.json_normalize(df['narrative_position'].apply(json.loads))
            
            well_scores_df.columns = [f'well_{col}' for col in well_scores_df.columns]
            narrative_df.columns = [f'narrative_{col}' for col in narrative_df.columns]
            
            # Combine dataframes
            df = pd.concat([df.drop(['well_scores', 'narrative_position'], axis=1), 
                           well_scores_df, narrative_df], axis=1)
        
        return df
    
    def _get_jobs_dataframe(self) -> pd.DataFrame:
        """Convert jobs table to pandas DataFrame"""
        conn = self._get_connection()
        query = "SELECT * FROM jobs ORDER BY timestamp DESC"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            # Handle JSON parsing for different database backends
            if self.use_postgresql:
                # PostgreSQL JSONB is already parsed as dict
                mean_scores_df = pd.json_normalize(df['mean_scores'].tolist())
            else:
                # SQLite stores as JSON strings
                mean_scores_df = pd.json_normalize(df['mean_scores'].apply(json.loads))
            
            mean_scores_df.columns = [f'mean_{col}' for col in mean_scores_df.columns]
            
            df = pd.concat([df.drop(['mean_scores'], axis=1), mean_scores_df], axis=1)
        
        return df
    
    def _get_variance_dataframe(self) -> pd.DataFrame:
        """Convert variance stats table to pandas DataFrame"""
        conn = self._get_connection()
        query = "SELECT * FROM variance_stats ORDER BY job_id, well_name"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def _prepare_spss_dataset(self, df_runs, df_jobs, df_variance) -> pd.DataFrame:
        """Prepare dataset optimized for SPSS analysis"""
        # Join key tables for comprehensive analysis
        spss_df = df_jobs[['job_id', 'speaker', 'model_name', 'total_cost', 'successful_runs', 'text_length']].copy()
        
        # Add calculated metrics
        spss_df['cost_per_run'] = spss_df['total_cost'] / spss_df['successful_runs']
        spss_df['success_rate'] = spss_df['successful_runs'] / 5  # Assuming 5 runs per job
        
        # Add variance metrics
        variance_summary = df_variance.groupby('job_id').agg({
            'variance': 'sum',
            'mean_score': 'mean'
        }).rename(columns={'variance': 'total_variance', 'mean_score': 'avg_well_score'})
        
        spss_df = spss_df.merge(variance_summary, on='job_id', how='left')
        
        return spss_df
    
    def _prepare_r_dataset(self, df_runs, df_jobs, df_variance) -> pd.DataFrame:
        """Prepare comprehensive dataset for R analysis"""
        # Simplify aggregation to avoid multi-level columns
        variance_summary = df_variance.groupby('job_id').agg({
            'variance': 'sum',
            'mean_score': 'mean'
        }).round(4)
        variance_summary.columns = ['total_variance', 'avg_mean_score']
        
        # Merge datasets
        return df_runs.merge(df_jobs, on='job_id', suffixes=('_run', '_job')).merge(
            variance_summary, on='job_id', how='left'
        )
    
    def _generate_r_script(self, data_file: str, script_file: str):
        """Generate R analysis script for the exported data"""
        r_code = f'''
# Narrative Gravity Analysis in R
# Generated: {datetime.now().isoformat()}

library(tidyverse)
library(corrplot)
library(psych)

# Load data
data <- read.csv("{data_file}")

# Basic descriptive statistics
summary(data)
describe(data)

# Variance analysis
variance_analysis <- data %>%
  group_by(speaker, model_name) %>%
  summarise(
    mean_variance = mean(total_variance, na.rm = TRUE),
    mean_cost = mean(cost_per_run, na.rm = TRUE),
    mean_civic_virtue = mean(civic_virtue_score, na.rm = TRUE),
    .groups = 'drop'
  )

print(variance_analysis)

# Correlation matrix
numeric_cols <- data %>% select_if(is.numeric)
correlation_matrix <- cor(numeric_cols, use = "complete.obs")
corrplot(correlation_matrix, method = "circle")

# Model comparison
model_comparison <- aov(total_variance ~ model_name + speaker, data = data)
summary(model_comparison)

# Save results
write.csv(variance_analysis, "variance_analysis_results.csv")
ggsave("correlation_plot.png", last_plot(), width = 10, height = 8)

print("Analysis complete! Check output files.")
'''
        
        with open(script_file, 'w') as f:
            f.write(r_code)

    def get_job_by_id(self, job_id: str) -> Optional[Dict]:
        """Retrieve job data by job_id for dashboard generation"""
        try:
            query = """
            SELECT * FROM jobs WHERE job_id = %s
            """
            result = self.execute_query(query, (job_id,))
            
            if result and len(result) > 0:
                # Convert to dictionary format matching our existing data structures
                job_data = result[0]
                return {
                    'job_id': job_data[0],
                    'speaker': job_data[1],
                    'speech_type': job_data[2],
                    'text_length': job_data[3],
                    'framework': job_data[4],
                    'model_name': job_data[5],
                    'total_runs': job_data[6],
                    'successful_runs': job_data[7],
                    'total_cost': job_data[8],
                    'total_duration_seconds': job_data[9],
                    'timestamp': job_data[10],
                    'mean_scores': job_data[11] if isinstance(job_data[11], dict) else json.loads(job_data[11]) if job_data[11] else {},
                    'variance_stats': job_data[12] if isinstance(job_data[12], dict) else json.loads(job_data[12]) if job_data[12] else {},
                    'threshold_category': job_data[13]
                }
            return None
        except Exception as e:
            print(f"Error retrieving job {job_id}: {e}")
            return None

    def get_runs_by_job_id(self, job_id: str) -> List[Dict]:
        """Retrieve all runs for a job_id for dashboard generation"""
        try:
            query = """
            SELECT * FROM runs WHERE job_id = %s ORDER BY run_number
            """
            results = self.execute_query(query, (job_id,))
            
            runs = []
            for run_data in results:
                run_dict = {
                    'run_id': run_data[0],
                    'job_id': run_data[1],
                    'run_number': run_data[2],
                    'well_scores': run_data[3] if isinstance(run_data[3], dict) else json.loads(run_data[3]) if run_data[3] else {},
                    'narrative_position': run_data[4] if isinstance(run_data[4], dict) else json.loads(run_data[4]) if run_data[4] else {},
                    'analysis_text': run_data[5],
                    'model_name': run_data[6],
                    'framework': run_data[7],
                    'timestamp': run_data[8],
                    'cost': run_data[9],
                    'duration_seconds': run_data[10],
                    'success': run_data[11],
                    'error_message': run_data[12],
                    'raw_prompt': run_data[13],
                    'raw_response': run_data[14],
                    'input_text': run_data[15],
                    'model_parameters': run_data[16] if isinstance(run_data[16], dict) else json.loads(run_data[16]) if run_data[16] else {},
                    'api_metadata': run_data[17] if isinstance(run_data[17], dict) else json.loads(run_data[17]) if run_data[17] else {}
                }
                runs.append(run_dict)
            
            return runs
        except Exception as e:
            print(f"Error retrieving runs for job {job_id}: {e}")
            return []

    def get_variance_statistics_by_job_id(self, job_id: str) -> Optional[Dict]:
        """Retrieve variance statistics for a job_id"""
        try:
            query = """
            SELECT * FROM variance_statistics WHERE job_id = %s
            """
            result = self.execute_query(query, (job_id,))
            
            if result and len(result) > 0:
                var_data = result[0]
                return {
                    'job_id': var_data[0],
                    'well_statistics': var_data[1] if isinstance(var_data[1], dict) else json.loads(var_data[1]) if var_data[1] else {},
                    'narrative_statistics': var_data[2] if isinstance(var_data[2], dict) else json.loads(var_data[2]) if var_data[2] else {},
                    'framework_info': var_data[3] if isinstance(var_data[3], dict) else json.loads(var_data[3]) if var_data[3] else {},
                    'timestamp': var_data[4]
                }
            return None
        except Exception as e:
            print(f"Error retrieving variance statistics for job {job_id}: {e}")
            return None

    def get_recent_jobs(self, limit: int = 10) -> List[Dict]:
        """Get recent jobs for dashboard selection"""
        try:
            query = """
            SELECT job_id, speaker, speech_type, framework, model_name, total_runs, timestamp 
            FROM jobs 
            ORDER BY timestamp DESC 
            LIMIT %s
            """
            results = self.execute_query(query, (limit,))
            
            jobs = []
            for job_data in results:
                jobs.append({
                    'job_id': job_data[0],
                    'speaker': job_data[1],
                    'speech_type': job_data[2],
                    'framework': job_data[3],
                    'model_name': job_data[4],
                    'total_runs': job_data[5],
                    'timestamp': job_data[6]
                })
            
            return jobs
        except Exception as e:
            print(f"Error retrieving recent jobs: {e}")
            return []

    def get_dashboard_data(self, job_id: str) -> Optional[Dict]:
        """Get complete data needed for dashboard generation from database"""
        try:
            # Get job metadata
            job_data = self.get_job_by_id(job_id)
            if not job_data:
                print(f"Job {job_id} not found in database")
                return None
            
            # Get all runs
            runs_data = self.get_runs_by_job_id(job_id)
            if not runs_data:
                print(f"No runs found for job {job_id}")
                return None
            
            # Get variance statistics (optional)
            try:
                variance_data = self.get_variance_statistics_by_job_id(job_id)
            except Exception as e:
                print(f"Warning: Could not load variance statistics: {e}")
                variance_data = None
            
            # Format data to match existing dashboard expectations
            dashboard_data = {
                'job_metadata': job_data,
                'individual_runs': [],
                'test_metadata': {
                    'total_runs': job_data['total_runs'],
                    'model': job_data['model_name'],
                    'timestamp': job_data['timestamp'],
                    'framework': job_data['framework']
                },
                'input_text': runs_data[0]['input_text'] if runs_data else '',
                'analysis_date': job_data['timestamp']
            }
            
            # Convert runs to expected format
            for run in runs_data:
                formatted_run = {
                    'result': {
                        'scores': run['well_scores'],
                        'analysis': run['analysis_text'],
                        'raw_response': run['raw_response']
                    },
                    'cost': run['cost'],
                    'duration': run['duration_seconds'],
                    'success': run['success'],
                    'prompt': run['raw_prompt'],
                    'model_parameters': run['model_parameters'],
                    'api_metadata': run['api_metadata']
                }
                dashboard_data['individual_runs'].append(formatted_run)
            
            # Add variance statistics if available
            if variance_data:
                dashboard_data['variance_statistics'] = variance_data
            
            return dashboard_data
            
        except Exception as e:
            print(f"Error getting dashboard data for job {job_id}: {e}")
            return None

# Global logger instance
logger = StatisticalLogger() 