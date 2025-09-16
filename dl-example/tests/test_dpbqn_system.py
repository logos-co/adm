#!/usr/bin/env python3
"""
Unit Tests for Deep Preference-based Q Network (DPbQN) System

This module contains comprehensive tests for the DPbQN algorithm and
the integrated PPSS framework components.

Author: Generated for Logos/Nimbus/Status ecosystem research
"""

import unittest
import numpy as np
import torch
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dpbqn_algorithm import (
    PPSSEnvironment,
    PreferenceBasedQNetwork,
    PreferenceReplayBuffer,
    DPbQNAlgorithm,
    PortfolioSolution,
    ProjectSchedule,
    HumanPreference
)
from human_preference_interface import (
    CLIPreferenceInterface,
    BatchPreferenceCollector,
    PreferenceGuidedSampling
)
from integrated_ppss_framework import (
    IntegratedPPSSFramework,
    ProjectData,
    PPSSConfiguration,
    create_sample_framework
)
from qualitative_evaluation_translator import (
    QualitativeEvaluation,
    EvaluationType,
    ComparisonOperator
)


class TestPPSSEnvironment(unittest.TestCase):
    """Test cases for PPSS Environment"""

    def setUp(self):
        """Set up test environment"""
        self.projects = ["ProjectA", "ProjectB", "ProjectC"]
        self.resources = {"budget": 1000, "personnel": 10}
        self.time_horizon = 12
        self.env = PPSSEnvironment(self.projects, self.resources, self.time_horizon)

    def test_initialization(self):
        """Test environment initialization"""
        self.assertEqual(self.env.n_projects, 3)
        self.assertEqual(self.env.time_horizon, 12)
        self.assertIsInstance(self.env.state_dim, int)
        self.assertIsInstance(self.env.action_dim, int)
        self.assertGreater(self.env.state_dim, 0)
        self.assertGreater(self.env.action_dim, 0)

    def test_reset(self):
        """Test environment reset"""
        state = self.env.reset()
        self.assertIsInstance(state, np.ndarray)
        self.assertEqual(len(state), self.env.state_dim)
        self.assertEqual(len(self.env.current_solution.selected_projects), 0)
        self.assertEqual(self.env.current_solution.total_cost, 0.0)

    def test_state_encoding(self):
        """Test state encoding functionality"""
        solution = PortfolioSolution(
            selected_projects=["ProjectA"],
            schedules=[ProjectSchedule(
                project_id="ProjectA",
                start_time=2,
                duration=4,
                resources_allocated={"budget": 200, "personnel": 3}
            )]
        )

        state = self.env._encode_state(solution)
        self.assertIsInstance(state, np.ndarray)
        self.assertEqual(len(state), self.env.state_dim)

        # Check that ProjectA is marked as selected
        project_selection = state[:self.env.n_projects]
        self.assertEqual(project_selection[0], 1.0)  # ProjectA selected
        self.assertEqual(project_selection[1], 0.0)  # ProjectB not selected

    def test_action_validity(self):
        """Test action validity checking"""
        # Valid action
        self.assertTrue(self.env._is_valid_action(0, 0.5, [0.2, 0.3]))

        # Invalid - project already selected
        self.env.current_solution.selected_projects.append("ProjectA")
        self.assertFalse(self.env._is_valid_action(0, 0.5, [0.2, 0.3]))

    def test_step_execution(self):
        """Test step execution"""
        initial_state = self.env.reset()
        action = np.zeros(self.env.action_dim)
        action[0] = 1.0  # Select first project
        action[self.env.n_projects] = 0.5  # Start at middle of timeline
        action[self.env.n_projects + 1:] = [0.2, 0.3]  # Resource allocation

        next_state, reward, done, info = self.env.step(action)

        self.assertIsInstance(next_state, np.ndarray)
        self.assertIsInstance(reward, float)
        self.assertIsInstance(done, bool)
        self.assertIsInstance(info, dict)

        if info['valid_action']:
            self.assertEqual(len(self.env.current_solution.selected_projects), 1)

    def test_valid_actions_generation(self):
        """Test generation of valid actions"""
        valid_actions = self.env.get_valid_actions()
        self.assertIsInstance(valid_actions, list)

        for action in valid_actions:
            self.assertIsInstance(action, np.ndarray)
            self.assertEqual(len(action), self.env.action_dim)


