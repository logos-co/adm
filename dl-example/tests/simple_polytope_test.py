"""
Simple Polytope Test

This script creates a minimal test case to verify the polytope visualization
system works correctly with a small, well-defined constraint set.
"""

import numpy as np
from qualitative_evaluation_translator import (
    QualitativeEvaluationTranslator, 
    QualitativeEvaluation, 
    EvaluationType,
    ComparisonOperator
)
from polytope_visualizer import PolytopeVisualizer


def create_simple_test_case():
    """Create a simple 2D test case with guaranteed feasible region"""
    
    # Simple 2-project, 2-criteria system
    projects = ["Project A", "Project B"]
    criteria = ["Value", "Cost"]
    
    translator = QualitativeEvaluationTranslator(projects, criteria)
    
    # Add simple constraints that create a bounded feasible region
    # Constraint 1: Project A has value between 0.4 and 0.9 (higher range)
    eval1 = QualitativeEvaluation(
        evaluator_id="expert_1",
        evaluation_type=EvaluationType.RANGE,
        projects=["Project A"],
        values=[0.4, 0.9],
        criteria="Value"
    )
    translator.add_evaluation(eval1)
    
    # Constraint 2: Project B has value between 0.1 and 0.6 (lower range)
    eval2 = QualitativeEvaluation(
        evaluator_id="expert_1",
        evaluation_type=EvaluationType.RANGE,
        projects=["Project B"],
        values=[0.1, 0.6],
        criteria="Value"
    )
    translator.add_evaluation(eval2)
    
    # Constraint 3: Both projects have cost between 0.2 and 0.8
    eval3 = QualitativeEvaluation(
        evaluator_id="expert_2",
        evaluation_type=EvaluationType.RANGE,
        projects=["Project A"],
        values=[0.2, 0.8],
        criteria="Cost"
    )
    translator.add_evaluation(eval3)
    
    eval4 = QualitativeEvaluation(
        evaluator_id="expert_2",
        evaluation_type=EvaluationType.RANGE,
        projects=["Project B"],
        values=[0.2, 0.8],
        criteria="Cost"
    )
    translator.add_evaluation(eval4)
    
    # Skip the comparison constraint for now to ensure feasibility
    # The ranges already ensure Project A can have higher value than Project B
    
    return translator


def test_simple_polytope():
    """Test the polytope visualization with a simple case"""
    print("=== Simple Polytope Test ===\n")
    
    # Create simple test case
    translator = create_simple_test_case()
    print(f"Created translator with {len(translator.projects)} projects and {len(translator.criteria)} criteria")
    print(f"Added {len(translator.evaluations)} evaluations")
    
    # Create visualizer
    visualizer = PolytopeVisualizer(translator)
    print(f"Generated {len(visualizer.constraints)} constraints")
    
    # Check constraint matrices
    A_ineq, b_ineq, A_eq, b_eq = translator.get_constraint_matrices()
    print(f"Constraint matrix shape: {A_ineq.shape}")
    print(f"Inequality constraints: {len(b_ineq)}")
    print(f"Equality constraints: {len(b_eq)}")
    
    # Compute polytope properties
    print("\nComputing polytope properties...")
    properties = visualizer.compute_polytope_properties()
    
    print("Polytope Properties:")
    for key, value in properties.items():
        if isinstance(value, (int, float)):
            print(f"  {key}: {value}")
        elif isinstance(value, np.ndarray):
            print(f"  {key}: {value}")
        elif isinstance(value, dict):
            print(f"  {key}: computed")
        else:
            print(f"  {key}: {value}")
    
    # Create visualizations if we have vertices
    if properties['n_vertices'] > 0:
        print(f"\nCreating visualizations with {properties['n_vertices']} vertices...")
        
        # Create 2D visualization
        fig_2d = visualizer.create_2d_visualization(
            dim_x=0, dim_y=1,
            show_vertices=True,
            show_constraints=True,
            show_feasible_region=True
        )
        fig_2d.write_html("simple_test_2d.html")
        print("  Saved 2D visualization to: simple_test_2d.html")
        
        # Create dashboard
        fig_dashboard = visualizer.create_dimension_selector_dashboard()
        fig_dashboard.write_html("simple_test_dashboard.html")
        print("  Saved dashboard to: simple_test_dashboard.html")
        
        # Export data
        visualizer.export_polytope_data("simple_test_data.json", format="json")
        print("  Exported data to: simple_test_data.json")
        
    else:
        print("\nNo vertices found - constraint system may be over-constrained")
        print("Constraint details:")
        for i, constraint in enumerate(visualizer.constraints):
            print(f"  {i+1}: {constraint.constraint_id}")
            print(f"      Coefficients: {constraint.coefficients}")
            print(f"      Bound: {constraint.bound}")
            print(f"      Is equality: {constraint.is_equality}")
    
    return visualizer, properties


def debug_constraint_system():
    """Debug the constraint system to understand why it's over-constrained"""
    print("\n=== Debugging Constraint System ===\n")
    
    translator = create_simple_test_case()
    A_ineq, b_ineq, A_eq, b_eq = translator.get_constraint_matrices()
    
    print(f"System dimensions: {A_ineq.shape[1]} variables, {A_ineq.shape[0]} constraints")
    print(f"Constraint matrix A_ineq:\n{A_ineq}")
    print(f"Bounds b_ineq: {b_ineq}")
    
    # Check for obvious infeasibilities
    print("\nChecking for obvious constraint conflicts...")
    
    # Try to find a feasible point using linear programming
    from scipy.optimize import linprog
    
    # Minimize sum of variables (arbitrary objective)
    c = np.ones(A_ineq.shape[1])
    
    try:
        result = linprog(c, A_ub=A_ineq, b_ub=b_ineq, method='highs')
        if result.success:
            print(f"Found feasible point: {result.x}")
            print(f"Objective value: {result.fun}")
        else:
            print(f"No feasible solution found: {result.message}")
    except Exception as e:
        print(f"Error in linear programming: {e}")


if __name__ == "__main__":
    # Run simple test
    visualizer, properties = test_simple_polytope()
    
    # Debug if no vertices found
    if properties['n_vertices'] == 0:
        debug_constraint_system()
    
    print("\n=== Test Complete ===")
