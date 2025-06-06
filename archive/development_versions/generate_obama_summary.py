#!/usr/bin/env python3
"""
Generate Complete Multi-Run Analysis Summary
Creates JSON summary with means/statistics and visualization with variance
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def extract_scores_from_raw_response(raw_response):
    """Extract scores from the raw JSON response"""
    try:
        lines = raw_response.strip().split('\n')
        json_lines = []
        in_json = False
        brace_count = 0
        
        for line in lines:
            if line.strip().startswith('{') and not in_json:
                in_json = True
                brace_count = 1
                json_lines.append(line)
            elif in_json:
                json_lines.append(line)
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0:
                    break
        
        if json_lines:
            json_str = '\n'.join(json_lines)
            parsed = json.loads(json_str)
            return parsed.get('scores', {})
    except:
        pass
    return {}

def generate_statistical_summary():
    """Generate comprehensive statistical summary"""
    results_file = "test_results/obama_multi_run_civic_virtue_20250606_142731.json"
    
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Results file not found: {results_file}")
        return None, None
    
    # Extract scores from all runs
    all_scores = []
    run_metadata = []
    
    for run in data['individual_runs']:
        if run['success']:
            raw_response = run['result']['raw_response']
            scores = extract_scores_from_raw_response(raw_response)
            
            if scores:
                all_scores.append(scores)
                run_metadata.append({
                    'run_number': run['run_number'],
                    'cost': run['cost'],
                    'duration': run['duration'],
                    'timestamp': run['timestamp']
                })
    
    if not all_scores:
        print("❌ No scores found")
        return None, None
    
    # Calculate comprehensive statistics
    wells = sorted(set().union(*all_scores))
    well_statistics = {}
    
    for well in wells:
        values = [scores.get(well, 0) for scores in all_scores]
        well_statistics[well] = {
            'mean': float(np.mean(values)),
            'std': float(np.std(values)),
            'min': float(np.min(values)),
            'max': float(np.max(values)),
            'range': float(np.max(values) - np.min(values)),
            'median': float(np.median(values)),
            'values': values,
            'runs': len(values)
        }
    
    # Categorize wells
    integrative_wells = ['Dignity', 'Truth', 'Hope', 'Justice', 'Pragmatism']
    disintegrative_wells = ['Tribalism', 'Manipulation', 'Fantasy', 'Resentment', 'Fear']
    
    # Calculate aggregate statistics
    integrative_stats = {
        'wells': integrative_wells,
        'means': [well_statistics[well]['mean'] for well in integrative_wells if well in well_statistics],
        'average': 0,
        'std': 0
    }
    
    disintegrative_stats = {
        'wells': disintegrative_wells, 
        'means': [well_statistics[well]['mean'] for well in disintegrative_wells if well in well_statistics],
        'average': 0,
        'std': 0
    }
    
    if integrative_stats['means']:
        integrative_stats['average'] = float(np.mean(integrative_stats['means']))
        integrative_stats['std'] = float(np.std(integrative_stats['means']))
    
    if disintegrative_stats['means']:
        disintegrative_stats['average'] = float(np.mean(disintegrative_stats['means']))
        disintegrative_stats['std'] = float(np.std(disintegrative_stats['means']))
    
    # Overall civic virtue analysis
    net_civic_virtue = integrative_stats['average'] - disintegrative_stats['average']
    
    # Generate summary
    summary = {
        'analysis_metadata': {
            'source_file': results_file,
            'analysis_timestamp': datetime.now().isoformat(),
            'test_type': 'multi_run_consistency',
            'model': 'claude-3.5-sonnet',
            'framework': 'civic_virtue',
            'text_source': 'Obama First Inaugural 2009'
        },
        'run_summary': {
            'total_runs': len(data['individual_runs']),
            'successful_runs': len(all_scores),
            'success_rate': len(all_scores) / len(data['individual_runs']),
            'total_cost': sum(run['cost'] for run in run_metadata),
            'average_duration': float(np.mean([run['duration'] for run in run_metadata])),
            'cost_per_run': float(np.mean([run['cost'] for run in run_metadata]))
        },
        'civic_virtue_analysis': {
            'integrative_wells': integrative_stats,
            'disintegrative_wells': disintegrative_stats,
            'net_civic_virtue_score': float(net_civic_virtue),
            'interpretation': (
                'strong' if net_civic_virtue > 0.5 else
                'moderate' if net_civic_virtue > 0.2 else
                'mild' if net_civic_virtue > 0 else 'low'
            )
        },
        'well_statistics': well_statistics,
        'consistency_analysis': {
            'high_consistency': [well for well, stats in well_statistics.items() if stats['std'] <= 0.05],
            'moderate_consistency': [well for well, stats in well_statistics.items() if 0.05 < stats['std'] <= 0.1],
            'variable_consistency': [well for well, stats in well_statistics.items() if stats['std'] > 0.1]
        },
        'raw_run_data': run_metadata
    }
    
    return summary, all_scores

def create_visualization(summary, all_scores):
    """Create comprehensive visualization with error bars"""
    
    # Set up the plot style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Obama Inaugural Speech - Multi-Run Civic Virtue Analysis\nClaude 3.5 Sonnet (5 runs)', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Extract data for plotting
    wells = list(summary['well_statistics'].keys())
    means = [summary['well_statistics'][well]['mean'] for well in wells]
    stds = [summary['well_statistics'][well]['std'] for well in wells]
    
    # Categorize wells for coloring
    integrative_wells = ['Dignity', 'Truth', 'Hope', 'Justice', 'Pragmatism']
    colors = ['#2E8B57' if well in integrative_wells else '#CD5C5C' for well in wells]
    
    # Plot 1: Bar chart with error bars
    bars = ax1.bar(range(len(wells)), means, yerr=stds, capsize=5, 
                   color=colors, alpha=0.7, edgecolor='black', linewidth=1)
    ax1.set_xlabel('Civic Virtue Wells')
    ax1.set_ylabel('Score (0.0 - 1.0)')
    ax1.set_title('Mean Scores with Standard Deviation', fontweight='bold')
    ax1.set_xticks(range(len(wells)))
    ax1.set_xticklabels(wells, rotation=45, ha='right')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    
    # Add value labels on bars
    for i, (bar, mean, std) in enumerate(zip(bars, means, stds)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + std + 0.02,
                f'{mean:.3f}±{std:.3f}', ha='center', va='bottom', fontsize=8)
    
    # Plot 2: Integrative vs Disintegrative comparison
    integrative_means = [summary['well_statistics'][well]['mean'] for well in integrative_wells]
    integrative_stds = [summary['well_statistics'][well]['std'] for well in integrative_wells]
    
    disintegrative_wells = ['Tribalism', 'Manipulation', 'Fantasy', 'Resentment', 'Fear']
    disintegrative_means = [summary['well_statistics'][well]['mean'] for well in disintegrative_wells]
    disintegrative_stds = [summary['well_statistics'][well]['std'] for well in disintegrative_wells]
    
    x_int = range(len(integrative_wells))
    x_dis = range(len(disintegrative_wells))
    
    ax2.bar(x_int, integrative_means, yerr=integrative_stds, capsize=3,
            color='#2E8B57', alpha=0.7, label='Integrative Wells', width=0.8)
    ax2.bar([x + len(integrative_wells) + 0.5 for x in x_dis], disintegrative_means, 
            yerr=disintegrative_stds, capsize=3,
            color='#CD5C5C', alpha=0.7, label='Disintegrative Wells', width=0.8)
    
    all_well_names = integrative_wells + disintegrative_wells
    ax2.set_xticks(list(x_int) + [x + len(integrative_wells) + 0.5 for x in x_dis])
    ax2.set_xticklabels(all_well_names, rotation=45, ha='right')
    ax2.set_ylabel('Score (0.0 - 1.0)')
    ax2.set_title('Integrative vs Disintegrative Wells', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1)
    
    # Plot 3: Consistency analysis (standard deviation)
    consistency_colors = ['#228B22' if std <= 0.05 else '#FFD700' if std <= 0.1 else '#FF6347' for std in stds]
    bars3 = ax3.bar(range(len(wells)), stds, color=consistency_colors, alpha=0.7, edgecolor='black')
    ax3.set_xlabel('Civic Virtue Wells')
    ax3.set_ylabel('Standard Deviation')
    ax3.set_title('Consistency Across Runs (Lower = More Consistent)', fontweight='bold')
    ax3.set_xticks(range(len(wells)))
    ax3.set_xticklabels(wells, rotation=45, ha='right')
    ax3.grid(True, alpha=0.3)
    
    # Add consistency legend
    ax3.axhline(y=0.05, color='green', linestyle='--', alpha=0.7, label='High consistency (≤0.05)')
    ax3.axhline(y=0.1, color='orange', linestyle='--', alpha=0.7, label='Moderate consistency (≤0.1)')
    ax3.legend(loc='upper right', fontsize=8)
    
    # Plot 4: Summary statistics
    ax4.axis('off')
    
    # Create summary text
    summary_text = f"""