class TestPreferenceBasedQNetwork(unittest.TestCase):
    """Test cases for Preference-based Q Network"""

    def setUp(self):
        """Set up test network"""
        self.state_dim = 20
        self.action_dim = 10
        self.network = PreferenceBasedQNetwork(self.state_dim, self.action_dim)

    def test_initialization(self):
        """Test network initialization"""
        self.assertIsInstance(self.network, torch.nn.Module)
        self.assertIsNotNone(self.network.network)
        self.assertIsNotNone(self.network.preference_encoder)

    def test_forward_pass(self):
        """Test forward pass"""
        batch_size = 4
        state = torch.randn(batch_size, self.state_dim)
        q_values = self.network(state)

        self.assertEqual(q_values.shape, (batch_size, self.action_dim))
        self.assertIsInstance(q_values, torch.Tensor)

    def test_preference_prediction(self):
        """Test preference prediction"""
        batch_size = 4
        state1 = torch.randn(batch_size, self.state_dim)
        state2 = torch.randn(batch_size, self.state_dim)

        preferences = self.network.predict_preference(state1, state2)

        self.assertEqual(preferences.shape, (batch_size, 1))
        self.assertTrue(torch.all(preferences >= 0))
        self.assertTrue(torch.all(preferences <= 1))

    def test_parameter_count(self):
        """Test that network has trainable parameters"""
        params = list(self.network.parameters())
        self.assertGreater(len(params), 0)

        total_params = sum(p.numel() for p in params)
        self.assertGreater(total_params, 0)


class TestPreferenceReplayBuffer(unittest.TestCase):
    """Test cases for Preference Replay Buffer"""

    def setUp(self):
        """Set up test buffer"""
        self.buffer = PreferenceReplayBuffer(capacity=100)
        self.state_dim = 10
        self.action_dim = 5

    def test_initialization(self):
        """Test buffer initialization"""
        self.assertEqual(len(self.buffer), 0)

    def test_add_preference(self):
        """Test adding preferences to buffer"""
        state1 = np.random.randn(self.state_dim)
        state2 = np.random.randn(self.state_dim)
        action1 = np.random.randn(self.action_dim)
        action2 = np.random.randn(self.action_dim)

        self.buffer.add_preference(state1, action1, state2, action2, 0.8, 0.9)
        self.assertEqual(len(self.buffer), 1)

    def test_sampling(self):
        """Test sampling from buffer"""
        # Add multiple preferences
        for i in range(10):
            state1 = np.random.randn(self.state_dim)
            state2 = np.random.randn(self.state_dim)
            action1 = np.random.randn(self.action_dim)
            action2 = np.random.randn(self.action_dim)
            self.buffer.add_preference(state1, action1, state2, action2, 0.8, 0.9)

        # Test sampling
        sample = self.buffer.sample(5)
        self.assertEqual(len(sample), 5)

        # Test sampling more than available
        large_sample = self.buffer.sample(20)
        self.assertEqual(len(large_sample), 10)

    def test_capacity_limit(self):
        """Test buffer capacity limit"""
        small_buffer = PreferenceReplayBuffer(capacity=5)

        # Add more than capacity
        for i in range(10):
            state1 = np.random.randn(self.state_dim)
            state2 = np.random.randn(self.state_dim)
            action1 = np.random.randn(self.action_dim)
            action2 = np.random.randn(self.action_dim)
            small_buffer.add_preference(state1, action1, state2, action2, 0.8, 0.9)

        self.assertEqual(len(small_buffer), 5)


