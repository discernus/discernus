#!/usr/bin/env python3
"""
Test Plotly Circular Visualization Pipeline
=========================================

This script tests the Plotly-based circular visualization system by:
1. Connecting to the database
2. Retrieving a text analyzed with the Civic Virtue framework (from the new schema)
3. Generating an interactive visualization using the new Plotly system

The visualization is saved as an HTML file in analysis_results/plotly_circular_test/.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from narrative_gravity.visualization.plotly_circular import PlotlyCircularVisualizer
from narrative_gravity.utils.database import get_database_url

# --- CONFIG ---
FRAMEWORK_NAME = 'civic_virtue'  # Framework to test
OUTPUT_DIR = 'analysis_results/plotly_circular_test/'


def main():
    """Run the Plotly circular visualization test pipeline using the new schema."""
    print("🧪 Testing Plotly Circular Visualization Pipeline (v2.1 schema)")
    print("=" * 60)

    try:
        # 1. Connect to the database
        print("\n1. Connecting to database...")
        db_url = get_database_url()
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        print("✅ Database connection successful")

        # 2. Find a text analyzed with the Civic Virtue framework (new schema)
        print("\n2. Retrieving analysis data from 'run' and 'document' tables...")
        query = text('''
            SELECT r.id as run_id, r.raw_scores, d.title, d.id as doc_id
            FROM run r
            JOIN document d ON r.text_id = d.text_id
            WHERE r.framework_version = :framework_name
            ORDER BY r.created_at DESC
            LIMIT 1
        ''')
        row = session.execute(query, {'framework_name': FRAMEWORK_NAME}).fetchone()
        if not row:
            print(f"❌ No analysis found for framework '{FRAMEWORK_NAME}' in the new schema.")
            return

        raw_scores = row['raw_scores']
        title = row['title']
        doc_id = row['doc_id']
        print(f"✅ Found analysis for: {title}")

        # 3. Parse well scores from raw_scores
        print("\n3. Processing analysis data...")
        if not raw_scores:
            print("❌ No well scores found in analysis result")
            return
        well_scores = raw_scores  # Should be a dict: {well_name: score}
        print(f"✅ Processed {len(well_scores)} well scores")

        # 4. Get well definitions (angles/types/weights) from the framework config
        print("\n4. Configuring visualization...")
        
        # Load actual Civic Virtue framework configuration
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from scripts.framework_loader import load_framework_config, extract_wells_config
        
        try:
            framework_config = load_framework_config('civic_virtue')
            wells_for_viz = extract_wells_config(framework_config)
            print(f"✅ Loaded framework configuration with {len(wells_for_viz)} wells")
        except Exception as e:
            print(f"⚠️  Could not load framework config ({e}), using fallback configuration")
            # Fallback to hardcoded config if framework loading fails
            wells_for_viz = {
                'Dignity': {'angle': 90, 'type': 'integrative', 'weight': 1.0},
                'Tribalism': {'angle': 270, 'type': 'disintegrative', 'weight': 1.0},
                'Truth': {'angle': 75, 'type': 'integrative', 'weight': 0.8},
                'Justice': {'angle': 105, 'type': 'integrative', 'weight': 0.8},
                'Manipulation': {'angle': 285, 'type': 'disintegrative', 'weight': 0.8},
                'Resentment': {'angle': 255, 'type': 'disintegrative', 'weight': 0.8},
                'Hope': {'angle': 60, 'type': 'integrative', 'weight': 0.6},
                'Pragmatism': {'angle': 120, 'type': 'integrative', 'weight': 0.6},
                'Fantasy': {'angle': 300, 'type': 'disintegrative', 'weight': 0.6},
                'Fear': {'angle': 240, 'type': 'disintegrative', 'weight': 0.6}
            }
        
        # Filter wells to only those present in the analysis data
        available_wells = {k: v for k, v in wells_for_viz.items() if k in well_scores}
        print(f"✅ Configured {len(available_wells)} wells for visualization")

        # 5. Visualize with PlotlyCircularVisualizer
        print("\n5. Generating visualization...")
        visualizer = PlotlyCircularVisualizer()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = Path(OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_html = output_dir / f"plotly_circular_{doc_id}_{timestamp}.html"

        fig = visualizer.plot(
            wells=available_wells,
            narrative_scores=well_scores,
            narrative_label=title,
            title=f"Civic Virtue Analysis: {title}",
            output_html=str(output_html),
            show=False
        )

        print(f"✅ Plotly circular visualization saved: {output_html}")
        print("\n🎉 Test completed successfully!")

    except SQLAlchemyError as e:
        print(f"\n❌ Database error: {e}")
        print("💡 Tip: Run 'python check_database.py' to verify database connection")
        return
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return


if __name__ == '__main__':
    main() 