import pandas as pd
import numpy as np
import json
from datetime import datetime
import os

def load_and_prepare_data():
    """
    Load all CSV files from toy-data directory and prepare unified dataset
    """

    # Load all CSV files
    print("Loading CSV files...")

    # Core project data
    projects = pd.read_csv('toy-data/projects.csv')
    dependencies = pd.read_csv('toy-data/dependencies.csv')
    resources = pd.read_csv('toy-data/resources.csv')
    resource_allocations = pd.read_csv('toy-data/resource_allocations.csv')
    strategic_dimensions = pd.read_csv('toy-data/strategic_dimensions.csv')
    timeline_events = pd.read_csv('toy-data/timeline_events.csv')
    portfolio_metrics = pd.read_csv('toy-data/portfolio_metrics.csv')
    dependency_impacts = pd.read_csv('toy-data/dependency_impacts.csv')
    time_series_snapshots = pd.read_csv('toy-data/time_series_snapshots.csv')

    print(f"Loaded {len(projects)} projects, {len(dependencies)} dependencies, {len(resources)} resources")

    # Data cleaning and type conversions
    print("Cleaning and preparing data...")

    # Convert date columns
    date_columns = {
        'projects': ['start_date', 'end_date', 'created_date', 'last_updated'],
        'dependencies': ['created_date'],
        'resource_allocations': ['allocation_start', 'allocation_end'],
        'timeline_events': ['planned_date', 'actual_date'],
        'portfolio_metrics': ['metric_date'],
        'time_series_snapshots': ['snapshot_date'],
        'strategic_dimensions': ['last_assessed']
    }

    for df_name, cols in date_columns.items():
        df = locals()[df_name]
        for col in cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

    # Create unified project dataset
    print("Creating unified project dataset...")

    # Start with projects as base
    unified_projects = projects.copy()

    # Add strategic dimensions
    unified_projects = unified_projects.merge(
        strategic_dimensions,
        on='project_id',
        how='left'
    )

    # Calculate resource allocation summaries per project
    resource_summary = resource_allocations.groupby('project_id').agg({
        'allocated_amount': 'sum',
        'allocation_percentage': 'sum',
        'resource_id': 'count'
    }).rename(columns={
        'allocated_amount': 'total_allocated_amount',
        'allocation_percentage': 'total_allocation_percentage',
        'resource_id': 'resource_count'
    }).reset_index()

    unified_projects = unified_projects.merge(
        resource_summary,
        on='project_id',
        how='left'
    )

    # Add dependency counts
    dep_out = dependencies.groupby('source_project_id').size().rename('dependencies_out').reset_index()
    dep_in = dependencies.groupby('target_project_id').size().rename('dependencies_in').reset_index()

    unified_projects = unified_projects.merge(
        dep_out.rename(columns={'source_project_id': 'project_id'}),
        on='project_id',
        how='left'
    )

    unified_projects = unified_projects.merge(
        dep_in.rename(columns={'target_project_id': 'project_id'}),
        on='project_id',
        how='left'
    )

    # Fill NaN values
    unified_projects['dependencies_out'] = unified_projects['dependencies_out'].fillna(0)
    unified_projects['dependencies_in'] = unified_projects['dependencies_in'].fillna(0)
    unified_projects['total_allocated_amount'] = unified_projects['total_allocated_amount'].fillna(0)
    unified_projects['total_allocation_percentage'] = unified_projects['total_allocation_percentage'].fillna(0)
    unified_projects['resource_count'] = unified_projects['resource_count'].fillna(0)

    # Calculate derived metrics
    unified_projects['budget_utilization'] = unified_projects['budget_spent'] / unified_projects['budget_allocated']
    unified_projects['strategic_score_avg'] = unified_projects[['innovation_score', 'market_impact_score', 'strategic_fit_score', 'customer_value_score', 'competitive_advantage_score']].mean(axis=1)

    # Prepare dependency network data
    print("Preparing dependency network data...")

    # Enhance dependencies with project names
    dependencies_enhanced = dependencies.merge(
        projects[['project_id', 'name']].rename(columns={'project_id': 'source_project_id', 'name': 'source_name'}),
        on='source_project_id',
        how='left'
    ).merge(
        projects[['project_id', 'name']].rename(columns={'project_id': 'target_project_id', 'name': 'target_name'}),
        on='target_project_id',
        how='left'
    )

    # Prepare resource allocation network data
    print("Preparing resource allocation data...")

    resource_allocations_enhanced = resource_allocations.merge(
        projects[['project_id', 'name']].rename(columns={'name': 'project_name'}),
        on='project_id',
        how='left'
    ).merge(
        resources[['resource_id', 'resource_name', 'resource_type']],
        on='resource_id',
        how='left'
    )

    # Get latest time series data for each project
    latest_snapshots = time_series_snapshots.loc[
        time_series_snapshots.groupby('project_id')['snapshot_date'].idxmax()
    ]

    # Prepare data for export
    datasets = {
        'projects': unified_projects,
        'dependencies': dependencies_enhanced,
        'resources': resources,
        'resource_allocations': resource_allocations_enhanced,
        'timeline_events': timeline_events,
        'portfolio_metrics': portfolio_metrics,
        'dependency_impacts': dependency_impacts,
        'time_series_snapshots': time_series_snapshots,
        'latest_snapshots': latest_snapshots
    }

    return datasets

