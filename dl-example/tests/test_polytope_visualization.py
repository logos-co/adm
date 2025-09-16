"""
Test Suite for Polytope Visualization Module

This module contains comprehensive tests for the polytope visualization
functionality, including unit tests and integration tests.
"""

import unittest
import numpy as np
import pandas as pd
import tempfile
import os
from typing import List, Dict, Any

from qualitative_evaluation_translator import (
    QualitativeEvaluationTranslator, 
    QualitativeEvaluation, 
    EvaluationType,
    ComparisonOperator
)
from polytope_visualizer import PolytopeVisualizer


class TestPolytopeVisualizer(unittest.TestCase):
    """Test cases for PolytopeVisualizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a simple test case with 2 projects and 2 criteria
        self.projects = ["Project A", "Project B"]
        self.criteria = ["Strategic Value", "Technical Feasibility"]
        
        self.translator = QualitativeEvaluationTranslator(
            projects=self.projects,
            criteria=self.criteria
        )
        
        # Add some basic evaluations
        evaluations = [
            QualitativeEvaluation(
                evaluator_id="test_evaluator_1",
                evaluation_type=EvaluationType.COMPARISON,
                projects=["Project A", "Project B"],
                operator=ComparisonOperator.GREATER,
                criteria="Strategic Value"
            ),
            QualitativeEvaluation(
                evaluator_id="test_evaluator_2",
                evaluation_type=EvaluationType.RANGE,
                projects=["Project A"],
                values=[0.6, 0.9],
                criteria="Strategic Value"
            ),
            QualitativeEvaluation(
                evaluator_id="test_evaluator_3",
                evaluation_type=EvaluationType.THRESHOLD,
                projects=["Project A"],
                operator=ComparisonOperator.GREATER_EQUAL,
                values=[0.5],
                criteria="Technical Feasibility"
            )
        ]
        
        for eval in evaluations:
            self.translator.add_evaluation(eval)
        
        self.visualizer = PolytopeVisualizer(self.translator)
    
    def test_initialization(self):
        """Test PolytopeVisualizer initialization."""
        self.assertEqual(self.visualizer.n_dimensions, 4)  # 2 projects × 2 criteria
        self.assertEqual(len(self.visualizer.dimension_names), 4)
        self.assertIsNotNone(self.visualizer.constraints)
        self.assertTrue(len(self.visualizer.constraints) > 0)
    
    def test_compute_vertices(self):
        """Test polytope vertex computation."""
        vertices = self.visualizer.compute_vertices()
        
        # Should return a numpy array
        self.assertIsInstance(vertices, np.ndarray)
        
        # If vertices exist, they should have the correct dimensionality
        if len(vertices) > 0:
            self.assertEqual(vertices.shape[1], self.visualizer.n_dimensions)
            
            # All vertices should satisfy constraints
            A_ineq, b_ineq, _, _ = self.translator.get_constraint_matrices()
            for vertex in vertices:
                constraint_violations = A_ineq @ vertex - b_ineq
                self.assertTrue(np.all(constraint_violations <= 1e-8), 
                              f"Vertex {vertex} violates constraints")
    
    def test_compute_polytope_properties(self):
        """Test polytope property computation."""
        properties = self.visualizer.compute_polytope_properties()
        
        # Check required properties
        required_keys = ['n_vertices', 'n_constraints', 'n_dimensions', 'dimension_names']
        for key in required_keys:
            self.assertIn(key, properties)
        
        # Check data types
        self.assertIsInstance(properties['n_vertices'], int)
        self.assertIsInstance(properties['n_constraints'], int)
        self.assertIsInstance(properties['n_dimensions'], int)
        self.assertIsInstance(properties['dimension_names'], list)
        
        # Check values make sense
        self.assertGreaterEqual(properties['n_vertices'], 0)
        self.assertGreater(properties['n_constraints'], 0)
        self.assertEqual(properties['n_dimensions'], 4)
    
    def test_2d_visualization(self):
        """Test 2D visualization creation."""
        fig = self.visualizer.create_2d_visualization(
            dim_x=0, dim_y=1,
            show_vertices=True,
            show_constraints=True,
            show_feasible_region=True
        )
        
        # Should return a plotly figure
        self.assertIsNotNone(fig)
        self.assertTrue(hasattr(fig, 'data'))
        self.assertTrue(hasattr(fig, 'layout'))
        
        # Should have some traces
        self.assertGreater(len(fig.data), 0)
    
    def test_3d_visualization(self):
        """Test 3D visualization creation."""
        fig = self.visualizer.create_3d_visualization(
            dim_x=0, dim_y=1, dim_z=2,
            show_vertices=True
        )
        
        # Should return a plotly figure
        self.assertIsNotNone(fig)
        self.assertTrue(hasattr(fig, 'data'))
        self.assertTrue(hasattr(fig, 'layout'))
    
    def test_dashboard_visualization(self):
        """Test dashboard visualization creation."""
        fig = self.visualizer.create_dimension_selector_dashboard()
        
        # Should return a plotly figure
        self.assertIsNotNone(fig)
        self.assertTrue(hasattr(fig, 'data'))
        self.assertTrue(hasattr(fig, 'layout'))
    
    def test_export_polytope_data(self):
        """Test polytope data export functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test JSON export
            json_file = os.path.join(temp_dir, "test_polytope.json")
            self.visualizer.export_polytope_data(json_file, format="json")
            self.assertTrue(os.path.exists(json_file))
            
            # Test CSV export
            csv_file = os.path.join(temp_dir, "test_polytope.csv")
            self.visualizer.export_polytope_data(csv_file, format="csv")
            # CSV file should exist if there are vertices
            vertices = self.visualizer.compute_vertices()
            if len(vertices) > 0:
                self.assertTrue(os.path.exists(csv_file))
            
            # Test NPZ export
            npz_file = os.path.join(temp_dir, "test_polytope.npz")
            self.visualizer.export_polytope_data(npz_file, format="npz")
            self.assertTrue(os.path.exists(npz_file))
    
    def test_invalid_export_format(self):
        """Test handling of invalid export format."""
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_file = os.path.join(temp_dir, "test.invalid")
            with self.assertRaises(ValueError):
                self.visualizer.export_polytope_data(invalid_file, format="invalid")