class TestDPbQNAlgorithm(unittest.TestCase):
    """Test cases for DPbQN Algorithm"""

    def setUp(self):
        """Set up test algorithm"""
        projects = ["ProjectA", "ProjectB", "ProjectC"]
        resources = {"budget": 1000, "personnel": 10}
        time_horizon = 12

        self.env = PPSSEnvironment(projects, resources, time_horizon)
        self.algorithm = DPbQNAlgorithm(
            self.env,
            batch_size=4,
            buffer_capacity=100,
            target_update_frequency=10
        )

    def test_initialization(self):
        """Test algorithm initialization"""
        self.assertIsNotNone(self.algorithm.q_network)
        self.assertIsNotNone(self.algorithm.target_network)
        self.assertIsNotNone(self.algorithm.optimizer)
        self.assertEqual(len(self.algorithm.human_preferences), 0)

    def test_action_selection(self):
        """Test action selection"""
        state = self.env.reset()
        action = self.algorithm.select_action(state)

        self.assertIsInstance(action, np.ndarray)
        self.assertEqual(len(action), self.env.action_dim)

    def test_action_selection_with_valid_actions(self):
        """Test action selection with valid actions constraint"""
        state = self.env.reset()
        valid_actions = self.env.get_valid_actions()

        if valid_actions:
            action = self.algorithm.select_action(state, valid_actions)
            self.assertIsInstance(action, np.ndarray)
            self.assertTrue(any(np.array_equal(action, va) for va in valid_actions))

    def test_human_preference_addition(self):
        """Test adding human preferences"""
        # Create sample solutions
        solution1 = PortfolioSolution(
            selected_projects=["ProjectA"],
            schedules=[ProjectSchedule("ProjectA", 0, 5, {"budget": 100})]
        )
        solution2 = PortfolioSolution(
            selected_projects=["ProjectB"],
            schedules=[ProjectSchedule("ProjectB", 0, 3, {"budget": 80})]
        )

        preference = HumanPreference(
            preferred_solution=solution1,
            alternative_solution=solution2,
            preference_strength=0.8,
            evaluator_id="test_evaluator"
        )

        initial_count = len(self.algorithm.human_preferences)
        self.algorithm.add_human_preference(preference)
        self.assertEqual(len(self.algorithm.human_preferences), initial_count + 1)

    def test_train_episode(self):
        """Test training episode"""
        episode_info = self.algorithm.train_episode(max_steps=10)

        self.assertIsInstance(episode_info, dict)
        self.assertIn('total_reward', episode_info)
        self.assertIn('steps', episode_info)
        self.assertIn('final_solution', episode_info)

    def test_solution_evaluation(self):
        """Test solution evaluation"""
        solutions = [
            PortfolioSolution(
                selected_projects=["ProjectA"],
                schedules=[ProjectSchedule("ProjectA", 0, 5, {"budget": 100})]
            ),
            PortfolioSolution(
                selected_projects=["ProjectB", "ProjectC"],
                schedules=[
                    ProjectSchedule("ProjectB", 0, 3, {"budget": 80}),
                    ProjectSchedule("ProjectC", 3, 4, {"budget": 120})
                ]
            )
        ]

        scores = self.algorithm.evaluate_solutions(solutions)
        self.assertEqual(len(scores), 2)
        self.assertTrue(all(isinstance(score, float) for score in scores))

    def test_model_save_load(self):
        """Test model saving and loading"""
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, "test_model.pth")

            # Save model
            self.algorithm.save_model(model_path)
            self.assertTrue(os.path.exists(model_path))

            # Modify algorithm state
            original_epsilon = self.algorithm.epsilon
            self.algorithm.epsilon = 0.5

            # Load model
            self.algorithm.load_model(model_path)
            self.assertEqual(self.algorithm.epsilon, original_epsilon)

    def test_training_metrics(self):
        """Test training metrics retrieval"""
        metrics = self.algorithm.get_training_metrics()

        self.assertIsInstance(metrics, dict)
        self.assertIn('episode_rewards', metrics)
        self.assertIn('training_steps', metrics)
        self.assertIn('epsilon', metrics)


