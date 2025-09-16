#!/usr/bin/env python3
"""
Portfolio Optimization Demo using Logos/Nimbus/Status Projects

This script demonstrates the complete workflow of the robust human-machine
project portfolio selection system using real project data from the ecosystem.
"""

import json
import numpy as np
from typing import List, Dict

from qualitative_evaluation_translator import (
    QualitativeEvaluationTranslator,
    QualitativeEvaluation,
    EvaluationType,
    ComparisonOperator
)
from evaluation_input_parser import StructuredDataParser


def load_project_data():
    """Load the generated project portfolio data"""
    with open("logos_nimbus_status_projects.json", 'r') as f:
        data = json.load(f)
    
    projects = data['projects']
    project_names = [p['name'] for p in projects]
    
    print("Loaded Project Portfolio:")
    print(f"  Total Projects: {len(projects)}")
    print(f"  Total Budget: ${data['metadata']['total_budget']:.1f}M")
    print(f"  Ecosystems: {', '.join(data['metadata']['ecosystems'])}")
    
    return projects, project_names


def load_stakeholder_evaluations():
    """Load stakeholder evaluations"""
    evaluations = StructuredDataParser.from_json("stakeholder_evaluations.json")
    
    print(f"\nLoaded Stakeholder Evaluations:")
    print(f"  Total Evaluations: {len(evaluations)}")
    
    evaluator_counts = {}
    for eval in evaluations:
        evaluator_counts[eval.evaluator_id] = evaluator_counts.get(eval.evaluator_id, 0) + 1
    
    for evaluator, count in evaluator_counts.items():
        print(f"    {evaluator}: {count} evaluations")
    
    return evaluations


def demonstrate_constraint_generation(projects, evaluations):
    """Demonstrate the constraint generation process"""
    print("\n" + "="*60)
    print("CONSTRAINT GENERATION DEMONSTRATION")
    print("="*60)
    
    # Extract project names and criteria
    project_names = [p['name'] for p in projects]
    criteria = ['strategic_value', 'technical_complexity', 'market_impact', 
                'resource_requirement', 'innovation_level']
    
    # Initialize translator
    translator = QualitativeEvaluationTranslator(project_names, criteria)
    
    print(f"Initialized translator:")
    print(f"  Projects: {len(project_names)}")
    print(f"  Criteria: {len(criteria)}")
    print(f"  Variables: {len(project_names)} × {len(criteria)} = {len(project_names) * len(criteria)}")
    
    # Add evaluations
    for evaluation in evaluations:
        translator.add_evaluation(evaluation)
    
    # Generate constraints
    constraints = translator.translate_evaluations()
    
    print(f"\nConstraint Generation Results:")
    print(f"  Input Evaluations: {len(evaluations)}")
    print(f"  Generated Constraints: {len(constraints)}")
    
    # Get constraint matrices
    A_ineq, b_ineq, A_eq, b_eq = translator.get_constraint_matrices()
    
    print(f"  Inequality Constraints: {A_ineq.shape[0]}")
    print(f"  Equality Constraints: {A_eq.shape[0] if A_eq.size > 0 else 0}")
    print(f"  Constraint Matrix Shape: {A_ineq.shape}")
    
    # Show example constraints
    print(f"\nExample Constraints:")
    for i, constraint in enumerate(constraints[:5]):
        constraint_type = "=" if constraint.is_equality else "≤"
        print(f"  {i+1}. {constraint.constraint_id}")
        print(f"     Type: {constraint_type} {constraint.bound}")
        print(f"     Source: {constraint.source_evaluation.evaluator_id if constraint.source_evaluation else 'N/A'}")
    
    if len(constraints) > 5:
        print(f"  ... and {len(constraints) - 5} more constraints")
    
    return translator, constraints