class TestPolytopeVisualizationIntegration(unittest.TestCase):
    """Integration tests for polytope visualization with real data."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        # Create a more complex scenario
        self.projects = ["Logos Core", "Nimbus Client", "Status App", "Waku Protocol"]
        self.criteria = ["Strategic Value", "Technical Feasibility", "Resource Efficiency"]
        
        self.translator = QualitativeEvaluationTranslator(
            projects=self.projects,
            criteria=self.criteria
        )
        
        # Add comprehensive evaluations
        evaluations = [
            # Comparisons
            QualitativeEvaluation(
                evaluator_id="test_evaluator_1",
                evaluation_type=EvaluationType.COMPARISON,
                projects=["Logos Core", "Status App"],
                operator=ComparisonOperator.GREATER,
                criteria="Strategic Value"
            ),
            QualitativeEvaluation(
                evaluator_id="test_evaluator_2",
                evaluation_type=EvaluationType.COMPARISON,
                projects=["Nimbus Client", "Waku Protocol"],
                operator=ComparisonOperator.GREATER,
                criteria="Technical Feasibility"
            ),
            
            # Ranges
            QualitativeEvaluation(
                evaluator_id="test_evaluator_3",
                evaluation_type=EvaluationType.RANGE,
                projects=["Logos Core"],
                values=[0.7, 0.95],
                criteria="Strategic Value"
            ),
            QualitativeEvaluation(
                evaluator_id="test_evaluator_4",
                evaluation_type=EvaluationType.RANGE,
                projects=["Nimbus Client"],
                values=[0.8, 1.0],
                criteria="Technical Feasibility"
            ),
            
            # Thresholds
            QualitativeEvaluation(
                evaluator_id="test_evaluator_5",
                evaluation_type=EvaluationType.THRESHOLD,
                projects=["Logos Core"],
                operator=ComparisonOperator.GREATER_EQUAL,
                values=[0.4],
                criteria="Strategic Value"
            ),
            QualitativeEvaluation(
                evaluator_id="test_evaluator_6",
                evaluation_type=EvaluationType.THRESHOLD,
                projects=["Nimbus Client"],
                operator=ComparisonOperator.GREATER_EQUAL,
                values=[0.3],
                criteria="Resource Efficiency"
            ),
            
            # Ranking
            QualitativeEvaluation(
                evaluator_id="test_evaluator_7",
                evaluation_type=EvaluationType.RANKING,
                projects=["Nimbus Client", "Logos Core", "Status App", "Waku Protocol"],
                criteria="Technical Feasibility"
            )
        ]
        
        for eval in evaluations:
            self.translator.add_evaluation(eval)
        
        self.visualizer = PolytopeVisualizer(self.translator)
    
    def test_complex_polytope_properties(self):
        """Test polytope properties with complex constraint set."""
        properties = self.visualizer.compute_polytope_properties()
        
        # Should have reasonable number of constraints
        self.assertGreater(properties['n_constraints'], 5)
        self.assertEqual(properties['n_dimensions'], 12)  # 4 projects × 3 criteria
        
        # Should be able to compute vertices
        vertices = self.visualizer.compute_vertices()
        self.assertEqual(properties['n_vertices'], len(vertices))
    
    def test_multiple_2d_projections(self):
        """Test creating multiple 2D projections."""
        # Test different dimension pairs
        dimension_pairs = [(0, 1), (0, 2), (1, 2), (3, 4)]
        
        for dim_x, dim_y in dimension_pairs:
            with self.subTest(dim_x=dim_x, dim_y=dim_y):
                fig = self.visualizer.create_2d_visualization(
                    dim_x=dim_x, dim_y=dim_y,
                    show_vertices=True,
                    show_constraints=True,
                    show_feasible_region=True
                )
                
                self.assertIsNotNone(fig)
                self.assertGreater(len(fig.data), 0)
    
    def test_3d_projections(self):
        """Test creating 3D projections."""
        # Test different dimension triplets
        dimension_triplets = [(0, 1, 2), (3, 4, 5), (0, 3, 6)]
        
        for dim_x, dim_y, dim_z in dimension_triplets:
            with self.subTest(dim_x=dim_x, dim_y=dim_y, dim_z=dim_z):
                fig = self.visualizer.create_3d_visualization(
                    dim_x=dim_x, dim_y=dim_y, dim_z=dim_z,
                    show_vertices=True
                )
                
                self.assertIsNotNone(fig)
    
    def test_constraint_sensitivity_analysis(self):
        """Test basic constraint sensitivity analysis."""
        original_properties = self.visualizer.compute_polytope_properties()
        original_n_vertices = original_properties['n_vertices']
        
        # Remove one constraint and check impact
        if len(self.visualizer.constraints) > 1:
            # Create new translator with one less constraint
            temp_translator = QualitativeEvaluationTranslator(
                projects=self.projects,
                criteria=self.criteria
            )
            
            # Add all but the first constraint
            for constraint in self.visualizer.constraints[1:]:
                temp_translator.constraints.append(constraint)
            
            temp_visualizer = PolytopeVisualizer(temp_translator)
            temp_properties = temp_visualizer.compute_polytope_properties()
            
            # Should have same or more vertices (less restrictive)
            self.assertGreaterEqual(temp_properties['n_vertices'], original_n_vertices)


class TestPolytopeVisualizationEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_constraint_set(self):
        """Test behavior with no constraints."""
        translator = QualitativeEvaluationTranslator(
            projects=["Project A"],
            criteria=["Criterion 1"]
        )
        
        visualizer = PolytopeVisualizer(translator)
        
        # Should handle empty constraint set gracefully
        properties = visualizer.compute_polytope_properties()
        self.assertEqual(properties['n_constraints'], 0)
    
    def test_infeasible_constraint_set(self):
        """Test behavior with infeasible constraints."""
        translator = QualitativeEvaluationTranslator(
            projects=["Project A"],
            criteria=["Criterion 1"]
        )
        
        # Add contradictory constraints
        eval1 = QualitativeEvaluation(
            evaluator_id="test_evaluator_1",
            evaluation_type=EvaluationType.RANGE,
            projects=["Project A"],
            values=[0.8, 0.9],
            criteria="Criterion 1"
        )
        
        eval2 = QualitativeEvaluation(
            evaluator_id="test_evaluator_2",
            evaluation_type=EvaluationType.RANGE,
            projects=["Project A"],
            values=[0.1, 0.2],
            criteria="Criterion 1"
        )
        
        translator.add_evaluation(eval1)
        translator.add_evaluation(eval2)
        
        visualizer = PolytopeVisualizer(translator)
        
        # Should handle infeasible constraints gracefully
        vertices = visualizer.compute_vertices()
        properties = visualizer.compute_polytope_properties()
        
        # Should have no vertices for infeasible system
        self.assertEqual(len(vertices), 0)
        self.assertEqual(properties['n_vertices'], 0)
    
    def test_single_dimension(self):
        """Test behavior with single dimension."""
        translator = QualitativeEvaluationTranslator(
            projects=["Project A"],
            criteria=["Criterion 1"]
        )
        
        eval1 = QualitativeEvaluation(
            evaluator_id="test_evaluator_1",
            evaluation_type=EvaluationType.RANGE,
            projects=["Project A"],
            values=[0.3, 0.7],
            criteria="Criterion 1"
        )
        
        translator.add_evaluation(eval1)
        visualizer = PolytopeVisualizer(translator)
        
        # Should handle single dimension gracefully
        properties = visualizer.compute_polytope_properties()
        self.assertEqual(properties['n_dimensions'], 1)


def run_visualization_tests():
    """Run all polytope visualization tests."""
    print("Running Polytope Visualization Tests...\n")
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPolytopeVisualizer))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPolytopeVisualizationIntegration))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPolytopeVisualizationEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\nTest Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_visualization_tests()
    exit(0 if success else 1)
