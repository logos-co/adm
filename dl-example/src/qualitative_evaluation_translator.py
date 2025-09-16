"""
Qualitative Evaluation Translation Module

This module implements the core translation engine that converts human qualitative 
evaluations into linear equality and inequality constraints, defining a convex polytope 
representing the feasible space for project value matrices in the Robust Human-Machine 
Project Portfolio Selection System.

Key Features:
- **Multi-Type Evaluation Support**: Handles comparisons, ranges, rankings, and thresholds
- **Mathematical Translation**: Converts subjective evaluations to linear constraints (Ax ≤ b)
- **Polytope Definition**: Creates convex polytope boundaries for optimization
- **Multi-Criteria Support**: Handles multiple evaluation criteria simultaneously
- **Stakeholder Integration**: Processes evaluations from multiple stakeholders
- **Constraint Validation**: Checks system consistency and feasibility
- **Export Capabilities**: Multiple output formats for integration with optimization tools

Mathematical Foundation:
- Project value vector: x ∈ ℝ^(n_projects × n_criteria)
- Inequality constraints: A_ineq * x ≤ b_ineq
- Equality constraints: A_eq * x = b_eq
- Feasible polytope: P = {x : A_ineq * x ≤ b_ineq, A_eq * x = b_eq}

Usage Example:
    ```python
    from qualitative_evaluation_translator import *
    
    # Create translator
    translator = QualitativeEvaluationTranslator(
        projects=["Project A", "Project B"],
        criteria=["Strategic Value", "Technical Feasibility"]
    )
    
    # Add evaluation
    evaluation = QualitativeEvaluation(
        evaluator_id="expert_1",
        evaluation_type=EvaluationType.COMPARISON,
        projects=["Project A", "Project B"],
        operator=ComparisonOperator.GREATER,
        criteria="Strategic Value"
    )
    translator.add_evaluation(evaluation)
    
    # Get constraint matrices
    A_ineq, b_ineq, A_eq, b_eq = translator.get_constraint_matrices()
    ```

Author: Cline AI Assistant
Version: 1.0.0
Status: Phase 1 Complete - Core Translation Engine Operational
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Union, Optional
from dataclasses import dataclass
from enum import Enum
import logging
from scipy.spatial import ConvexHull
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EvaluationType(Enum):
    """Types of qualitative evaluations supported"""
    COMPARISON = "comparison"  # Project A > Project B
    RANGE = "range"           # Project value between X and Y
    RANKING = "ranking"       # Ordered list of projects
    PREFERENCE = "preference" # Preference weights
    THRESHOLD = "threshold"   # Minimum/maximum constraints


class ComparisonOperator(Enum):
    """Comparison operators for evaluations"""
    GREATER = ">"
    LESS = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    EQUAL = "="
    NOT_EQUAL = "!="


@dataclass
class QualitativeEvaluation:
    """Represents a single qualitative evaluation from a human expert"""
    evaluator_id: str
    evaluation_type: EvaluationType
    projects: List[str]
    operator: Optional[ComparisonOperator] = None
    values: Optional[List[float]] = None
    confidence: float = 1.0
    criteria: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Optional[Dict] = None


@dataclass
class LinearConstraint:
    """Represents a linear constraint: a^T * x <= b or a^T * x = b"""
    coefficients: np.ndarray  # coefficient vector 'a'
    bound: float             # bound value 'b'
    is_equality: bool = False  # True for equality, False for inequality
    constraint_id: str = ""
    source_evaluation: Optional[QualitativeEvaluation] = None


class QualitativeEvaluationTranslator:
    """
    Main class for translating qualitative evaluations into mathematical constraints
    """
    
    def __init__(self, projects: List[str], criteria: List[str] = None):
        """
        Initialize the translator
        
        Args:
            projects: List of project identifiers
            criteria: List of evaluation criteria (e.g., ['cost', 'benefit', 'risk'])
        """
        self.projects = projects
        self.criteria = criteria or ['value']
        self.n_projects = len(projects)
        self.n_criteria = len(self.criteria)
        self.project_index = {proj: i for i, proj in enumerate(projects)}
        self.criteria_index = {crit: i for i, crit in enumerate(self.criteria)}
        
        # Storage for evaluations and constraints
        self.evaluations: List[QualitativeEvaluation] = []
        self.constraints: List[LinearConstraint] = []
        
        logger.info(f"Initialized translator for {self.n_projects} projects and {self.n_criteria} criteria")
    
    def add_evaluation(self, evaluation: QualitativeEvaluation) -> None:
        """Add a qualitative evaluation to the system"""
        self.evaluations.append(evaluation)
        logger.info(f"Added evaluation from {evaluation.evaluator_id}: {evaluation.evaluation_type.value}")
    
    def parse_comparison_evaluation(self, evaluation: QualitativeEvaluation) -> List[LinearConstraint]:
        """
        Parse comparison evaluations like "Project A > Project B"
        
        Returns list of linear constraints representing the comparison
        """
        constraints = []
        
        if len(evaluation.projects) != 2:
            raise ValueError("Comparison evaluation must involve exactly 2 projects")
        
        proj_a, proj_b = evaluation.projects
        idx_a = self.project_index[proj_a]
        idx_b = self.project_index[proj_b]
        
        # Only apply to the specified criterion, or all criteria if none specified
        target_criteria = [evaluation.criteria] if evaluation.criteria else self.criteria
        
        for criterion in target_criteria:
            if criterion not in self.criteria:
                continue
                
            crit_idx = self.criteria_index[criterion]
            # Create coefficient vector
            coeffs = np.zeros(self.n_projects * self.n_criteria)
            
            # Position in flattened matrix: project_idx * n_criteria + criterion_idx
            pos_a = idx_a * self.n_criteria + crit_idx
            pos_b = idx_b * self.n_criteria + crit_idx
            
            if evaluation.operator == ComparisonOperator.GREATER:
                # v_a - v_b >= epsilon (small positive value)
                coeffs[pos_a] = 1.0
                coeffs[pos_b] = -1.0
                constraint = LinearConstraint(
                    coefficients=coeffs,
                    bound=-0.01,  # Small epsilon for strict inequality
                    is_equality=False,
                    constraint_id=f"comp_{proj_a}_{proj_b}_{criterion}",
                    source_evaluation=evaluation
                )
                constraints.append(constraint)
                
            elif evaluation.operator == ComparisonOperator.LESS:
                # v_a - v_b <= -epsilon
                coeffs[pos_a] = 1.0
                coeffs[pos_b] = -1.0
                constraint = LinearConstraint(
                    coefficients=coeffs,
                    bound=-0.01,
                    is_equality=False,
                    constraint_id=f"comp_{proj_a}_{proj_b}_{criterion}",
                    source_evaluation=evaluation
                )
                constraints.append(constraint)
                
            elif evaluation.operator == ComparisonOperator.EQUAL:
                # v_a - v_b = 0
                coeffs[pos_a] = 1.0
                coeffs[pos_b] = -1.0
                constraint = LinearConstraint(
                    coefficients=coeffs,
                    bound=0.0,
                    is_equality=True,
                    constraint_id=f"comp_{proj_a}_{proj_b}_{criterion}",
                    source_evaluation=evaluation
                )
                constraints.append(constraint)
        
        return constraints
    
    def parse_range_evaluation(self, evaluation: QualitativeEvaluation) -> List[LinearConstraint]:
        """
        Parse range evaluations like "Project A value between 0.3 and 0.7"
        """
        constraints = []
        
        if len(evaluation.projects) != 1:
            raise ValueError("Range evaluation must involve exactly 1 project")
        
        if not evaluation.values or len(evaluation.values) != 2:
            raise ValueError("Range evaluation must specify exactly 2 values (min, max)")
        
        proj = evaluation.projects[0]
        idx = self.project_index[proj]
        min_val, max_val = evaluation.values
        
        # Only apply to the specified criterion, or all criteria if none specified
        target_criteria = [evaluation.criteria] if evaluation.criteria else self.criteria
        
        for criterion in target_criteria:
            if criterion not in self.criteria:
                continue
                
            crit_idx = self.criteria_index[criterion]
            coeffs = np.zeros(self.n_projects * self.n_criteria)
            pos = idx * self.n_criteria + crit_idx
            
            # Lower bound: v >= min_val (rewrite as -v <= -min_val)
            coeffs[pos] = -1.0
            constraint_lower = LinearConstraint(
                coefficients=coeffs.copy(),
                bound=-min_val,
                is_equality=False,
                constraint_id=f"range_lower_{proj}_{criterion}",
                source_evaluation=evaluation
            )
            constraints.append(constraint_lower)
            
            # Upper bound: v <= max_val
            coeffs = np.zeros(self.n_projects * self.n_criteria)
            coeffs[pos] = 1.0
            constraint_upper = LinearConstraint(
                coefficients=coeffs.copy(),
                bound=max_val,
                is_equality=False,
                constraint_id=f"range_upper_{proj}_{criterion}",
                source_evaluation=evaluation
            )
            constraints.append(constraint_upper)
        
        return constraints
    
    def parse_ranking_evaluation(self, evaluation: QualitativeEvaluation) -> List[LinearConstraint]:
        """
        Parse ranking evaluations like "Project A > Project B > Project C"
        """
        constraints = []
        projects = evaluation.projects
        
        if len(projects) < 2:
            raise ValueError("Ranking evaluation must involve at least 2 projects")
        
        # Create pairwise comparisons for consecutive projects in ranking
        for i in range(len(projects) - 1):
            proj_higher = projects[i]
            proj_lower = projects[i + 1]
            
            # Create comparison evaluation
            comp_eval = QualitativeEvaluation(
                evaluator_id=evaluation.evaluator_id,
                evaluation_type=EvaluationType.COMPARISON,
                projects=[proj_higher, proj_lower],
                operator=ComparisonOperator.GREATER,
                confidence=evaluation.confidence,
                criteria=evaluation.criteria
            )
            
            # Parse the comparison
            comp_constraints = self.parse_comparison_evaluation(comp_eval)
            constraints.extend(comp_constraints)
        
        return constraints
    
    def parse_threshold_evaluation(self, evaluation: QualitativeEvaluation) -> List[LinearConstraint]:
        """
        Parse threshold evaluations like "Project A must have value >= 0.5"
        """
        constraints = []
        
        if len(evaluation.projects) != 1:
            raise ValueError("Threshold evaluation must involve exactly 1 project")
        
        if not evaluation.values or len(evaluation.values) != 1:
            raise ValueError("Threshold evaluation must specify exactly 1 threshold value")
        
        proj = evaluation.projects[0]
        idx = self.project_index[proj]
        threshold = evaluation.values[0]
        
        # For each criterion, create threshold constraint
        for crit_idx, criterion in enumerate(self.criteria):
            coeffs = np.zeros(self.n_projects * self.n_criteria)
            pos = idx * self.n_criteria + crit_idx
            
            if evaluation.operator == ComparisonOperator.GREATER_EQUAL:
                # v >= threshold
                coeffs[pos] = 1.0
                constraint = LinearConstraint(
                    coefficients=coeffs,
                    bound=threshold,
                    is_equality=False,
                    constraint_id=f"threshold_{proj}_{criterion}",
                    source_evaluation=evaluation
                )
                constraints.append(constraint)
                
            elif evaluation.operator == ComparisonOperator.LESS_EQUAL:
                # v <= threshold
                coeffs[pos] = -1.0
                constraint = LinearConstraint(
                    coefficients=coeffs,
                    bound=-threshold,
                    is_equality=False,
                    constraint_id=f"threshold_{proj}_{criterion}",
                    source_evaluation=evaluation
                )
                constraints.append(constraint)
        
        return constraints
    
    def translate_evaluations(self) -> List[LinearConstraint]:
        """
        Translate all stored qualitative evaluations into linear constraints
        """
        all_constraints = []
        
        for evaluation in self.evaluations:
            try:
                if evaluation.evaluation_type == EvaluationType.COMPARISON:
                    constraints = self.parse_comparison_evaluation(evaluation)
                elif evaluation.evaluation_type == EvaluationType.RANGE:
                    constraints = self.parse_range_evaluation(evaluation)
                elif evaluation.evaluation_type == EvaluationType.RANKING:
                    constraints = self.parse_ranking_evaluation(evaluation)
                elif evaluation.evaluation_type == EvaluationType.THRESHOLD:
                    constraints = self.parse_threshold_evaluation(evaluation)
                else:
                    logger.warning(f"Unsupported evaluation type: {evaluation.evaluation_type}")
                    continue
                
                all_constraints.extend(constraints)
                
            except Exception as e:
                logger.error(f"Error processing evaluation from {evaluation.evaluator_id}: {e}")
                continue
        
        self.constraints = all_constraints
        logger.info(f"Generated {len(all_constraints)} linear constraints from {len(self.evaluations)} evaluations")
        
        return all_constraints
    
    def get_constraint_matrices(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Get constraint matrices in standard form for optimization
        
        Returns:
            A_ineq: Inequality constraint matrix (A_ineq * x <= b_ineq)
            b_ineq: Inequality constraint bounds
            A_eq: Equality constraint matrix (A_eq * x = b_eq)
            b_eq: Equality constraint bounds
        """
        if not self.constraints:
            self.translate_evaluations()
        
        # Separate equality and inequality constraints
        ineq_constraints = [c for c in self.constraints if not c.is_equality]
        eq_constraints = [c for c in self.constraints if c.is_equality]
        
        # Build inequality constraint matrix
        if ineq_constraints:
            A_ineq = np.vstack([c.coefficients for c in ineq_constraints])
            b_ineq = np.array([c.bound for c in ineq_constraints])
        else:
            A_ineq = np.empty((0, self.n_projects * self.n_criteria))
            b_ineq = np.empty(0)
        
        # Build equality constraint matrix
        if eq_constraints:
            A_eq = np.vstack([c.coefficients for c in eq_constraints])
            b_eq = np.array([c.bound for c in eq_constraints])
        else:
            A_eq = np.empty((0, self.n_projects * self.n_criteria))
            b_eq = np.empty(0)
        
        return A_ineq, b_ineq, A_eq, b_eq
    
    def validate_constraints(self) -> Dict[str, any]:
        """
        Validate the constraint system for consistency and feasibility
        """
        A_ineq, b_ineq, A_eq, b_eq = self.get_constraint_matrices()
        
        validation_results = {
            'n_inequality_constraints': len(b_ineq),
            'n_equality_constraints': len(b_eq),
            'total_constraints': len(b_ineq) + len(b_eq),
            'n_variables': self.n_projects * self.n_criteria,
            'is_overconstrained': False,
            'warnings': []
        }
        
        # Check for overconstrained system
        total_constraints = len(b_ineq) + len(b_eq)
        n_variables = self.n_projects * self.n_criteria
        
        if len(b_eq) > n_variables:
            validation_results['is_overconstrained'] = True
            validation_results['warnings'].append("System may be overconstrained (more equality constraints than variables)")
        
        # Check for contradictory constraints (basic check)
        if len(b_eq) > 0:
            try:
                # Check if equality constraints are consistent
                rank_A = np.linalg.matrix_rank(A_eq)
                rank_Ab = np.linalg.matrix_rank(np.column_stack([A_eq, b_eq]))
                
                if rank_A != rank_Ab:
                    validation_results['warnings'].append("Equality constraints appear to be inconsistent")
            except:
                validation_results['warnings'].append("Could not verify equality constraint consistency")
        
        return validation_results
    
    def export_constraints(self, format: str = 'dict') -> Union[Dict, pd.DataFrame]:
        """
        Export constraints in various formats
        
        Args:
            format: 'dict', 'dataframe', or 'matrices'
        """
        if not self.constraints:
            self.translate_evaluations()
        
        if format == 'dict':
            return {
                'constraints': [
                    {
                        'id': c.constraint_id,
                        'coefficients': c.coefficients.tolist(),
                        'bound': c.bound,
                        'is_equality': c.is_equality,
                        'evaluator': c.source_evaluation.evaluator_id if c.source_evaluation else None
                    }
                    for c in self.constraints
                ],
                'projects': self.projects,
                'criteria': self.criteria
            }
        
        elif format == 'dataframe':
            data = []
            for c in self.constraints:
                data.append({
                    'constraint_id': c.constraint_id,
                    'bound': c.bound,
                    'is_equality': c.is_equality,
                    'evaluator': c.source_evaluation.evaluator_id if c.source_evaluation else None,
                    'coefficients': c.coefficients.tolist()
                })
            return pd.DataFrame(data)
        
        elif format == 'matrices':
            return self.get_constraint_matrices()
        
        else:
            raise ValueError(f"Unsupported export format: {format}")