ANALYSIS SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test Configuration:
• Model: Claude 3.5 Sonnet
• Framework: Civic Virtue  
• Runs: {summary['run_summary']['successful_runs']}/{summary['run_summary']['total_runs']}
• Success Rate: {summary['run_summary']['success_rate']:.1%}

Performance Metrics:
• Total Cost: ${summary['run_summary']['total_cost']:.4f}
• Avg Duration: {summary['run_summary']['average_duration']:.1f}s
• Cost per Run: ${summary['run_summary']['cost_per_run']:.4f}

Civic Virtue Analysis:
• Integrative Avg: {summary['civic_virtue_analysis']['integrative_wells']['average']:.3f}
• Disintegrative Avg: {summary['civic_virtue_analysis']['disintegrative_wells']['average']:.3f}
• Net Civic Virtue: {summary['civic_virtue_analysis']['net_civic_virtue_score']:.3f}
• Interpretation: {summary['civic_virtue_analysis']['interpretation'].upper()}

Consistency Results:
• High Consistency: {len(summary['consistency_analysis']['high_consistency'])} wells
• Moderate Consistency: {len(summary['consistency_analysis']['moderate_consistency'])} wells  
• Variable Consistency: {len(summary['consistency_analysis']['variable_consistency'])} wells

Top Civic Virtue Scores:
• {max(summary['well_statistics'].items(), key=lambda x: x[1]['mean'])[0]}: {max(summary['well_statistics'].items(), key=lambda x: x[1]['mean'])[1]['mean']:.3f}
• Most Consistent: {min(summary['well_statistics'].items(), key=lambda x: x[1]['std'])[0]} (σ={min(summary['well_statistics'].items(), key=lambda x: x[1]['std'])[1]['std']:.3f})
"""
    
    ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    return fig

def main():
    """Generate complete analysis summary and visualization"""
    print("🔄 Generating comprehensive multi-run analysis summary...")
    
    # Generate statistical summary
    summary, all_scores = generate_statistical_summary()
    if not summary:
        return
    
    # Save JSON summary
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = f"test_results/obama_multirun_summary_{timestamp}.json"
    
    with open(json_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Statistical summary saved: {json_file}")
    
    # Create visualization
    print("🎨 Creating visualization...")
    fig = create_visualization(summary, all_scores)
    
    # Save visualization
    viz_file = f"test_results/obama_multirun_visualization_{timestamp}.png"
    fig.savefig(viz_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ Visualization saved: {viz_file}")
    
    # Print key findings
    print(f"\n📊 KEY FINDINGS:")
    print(f"   Net Civic Virtue Score: {summary['civic_virtue_analysis']['net_civic_virtue_score']:.3f}")
    print(f"   Interpretation: {summary['civic_virtue_analysis']['interpretation'].upper()}")
    print(f"   Most Consistent Well: {min(summary['well_statistics'].items(), key=lambda x: x[1]['std'])[0]}")
    print(f"   Highest Scoring Well: {max(summary['well_statistics'].items(), key=lambda x: x[1]['mean'])[0]} ({max(summary['well_statistics'].items(), key=lambda x: x[1]['mean'])[1]['mean']:.3f})")
    
    print(f"\n📁 Generated Files:")
    print(f"   📊 Summary JSON: {json_file}")
    print(f"   📈 Visualization: {viz_file}")

if __name__ == "__main__":
    main() 