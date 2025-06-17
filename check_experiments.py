#!/usr/bin/env python3
"""Check what experiments are in the database."""
import sys
import os
from pathlib import Path
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.narrative_gravity.utils.database import get_database_url
from src.narrative_gravity.models.models import Experiment, Run

def main():
    try:
        engine = create_engine(get_database_url())
        Session = sessionmaker(bind=engine)
        session = Session()
        
        experiments = session.query(Experiment).all()
        print(f'Found {len(experiments)} experiments:')
        print()
        
        for exp in experiments:
            runs_count = session.query(Run).filter(Run.experiment_id == exp.id).count()
            print(f'🔍 Experiment ID: {exp.id}')
            print(f'   Name: "{exp.name}"')
            print(f'   Status: {exp.status}')
            print(f'   Total Runs (metadata): {exp.total_runs}')
            print(f'   Actual Runs (database): {runs_count}')
            print(f'   Framework: {exp.framework_config_id}')
            print(f'   Created: {exp.created_at}')
            
            # Check if this might be IDITI experiment (8 runs, IDITI framework, recent date)
            might_be_iditi = (
                runs_count == 8 or 
                exp.total_runs == 8 or 
                "iditi" in str(exp.framework_config_id).lower() or
                "iditi" in str(exp.name).lower()
            )
            
            if might_be_iditi:
                print(f'   ⭐ POTENTIAL IDITI EXPERIMENT!')
                
                # Get sample run data
                runs = session.query(Run).filter(Run.experiment_id == exp.id).limit(3).all()
                if runs:
                    print(f'   Sample runs:')
                    for run in runs:
                        print(f'     - Run {run.run_number}: {run.text_id}, Model: {run.llm_model}')
                        if run.raw_scores:
                            if isinstance(run.raw_scores, str):
                                scores = json.loads(run.raw_scores)
                            else:
                                scores = run.raw_scores
                            sample_wells = list(scores.keys())[:3] if scores else []
                            print(f'       Wells: {sample_wells}')
            
            print()
        
        session.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 