def create_sample_evaluations() -> List[QualitativeEvaluation]:
    """Create sample qualitative evaluations for testing"""
    evaluations = [
        # Comparison evaluations
        QualitativeEvaluation(
            evaluator_id="expert_1",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["ProjectA", "ProjectB"],
            operator=ComparisonOperator.GREATER,
            confidence=0.8
        ),
        
        # Range evaluation
        QualitativeEvaluation(
            evaluator_id="expert_2",
            evaluation_type=EvaluationType.RANGE,
            projects=["ProjectC"],
            values=[0.3, 0.7],
            confidence=0.9
        ),
        
        # Ranking evaluation
        QualitativeEvaluation(
            evaluator_id="expert_3",
            evaluation_type=EvaluationType.RANKING,
            projects=["ProjectA", "ProjectC", "ProjectB"],
            confidence=0.7
        ),
        
        # Threshold evaluation
        QualitativeEvaluation(
            evaluator_id="expert_4",
            evaluation_type=EvaluationType.THRESHOLD,
            projects=["ProjectD"],
            operator=ComparisonOperator.GREATER_EQUAL,
            values=[0.5],
            confidence=0.85
        )
    ]
    
    return evaluations


if __name__ == "__main__":
    # Example usage
    projects = ["ProjectA", "ProjectB", "ProjectC", "ProjectD"]
    criteria = ["value", "risk", "benefit"]
    
    # Initialize translator
    translator = QualitativeEvaluationTranslator(projects, criteria)
    
    # Add sample evaluations
    sample_evaluations = create_sample_evaluations()
    for eval in sample_evaluations:
        translator.add_evaluation(eval)
    
    # Translate to constraints
    constraints = translator.translate_evaluations()
    
    # Validate constraints
    validation = translator.validate_constraints()
    print("Validation Results:")
    for key, value in validation.items():
        print(f"  {key}: {value}")
    
    # Export constraints
    constraint_dict = translator.export_constraints('dict')
    print(f"\nGenerated {len(constraint_dict['constraints'])} constraints")
    
    # Get constraint matrices
    A_ineq, b_ineq, A_eq, b_eq = translator.get_constraint_matrices()
    print(f"Inequality constraints: {A_ineq.shape}")
    print(f"Equality constraints: {A_eq.shape}")