def demonstrate_budget_constraints(projects):
    """Demonstrate budget constraint analysis"""
    print("\n" + "="*60)
    print("BUDGET CONSTRAINT ANALYSIS")
    print("="*60)
    
    with open("budget_constraints.json", 'r') as f:
        budget_data = json.load(f)
    
    print("Annual Budget Limits:")
    for year, budget in budget_data['annual_budgets'].items():
        print(f"  {year}: ${budget:.1f}M")
    
    print("\nBudget Utilization:")
    for year, data in budget_data['utilization_rates'].items():
        status = "⚠️  OVER BUDGET" if data['over_budget'] else "✅ Within Budget"
        print(f"  {year}: ${data['allocated']:.1f}M / ${data['limit']:.1f}M ({data['utilization_rate']:.1%}) {status}")
    
    if budget_data['constraint_violations']:
        print(f"\nBudget Violations: {len(budget_data['constraint_violations'])}")
        for violation in budget_data['constraint_violations']:
            print(f"  {violation['year']}: ${violation['excess']:.1f}M excess")
            print(f"    Affected projects: {len(violation['projects_affected'])}")
    
    return budget_data


def demonstrate_project_constraints(projects):
    """Demonstrate project interdependency constraints"""
    print("\n" + "="*60)
    print("PROJECT INTERDEPENDENCY ANALYSIS")
    print("="*60)
    
    cooperation_pairs = []
    precedence_pairs = []
    exclusive_pairs = []
    
    for project in projects:
        project_name = project['name']
        
        # Cooperation constraints
        for coop_project in project['cooperation_projects']:
            cooperation_pairs.append((project_name, coop_project))
        
        # Precedence constraints
        for prec_project in project['precedence_projects']:
            precedence_pairs.append((prec_project, project_name))  # prec_project must come before project_name
        
        # Exclusive constraints
        for excl_project in project['exclusive_projects']:
            exclusive_pairs.append((project_name, excl_project))
    
    print(f"Cooperation Constraints: {len(cooperation_pairs)}")
    if cooperation_pairs:
        print("  Projects with synergistic benefits:")
        for proj1, proj2 in cooperation_pairs[:3]:
            print(f"    • {proj1} ↔ {proj2}")
        if len(cooperation_pairs) > 3:
            print(f"    ... and {len(cooperation_pairs) - 3} more")
    
    print(f"\nPrecedence Constraints: {len(precedence_pairs)}")
    if precedence_pairs:
        print("  Project dependencies:")
        for proj1, proj2 in precedence_pairs:
            print(f"    • {proj1} → {proj2}")
    
    print(f"\nExclusive Constraints: {len(exclusive_pairs)}")
    if exclusive_pairs:
        print("  Mutually exclusive projects:")
        for proj1, proj2 in exclusive_pairs:
            print(f"    • {proj1} ⊗ {proj2}")
    
    return {
        'cooperation': cooperation_pairs,
        'precedence': precedence_pairs,
        'exclusive': exclusive_pairs
    }


def demonstrate_optimization_integration(translator, constraints):
    """Demonstrate integration with optimization frameworks"""
    print("\n" + "="*60)
    print("OPTIMIZATION FRAMEWORK INTEGRATION")
    print("="*60)
    
    # Get constraint matrices
    A_ineq, b_ineq, A_eq, b_eq = translator.get_constraint_matrices()
    
    print("Constraint System for Optimization:")
    print(f"  Decision Variables: {A_ineq.shape[1]}")
    print(f"  Inequality Constraints: A_ineq * x ≤ b_ineq")
    print(f"    Matrix Shape: {A_ineq.shape}")
    print(f"    Bounds Vector: {b_ineq.shape}")
    
    if A_eq.size > 0:
        print(f"  Equality Constraints: A_eq * x = b_eq")
        print(f"    Matrix Shape: {A_eq.shape}")
        print(f"    Bounds Vector: {b_eq.shape}")
    
    # Validate constraint system
    validation = translator.validate_constraints()
    print(f"\nConstraint System Validation:")
    print(f"  Feasible: {not validation['is_overconstrained']}")
    print(f"  Total Constraints: {validation['total_constraints']}")
    print(f"  Variables: {validation['n_variables']}")
    
    if validation['warnings']:
        print(f"  Warnings: {len(validation['warnings'])}")
        for warning in validation['warnings']:
            print(f"    - {warning}")
    
    # Example optimization setup
    print(f"\nExample Optimization Setup:")
    print(f"```python")
    print(f"from scipy.optimize import linprog")
    print(f"import numpy as np")
    print(f"")
    print(f"# Objective: maximize total strategic value")
    print(f"c = -np.ones({A_ineq.shape[1]})  # Negative for maximization")
    print(f"")
    print(f"# Constraints from qualitative evaluations")
    print(f"result = linprog(")
    print(f"    c=c,")
    print(f"    A_ub=A_ineq,")
    print(f"    b_ub=b_ineq,")
    if A_eq.size > 0:
        print(f"    A_eq=A_eq,")
        print(f"    b_eq=b_eq,")
    print(f"    bounds=[(0, 1) for _ in range({A_ineq.shape[1]})],")
    print(f"    method='highs'")
    print(f")")
    print(f"```")
    
    return A_ineq, b_ineq, A_eq, b_eq


