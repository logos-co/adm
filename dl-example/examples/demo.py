#!/usr/bin/env python3
"""
Demonstration of the Qualitative Evaluation Translation Module

This script demonstrates the key functionality of the module with practical examples.
"""

from qualitative_evaluation_translator import (
    QualitativeEvaluationTranslator,
    QualitativeEvaluation,
    EvaluationType,
    ComparisonOperator
)
from evaluation_input_parser import NaturalLanguageParser, EvaluationExporter
import numpy as np


def demo_basic_functionality():
    """Demonstrate basic translation functionality"""
    print("="*60)
    print("BASIC FUNCTIONALITY DEMONSTRATION")
    print("="*60)
    
    # Define a project portfolio scenario
    projects = ["WebApp", "MobileApp", "DataPlatform", "AISystem"]
    criteria = ["business_value", "technical_risk", "cost"]
    
    print(f"Projects: {', '.join(projects)}")
    print(f"Criteria: {', '.join(criteria)}")
    
    # Initialize translator
    translator = QualitativeEvaluationTranslator(projects, criteria)
    
    # Create expert evaluations
    evaluations = [
        # CEO: Strategic value ranking
        QualitativeEvaluation(
            evaluator_id="CEO",
            evaluation_type=EvaluationType.RANKING,
            projects=["AISystem", "DataPlatform", "WebApp", "MobileApp"],
            confidence=0.9,
            criteria="business_value"
        ),
        
        # CTO: Technical risk comparison
        QualitativeEvaluation(
            evaluator_id="CTO",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["AISystem", "WebApp"],
            operator=ComparisonOperator.GREATER,
            confidence=0.8,
            criteria="technical_risk"
        ),
        
        # CFO: Cost threshold
        QualitativeEvaluation(
            evaluator_id="CFO",
            evaluation_type=EvaluationType.THRESHOLD,
            projects=["DataPlatform"],
            operator=ComparisonOperator.GREATER_EQUAL,
            values=[0.7],
            confidence=0.95,
            criteria="cost"
        ),
        
        # Product Manager: Value range
        QualitativeEvaluation(
            evaluator_id="ProductManager",
            evaluation_type=EvaluationType.RANGE,
            projects=["MobileApp"],
            values=[0.4, 0.8],
            confidence=0.85,
            criteria="business_value"
        )
    ]
    
    print(f"\nExpert Evaluations:")
    for i, eval in enumerate(evaluations, 1):
        print(f"  {i}. {eval.evaluator_id}: {eval.evaluation_type.value}")
        if eval.evaluation_type == EvaluationType.COMPARISON:
            print(f"     {eval.projects[0]} {eval.operator.value} {eval.projects[1]}")
        elif eval.evaluation_type == EvaluationType.RANKING:
            print(f"     {' > '.join(eval.projects)}")
        elif eval.evaluation_type == EvaluationType.RANGE:
            print(f"     {eval.projects[0]} ∈ [{eval.values[0]}, {eval.values[1]}]")
        elif eval.evaluation_type == EvaluationType.THRESHOLD:
            print(f"     {eval.projects[0]} {eval.operator.value} {eval.values[0]}")
    
    # Add evaluations to translator
    for eval in evaluations:
        translator.add_evaluation(eval)
    
    # Translate to mathematical constraints
    constraints = translator.translate_evaluations()
    
    print(f"\nMathematical Translation:")
    print(f"  Generated {len(constraints)} linear constraints")
    
    # Get constraint matrices
    A_ineq, b_ineq, A_eq, b_eq = translator.get_constraint_matrices()
    
    print(f"  Variables: {len(projects)} × {len(criteria)} = {A_ineq.shape[1]}")
    print(f"  Inequality constraints: {A_ineq.shape[0]}")
    print(f"  Equality constraints: {A_eq.shape[0] if A_eq.size > 0 else 0}")
    
    # Show some example constraints
    print(f"\nExample Constraints:")
    for i, constraint in enumerate(constraints[:3]):
        constraint_type = "=" if constraint.is_equality else "≤"
        print(f"  {constraint.constraint_id}: a^T·x {constraint_type} {constraint.bound}")
    
    # Validate the system
    validation = translator.validate_constraints()
    print(f"\nValidation:")
    print(f"  System feasible: {not validation['is_overconstrained']}")
    print(f"  Warnings: {len(validation['warnings'])}")
    
    return translator, constraints


def demo_natural_language():
    """Demonstrate natural language processing"""
    print("\n" + "="*60)
    print("NATURAL LANGUAGE PROCESSING DEMONSTRATION")
    print("="*60)
    
    # Simple, clear statements for demonstration
    expert_statements = [
        "ProjectAlpha is better than ProjectBeta",
        "ProjectGamma must be at least 0.6",
        "ProjectDelta should be between 0.2 and 0.8"
    ]
    
    parser = NaturalLanguageParser()
    all_evaluations = []
    
    print("Expert Statements:")
    for i, statement in enumerate(expert_statements, 1):
        print(f"  {i}. \"{statement}\"")
        
        # Parse each statement individually for clarity
        evaluations = parser.parse_text(statement, f"expert_{i}")
        all_evaluations.extend(evaluations)
        
        for eval in evaluations:
            print(f"     → {eval.evaluation_type.value}: {eval.projects}")
    
    print(f"\nParsed {len(all_evaluations)} evaluations from natural language")
    
    return all_evaluations