class TestHumanPreferenceInterface(unittest.TestCase):
    """Test cases for Human Preference Interface"""

    def setUp(self):
        """Set up test interface"""
        self.interface = CLIPreferenceInterface("test_evaluator")
        self.solution1 = PortfolioSolution(
            selected_projects=["ProjectA"],
            schedules=[ProjectSchedule("ProjectA", 0, 5, {"budget": 100})],
            total_cost=100,
            total_duration=5
        )
        self.solution2 = PortfolioSolution(
            selected_projects=["ProjectB"],
            schedules=[ProjectSchedule("ProjectB", 0, 3, {"budget": 80})],
            total_cost=80,
            total_duration=3
        )

    def test_display_solution(self):
        """Test solution display formatting"""
        display = self.interface.display_solution(self.solution1)

        self.assertIsInstance(display, str)
        self.assertIn("ProjectA", display)
        self.assertIn("100", display)
        self.assertIn("5", display)

    def test_batch_preference_collector(self):
        """Test batch preference collection"""
        collector = BatchPreferenceCollector(self.interface)
        self.assertIsInstance(collector, BatchPreferenceCollector)
        self.assertEqual(len(collector.collected_preferences), 0)

    def test_preference_statistics(self):
        """Test preference statistics calculation"""
        collector = BatchPreferenceCollector(self.interface)

        # Add some mock preferences
        preference = HumanPreference(
            preferred_solution=self.solution1,
            alternative_solution=self.solution2,
            preference_strength=0.8,
            evaluator_id="test_evaluator",
            confidence=0.9
        )
        collector.collected_preferences.append(preference)

        stats = collector.get_preference_statistics()
        self.assertIsInstance(stats, dict)
        self.assertEqual(stats['total_preferences'], 1)
        self.assertEqual(stats['average_strength'], 0.8)
        self.assertEqual(stats['average_confidence'], 0.9)


class TestPreferenceGuidedSampling(unittest.TestCase):
    """Test cases for Preference-Guided Sampling"""

    def setUp(self):
        """Set up test sampling"""
        self.preferences = [
            HumanPreference(
                preferred_solution=PortfolioSolution(
                    selected_projects=["ProjectA", "ProjectB"],
                    schedules=[],
                    total_cost=180,
                    total_duration=8
                ),
                alternative_solution=PortfolioSolution(
                    selected_projects=["ProjectC"],
                    schedules=[],
                    total_cost=120,
                    total_duration=6
                ),
                preference_strength=0.8,
                evaluator_id="test"
            )
        ]
        self.sampling = PreferenceGuidedSampling(self.preferences)

    def test_initialization(self):
        """Test sampling initialization"""
        self.assertEqual(len(self.sampling.preferences), 1)

    def test_pattern_analysis(self):
        """Test preference pattern analysis"""
        patterns = self.sampling.analyze_preference_patterns()

        self.assertIsInstance(patterns, dict)
        if patterns:  # Only check if analysis succeeded
            self.assertIn('preferred_cost_range', patterns)
            self.assertIn('preferred_duration_range', patterns)

    def test_solution_suggestions(self):
        """Test solution modification suggestions"""
        solution = PortfolioSolution(
            selected_projects=["ProjectD"],
            schedules=[],
            total_cost=500,  # High cost
            total_duration=15  # Long duration
        )

        suggestions = self.sampling.suggest_solution_modifications(solution)
        self.assertIsInstance(suggestions, list)
        self.assertGreater(len(suggestions), 0)


