"""
Test Suite for Qualitative Evaluation Translation Module

This module contains comprehensive tests for the qualitative evaluation translation system,
including unit tests, integration tests, and example scenarios.
"""

import unittest
import numpy as np
import tempfile
import os
import json
from typing import List

from qualitative_evaluation_translator import (
    QualitativeEvaluationTranslator,
    QualitativeEvaluation,
    EvaluationType,
    ComparisonOperator,
    LinearConstraint
)
from evaluation_input_parser import (
    NaturalLanguageParser,
    StructuredDataParser,
    EvaluationExporter
)


class TestQualitativeEvaluationTranslator(unittest.TestCase):
    """Test cases for the main translator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.projects = ["ProjectA", "ProjectB", "ProjectC", "ProjectD"]
        self.criteria = ["value", "risk"]
        self.translator = QualitativeEvaluationTranslator(self.projects, self.criteria)
    
    def test_initialization(self):
        """Test translator initialization"""
        self.assertEqual(self.translator.n_projects, 4)
        self.assertEqual(self.translator.n_criteria, 2)
        self.assertEqual(len(self.translator.project_index), 4)
        self.assertEqual(len(self.translator.criteria_index), 2)
    
    def test_comparison_evaluation_greater(self):
        """Test parsing of greater-than comparison evaluations"""
        evaluation = QualitativeEvaluation(
            evaluator_id="test_expert",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["ProjectA", "ProjectB"],
            operator=ComparisonOperator.GREATER
        )
        
        constraints = self.translator.parse_comparison_evaluation(evaluation)
        
        # Should create one constraint per criterion
        self.assertEqual(len(constraints), 2)
        
        # Check first constraint (value criterion)
        constraint = constraints[0]
        self.assertFalse(constraint.is_equality)
        self.assertEqual(constraint.bound, -0.01)  # epsilon for strict inequality
        
        # Check coefficient vector: ProjectA coefficient should be 1, ProjectB should be -1
        expected_coeffs = np.zeros(8)  # 4 projects * 2 criteria
        expected_coeffs[0] = 1.0   # ProjectA, value criterion
        expected_coeffs[2] = -1.0  # ProjectB, value criterion
        np.testing.assert_array_equal(constraint.coefficients, expected_coeffs)
    
    def test_comparison_evaluation_equal(self):
        """Test parsing of equality comparison evaluations"""
        evaluation = QualitativeEvaluation(
            evaluator_id="test_expert",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["ProjectA", "ProjectB"],
            operator=ComparisonOperator.EQUAL
        )
        
        constraints = self.translator.parse_comparison_evaluation(evaluation)
        
        # Should create equality constraints
        for constraint in constraints:
            self.assertTrue(constraint.is_equality)
            self.assertEqual(constraint.bound, 0.0)
    
    def test_range_evaluation(self):
        """Test parsing of range evaluations"""
        evaluation = QualitativeEvaluation(
            evaluator_id="test_expert",
            evaluation_type=EvaluationType.RANGE,
            projects=["ProjectA"],
            values=[0.3, 0.7]
        )
        
        constraints = self.translator.parse_range_evaluation(evaluation)
        
        # Should create 2 constraints per criterion (lower and upper bounds)
        self.assertEqual(len(constraints), 4)  # 2 criteria * 2 bounds each
        
        # Check bounds
        bounds = [c.bound for c in constraints]
        self.assertIn(0.3, bounds)   # Lower bound
        self.assertIn(-0.7, bounds)  # Upper bound (negated for <= constraint)
    
    def test_ranking_evaluation(self):
        """Test parsing of ranking evaluations"""
        evaluation = QualitativeEvaluation(
            evaluator_id="test_expert",
            evaluation_type=EvaluationType.RANKING,
            projects=["ProjectA", "ProjectB", "ProjectC"]
        )
        
        constraints = self.translator.parse_ranking_evaluation(evaluation)
        
        # Should create pairwise comparisons: A>B and B>C
        # Each comparison creates 2 constraints (one per criterion)
        self.assertEqual(len(constraints), 4)  # 2 comparisons * 2 criteria
    
    def test_threshold_evaluation(self):
        """Test parsing of threshold evaluations"""
        evaluation = QualitativeEvaluation(
            evaluator_id="test_expert",
            evaluation_type=EvaluationType.THRESHOLD,
            projects=["ProjectA"],
            operator=ComparisonOperator.GREATER_EQUAL,
            values=[0.5]
        )
        
        constraints = self.translator.parse_threshold_evaluation(evaluation)
        
        # Should create one constraint per criterion
        self.assertEqual(len(constraints), 2)
        
        for constraint in constraints:
            self.assertFalse(constraint.is_equality)
            self.assertEqual(constraint.bound, 0.5)
    
    def test_constraint_matrices(self):
        """Test generation of constraint matrices"""
        # Add some evaluations
        evaluations = [
            QualitativeEvaluation(
                evaluator_id="expert1",
                evaluation_type=EvaluationType.COMPARISON,
                projects=["ProjectA", "ProjectB"],
                operator=ComparisonOperator.GREATER
            ),
            QualitativeEvaluation(
                evaluator_id="expert2",
                evaluation_type=EvaluationType.COMPARISON,
                projects=["ProjectA", "ProjectB"],
                operator=ComparisonOperator.EQUAL
            )
        ]
        
        for eval in evaluations:
            self.translator.add_evaluation(eval)
        
        A_ineq, b_ineq, A_eq, b_eq = self.translator.get_constraint_matrices()
        
        # Should have inequality constraints from first evaluation
        self.assertGreater(A_ineq.shape[0], 0)
        self.assertEqual(A_ineq.shape[1], 8)  # 4 projects * 2 criteria
        
        # Should have equality constraints from second evaluation
        self.assertGreater(A_eq.shape[0], 0)
        self.assertEqual(A_eq.shape[1], 8)
    
    def test_validation(self):
        """Test constraint validation"""
        # Add a simple evaluation
        evaluation = QualitativeEvaluation(
            evaluator_id="expert1",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["ProjectA", "ProjectB"],
            operator=ComparisonOperator.GREATER
        )
        self.translator.add_evaluation(evaluation)
        
        validation = self.translator.validate_constraints()
        
        self.assertIn('n_inequality_constraints', validation)
        self.assertIn('n_equality_constraints', validation)
        self.assertIn('total_constraints', validation)
        self.assertIn('n_variables', validation)
        self.assertIn('is_overconstrained', validation)
        self.assertIn('warnings', validation)
    
    def test_export_constraints(self):
        """Test constraint export functionality"""
        evaluation = QualitativeEvaluation(
            evaluator_id="expert1",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["ProjectA", "ProjectB"],
            operator=ComparisonOperator.GREATER
        )
        self.translator.add_evaluation(evaluation)
        
        # Test dict export
        constraint_dict = self.translator.export_constraints('dict')
        self.assertIn('constraints', constraint_dict)
        self.assertIn('projects', constraint_dict)
        self.assertIn('criteria', constraint_dict)
        
        # Test dataframe export
        constraint_df = self.translator.export_constraints('dataframe')
        self.assertGreater(len(constraint_df), 0)
        
        # Test matrices export
        matrices = self.translator.export_constraints('matrices')
        self.assertEqual(len(matrices), 4)  # A_ineq, b_ineq, A_eq, b_eq


class TestNaturalLanguageParser(unittest.TestCase):
    """Test cases for natural language parsing"""
    
    def setUp(self):
        self.parser = NaturalLanguageParser()
    
    def test_comparison_parsing(self):
        """Test parsing of comparison statements"""
        text = "ProjectA is better than ProjectB"
        evaluations = self.parser.parse_text(text, "expert1")
        
        # Should find at least one comparison evaluation
        self.assertGreaterEqual(len(evaluations), 1)
        
        # Find the comparison evaluation
        comparison_evals = [e for e in evaluations if e.evaluation_type == EvaluationType.COMPARISON]
        self.assertGreaterEqual(len(comparison_evals), 1)
        
        eval = comparison_evals[0]
        self.assertEqual(eval.evaluation_type, EvaluationType.COMPARISON)
        self.assertEqual(eval.projects, ["projecta", "projectb"])
        self.assertEqual(eval.operator, ComparisonOperator.GREATER)
    
    def test_range_parsing(self):
        """Test parsing of range statements"""
        text = "ProjectC should be between 0.3 and 0.7"
        evaluations = self.parser.parse_text(text, "expert1")
        
        # Should find at least one range evaluation
        self.assertGreaterEqual(len(evaluations), 1)
        
        # Find the range evaluation
        range_evals = [e for e in evaluations if e.evaluation_type == EvaluationType.RANGE]
        self.assertGreaterEqual(len(range_evals), 1)
        
        eval = range_evals[0]
        self.assertEqual(eval.evaluation_type, EvaluationType.RANGE)
        self.assertEqual(eval.projects, ["projectc"])
        self.assertEqual(eval.values, [0.3, 0.7])
    
    def test_threshold_parsing(self):
        """Test parsing of threshold statements"""
        text = "ProjectD must be at least 0.5"
        evaluations = self.parser.parse_text(text, "expert1")
        
        # Should find at least one threshold evaluation
        self.assertGreaterEqual(len(evaluations), 1)
        
        # Find the threshold evaluation
        threshold_evals = [e for e in evaluations if e.evaluation_type == EvaluationType.THRESHOLD]
        self.assertGreaterEqual(len(threshold_evals), 1)
        
        eval = threshold_evals[0]
        self.assertEqual(eval.evaluation_type, EvaluationType.THRESHOLD)
        self.assertEqual(eval.projects, ["projectd"])
        self.assertEqual(eval.operator, ComparisonOperator.GREATER_EQUAL)
        self.assertEqual(eval.values, [0.5])
    
    def test_multiple_statements(self):
        """Test parsing multiple statements in one text"""
        text = """
        ProjectA is better than ProjectB.
        ProjectC should be between 0.3 and 0.7.
        ProjectD must be at least 0.5.
        """
        evaluations = self.parser.parse_text(text, "expert1")
        
        # Should find at least 3 evaluations (may find more due to overlapping patterns)
        self.assertGreaterEqual(len(evaluations), 3)
        
        # Check that we have all expected types
        types = [eval.evaluation_type for eval in evaluations]
        self.assertIn(EvaluationType.COMPARISON, types)
        self.assertIn(EvaluationType.RANGE, types)
        self.assertIn(EvaluationType.THRESHOLD, types)


class TestStructuredDataParser(unittest.TestCase):
    """Test cases for structured data parsing"""
    
    def test_csv_export_import(self):
        """Test CSV export and import roundtrip"""
        evaluations = [
            QualitativeEvaluation(
                evaluator_id="expert1",
                evaluation_type=EvaluationType.COMPARISON,
                projects=["ProjectA", "ProjectB"],
                operator=ComparisonOperator.GREATER,
                confidence=0.8
            ),
            QualitativeEvaluation(
                evaluator_id="expert2",
                evaluation_type=EvaluationType.RANGE,
                projects=["ProjectC"],
                values=[0.3, 0.7],
                confidence=0.9
            )
        ]
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            # Export to CSV
            EvaluationExporter.to_csv(evaluations, temp_file)
            
            # Import from CSV
            imported_evaluations = StructuredDataParser.from_csv(temp_file)
            
            # Check that we got the same number of evaluations
            self.assertEqual(len(imported_evaluations), len(evaluations))
            
            # Check first evaluation
            eval1 = imported_evaluations[0]
            self.assertEqual(eval1.evaluator_id, "expert1")
            self.assertEqual(eval1.evaluation_type, EvaluationType.COMPARISON)
            self.assertEqual(eval1.projects, ["ProjectA", "ProjectB"])
            self.assertEqual(eval1.operator, ComparisonOperator.GREATER)
            self.assertEqual(eval1.confidence, 0.8)
            
        finally:
            # Clean up
            os.unlink(temp_file)
    
    def test_json_export_import(self):
        """Test JSON export and import roundtrip"""
        evaluations = [
            QualitativeEvaluation(
                evaluator_id="expert1",
                evaluation_type=EvaluationType.THRESHOLD,
                projects=["ProjectD"],
                operator=ComparisonOperator.GREATER_EQUAL,
                values=[0.5],
                confidence=0.85
            )
        ]
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Export to JSON
            EvaluationExporter.to_json(evaluations, temp_file)
            
            # Import from JSON
            imported_evaluations = StructuredDataParser.from_json(temp_file)
            
            # Check that we got the same evaluation
            self.assertEqual(len(imported_evaluations), 1)
            eval1 = imported_evaluations[0]
            self.assertEqual(eval1.evaluator_id, "expert1")
            self.assertEqual(eval1.evaluation_type, EvaluationType.THRESHOLD)
            self.assertEqual(eval1.projects, ["ProjectD"])
            self.assertEqual(eval1.operator, ComparisonOperator.GREATER_EQUAL)
            self.assertEqual(eval1.values, [0.5])
            
        finally:
            # Clean up
            os.unlink(temp_file)


class TestIntegrationScenarios(unittest.TestCase):
    """Integration tests with realistic scenarios"""
    
    def test_portfolio_selection_scenario(self):
        """Test a realistic portfolio selection scenario"""
        projects = ["WebApp", "MobileApp", "DataPlatform", "AISystem", "SecurityUpgrade"]
        criteria = ["business_value", "technical_risk", "resource_requirement"]
        
        translator = QualitativeEvaluationTranslator(projects, criteria)
        
        # Add various expert evaluations
        evaluations = [
            # Business expert comparisons
            QualitativeEvaluation(
                evaluator_id="business_expert",
                evaluation_type=EvaluationType.COMPARISON,
                projects=["WebApp", "MobileApp"],
                operator=ComparisonOperator.GREATER,
                confidence=0.8,
                criteria="business_value"
            ),
            QualitativeEvaluation(
                evaluator_id="business_expert",
                evaluation_type=EvaluationType.RANKING,
                projects=["AISystem", "DataPlatform", "SecurityUpgrade"],
                confidence=0.7,
                criteria="business_value"
            ),
            
            # Technical expert assessments
            QualitativeEvaluation(
                evaluator_id="tech_expert",
                evaluation_type=EvaluationType.RANGE,
                projects=["AISystem"],
                values=[0.7, 0.9],  # High technical risk
                confidence=0.9,
                criteria="technical_risk"
            ),
            QualitativeEvaluation(
                evaluator_id="tech_expert",
                evaluation_type=EvaluationType.THRESHOLD,
                projects=["SecurityUpgrade"],
                operator=ComparisonOperator.LESS_EQUAL,
                values=[0.3],  # Low technical risk
                confidence=0.85,
                criteria="technical_risk"
            ),
            
            # Resource manager constraints
            QualitativeEvaluation(
                evaluator_id="resource_manager",
                evaluation_type=EvaluationType.THRESHOLD,
                projects=["DataPlatform"],
                operator=ComparisonOperator.GREATER_EQUAL,
                values=[0.8],  # High resource requirement
                confidence=0.9,
                criteria="resource_requirement"
            )
        ]
        
        # Add all evaluations
        for eval in evaluations:
            translator.add_evaluation(eval)
        
        # Translate to constraints
        constraints = translator.translate_evaluations()
        
        # Should have generated multiple constraints
        self.assertGreater(len(constraints), 0)
        
        # Validate the constraint system
        validation = translator.validate_constraints()
        self.assertFalse(validation['is_overconstrained'])
        
        # Get constraint matrices
        A_ineq, b_ineq, A_eq, b_eq = translator.get_constraint_matrices()
        
        # Check dimensions
        expected_vars = len(projects) * len(criteria)  # 5 projects * 3 criteria = 15
        self.assertEqual(A_ineq.shape[1], expected_vars)
        if A_eq.size > 0:
            self.assertEqual(A_eq.shape[1], expected_vars)
        
        print(f"Generated {len(constraints)} constraints for portfolio selection scenario")
        print(f"Inequality constraints: {A_ineq.shape[0]}")
        print(f"Equality constraints: {A_eq.shape[0] if A_eq.size > 0 else 0}")
        print(f"Variables: {expected_vars}")
    
    def test_natural_language_integration(self):
        """Test integration with natural language input"""
        projects = ["ProjectAlpha", "ProjectBeta", "ProjectGamma"]
        translator = QualitativeEvaluationTranslator(projects)
        parser = NaturalLanguageParser()
        
        # Expert provides natural language evaluation
        expert_text = """
        ProjectAlpha is better than ProjectBeta.
        ProjectGamma should be between 0.4 and 0.8.
        ProjectBeta must be at least 0.3.
        Ranking: ProjectAlpha > ProjectGamma > ProjectBeta
        """
        
        # Parse natural language
        evaluations = parser.parse_text(expert_text, "domain_expert")
        
        # Add to translator
        for eval in evaluations:
            translator.add_evaluation(eval)
        
        # Generate constraints
        constraints = translator.translate_evaluations()
        
        # Should have generated constraints from all parsed evaluations
        self.assertGreater(len(constraints), 0)
        
        # Export for review
        constraint_dict = translator.export_constraints('dict')
        self.assertIn('constraints', constraint_dict)
        
        print(f"Parsed {len(evaluations)} evaluations from natural language")
        print(f"Generated {len(constraints)} mathematical constraints")


def create_example_scenario():
    """Create a comprehensive example scenario for demonstration"""
    print("\n" + "="*60)
    print("QUALITATIVE EVALUATION TRANSLATION MODULE EXAMPLE")
    print("="*60)
    
    # Define projects and criteria
    projects = ["CloudMigration", "MobileApp", "DataAnalytics", "CyberSecurity", "UserExperience"]
    criteria = ["strategic_value", "implementation_risk", "resource_cost"]
    
    print(f"\nProjects: {', '.join(projects)}")
    print(f"Evaluation Criteria: {', '.join(criteria)}")
    
    # Initialize translator
    translator = QualitativeEvaluationTranslator(projects, criteria)
    
    # Create diverse expert evaluations
    evaluations = [
        # CEO strategic priorities
        QualitativeEvaluation(
            evaluator_id="CEO",
            evaluation_type=EvaluationType.RANKING,
            projects=["CloudMigration", "CyberSecurity", "DataAnalytics", "MobileApp", "UserExperience"],
            confidence=0.9,
            criteria="strategic_value",
            metadata={"role": "executive", "department": "leadership"}
        ),
        
        # CTO technical risk assessment
        QualitativeEvaluation(
            evaluator_id="CTO",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["CloudMigration", "DataAnalytics"],
            operator=ComparisonOperator.GREATER,
            confidence=0.85,
            criteria="implementation_risk",
            metadata={"role": "technical", "department": "engineering"}
        ),
        
        # CFO budget constraints
        QualitativeEvaluation(
            evaluator_id="CFO",
            evaluation_type=EvaluationType.THRESHOLD,
            projects=["CloudMigration"],
            operator=ComparisonOperator.GREATER_EQUAL,
            values=[0.8],
            confidence=0.95,
            criteria="resource_cost",
            metadata={"role": "financial", "department": "finance"}
        ),
        
        # Product Manager user focus
        QualitativeEvaluation(
            evaluator_id="ProductManager",
            evaluation_type=EvaluationType.RANGE,
            projects=["UserExperience"],
            values=[0.7, 0.9],
            confidence=0.8,
            criteria="strategic_value",
            metadata={"role": "product", "department": "product"}
        ),
        
        # Security Expert assessment
        QualitativeEvaluation(
            evaluator_id="SecurityExpert",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["CyberSecurity", "CloudMigration"],
            operator=ComparisonOperator.LESS,
            confidence=0.9,
            criteria="implementation_risk",
            metadata={"role": "specialist", "department": "security"}
        )
    ]
    
    print(f"\nCollected {len(evaluations)} expert evaluations:")
    for i, eval in enumerate(evaluations, 1):
        print(f"  {i}. {eval.evaluator_id}: {eval.evaluation_type.value} - {eval.projects}")
    
    # Add evaluations to translator
    for eval in evaluations:
        translator.add_evaluation(eval)
    
    # Translate to mathematical constraints
    constraints = translator.translate_evaluations()
    
    print(f"\nGenerated {len(constraints)} mathematical constraints:")
    for i, constraint in enumerate(constraints[:5], 1):  # Show first 5
        constraint_type = "equality" if constraint.is_equality else "inequality"
        print(f"  {i}. {constraint.constraint_id} ({constraint_type}): bound = {constraint.bound}")
    if len(constraints) > 5:
        print(f"  ... and {len(constraints) - 5} more constraints")
    
    # Get constraint matrices
    A_ineq, b_ineq, A_eq, b_eq = translator.get_constraint_matrices()
    
    print(f"\nConstraint System Summary:")
    print(f"  Variables: {len(projects)} projects × {len(criteria)} criteria = {len(projects) * len(criteria)}")
    print(f"  Inequality constraints: {A_ineq.shape[0]}")
    print(f"  Equality constraints: {A_eq.shape[0] if A_eq.size > 0 else 0}")
    print(f"  Total constraints: {A_ineq.shape[0] + (A_eq.shape[0] if A_eq.size > 0 else 0)}")
    
    # Validate constraint system
    validation = translator.validate_constraints()
    print(f"\nValidation Results:")
    print(f"  Overconstrained: {validation['is_overconstrained']}")
    print(f"  Warnings: {len(validation['warnings'])}")
    for warning in validation['warnings']:
        print(f"    - {warning}")
    
    # Export constraints
    constraint_dict = translator.export_constraints('dict')
    
    print(f"\nConstraint Export:")
    print(f"  Format: Dictionary with {len(constraint_dict['constraints'])} constraints")
    print(f"  Projects: {constraint_dict['projects']}")
    print(f"  Criteria: {constraint_dict['criteria']}")
    
    return translator, constraints, validation


if __name__ == "__main__":
    # Run the example scenario
    create_example_scenario()
    
    print("\n" + "="*60)
    print("RUNNING UNIT TESTS")
    print("="*60)
    
    # Run unit tests
    unittest.main(verbosity=2, exit=False)