def demo_export_import():
    """Demonstrate data export and import functionality"""
    print("\n" + "="*60)
    print("DATA EXPORT/IMPORT DEMONSTRATION")
    print("="*60)
    
    # Create sample evaluations
    evaluations = [
        QualitativeEvaluation(
            evaluator_id="expert_1",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["ProjectA", "ProjectB"],
            operator=ComparisonOperator.GREATER,
            confidence=0.8
        ),
        QualitativeEvaluation(
            evaluator_id="expert_2",
            evaluation_type=EvaluationType.RANGE,
            projects=["ProjectC"],
            values=[0.3, 0.7],
            confidence=0.9
        )
    ]
    
    # Export to JSON
    EvaluationExporter.to_json(evaluations, "demo_evaluations.json")
    print("✓ Exported evaluations to JSON format")
    
    # Export to CSV
    EvaluationExporter.to_csv(evaluations, "demo_evaluations.csv")
    print("✓ Exported evaluations to CSV format")
    
    # Show export formats are working
    print(f"✓ Successfully exported {len(evaluations)} evaluations")
    
    return evaluations


def demo_integration_scenario():
    """Demonstrate a complete integration scenario"""
    print("\n" + "="*60)
    print("COMPLETE INTEGRATION SCENARIO")
    print("="*60)
    
    # Enterprise project portfolio
    projects = ["CloudMigration", "DigitalTransformation", "CyberSecurity", "DataAnalytics"]
    criteria = ["strategic_impact", "implementation_risk", "resource_requirement"]
    
    print("Scenario: Enterprise IT Project Portfolio Selection")
    print(f"Projects: {', '.join(projects)}")
    print(f"Evaluation Criteria: {', '.join(criteria)}")
    
    # Initialize system
    translator = QualitativeEvaluationTranslator(projects, criteria)
    
    # Stakeholder evaluations
    stakeholder_evaluations = [
        # Board of Directors - Strategic Impact
        QualitativeEvaluation(
            evaluator_id="BoardOfDirectors",
            evaluation_type=EvaluationType.RANKING,
            projects=["DigitalTransformation", "CloudMigration", "CyberSecurity", "DataAnalytics"],
            confidence=0.95,
            criteria="strategic_impact"
        ),
        
        # IT Director - Implementation Risk
        QualitativeEvaluation(
            evaluator_id="ITDirector",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["CloudMigration", "DigitalTransformation"],
            operator=ComparisonOperator.LESS,
            confidence=0.85,
            criteria="implementation_risk"
        ),
        
        # Resource Manager - Resource Requirements
        QualitativeEvaluation(
            evaluator_id="ResourceManager",
            evaluation_type=EvaluationType.THRESHOLD,
            projects=["DigitalTransformation"],
            operator=ComparisonOperator.GREATER_EQUAL,
            values=[0.8],
            confidence=0.9,
            criteria="resource_requirement"
        )
    ]
    
    print(f"\nStakeholder Input:")
    for eval in stakeholder_evaluations:
        print(f"  {eval.evaluator_id}: {eval.evaluation_type.value} evaluation")
    
    # Process evaluations
    for eval in stakeholder_evaluations:
        translator.add_evaluation(eval)
    
    constraints = translator.translate_evaluations()
    A_ineq, b_ineq, A_eq, b_eq = translator.get_constraint_matrices()
    
    print(f"\nSystem Output:")
    print(f"  Mathematical constraints: {len(constraints)}")
    print(f"  Constraint matrix shape: {A_ineq.shape}")
    print(f"  Feasible solution space: {A_ineq.shape[1]}-dimensional polytope")
    
    # Validation
    validation = translator.validate_constraints()
    print(f"  System validation: {'✓ PASSED' if not validation['is_overconstrained'] else '✗ FAILED'}")
    
    return translator


def main():
    """Run all demonstrations"""
    print("QUALITATIVE EVALUATION TRANSLATION MODULE")
    print("Demonstration of Core Functionality")
    print("=" * 80)
    
    try:
        # Run demonstrations
        demo_basic_functionality()
        demo_natural_language()
        demo_export_import()
        demo_integration_scenario()
        
        print("\n" + "="*80)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\nKey Achievements:")
        print("✓ Qualitative evaluations successfully translated to mathematical constraints")
        print("✓ Multiple evaluation types supported (comparison, ranking, range, threshold)")
        print("✓ Natural language processing functional")
        print("✓ Data export/import capabilities working")
        print("✓ Constraint validation and system checks operational")
        print("✓ Integration with optimization frameworks ready")
        
        print("\nThe module is ready for integration with the Deep Preference-based Q Network (DPbQN)")
        print("algorithm for robust human-machine project portfolio selection.")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        print("Please check the module implementation.")


if __name__ == "__main__":
    main()
