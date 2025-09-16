#!/usr/bin/env python3
"""
Test script to validate portfolio visualization data and functionality.
This script checks data integrity, file existence, and basic validation.
"""

import os
import json
import pandas as pd
from datetime import datetime

def test_data_files():
    """Test that all required data files exist and are valid."""
    print("=== Testing Data Files ===")

    # Check CSV files
    csv_files = [
        'toy-data/projects.csv',
        'toy-data/dependencies.csv',
        'toy-data/resources.csv',
        'toy-data/resource_allocations.csv',
        'toy-data/strategic_dimensions.csv',
        'toy-data/timeline_events.csv',
        'toy-data/portfolio_metrics.csv',
        'toy-data/dependency_impacts.csv',
        'toy-data/time_series_snapshots.csv'
    ]

    for file_path in csv_files:
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                print(f"✓ {file_path}: {len(df)} rows")
            except Exception as e:
                print(f"✗ {file_path}: Error reading - {e}")
        else:
            print(f"✗ {file_path}: File not found")

    # Check JSON files
    json_files = [
        'visualization_data/dependency_network.json',
        'visualization_data/resource_matrix.json',
        'visualization_data/strategic_positioning.json',
        'visualization_data/decision_tree.json'
    ]

    for file_path in json_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                print(f"✓ {file_path}: Valid JSON")
            except Exception as e:
                print(f"✗ {file_path}: Error reading - {e}")
        else:
            print(f"✗ {file_path}: File not found")

def test_visualization_files():
    """Test that all visualization JavaScript files exist."""
    print("\n=== Testing Visualization Files ===")

    js_files = [
        'js/dependency-graph.js',
        'js/resource-matrix.js',
        'js/strategic-matrix.js',
        'js/timeline-gantt.js',
        'js/portfolio-dashboard.js',
        'js/decision-tree.js'
    ]

    for file_path in js_files:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if 'function' in content and 'd3.' in content:
                    print(f"✓ {file_path}: Valid D3.js visualization")
                else:
                    print(f"⚠ {file_path}: May not be a valid D3.js file")
        else:
            print(f"✗ {file_path}: File not found")

    # Check main HTML file
    if os.path.exists('portfolio_visualizations.html'):
        with open('portfolio_visualizations.html', 'r') as f:
            content = f.read()
            if all(js_file.split('/')[-1] in content for js_file in js_files):
                print("✓ portfolio_visualizations.html: All JS files included")
            else:
                print("⚠ portfolio_visualizations.html: Some JS files may not be included")
    else:
        print("✗ portfolio_visualizations.html: File not found")

def test_data_integrity():
    """Test data integrity and relationships."""
    print("\n=== Testing Data Integrity ===")

    try:
        # Load core data
        projects = pd.read_csv('toy-data/projects.csv')
        dependencies = pd.read_csv('toy-data/dependencies.csv')
        resources = pd.read_csv('toy-data/resources.csv')
        allocations = pd.read_csv('toy-data/resource_allocations.csv')
        strategic = pd.read_csv('toy-data/strategic_dimensions.csv')

        # Test project IDs consistency
        project_ids = set(projects['project_id'])
        dep_source_ids = set(dependencies['source_project_id'])
        dep_target_ids = set(dependencies['target_project_id'])
        alloc_project_ids = set(allocations['project_id'])
        strategic_project_ids = set(strategic['project_id'])

        # Check for orphaned dependencies
        orphaned_deps = (dep_source_ids | dep_target_ids) - project_ids
        if orphaned_deps:
            print(f"⚠ Found orphaned dependency project IDs: {orphaned_deps}")
        else:
            print("✓ All dependency project IDs exist in projects table")

        # Check for orphaned allocations
        orphaned_allocs = alloc_project_ids - project_ids
        if orphaned_allocs:
            print(f"⚠ Found orphaned allocation project IDs: {orphaned_allocs}")
        else:
            print("✓ All allocation project IDs exist in projects table")

        # Check for orphaned strategic data
        orphaned_strategic = strategic_project_ids - project_ids
        if orphaned_strategic:
            print(f"⚠ Found orphaned strategic project IDs: {orphaned_strategic}")
        else:
            print("✓ All strategic project IDs exist in projects table")

        # Check resource IDs consistency
        resource_ids = set(resources['resource_id'])
        alloc_resource_ids = set(allocations['resource_id'])

        orphaned_resource_allocs = alloc_resource_ids - resource_ids
        if orphaned_resource_allocs:
            print(f"⚠ Found orphaned allocation resource IDs: {orphaned_resource_allocs}")
        else:
            print("✓ All allocation resource IDs exist in resources table")

        # Check for required fields
        required_project_fields = ['project_id', 'name', 'status', 'budget_allocated']
        missing_fields = [field for field in required_project_fields if field not in projects.columns]
        if missing_fields:
            print(f"✗ Missing required project fields: {missing_fields}")
        else:
            print("✓ All required project fields present")

        # Check for null values in critical fields
        null_counts = projects[required_project_fields].isnull().sum()
        if null_counts.any():
            print(f"⚠ Found null values in critical fields: {null_counts[null_counts > 0].to_dict()}")
        else:
            print("✓ No null values in critical project fields")

        print(f"✓ Data summary: {len(projects)} projects, {len(dependencies)} dependencies, {len(resources)} resources")

    except Exception as e:
        print(f"✗ Error testing data integrity: {e}")

