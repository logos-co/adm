"""
Integrated Project Portfolio Selection and Scheduling (PPSS) Framework

This module integrates the two main components of the human-machine framework:
1. Machine-Assisted Project Evaluation by Humans (qualitative evaluation translation)
2. Preference-Based Deep Reinforcement Learning for Optimization (DPbQN algorithm)

The framework provides a complete end-to-end solution for robust project portfolio
selection and scheduling with human-in-the-loop guidance.

Author: Generated for Logos/Nimbus/Status ecosystem research
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Callable, Union
from dataclasses import dataclass, field
import json
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Import from existing modules
from qualitative_evaluation_translator import (
    QualitativeEvaluationTranslator,
    QualitativeEvaluation,
    EvaluationType,
    ComparisonOperator
)
from polytope_visualizer import PolytopeVisualizer
from tradeoff_analyzer import TradeoffAnalyzer
from dpbqn_algorithm import (
    DPbQNAlgorithm,
    PPSSEnvironment,
    PortfolioSolution,
    HumanPreference,
    ProjectSchedule
)
from human_preference_interface import (
    PreferenceInterface,
    CLIPreferenceInterface,
    GUIPreferenceInterface,
    BatchPreferenceCollector,
    PreferenceGuidedSampling
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ProjectData:
    """Represents comprehensive project data"""
    project_id: str
    name: str
    description: str
    estimated_duration: int
    resource_requirements: Dict[str, float]
    dependencies: List[str] = field(default_factory=list)
    risk_factors: Dict[str, float] = field(default_factory=dict)
    strategic_alignment: float = 0.0
    technical_complexity: float = 0.0
    expected_roi: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PPSSConfiguration:
    """Configuration for the integrated PPSS framework"""
    # Environment parameters
    time_horizon: int = 24
    resource_types: List[str] = field(default_factory=lambda: ["budget", "personnel", "equipment"])
    total_resources: Dict[str, float] = field(default_factory=lambda: {"budget": 1000000, "personnel": 50, "equipment": 20})

    # DPbQN parameters
    learning_rate: float = 0.001
    discount_factor: float = 0.95
    epsilon_start: float = 1.0
    epsilon_end: float = 0.01
    epsilon_decay: float = 0.995
    batch_size: int = 32
    buffer_capacity: int = 10000
    target_update_frequency: int = 100

    # Training parameters
    max_episodes: int = 1000
    max_steps_per_episode: int = 100
    evaluation_frequency: int = 50

    # Human interaction parameters
    preference_interface: str = "CLI"  # "CLI" or "GUI"
    max_preference_comparisons: int = 20
    preference_collection_frequency: int = 10

    # Optimization parameters
    optimization_criteria: List[str] = field(default_factory=lambda: ["business_value", "technical_risk", "cost"])


class IntegratedPPSSFramework:
    """
    Main framework class integrating qualitative evaluation and DPbQN optimization
    """

    def __init__(self, projects_data: List[ProjectData], config: PPSSConfiguration):
        """
        Initialize the integrated PPSS framework

        Args:
            projects_data: List of project data
            config: Framework configuration
        """
        self.projects_data = {proj.project_id: proj for proj in projects_data}
        self.config = config
        self.project_ids = list(self.projects_data.keys())

        # Initialize qualitative evaluation components
        self.evaluation_translator = QualitativeEvaluationTranslator(
            self.project_ids,
            config.optimization_criteria
        )
        self.polytope_visualizer = None
        self.tradeoff_analyzer = None

        # Initialize DPbQN components
        self.environment = None
        self.dpbqn_algorithm = None

        # Initialize preference collection
        if config.preference_interface.upper() == "GUI":
            self.preference_interface = GUIPreferenceInterface()
        else:
            self.preference_interface = CLIPreferenceInterface()

        self.preference_collector = BatchPreferenceCollector(self.preference_interface)

        # Training and evaluation metrics
        self.training_history = {
            'episodes': [],
            'rewards': [],
            'preference_accuracies': [],
            'solution_qualities': [],
            'human_feedback_sessions': []
        }

        # Generated solutions and evaluations
        self.generated_solutions: List[PortfolioSolution] = []
        self.solution_evaluations: List[float] = []
        self.human_preferences: List[HumanPreference] = []

        logger.info("Integrated PPSS Framework initialized")

    def add_qualitative_evaluations(self, evaluations: List[QualitativeEvaluation]):
        """
        Add qualitative evaluations from human experts

        Args:
            evaluations: List of qualitative evaluations
        """
        for evaluation in evaluations:
            self.evaluation_translator.add_evaluation(evaluation)

        # Translate evaluations to constraints
        constraints = self.evaluation_translator.translate_evaluations()
        logger.info(f"Added {len(evaluations)} evaluations, generated {len(constraints)} constraints")

        # Initialize visualization components
        self.polytope_visualizer = PolytopeVisualizer(self.evaluation_translator)
        self.tradeoff_analyzer = TradeoffAnalyzer(self.polytope_visualizer)

        # Update environment with constraint data
        self._update_environment_constraints()

    def _update_environment_constraints(self):
        """Update the DPbQN environment with constraint data from qualitative evaluations"""
        if self.evaluation_translator:
            A_ineq, b_ineq, A_eq, b_eq = self.evaluation_translator.get_constraint_matrices()
            constraints_data = {
                'A_ineq': A_ineq,
                'b_ineq': b_ineq,
                'A_eq': A_eq,
                'b_eq': b_eq,
                'validation': self.evaluation_translator.validate_constraints()
            }
        else:
            constraints_data = {}

        # Initialize or update environment
        self.environment = PPSSEnvironment(
            projects=self.project_ids,
            resources=self.config.total_resources,
            time_horizon=self.config.time_horizon,
            constraints_data=constraints_data
        )

        # Initialize DPbQN algorithm
        self.dpbqn_algorithm = DPbQNAlgorithm(
            environment=self.environment,
            learning_rate=self.config.learning_rate,
            discount_factor=self.config.discount_factor,
            epsilon_start=self.config.epsilon_start,
            epsilon_end=self.config.epsilon_end,
            epsilon_decay=self.config.epsilon_decay,
            batch_size=self.config.batch_size,
            buffer_capacity=self.config.buffer_capacity,
            target_update_frequency=self.config.target_update_frequency
        )

        logger.info("Environment and DPbQN algorithm updated with constraint data")

    def collect_human_preferences(self, solutions: List[PortfolioSolution] = None,
                                 max_comparisons: Optional[int] = None) -> List[HumanPreference]:
        """
        Collect human preferences for portfolio solutions

        Args:
            solutions: List of solutions to compare (if None, uses generated solutions)
            max_comparisons: Maximum number of pairwise comparisons

        Returns:
            List of collected preferences
        """
        if solutions is None:
            if not self.generated_solutions:
                logger.warning("No solutions available for preference collection")
                return []
            solutions = self.generated_solutions[-10:]  # Use latest 10 solutions

        if max_comparisons is None:
            max_comparisons = self.config.max_preference_comparisons

        logger.info(f"Collecting preferences for {len(solutions)} solutions")
        preferences = self.preference_collector.collect_pairwise_preferences(
            solutions, max_comparisons
        )

        # Add preferences to DPbQN algorithm
        for preference in preferences:
            self.dpbqn_algorithm.add_human_preference(preference)
            self.human_preferences.append(preference)

        # Record feedback session
        self.training_history['human_feedback_sessions'].append({
            'episode': len(self.training_history['episodes']),
            'preferences_collected': len(preferences),
            'solutions_compared': len(solutions)
        })

        logger.info(f"Collected {len(preferences)} preferences")
        return preferences

    def train_episode(self) -> Dict[str, Any]:
        """
        Train one episode with the DPbQN algorithm

        Returns:
            Episode training results
        """
        if not self.dpbqn_algorithm:
            raise RuntimeError("Framework not initialized. Call add_qualitative_evaluations() first.")

        episode_info = self.dpbqn_algorithm.train_episode(self.config.max_steps_per_episode)

        # Store generated solution
        if 'final_solution' in episode_info:
            solution = episode_info['final_solution']
            self.generated_solutions.append(solution)

            # Evaluate solution quality using constraint feasibility
            quality_score = self._evaluate_solution_quality(solution)
            self.solution_evaluations.append(quality_score)
            episode_info['solution_quality'] = quality_score

        # Update training history
        self.training_history['episodes'].append(len(self.training_history['episodes']) + 1)
        self.training_history['rewards'].append(episode_info['total_reward'])

        metrics = self.dpbqn_algorithm.get_training_metrics()
        if metrics['preference_accuracies']:
            self.training_history['preference_accuracies'].append(metrics['preference_accuracies'][-1])

        if 'solution_quality' in episode_info:
            self.training_history['solution_qualities'].append(episode_info['solution_quality'])

        return episode_info

    def train(self, episodes: Optional[int] = None) -> Dict[str, Any]:
        """
        Train the framework for multiple episodes with periodic human feedback

        Args:
            episodes: Number of episodes to train (if None, uses config)

        Returns:
            Training results summary
        """
        if episodes is None:
            episodes = self.config.max_episodes

        logger.info(f"Starting training for {episodes} episodes")

        for episode in range(episodes):
            # Train episode
            episode_info = self.train_episode()

            # Periodic human feedback collection
            if (episode + 1) % self.config.preference_collection_frequency == 0:
                if len(self.generated_solutions) >= 2:
                    logger.info(f"Collecting human feedback at episode {episode + 1}")
                    try:
                        self.collect_human_preferences()
                    except KeyboardInterrupt:
                        logger.info("Human feedback collection interrupted")
                    except Exception as e:
                        logger.warning(f"Error during preference collection: {e}")

            # Periodic evaluation and logging
            if (episode + 1) % self.config.evaluation_frequency == 0:
                self._log_training_progress(episode + 1, episodes)

        # Final training summary
        training_summary = {
            'total_episodes': episodes,
            'final_epsilon': self.dpbqn_algorithm.epsilon,
            'total_preferences_collected': len(self.human_preferences),
            'total_solutions_generated': len(self.generated_solutions),
            'average_solution_quality': np.mean(self.solution_evaluations) if self.solution_evaluations else 0,
            'training_metrics': self.dpbqn_algorithm.get_training_metrics()
        }

        logger.info("Training completed")
        return training_summary

    def _evaluate_solution_quality(self, solution: PortfolioSolution) -> float:
        """
        Evaluate the quality of a portfolio solution

        Args:
            solution: Portfolio solution to evaluate

        Returns:
            Quality score (0-1)
        """
        if not self.evaluation_translator:
            return solution.feasibility_score

        # Use constraint satisfaction as a quality measure
        state = self.environment._encode_state(solution)

        # Check constraint satisfaction
        A_ineq, b_ineq, A_eq, b_eq = self.evaluation_translator.get_constraint_matrices()

        if A_ineq.size > 0:
            # Map state to value matrix format expected by constraints
            n_projects = len(self.project_ids)
            n_criteria = len(self.config.optimization_criteria)

            if len(state) >= n_projects * n_criteria:
                # Extract value matrix from state
                value_vector = state[:n_projects * n_criteria]

                # Check inequality constraints
                constraint_violations = np.maximum(0, A_ineq.dot(value_vector) - b_ineq)
                feasibility_score = 1.0 - np.mean(constraint_violations)
            else:
                feasibility_score = solution.feasibility_score
        else:
            feasibility_score = solution.feasibility_score

        # Combine with other quality measures
        quality_score = 0.6 * feasibility_score + 0.4 * (1.0 - solution.risk_score)
        return max(0.0, min(1.0, quality_score))

    def _log_training_progress(self, episode: int, total_episodes: int):
        """Log training progress"""
        if not self.training_history['rewards']:
            return

        recent_rewards = self.training_history['rewards'][-10:]
        recent_qualities = self.training_history['solution_qualities'][-10:] if self.training_history['solution_qualities'] else []

        logger.info(f"Episode {episode}/{total_episodes}")
        logger.info(f"  Average reward (last 10): {np.mean(recent_rewards):.3f}")
        if recent_qualities:
            logger.info(f"  Average quality (last 10): {np.mean(recent_qualities):.3f}")
        logger.info(f"  Epsilon: {self.dpbqn_algorithm.epsilon:.3f}")
        logger.info(f"  Preferences collected: {len(self.human_preferences)}")
        logger.info(f"  Solutions generated: {len(self.generated_solutions)}")

    def generate_optimized_portfolio(self, evaluation_mode: bool = True) -> PortfolioSolution:
        """
        Generate an optimized portfolio solution using the trained model

        Args:
            evaluation_mode: Whether to use evaluation mode (no exploration)

        Returns:
            Optimized portfolio solution
        """
        if not self.dpbqn_algorithm:
            raise RuntimeError("Framework not initialized. Call add_qualitative_evaluations() first.")

        # Save current epsilon for restoration
        original_epsilon = self.dpbqn_algorithm.epsilon

        if evaluation_mode:
            # Set epsilon to 0 for pure exploitation
            self.dpbqn_algorithm.epsilon = 0.0

        try:
            # Generate solution
            state = self.environment.reset()
            steps = 0

            while steps < self.config.max_steps_per_episode:
                valid_actions = self.environment.get_valid_actions()
                if not valid_actions:
                    break

                action = self.dpbqn_algorithm.select_action(state, valid_actions)
                next_state, reward, done, info = self.environment.step(action)

                state = next_state
                steps += 1

                if done:
                    break

            optimized_solution = self.environment.current_solution

            # Enhance solution with project data
            self._enhance_solution_with_project_data(optimized_solution)

            return optimized_solution

        finally:
            # Restore original epsilon
            self.dpbqn_algorithm.epsilon = original_epsilon

    def _enhance_solution_with_project_data(self, solution: PortfolioSolution):
        """Enhance solution with additional project data"""
        # Calculate risk score based on project risk factors
        total_risk = 0.0
        for schedule in solution.schedules:
            project_data = self.projects_data.get(schedule.project_id)
            if project_data and project_data.risk_factors:
                project_risk = sum(project_data.risk_factors.values()) / len(project_data.risk_factors)
                total_risk += project_risk

        if solution.schedules:
            solution.risk_score = total_risk / len(solution.schedules)

        # Add metadata
        solution.metadata.update({
            'generation_method': 'DPbQN',
            'constraints_satisfied': solution.feasibility_score > 0.8,
            'preference_guided': len(self.human_preferences) > 0
        })

    def analyze_solution_tradeoffs(self, solution: PortfolioSolution) -> Dict[str, Any]:
        """
        Analyze trade-offs in a portfolio solution

        Args:
            solution: Portfolio solution to analyze

        Returns:
            Trade-off analysis results
        """
        if not self.tradeoff_analyzer:
            logger.warning("Trade-off analyzer not available. Add qualitative evaluations first.")
            return {}

        # Use the trade-off analyzer from the qualitative evaluation module
        try:
            analysis_results = self.tradeoff_analyzer.analyze_objective_tradeoffs(
                n_samples=100,
                sampling_method='uniform'
            )
            return analysis_results
        except Exception as e:
            logger.error(f"Error in trade-off analysis: {e}")
            return {}

    def visualize_training_progress(self, save_path: Optional[str] = None) -> go.Figure:
        """
        Create interactive visualization of training progress

        Args:
            save_path: Optional path to save the visualization

        Returns:
            Plotly figure
        """
        if not self.training_history['episodes']:
            logger.warning("No training history available")
            return go.Figure()

        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Training Rewards', 'Solution Quality', 'Preference Accuracy', 'Human Feedback'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )

        episodes = self.training_history['episodes']

        # Training rewards
        fig.add_trace(
            go.Scatter(x=episodes, y=self.training_history['rewards'],
                      mode='lines', name='Rewards', line=dict(color='blue')),
            row=1, col=1
        )

        # Solution quality
        if self.training_history['solution_qualities']:
            fig.add_trace(
                go.Scatter(x=episodes[:len(self.training_history['solution_qualities'])],
                          y=self.training_history['solution_qualities'],
                          mode='lines', name='Quality', line=dict(color='green')),
                row=1, col=2
            )

        # Preference accuracy
        if self.training_history['preference_accuracies']:
            pref_episodes = episodes[:len(self.training_history['preference_accuracies'])]
            fig.add_trace(
                go.Scatter(x=pref_episodes, y=self.training_history['preference_accuracies'],
                          mode='lines', name='Accuracy', line=dict(color='red')),
                row=2, col=1
            )

        # Human feedback sessions
        feedback_episodes = [session['episode'] for session in self.training_history['human_feedback_sessions']]
        feedback_counts = [session['preferences_collected'] for session in self.training_history['human_feedback_sessions']]

        if feedback_episodes:
            fig.add_trace(
                go.Bar(x=feedback_episodes, y=feedback_counts,
                       name='Preferences', marker_color='orange'),
                row=2, col=2
            )

        fig.update_layout(
            title='DPbQN Training Progress',
            showlegend=True,
            height=600
        )

        if save_path:
            fig.write_html(save_path)
            logger.info(f"Training visualization saved to {save_path}")

        return fig

    def export_framework_state(self, directory: str):
        """
        Export the complete framework state for later use

        Args:
            directory: Directory to save framework state
        """
        try:
            export_dir = Path(directory)
            export_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Exporting framework state to {directory}")

            # Save DPbQN model
            try:
                if self.dpbqn_algorithm:
                    model_path = str(export_dir / "dpbqn_model.pth")
                    self.dpbqn_algorithm.save_model(model_path)
                    logger.info("DPbQN model saved successfully")
                else:
                    logger.warning("No DPbQN algorithm to save")
            except Exception as e:
                logger.error(f"Failed to save DPbQN model: {e}")

            # Save qualitative evaluations and constraints
            try:
                if self.evaluation_translator:
                    constraints_data = self.evaluation_translator.export_constraints('dict')
                    with open(export_dir / "constraints.json", 'w') as f:
                        json.dump(constraints_data, f, indent=2)
                    logger.info("Constraints data saved successfully")
                else:
                    logger.warning("No evaluation translator to save")
            except Exception as e:
                logger.error(f"Failed to save constraints: {e}")

            # Save preferences
            try:
                self.preference_collector.export_preferences(str(export_dir / "preferences.json"))
                logger.info("Preferences saved successfully")
            except Exception as e:
                logger.error(f"Failed to save preferences: {e}")

            # Save training history
            try:
                with open(export_dir / "training_history.json", 'w') as f:
                    # Convert numpy arrays and other non-serializable types to lists for JSON serialization
                    history_serializable = {}
                    for key, value in self.training_history.items():
                        try:
                            if isinstance(value, list):
                                # Handle list items that might be numpy arrays or other non-serializable types
                                serializable_list = []
                                for item in value:
                                    if hasattr(item, 'tolist'):  # NumPy array
                                        serializable_list.append(item.tolist())
                                    elif hasattr(item, '__dict__'):  # Complex object
                                        # Convert objects to dict representation
                                        try:
                                            serializable_list.append(item.__dict__)
                                        except:
                                            serializable_list.append(str(item))
                                    else:
                                        serializable_list.append(item)
                                history_serializable[key] = serializable_list
                            elif hasattr(value, 'tolist'):  # NumPy array
                                history_serializable[key] = value.tolist()
                            else:
                                history_serializable[key] = str(value)
                        except Exception as e:
                            logger.warning(f"Failed to serialize training history key '{key}': {e}")
                            history_serializable[key] = f"<serialization_error: {str(e)}>"

                    json.dump(history_serializable, f, indent=2)
                logger.info("Training history saved successfully")
            except Exception as e:
                logger.error(f"Failed to save training history: {e}")

            # Save configuration
            try:
                config_dict = {
                    'time_horizon': self.config.time_horizon,
                    'resource_types': self.config.resource_types,
                    'total_resources': self.config.total_resources,
                    'optimization_criteria': self.config.optimization_criteria,
                    'max_episodes': self.config.max_episodes,
                    'preference_interface': self.config.preference_interface
                }
                with open(export_dir / "config.json", 'w') as f:
                    json.dump(config_dict, f, indent=2)
                logger.info("Configuration saved successfully")
            except Exception as e:
                logger.error(f"Failed to save configuration: {e}")

            # Save project data
            try:
                projects_data = []
                for project_id, project in self.projects_data.items():
                    project_dict = {
                        'project_id': project.project_id,
                        'name': project.name,
                        'description': project.description,
                        'estimated_duration': project.estimated_duration,
                        'resource_requirements': project.resource_requirements,
                        'dependencies': project.dependencies,
                        'risk_factors': project.risk_factors,
                        'strategic_alignment': project.strategic_alignment,
                        'technical_complexity': project.technical_complexity,
                        'expected_roi': project.expected_roi,
                        'metadata': project.metadata
                    }
                    projects_data.append(project_dict)

                with open(export_dir / "projects_data.json", 'w') as f:
                    json.dump(projects_data, f, indent=2)
                logger.info("Project data saved successfully")
            except Exception as e:
                logger.error(f"Failed to save project data: {e}")

            logger.info(f"Framework state export completed to {directory}")

        except Exception as e:
            logger.error(f"Framework state export failed: {e}")
            raise

    def get_framework_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive summary of the framework state

        Returns:
            Framework summary dictionary
        """
        summary = {
            'framework_status': {
                'initialized': self.dpbqn_algorithm is not None,
                'qualitative_evaluations_added': self.evaluation_translator is not None,
                'constraints_available': bool(self.evaluation_translator and
                                             len(self.evaluation_translator.constraints) > 0),
                'trained': len(self.training_history['episodes']) > 0
            },
            'project_portfolio': {
                'total_projects': len(self.project_ids),
                'project_ids': self.project_ids,
                'resource_types': self.config.resource_types,
                'total_resources': self.config.total_resources,
                'optimization_criteria': self.config.optimization_criteria
            },
            'training_statistics': {
                'episodes_completed': len(self.training_history['episodes']),
                'solutions_generated': len(self.generated_solutions),
                'human_preferences_collected': len(self.human_preferences),
                'feedback_sessions': len(self.training_history['human_feedback_sessions']),
                'average_reward': np.mean(self.training_history['rewards']) if self.training_history['rewards'] else 0,
                'average_solution_quality': np.mean(self.solution_evaluations) if self.solution_evaluations else 0
            },
            'constraint_analysis': {},
            'preference_analysis': {}
        }

        # Add constraint analysis
        if self.evaluation_translator:
            validation = self.evaluation_translator.validate_constraints()
            summary['constraint_analysis'] = {
                'total_constraints': len(self.evaluation_translator.constraints),
                'is_feasible': not validation.get('is_overconstrained', True),
                'warnings': validation.get('warnings', []),
                'constraint_types': list(set(c.source_evaluation.evaluation_type.value
                                           for c in self.evaluation_translator.constraints
                                           if c.source_evaluation))
            }

        # Add preference analysis
        if self.human_preferences:
            strengths = [p.preference_strength for p in self.human_preferences]
            confidences = [p.confidence for p in self.human_preferences]
            evaluators = list(set(p.evaluator_id for p in self.human_preferences))

            summary['preference_analysis'] = {
                'average_strength': np.mean(strengths),
                'average_confidence': np.mean(confidences),
                'unique_evaluators': len(evaluators),
                'evaluator_ids': evaluators,
                'preferences_with_reasoning': sum(1 for p in self.human_preferences if p.reasoning)
            }

        return summary