def demonstrate_robust_evaluation():
    """Demonstrate robust evaluation criteria"""
    print("\n" + "="*60)
    print("ROBUST EVALUATION CRITERIA")
    print("="*60)
    
    print("The robust evaluation framework addresses uncertainty in project values:")
    print("1. Qualitative evaluations define a convex polytope of feasible values")
    print("2. Project values are not fixed points but regions in value space")
    print("3. Portfolio comparison uses boundary point evaluation")
    print("4. Dominance relationships are determined robustly")
    
    print("\nKey Benefits:")
    print("  • Handles uncertainty in expert assessments")
    print("  • Reduces dependence on exact numerical values")
    print("  • Enables broader stakeholder participation")
    print("  • Provides robust portfolio recommendations")
    
    print("\nIntegration with Deep Preference-based Q Network (DPbQN):")
    print("  • Constraint matrices define feasible action space")
    print("  • Boundary points enable robust state-action evaluation")
    print("  • Preference comparisons guide reinforcement learning")
    print("  • Human feedback improves optimization over time")


def main():
    """Run the complete portfolio optimization demonstration"""
    print("LOGOS/NIMBUS/STATUS PROJECT PORTFOLIO OPTIMIZATION")
    print("Robust Human-Machine Framework Demonstration")
    print("=" * 80)
    
    try:
        # Load data
        projects, project_names = load_project_data()
        evaluations = load_stakeholder_evaluations()
        
        # Demonstrate constraint generation
        translator, constraints = demonstrate_constraint_generation(projects, evaluations)
        
        # Demonstrate budget analysis
        budget_data = demonstrate_budget_constraints(projects)
        
        # Demonstrate project constraints
        project_constraints = demonstrate_project_constraints(projects)
        
        # Demonstrate optimization integration
        A_ineq, b_ineq, A_eq, b_eq = demonstrate_optimization_integration(translator, constraints)
        
        # Demonstrate robust evaluation
        demonstrate_robust_evaluation()
        
        print("\n" + "="*80)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY")
        print("="*80)
        
        print("\nSummary:")
        print(f"✅ Processed {len(projects)} projects from {len(set(p['ecosystem'] for p in projects))} ecosystems")
        print(f"✅ Translated {len(evaluations)} stakeholder evaluations into {len(constraints)} mathematical constraints")
        print(f"✅ Generated constraint system with {A_ineq.shape[1]} variables and {A_ineq.shape[0]} constraints")
        print(f"✅ Identified {len(project_constraints['cooperation'])} cooperation and {len(project_constraints['exclusive'])} exclusivity constraints")
        print(f"✅ Analyzed budget constraints with {len(budget_data['constraint_violations'])} violations")
        print(f"✅ Prepared optimization framework integration")
        
        print("\nNext Steps:")
        print("1. Implement Deep Preference-based Q Network (DPbQN) algorithm")
        print("2. Integrate constraint matrices with reinforcement learning")
        print("3. Develop robust evaluation criteria module")
        print("4. Create experience pool for preference learning")
        print("5. Deploy human-machine optimization system")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