def test_decision_tree_data():
    """Test decision tree data structure."""
    print("\n=== Testing Decision Tree Data ===")

    try:
        with open('visualization_data/decision_tree.json', 'r') as f:
            tree_data = json.load(f)

        def validate_node(node, path="root"):
            """Recursively validate tree node structure."""
            required_fields = ['name', 'type']
            for field in required_fields:
                if field not in node:
                    print(f"✗ Missing field '{field}' in node at {path}")
                    return False

            if node['type'] == 'decision':
                if 'question' not in node:
                    print(f"✗ Decision node missing 'question' at {path}")
                    return False
                if 'children' not in node or not isinstance(node['children'], list):
                    print(f"✗ Decision node missing valid 'children' at {path}")
                    return False

                # Validate children
                for i, child in enumerate(node['children']):
                    if not validate_node(child, f"{path}/child_{i}"):
                        return False

            elif node['type'] == 'outcome':
                required_outcome_fields = ['recommendation', 'reasoning', 'projects']
                for field in required_outcome_fields:
                    if field not in node:
                        print(f"✗ Outcome node missing '{field}' at {path}")
                        return False

                if not isinstance(node['projects'], list):
                    print(f"✗ Outcome node 'projects' not a list at {path}")
                    return False

            return True

        if validate_node(tree_data):
            print("✓ Decision tree structure is valid")

            # Count nodes
            def count_nodes(node):
                count = 1
                if node.get('children'):
                    for child in node['children']:
                        count += count_nodes(child)
                return count

            total_nodes = count_nodes(tree_data)
            print(f"✓ Decision tree contains {total_nodes} nodes")
        else:
            print("✗ Decision tree structure validation failed")

    except Exception as e:
        print(f"✗ Error testing decision tree: {e}")

def test_server_accessibility():
    """Test if the HTTP server is running and files are accessible."""
    print("\n=== Testing Server Accessibility ===")

    try:
        import urllib.request
        import urllib.error

        base_url = "http://localhost:8000"
        test_files = [
            "/portfolio_visualizations.html",
            "/js/dependency-graph.js",
            "/visualization_data/dependency_network.json"
        ]

        for file_path in test_files:
            try:
                response = urllib.request.urlopen(f"{base_url}{file_path}")
                if response.getcode() == 200:
                    print(f"✓ {file_path}: Accessible")
                else:
                    print(f"⚠ {file_path}: HTTP {response.getcode()}")
            except urllib.error.URLError:
                print(f"✗ {file_path}: Not accessible (server may not be running)")
                break
        else:
            print("✓ HTTP server appears to be running correctly")

    except ImportError:
        print("⚠ Cannot test server accessibility (urllib not available)")

def main():
    """Run all tests."""
    print("Portfolio Visualization Test Suite")
    print("=" * 50)

    test_data_files()
    test_visualization_files()
    test_data_integrity()
    test_decision_tree_data()
    test_server_accessibility()

    print("\n" + "=" * 50)
    print("Test suite completed!")
    print("\nTo run the visualizations:")
    print("1. Ensure HTTP server is running: python -m http.server 8000")
    print("2. Open browser to: http://localhost:8000/portfolio_visualizations.html")

if __name__ == "__main__":
    main()