def create_decision_tree_data(projects_df):
    """
    Create decision tree data structure for portfolio investment decisions
    """
    print("Creating decision tree data...")

    # Define decision tree structure for portfolio investment decisions
    # Root question: Should we invest in this project?

    def create_node(name, question=None, condition=None, children=None, projects=None, recommendation=None, reasoning=None):
        node = {
            "name": name,
            "type": "decision" if question else "outcome",
            "projects": projects or [],
            "project_count": len(projects) if projects else 0
        }

        if question:
            node["question"] = question
            node["children"] = children or []
        else:
            node["recommendation"] = recommendation
            node["reasoning"] = reasoning

        return node

    # Get all projects with complete data
    complete_projects = projects_df.dropna(subset=['strategic_score_avg', 'risk_score', 'roi_projected']).copy()

    # Create project summaries for leaf nodes
    def get_project_summary(project_list):
        return [
            {
                "id": row['project_id'],
                "name": row['name'],
                "budget": row['budget_allocated'],
                "strategic_score": round(row['strategic_score_avg'], 1),
                "risk_score": row['risk_score'],
                "roi": row['roi_projected'],
                "status": row['status'],
                "priority": row['strategic_priority']
            }
            for _, row in project_list.iterrows()
        ]

    # Level 1: Strategic Priority
    high_priority = complete_projects[complete_projects['strategic_priority'].isin(['Critical', 'High'])]
    medium_low_priority = complete_projects[complete_projects['strategic_priority'].isin(['Medium', 'Low'])]

    # Level 2a: High Priority -> Risk Assessment
    high_priority_low_risk = high_priority[high_priority['risk_score'] <= 5]
    high_priority_high_risk = high_priority[high_priority['risk_score'] > 5]

    # Level 2b: Medium/Low Priority -> ROI Assessment
    medium_low_high_roi = medium_low_priority[medium_low_priority['roi_projected'] >= 1.5]
    medium_low_low_roi = medium_low_priority[medium_low_priority['roi_projected'] < 1.5]

    # Level 3a: High Priority, Low Risk -> Budget Assessment
    hp_lr_high_budget = high_priority_low_risk[high_priority_low_risk['budget_allocated'] >= 300000]
    hp_lr_low_budget = high_priority_low_risk[high_priority_low_risk['budget_allocated'] < 300000]

    # Level 3b: High Priority, High Risk -> Strategic Score Assessment
    hp_hr_high_strategic = high_priority_high_risk[high_priority_high_risk['strategic_score_avg'] >= 8.0]
    hp_hr_low_strategic = high_priority_high_risk[high_priority_high_risk['strategic_score_avg'] < 8.0]

    # Level 3c: Medium/Low Priority, High ROI -> Risk Assessment
    ml_hr_low_risk = medium_low_high_roi[medium_low_high_roi['risk_score'] <= 4]
    ml_hr_high_risk = medium_low_high_roi[medium_low_high_roi['risk_score'] > 4]

    # Build the decision tree structure
    decision_tree = create_node(
        name="Portfolio Investment Decision",
        question="What is the strategic priority of the project?",
        children=[
            create_node(
                name="High/Critical Priority",
                question="What is the risk level?",
                children=[
                    create_node(
                        name="Low Risk (≤5)",
                        question="What is the budget requirement?",
                        children=[
                            create_node(
                                name="High Budget (≥$300K)",
                                projects=get_project_summary(hp_lr_high_budget),
                                recommendation="PROCEED WITH CAUTION",
                                reasoning="High strategic value but significant investment. Ensure strong governance and milestone tracking."
                            ),
                            create_node(
                                name="Low Budget (<$300K)",
                                projects=get_project_summary(hp_lr_low_budget),
                                recommendation="STRONGLY RECOMMEND",
                                reasoning="High strategic value, low risk, manageable budget. Ideal portfolio addition."
                            )
                        ]
                    ),
                    create_node(
                        name="High Risk (>5)",
                        question="Is the strategic score high (≥8.0)?",
                        children=[
                            create_node(
                                name="High Strategic Score",
                                projects=get_project_summary(hp_hr_high_strategic),
                                recommendation="CONDITIONAL APPROVAL",
                                reasoning="High strategic value justifies risk. Implement strong risk mitigation strategies."
                            ),
                            create_node(
                                name="Lower Strategic Score",
                                projects=get_project_summary(hp_hr_low_strategic),
                                recommendation="DEFER OR REDESIGN",
                                reasoning="High risk without sufficient strategic justification. Consider alternatives or risk reduction."
                            )
                        ]
                    )
                ]
            ),
            create_node(
                name="Medium/Low Priority",
                question="Is the projected ROI attractive (≥1.5)?",
                children=[
                    create_node(
                        name="High ROI (≥1.5)",
                        question="What is the risk level?",
                        children=[
                            create_node(
                                name="Low Risk (≤4)",
                                projects=get_project_summary(ml_hr_low_risk),
                                recommendation="RECOMMEND",
                                reasoning="Good financial returns with manageable risk. Solid portfolio addition."
                            ),
                            create_node(
                                name="Higher Risk (>4)",
                                projects=get_project_summary(ml_hr_high_risk),
                                recommendation="EVALUATE ALTERNATIVES",
                                reasoning="Good ROI but elevated risk. Compare with other opportunities."
                            )
                        ]
                    ),
                    create_node(
                        name="Lower ROI (<1.5)",
                        projects=get_project_summary(medium_low_low_roi),
                        recommendation="DO NOT RECOMMEND",
                        reasoning="Limited strategic priority and poor financial returns. Resources better allocated elsewhere."
                    )
                ]
            )
        ]
    )

    return decision_tree