def create_sample_framework() -> IntegratedPPSSFramework:
    """
    Create a sample framework instance for demonstration purposes

    Returns:
        Initialized framework with sample data
    """
    # Sample project data
    projects = [
        ProjectData(
            project_id="WebApp",
            name="Web Application Development",
            description="Develop a modern web application for customer engagement",
            estimated_duration=8,
            resource_requirements={"budget": 150000, "personnel": 5, "equipment": 2},
            risk_factors={"technical": 0.3, "market": 0.2, "resource": 0.1},
            strategic_alignment=0.8,
            technical_complexity=0.6,
            expected_roi=1.5
        ),
        ProjectData(
            project_id="MobileApp",
            name="Mobile Application",
            description="Cross-platform mobile app for iOS and Android",
            estimated_duration=10,
            resource_requirements={"budget": 200000, "personnel": 6, "equipment": 3},
            risk_factors={"technical": 0.4, "market": 0.3, "resource": 0.2},
            strategic_alignment=0.9,
            technical_complexity=0.7,
            expected_roi=2.0
        ),
        ProjectData(
            project_id="DataPlatform",
            name="Data Analytics Platform",
            description="Big data platform for business intelligence",
            estimated_duration=12,
            resource_requirements={"budget": 300000, "personnel": 8, "equipment": 5},
            risk_factors={"technical": 0.5, "market": 0.1, "resource": 0.3},
            strategic_alignment=0.7,
            technical_complexity=0.8,
            expected_roi=2.5
        ),
        ProjectData(
            project_id="AISystem",
            name="AI/ML System",
            description="Machine learning system for predictive analytics",
            estimated_duration=15,
            resource_requirements={"budget": 400000, "personnel": 10, "equipment": 7},
            risk_factors={"technical": 0.7, "market": 0.2, "resource": 0.4},
            strategic_alignment=0.95,
            technical_complexity=0.9,
            expected_roi=3.0
        )
    ]

    # Configuration
    config = PPSSConfiguration(
        time_horizon=24,
        total_resources={"budget": 800000, "personnel": 20, "equipment": 15},
        max_episodes=100,
        max_preference_comparisons=10,
        preference_collection_frequency=20
    )

    # Create framework
    framework = IntegratedPPSSFramework(projects, config)

    # Add sample qualitative evaluations
    sample_evaluations = [
        QualitativeEvaluation(
            evaluator_id="CEO",
            evaluation_type=EvaluationType.RANKING,
            projects=["AISystem", "DataPlatform", "MobileApp", "WebApp"],
            confidence=0.9,
            criteria="business_value"
        ),
        QualitativeEvaluation(
            evaluator_id="CTO",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["AISystem", "WebApp"],
            operator=ComparisonOperator.GREATER,
            confidence=0.8,
            criteria="technical_risk"
        ),
        QualitativeEvaluation(
            evaluator_id="CFO",
            evaluation_type=EvaluationType.THRESHOLD,
            projects=["DataPlatform"],
            operator=ComparisonOperator.GREATER_EQUAL,
            values=[0.7],
            confidence=0.95,
            criteria="cost"
        )
    ]

    framework.add_qualitative_evaluations(sample_evaluations)

    return framework