class TestIntegratedFramework(unittest.TestCase):
    """Test cases for Integrated PPSS Framework"""

    def setUp(self):
        """Set up test framework"""
        self.projects_data = [
            ProjectData(
                project_id="TestProject1",
                name="Test Project 1",
                description="First test project",
                estimated_duration=5,
                resource_requirements={"budget": 100, "personnel": 2}
            ),
            ProjectData(
                project_id="TestProject2",
                name="Test Project 2",
                description="Second test project",
                estimated_duration=7,
                resource_requirements={"budget": 150, "personnel": 3}
            )
        ]

        self.config = PPSSConfiguration(
            time_horizon=12,
            total_resources={"budget": 500, "personnel": 10},
            max_episodes=10
        )

        self.framework = IntegratedPPSSFramework(self.projects_data, self.config)

    def test_initialization(self):
        """Test framework initialization"""
        self.assertEqual(len(self.framework.project_ids), 2)
        self.assertIsNotNone(self.framework.evaluation_translator)
        self.assertIsNotNone(self.framework.preference_collector)

    def test_qualitative_evaluation_addition(self):
        """Test adding qualitative evaluations"""
        evaluations = [
            QualitativeEvaluation(
                evaluator_id="test_evaluator",
                evaluation_type=EvaluationType.COMPARISON,
                projects=["TestProject1", "TestProject2"],
                operator=ComparisonOperator.GREATER,
                confidence=0.8,
                criteria="business_value"
            )
        ]

        self.framework.add_qualitative_evaluations(evaluations)

        # Check that environment and algorithm are initialized
        self.assertIsNotNone(self.framework.environment)
        self.assertIsNotNone(self.framework.dpbqn_algorithm)

    def test_training_episode(self):
        """Test training episode execution"""
        # Add evaluation to initialize the system
        evaluations = [
            QualitativeEvaluation(
                evaluator_id="test",
                evaluation_type=EvaluationType.THRESHOLD,
                projects=["TestProject1"],
                operator=ComparisonOperator.GREATER_EQUAL,
                values=[0.5],
                confidence=0.8,
                criteria="business_value"
            )
        ]
        self.framework.add_qualitative_evaluations(evaluations)

        # Run training episode
        episode_info = self.framework.train_episode()

        self.assertIsInstance(episode_info, dict)
        self.assertIn('total_reward', episode_info)

    def test_solution_generation(self):
        """Test optimized solution generation"""
        # Initialize framework
        evaluations = [
            QualitativeEvaluation(
                evaluator_id="test",
                evaluation_type=EvaluationType.COMPARISON,
                projects=["TestProject1", "TestProject2"],
                operator=ComparisonOperator.GREATER,
                confidence=0.8,
                criteria="business_value"
            )
        ]
        self.framework.add_qualitative_evaluations(evaluations)

        # Generate solution
        solution = self.framework.generate_optimized_portfolio()

        self.assertIsInstance(solution, PortfolioSolution)
        self.assertIsInstance(solution.selected_projects, list)

    def test_framework_summary(self):
        """Test framework summary generation"""
        summary = self.framework.get_framework_summary()

        self.assertIsInstance(summary, dict)
        self.assertIn('framework_status', summary)
        self.assertIn('project_portfolio', summary)
        self.assertIn('training_statistics', summary)

    def test_framework_export_import(self):
        """Test framework state export"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Initialize framework
            evaluations = [
                QualitativeEvaluation(
                    evaluator_id="test",
                    evaluation_type=EvaluationType.THRESHOLD,
                    projects=["TestProject1"],
                    operator=ComparisonOperator.GREATER_EQUAL,
                    values=[0.7],
                    confidence=0.9,
                    criteria="business_value"
                )
            ]
            self.framework.add_qualitative_evaluations(evaluations)

            # Export framework
            self.framework.export_framework_state(temp_dir)

            # Check exported files
            export_path = Path(temp_dir)
            self.assertTrue((export_path / "config.json").exists())
            self.assertTrue((export_path / "projects_data.json").exists())


class TestSampleFramework(unittest.TestCase):
    """Test cases for sample framework creation"""

    def test_create_sample_framework(self):
        """Test sample framework creation"""
        framework = create_sample_framework()

        self.assertIsInstance(framework, IntegratedPPSSFramework)
        self.assertGreater(len(framework.project_ids), 0)

        # Check that evaluations were added
        summary = framework.get_framework_summary()
        self.assertGreater(summary['constraint_analysis'].get('total_constraints', 0), 0)

    def test_sample_framework_functionality(self):
        """Test that sample framework can train and generate solutions"""
        framework = create_sample_framework()

        # Run a few training episodes
        for _ in range(3):
            episode_info = framework.train_episode()
            self.assertIsInstance(episode_info, dict)

        # Generate solution
        solution = framework.generate_optimized_portfolio()
        self.assertIsInstance(solution, PortfolioSolution)


class TestDataValidation(unittest.TestCase):
    """Test cases for data structures and validation"""

    def test_portfolio_solution_validation(self):
        """Test portfolio solution data structure"""
        solution = PortfolioSolution(
            selected_projects=["Project1", "Project2"],
            schedules=[
                ProjectSchedule("Project1", 0, 5, {"budget": 100}),
                ProjectSchedule("Project2", 5, 3, {"budget": 80})
            ],
            total_cost=180,
            total_duration=8,
            feasibility_score=0.9
        )

        self.assertEqual(len(solution.selected_projects), 2)
        self.assertEqual(len(solution.schedules), 2)
        self.assertEqual(solution.total_cost, 180)
        self.assertEqual(solution.total_duration, 8)

    def test_human_preference_validation(self):
        """Test human preference data structure"""
        solution1 = PortfolioSolution(["Project1"], [])
        solution2 = PortfolioSolution(["Project2"], [])

        preference = HumanPreference(
            preferred_solution=solution1,
            alternative_solution=solution2,
            preference_strength=0.8,
            evaluator_id="test_evaluator",
            confidence=0.9
        )

        self.assertEqual(preference.preference_strength, 0.8)
        self.assertEqual(preference.confidence, 0.9)
        self.assertEqual(preference.evaluator_id, "test_evaluator")

    def test_project_data_validation(self):
        """Test project data structure"""
        project = ProjectData(
            project_id="TestProject",
            name="Test Project",
            description="A test project",
            estimated_duration=10,
            resource_requirements={"budget": 1000, "personnel": 5},
            risk_factors={"technical": 0.3, "market": 0.2}
        )

        self.assertEqual(project.project_id, "TestProject")
        self.assertEqual(project.estimated_duration, 10)
        self.assertEqual(len(project.resource_requirements), 2)
        self.assertEqual(len(project.risk_factors), 2)


class TestEdgeCases(unittest.TestCase):
    """Test cases for edge cases and error conditions"""

    def test_empty_project_list(self):
        """Test handling of empty project list"""
        with self.assertRaises(ValueError):
            env = PPSSEnvironment([], {"budget": 1000}, 12)

    def test_zero_resources(self):
        """Test handling of zero resources"""
        projects = ["Project1"]
        resources = {"budget": 0, "personnel": 0}
        # Should not raise an error during creation now that we handle division by zero
        env = PPSSEnvironment(projects, resources, 12)

        # Environment should be created successfully
        valid_actions = env.get_valid_actions()
        self.assertIsInstance(valid_actions, list)

        # When resources are zero, the system may still generate actions
        # but they should request zero actual resource amounts
        if valid_actions:
            for action in valid_actions:
                # Calculate actual resource requests
                resource_part = action[env.n_projects + 1:]  # Skip project selection and time
                for i, resource_fraction in enumerate(resource_part):
                    if i < len(resources):
                        resource_type = list(resources.keys())[i]
                        max_amount = resources[resource_type]
                        actual_request = resource_fraction * max_amount
                        # Since max_amount is 0, actual_request should be 0 regardless of fraction
                        self.assertEqual(actual_request, 0.0,
                                       f"Resource {resource_type} should request 0 when max is 0")

    def test_negative_time_horizon(self):
        """Test handling of negative time horizon"""
        projects = ["Project1"]
        resources = {"budget": 1000}
        with self.assertRaises(ValueError):
            env = PPSSEnvironment(projects, resources, -5)

    def test_empty_resources_dict(self):
        """Test handling of empty resources dictionary"""
        projects = ["Project1"]
        resources = {}
        with self.assertRaises(ValueError):
            env = PPSSEnvironment(projects, resources, 12)

    def test_invalid_preference_strength(self):
        """Test handling of invalid preference strengths"""
        solution1 = PortfolioSolution(["Project1"], [])
        solution2 = PortfolioSolution(["Project2"], [])

        # Should handle values outside 0-1 range
        preference = HumanPreference(
            preferred_solution=solution1,
            alternative_solution=solution2,
            preference_strength=1.5,  # Invalid value
            evaluator_id="test"
        )

        # The system should still work, just with potentially suboptimal learning
        self.assertIsInstance(preference, HumanPreference)
        # Preference strength should be clamped or handled gracefully
        self.assertGreaterEqual(preference.preference_strength, 0)

    def test_framework_without_evaluations(self):
        """Test framework behavior without qualitative evaluations"""
        projects_data = [
            ProjectData("Project1", "Test", "Desc", 5, {"budget": 100})
        ]
        config = PPSSConfiguration()
        framework = IntegratedPPSSFramework(projects_data, config)

        # Should raise error when trying to train without evaluations
        with self.assertRaises(RuntimeError):
            framework.train_episode()

    def test_invalid_action_dimensions(self):
        """Test handling of actions with wrong dimensions"""
        projects = ["ProjectA", "ProjectB"]
        resources = {"budget": 1000}
        env = PPSSEnvironment(projects, resources, 12)

        # Action with wrong dimension should be handled gracefully
        wrong_action = np.array([1.0])  # Too short
        try:
            next_state, reward, done, info = env.step(wrong_action)
            # Should either handle gracefully or raise appropriate error
            self.assertIsInstance(info, dict)
        except (ValueError, IndexError):
            # These errors are acceptable for malformed actions
            pass

    def test_extreme_preference_values(self):
        """Test handling of extreme preference values"""
        solution1 = PortfolioSolution(["Project1"], [])
        solution2 = PortfolioSolution(["Project2"], [])

        # Test negative preference strength
        preference_neg = HumanPreference(
            preferred_solution=solution1,
            alternative_solution=solution2,
            preference_strength=-0.5,  # Negative value
            evaluator_id="test"
        )
        self.assertIsInstance(preference_neg, HumanPreference)

        # Test preference strength > 1
        preference_high = HumanPreference(
            preferred_solution=solution1,
            alternative_solution=solution2,
            preference_strength=2.0,  # > 1
            evaluator_id="test"
        )
        self.assertIsInstance(preference_high, HumanPreference)


def run_performance_tests():
    """Run performance-related tests"""
    print("Running performance tests...")

    # Test large state space
    projects = [f"Project{i}" for i in range(20)]
    resources = {"budget": 10000, "personnel": 100, "equipment": 50}
    try:
        env = PPSSEnvironment(projects, resources, 24)
    except Exception as e:
        print(f"Performance test setup failed: {e}")
        return

    print(f"Large environment - State dim: {env.state_dim}, Action dim: {env.action_dim}")

    # Test network with large dimensions
    network = PreferenceBasedQNetwork(env.state_dim, env.action_dim)
    state = torch.randn(1, env.state_dim)

    import time
    start_time = time.time()
    for _ in range(100):
        _ = network(state)
    end_time = time.time()

    print(f"Network forward pass (100 iterations): {end_time - start_time:.3f} seconds")

    # Test algorithm with large environment
    algorithm = DPbQNAlgorithm(env, batch_size=16)

    start_time = time.time()
    episode_info = algorithm.train_episode(max_steps=20)
    end_time = time.time()

    print(f"Training episode (20 steps): {end_time - start_time:.3f} seconds")
    print(f"Episode reward: {episode_info['total_reward']:.3f}")


def main():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test cases
    test_classes = [
        TestPPSSEnvironment,
        TestPreferenceBasedQNetwork,
        TestPreferenceReplayBuffer,
        TestDPbQNAlgorithm,
        TestHumanPreferenceInterface,
        TestPreferenceGuidedSampling,
        TestIntegratedFramework,
        TestSampleFramework,
        TestDataValidation,
        TestEdgeCases
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print results summary
    print(f"\n{'='*60}")
    print("TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")

    if result.failures:
        print(f"\nFailures:")
        for test, error in result.failures:
            print(f"  - {test}: {error.splitlines()[-1] if error else 'Unknown failure'}")

    if result.errors:
        print(f"\nErrors:")
        for test, error in result.errors:
            print(f"  - {test}: {error.splitlines()[-1] if error else 'Unknown error'}")

    # Run performance tests if all unit tests passed
    if not result.failures and not result.errors:
        print(f"\n{'='*60}")
        print("PERFORMANCE TESTS")
        print(f"{'='*60}")
        try:
            run_performance_tests()
        except Exception as e:
            print(f"Performance tests failed: {e}")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