def export_for_visualization(datasets):
    """
    Export processed data in formats suitable for D3.js visualizations
    """
    print("Exporting data for visualizations...")

    # Create output directory
    os.makedirs('visualization_data', exist_ok=True)

    # Export as JSON for D3.js
    for name, df in datasets.items():
        # Convert datetime columns to strings for JSON serialization
        df_export = df.copy()
        for col in df_export.columns:
            if df_export[col].dtype == 'datetime64[ns]':
                df_export[col] = df_export[col].dt.strftime('%Y-%m-%d')

        # Export as JSON
        df_export.to_json(f'visualization_data/{name}.json', orient='records', indent=2)

        # Also export as CSV for backup
        df_export.to_csv(f'visualization_data/{name}_processed.csv', index=False)

    # Create specific datasets for visualizations

    # 1. Dependency network nodes and links
    projects_for_network = datasets['projects'][['project_id', 'name', 'budget_allocated', 'strategic_score_avg', 'status', 'portfolio_theme', 'risk_level']].copy()

    # Filter dependencies to only include those where both source and target projects exist
    valid_project_ids = set(projects_for_network['project_id'])
    dependencies_for_network = datasets['dependencies'][
        (datasets['dependencies']['source_project_id'].isin(valid_project_ids)) &
        (datasets['dependencies']['target_project_id'].isin(valid_project_ids))
    ][['source_project_id', 'target_project_id', 'dependency_type', 'dependency_strength', 'impact_if_broken']].copy()

    network_data = {
        'nodes': projects_for_network.to_dict('records'),
        'links': dependencies_for_network.to_dict('records')
    }

    with open('visualization_data/dependency_network.json', 'w') as f:
        json.dump(network_data, f, indent=2)

    # 2. Resource allocation matrix data
    resource_matrix = datasets['resource_allocations'].pivot_table(
        index='project_name',
        columns='resource_name',
        values='allocated_amount',
        fill_value=0
    )

    resource_matrix_data = {
        'projects': resource_matrix.index.tolist(),
        'resources': resource_matrix.columns.tolist(),
        'matrix': resource_matrix.values.tolist()
    }

    with open('visualization_data/resource_matrix.json', 'w') as f:
        json.dump(resource_matrix_data, f, indent=2)

    # 3. Strategic positioning data
    strategic_data = datasets['projects'][['project_id', 'name', 'budget_allocated', 'strategic_score_avg', 'risk_score', 'completion_percentage', 'status', 'portfolio_theme']].copy()
    strategic_data = strategic_data.dropna(subset=['strategic_score_avg', 'risk_score'])

    with open('visualization_data/strategic_positioning.json', 'w') as f:
        json.dump(strategic_data.to_dict('records'), f, indent=2)

    # 4. Decision tree data for portfolio investment decisions
    decision_tree_data = create_decision_tree_data(datasets['projects'])

    with open('visualization_data/decision_tree.json', 'w') as f:
        json.dump(decision_tree_data, f, indent=2)

    print("Data export complete!")
    print("Files created in visualization_data/ directory:")
    for file in os.listdir('visualization_data'):
        print(f"  - {file}")

def main():
    """
    Main execution function
    """
    print("=== Portfolio Data Preparation ===")

    # Load and prepare data
    datasets = load_and_prepare_data()

    # Print summary statistics
    print("\n=== Data Summary ===")
    print(f"Total projects: {len(datasets['projects'])}")
    print(f"Total dependencies: {len(datasets['dependencies'])}")
    print(f"Total resources: {len(datasets['resources'])}")
    print(f"Total resource allocations: {len(datasets['resource_allocations'])}")

    # Show sample of unified project data
    print("\n=== Sample Project Data ===")
    sample_cols = ['project_id', 'name', 'status', 'budget_allocated', 'strategic_score_avg', 'dependencies_out', 'dependencies_in']
    print(datasets['projects'][sample_cols].head())

    # Export for visualizations
    export_for_visualization(datasets)

    return datasets

if __name__ == "__main__":
    datasets = main()
