"""
Trade-off Analysis Module for Polytope-based Project Portfolio Selection

This module implements the TradeoffAnalyzer class for Phase 2 of the qualitative evaluation
translation system, enabling systematic exploration of competing objectives within the
feasible polytope space.

Author: Generated for Logos/Nimbus/Status ecosystem research
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.optimize import minimize
from scipy.spatial.distance import pdist, squareform
from typing import Dict, List, Tuple, Optional, Callable, Any
import warnings
from dataclasses import dataclass


@dataclass
class TradeoffMetrics:
    """Container for trade-off analysis metrics"""
    correlation: float
    avg_exchange_rate: float
    pareto_efficiency: float
    knee_points: List[int]
    dominated_ratio: float


class TradeoffAnalyzer:
    """
    Analyzes trade-offs between competing objectives within a feasible polytope space.
    
    This class provides systematic exploration of objective trade-offs, Pareto frontier
    identification, and interactive visualization capabilities for multi-objective
    project portfolio optimization.
    """
    
    def __init__(self, polytope_visualizer):
        """
        Initialize TradeoffAnalyzer with an existing PolytopeVisualizer.
        
        Args:
            polytope_visualizer: PolytopeVisualizer instance with constraint data
        """
        self.visualizer = polytope_visualizer
        self.translator = polytope_visualizer.translator
        self.objectives = {}
        self.sample_cache = {}
        self.pareto_cache = {}
        
        # Get constraint matrices
        self.A_ineq, self.b_ineq, self.A_eq, self.b_eq = self.translator.get_constraint_matrices()
        
        # Compute polytope properties for sampling bounds
        self.polytope_properties = self.visualizer.compute_polytope_properties()
        
    def set_objectives(self, objectives: Dict[str, Callable]):
        """
        Define objective functions for trade-off analysis.
        
        Args:
            objectives: Dictionary mapping objective names to functions that take
                       a solution vector x and return a scalar objective value
        """
        self.objectives = objectives.copy()
        # Clear caches when objectives change
        self.pareto_cache.clear()
        
    def sample_polytope(self, n_samples: int = 1000, method: str = 'uniform') -> np.ndarray:
        """
        Generate representative sample points within the feasible polytope.
        
        Args:
            n_samples: Number of sample points to generate
            method: Sampling strategy ('uniform', 'grid', 'monte_carlo', 'latin_hypercube')
            
        Returns:
            Array of sample points (n_samples × n_dimensions)
        """
        cache_key = f"{n_samples}_{method}"
        if cache_key in self.sample_cache:
            return self.sample_cache[cache_key]
            
        n_dims = len(self.translator.projects) * len(self.translator.criteria)
        
        if method == 'uniform':
            samples = self._uniform_sampling(n_samples, n_dims)
        elif method == 'grid':
            samples = self._grid_sampling(n_samples, n_dims)
        elif method == 'monte_carlo':
            samples = self._monte_carlo_sampling(n_samples, n_dims)
        elif method == 'latin_hypercube':
            samples = self._latin_hypercube_sampling(n_samples, n_dims)
        else:
            raise ValueError(f"Unknown sampling method: {method}")
            
        # Filter to feasible points
        feasible_samples = self._filter_feasible_points(samples)
        
        # If we don't have enough feasible points, generate more
        if len(feasible_samples) < n_samples * 0.1:  # At least 10% success rate
            warnings.warn(f"Low feasible sample rate: {len(feasible_samples)}/{len(samples)}")
            
        self.sample_cache[cache_key] = feasible_samples
        return feasible_samples
        
    def _uniform_sampling(self, n_samples: int, n_dims: int) -> np.ndarray:
        """Generate uniform random samples in [0,1]^n_dims"""
        return np.random.uniform(0, 1, (n_samples, n_dims))
        
    def _grid_sampling(self, n_samples: int, n_dims: int) -> np.ndarray:
        """Generate structured grid samples"""
        points_per_dim = int(np.ceil(n_samples ** (1/n_dims)))
        coords = [np.linspace(0, 1, points_per_dim) for _ in range(n_dims)]
        grid = np.meshgrid(*coords, indexing='ij')
        samples = np.column_stack([g.ravel() for g in grid])
        return samples[:n_samples]  # Truncate to requested size
        
    def _monte_carlo_sampling(self, n_samples: int, n_dims: int) -> np.ndarray:
        """Generate Monte Carlo samples (same as uniform for this case)"""
        return self._uniform_sampling(n_samples, n_dims)
        
    def _latin_hypercube_sampling(self, n_samples: int, n_dims: int) -> np.ndarray:
        """Generate Latin Hypercube samples for better space coverage"""
        # Simple LHS implementation
        samples = np.zeros((n_samples, n_dims))
        for i in range(n_dims):
            samples[:, i] = (np.random.permutation(n_samples) + np.random.uniform(0, 1, n_samples)) / n_samples
        return samples
        
    def _filter_feasible_points(self, samples: np.ndarray) -> np.ndarray:
        """Filter samples to only include feasible points"""
        feasible_mask = np.ones(len(samples), dtype=bool)
        
        # Check inequality constraints
        if self.A_ineq is not None and self.b_ineq is not None:
            violations = np.dot(samples, self.A_ineq.T) - self.b_ineq
            feasible_mask &= np.all(violations <= 1e-10, axis=1)  # Small tolerance for numerical errors
            
        # Check equality constraints
        if self.A_eq is not None and self.b_eq is not None:
            violations = np.abs(np.dot(samples, self.A_eq.T) - self.b_eq)
            feasible_mask &= np.all(violations <= 1e-8, axis=1)
            
        return samples[feasible_mask]
        
    def compute_pareto_frontier(self, objectives: List[str], resolution: int = 100) -> Dict[str, Any]:
        """
        Identify Pareto optimal solutions for given objectives.
        
        Args:
            objectives: List of objective function names
            resolution: Number of points to compute along frontier
            
        Returns:
            Dictionary with frontier points, objective values, and trade-off rates
        """
        cache_key = f"{'-'.join(objectives)}_{resolution}"
        if cache_key in self.pareto_cache:
            return self.pareto_cache[cache_key]
            
        if not all(obj in self.objectives for obj in objectives):
            missing = [obj for obj in objectives if obj not in self.objectives]
            raise ValueError(f"Objectives not defined: {missing}")
            
        # Generate sample points for Pareto analysis
        samples = self.sample_polytope(n_samples=resolution * 10, method='latin_hypercube')
        
        if len(samples) == 0:
            raise ValueError("No feasible samples found for Pareto frontier computation")
            
        # Evaluate objectives for all samples
        objective_values = {}
        for obj_name in objectives:
            objective_values[obj_name] = np.array([self.objectives[obj_name](x) for x in samples])
            
        # Find Pareto optimal points
        pareto_mask = self._find_pareto_optimal(objective_values, objectives)
        pareto_points = samples[pareto_mask]
        pareto_objectives = {obj: vals[pareto_mask] for obj, vals in objective_values.items()}
        
        # Compute trade-off rates along frontier
        tradeoff_rates = self._compute_tradeoff_rates(pareto_objectives, objectives)
        
        # Compute objective ranges
        objective_ranges = {obj: (vals.min(), vals.max()) for obj, vals in pareto_objectives.items()}
        
        result = {
            'points': pareto_points,
            'objectives': pareto_objectives,
            'objective_ranges': objective_ranges,
            'tradeoff_rates': tradeoff_rates,
            'avg_tradeoff_rate': np.mean(list(tradeoff_rates.values())) if tradeoff_rates else 0,
            'n_pareto_points': len(pareto_points),
            'pareto_efficiency': len(pareto_points) / len(samples)
        }
        
        self.pareto_cache[cache_key] = result
        return result
        
    def _find_pareto_optimal(self, objective_values: Dict[str, np.ndarray], objectives: List[str]) -> np.ndarray:
        """Find Pareto optimal points (assuming maximization)"""
        n_points = len(next(iter(objective_values.values())))
        pareto_mask = np.ones(n_points, dtype=bool)
        
        # Create objective matrix (n_points × n_objectives)
        obj_matrix = np.column_stack([objective_values[obj] for obj in objectives])
        
        for i in range(n_points):
            if not pareto_mask[i]:
                continue
                
            # Check if point i is dominated by any other point
            for j in range(n_points):
                if i == j or not pareto_mask[j]:
                    continue
                    
                # Point j dominates point i if j is >= i in all objectives and > i in at least one
                dominates = np.all(obj_matrix[j] >= obj_matrix[i]) and np.any(obj_matrix[j] > obj_matrix[i])
                if dominates:
                    pareto_mask[i] = False
                    break
                    
        return pareto_mask
        
    def _compute_tradeoff_rates(self, pareto_objectives: Dict[str, np.ndarray], objectives: List[str]) -> Dict[str, float]:
        """Compute trade-off rates between objective pairs"""
        tradeoff_rates = {}
        
        for i, obj1 in enumerate(objectives):
            for j, obj2 in enumerate(objectives[i+1:], i+1):
                # Compute correlation as a proxy for trade-off rate
                corr = np.corrcoef(pareto_objectives[obj1], pareto_objectives[obj2])[0, 1]
                tradeoff_rates[f"{obj1}_vs_{obj2}"] = abs(corr) if not np.isnan(corr) else 0
                
        return tradeoff_rates
        
    def analyze_tradeoffs(self, objective_pairs: List[Tuple[str, str]], 
                         sample_points: Optional[np.ndarray] = None) -> Dict[str, TradeoffMetrics]:
        """
        Quantify trade-off relationships between objective pairs.
        
        Args:
            objective_pairs: List of (obj1, obj2) tuples to analyze
            sample_points: Optional pre-computed sample points
            
        Returns:
            Trade-off analysis results including correlation, exchange rates, and efficiency metrics
        """
        if sample_points is None:
            sample_points = self.sample_polytope(n_samples=2000, method='latin_hypercube')
            
        results = {}
        
        for obj1, obj2 in objective_pairs:
            if obj1 not in self.objectives or obj2 not in self.objectives:
                raise ValueError(f"Objectives not defined: {obj1}, {obj2}")
                
            # Evaluate objectives
            values1 = np.array([self.objectives[obj1](x) for x in sample_points])
            values2 = np.array([self.objectives[obj2](x) for x in sample_points])
            
            # Compute metrics
            correlation = np.corrcoef(values1, values2)[0, 1] if len(values1) > 1 else 0
            if np.isnan(correlation):
                correlation = 0
                
            # Compute exchange rate (slope of regression line)
            if np.std(values1) > 1e-10:
                exchange_rate = abs(np.cov(values1, values2)[0, 1] / np.var(values1))
            else:
                exchange_rate = 0
                
            # Find Pareto optimal points for this pair
            pareto_frontier = self.compute_pareto_frontier([obj1, obj2], resolution=100)
            pareto_efficiency = pareto_frontier['pareto_efficiency']
            
            # Find knee points (points with high curvature)
            knee_points = self._find_knee_points(pareto_frontier['objectives'][obj1], 
                                               pareto_frontier['objectives'][obj2])
            
            # Compute dominated ratio
            dominated_ratio = 1 - pareto_efficiency
            
            metrics = TradeoffMetrics(
                correlation=correlation,
                avg_exchange_rate=exchange_rate,
                pareto_efficiency=pareto_efficiency,
                knee_points=knee_points,
                dominated_ratio=dominated_ratio
            )
            
            results[f"{obj1}_vs_{obj2}"] = metrics
            
        return results
        
    def _find_knee_points(self, values1: np.ndarray, values2: np.ndarray) -> List[int]:
        """Find knee points (high curvature points) in Pareto frontier"""
        if len(values1) < 3:
            return []
            
        # Sort points by first objective
        sorted_indices = np.argsort(values1)
        sorted_v1 = values1[sorted_indices]
        sorted_v2 = values2[sorted_indices]
        
        # Compute curvature using second derivative approximation
        curvatures = []
        for i in range(1, len(sorted_v1) - 1):
            # Second derivative approximation
            d2 = (sorted_v2[i+1] - 2*sorted_v2[i] + sorted_v2[i-1])
            curvatures.append(abs(d2))
            
        # Find points with high curvature (top 20%)
        if curvatures:
            threshold = np.percentile(curvatures, 80)
            knee_indices = [i+1 for i, curv in enumerate(curvatures) if curv >= threshold]
            return [sorted_indices[i] for i in knee_indices]
        
        return []
        
    def create_tradeoff_visualization(self, objectives: List[str], interactive: bool = True) -> go.Figure:
        """
        Generate interactive visualizations of trade-off relationships.
        
        Args:
            objectives: List of 2-3 objectives to visualize
            interactive: Whether to create interactive Plotly plots
            
        Returns:
            Plotly figure object with trade-off visualization
        """
        if len(objectives) < 2 or len(objectives) > 3:
            raise ValueError("Can only visualize 2 or 3 objectives")
            
        if not all(obj in self.objectives for obj in objectives):
            missing = [obj for obj in objectives if obj not in self.objectives]
            raise ValueError(f"Objectives not defined: {missing}")
            
        # Generate samples and compute Pareto frontier
        samples = self.sample_polytope(n_samples=1000, method='latin_hypercube')
        pareto_frontier = self.compute_pareto_frontier(objectives, resolution=200)
        
        # Evaluate objectives for all samples
        sample_objectives = {}
        for obj_name in objectives:
            sample_objectives[obj_name] = np.array([self.objectives[obj_name](x) for x in samples])
            
        if len(objectives) == 2:
            return self._create_2d_tradeoff_plot(sample_objectives, pareto_frontier, objectives, interactive)
        else:
            return self._create_3d_tradeoff_plot(sample_objectives, pareto_frontier, objectives, interactive)
            
    def _create_2d_tradeoff_plot(self, sample_objectives: Dict[str, np.ndarray], 
                                pareto_frontier: Dict[str, Any], objectives: List[str], 
                                interactive: bool) -> go.Figure:
        """Create 2D trade-off visualization"""
        obj1, obj2 = objectives
        
        fig = go.Figure()
        
        # Add all sample points
        fig.add_trace(go.Scatter(
            x=sample_objectives[obj1],
            y=sample_objectives[obj2],
            mode='markers',
            marker=dict(size=4, color='lightblue', opacity=0.6),
            name='Feasible Solutions',
            hovertemplate=f'{obj1}: %{{x:.3f}}<br>{obj2}: %{{y:.3f}}<extra></extra>'
        ))
        
        # Add Pareto frontier
        pareto_x = pareto_frontier['objectives'][obj1]
        pareto_y = pareto_frontier['objectives'][obj2]
        
        # Sort Pareto points for better line visualization
        sorted_indices = np.argsort(pareto_x)
        pareto_x_sorted = pareto_x[sorted_indices]
        pareto_y_sorted = pareto_y[sorted_indices]
        
        fig.add_trace(go.Scatter(
            x=pareto_x_sorted,
            y=pareto_y_sorted,
            mode='markers+lines',
            marker=dict(size=8, color='red'),
            line=dict(color='red', width=2),
            name='Pareto Frontier',
            hovertemplate=f'{obj1}: %{{x:.3f}}<br>{obj2}: %{{y:.3f}}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'Trade-off Analysis: {obj1} vs {obj2}',
            xaxis_title=obj1,
            yaxis_title=obj2,
            hovermode='closest',
            showlegend=True
        )
        
        return fig
        
    def _create_3d_tradeoff_plot(self, sample_objectives: Dict[str, np.ndarray], 
                                pareto_frontier: Dict[str, Any], objectives: List[str], 
                                interactive: bool) -> go.Figure:
        """Create 3D trade-off visualization"""
        obj1, obj2, obj3 = objectives
        
        fig = go.Figure()
        
        # Add all sample points
        fig.add_trace(go.Scatter3d(
            x=sample_objectives[obj1],
            y=sample_objectives[obj2],
            z=sample_objectives[obj3],
            mode='markers',
            marker=dict(size=3, color='lightblue', opacity=0.4),
            name='Feasible Solutions',
            hovertemplate=f'{obj1}: %{{x:.3f}}<br>{obj2}: %{{y:.3f}}<br>{obj3}: %{{z:.3f}}<extra></extra>'
        ))
        
        # Add Pareto frontier
        fig.add_trace(go.Scatter3d(
            x=pareto_frontier['objectives'][obj1],
            y=pareto_frontier['objectives'][obj2],
            z=pareto_frontier['objectives'][obj3],
            mode='markers',
            marker=dict(size=6, color='red'),
            name='Pareto Frontier',
            hovertemplate=f'{obj1}: %{{x:.3f}}<br>{obj2}: %{{y:.3f}}<br>{obj3}: %{{z:.3f}}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'3D Trade-off Analysis: {obj1} vs {obj2} vs {obj3}',
            scene=dict(
                xaxis_title=obj1,
                yaxis_title=obj2,
                zaxis_title=obj3
            ),
            showlegend=True
        )
        
        return fig
        
    def create_tradeoff_dashboard(self, objectives: List[str], include_pareto: bool = True,
                                 include_samples: bool = True, include_sensitivity: bool = True) -> go.Figure:
        """
        Create comprehensive trade-off analysis dashboard.
        
        Args:
            objectives: List of objectives to analyze
            include_pareto: Whether to include Pareto frontier analysis
            include_samples: Whether to include sample distribution plots
            include_sensitivity: Whether to include sensitivity analysis
            
        Returns:
            Plotly figure with comprehensive dashboard
        """
        if len(objectives) < 2:
            raise ValueError("Need at least 2 objectives for dashboard")
            
        # Create subplot structure
        n_pairs = len(objectives) * (len(objectives) - 1) // 2
        n_cols = min(3, n_pairs)
        n_rows = (n_pairs + n_cols - 1) // n_cols
        
        subplot_titles = []
        for i, obj1 in enumerate(objectives):
            for obj2 in objectives[i+1:]:
                subplot_titles.append(f"{obj1} vs {obj2}")
                
        fig = make_subplots(
            rows=n_rows, cols=n_cols,
            subplot_titles=subplot_titles,
            specs=[[{"secondary_y": False} for _ in range(n_cols)] for _ in range(n_rows)]
        )
        
        # Generate samples once
        samples = self.sample_polytope(n_samples=1000, method='latin_hypercube')
        
        # Create plots for each objective pair
        plot_idx = 0
        for i, obj1 in enumerate(objectives):
            for j, obj2 in enumerate(objectives[i+1:], i+1):
                row = plot_idx // n_cols + 1
                col = plot_idx % n_cols + 1
                
                # Evaluate objectives
                values1 = np.array([self.objectives[obj1](x) for x in samples])
                values2 = np.array([self.objectives[obj2](x) for x in samples])
                
                # Add sample points
                if include_samples:
                    fig.add_trace(
                        go.Scatter(
                            x=values1, y=values2,
                            mode='markers',
                            marker=dict(size=3, color='lightblue', opacity=0.6),
                            name=f'Samples ({obj1}-{obj2})',
                            showlegend=(plot_idx == 0)
                        ),
                        row=row, col=col
                    )
                
                # Add Pareto frontier
                if include_pareto:
                    pareto_frontier = self.compute_pareto_frontier([obj1, obj2], resolution=100)
                    pareto_x = pareto_frontier['objectives'][obj1]
                    pareto_y = pareto_frontier['objectives'][obj2]
                    
                    # Sort for better visualization
                    sorted_indices = np.argsort(pareto_x)
                    
                    fig.add_trace(
                        go.Scatter(
                            x=pareto_x[sorted_indices],
                            y=pareto_y[sorted_indices],
                            mode='markers+lines',
                            marker=dict(size=5, color='red'),
                            line=dict(color='red', width=2),
                            name=f'Pareto ({obj1}-{obj2})',
                            showlegend=(plot_idx == 0)
                        ),
                        row=row, col=col
                    )
                
                plot_idx += 1
                
        fig.update_layout(
            title="Trade-off Analysis Dashboard",
            height=300 * n_rows,
            showlegend=True
        )
        
        return fig
        
    def adaptive_sample_pareto_regions(self, objectives: List[str], initial_samples: int = 500,
                                     refinement_iterations: int = 3) -> np.ndarray:
        """
        Focus sampling on Pareto regions for better frontier approximation.
        
        Args:
            objectives: List of objectives to focus on
            initial_samples: Number of initial samples
            refinement_iterations: Number of refinement iterations
            
        Returns:
            Array of samples focused on Pareto regions
        """
        # Start with initial uniform sampling
        samples = self.sample_polytope(n_samples=initial_samples, method='latin_hypercube')
        
        for iteration in range(refinement_iterations):
            # Find current Pareto frontier
            pareto_frontier = self.compute_pareto_frontier(objectives, resolution=len(samples))
            pareto_points = pareto_frontier['points']
            
            if len(pareto_points) == 0:
                break
                
            # Generate new samples around Pareto points
            n_new_samples = initial_samples // (iteration + 2)  # Decreasing samples per iteration
            new_samples = []
            
            for pareto_point in pareto_points:
                # Add noise around each Pareto point
                noise_scale = 0.1 / (iteration + 1)  # Decreasing noise
                for _ in range(max(1, n_new_samples // len(pareto_points))):
                    noise = np.random.normal(0, noise_scale, len(pareto_point))
                    new_point = np.clip(pareto_point + noise, 0, 1)
                    new_samples.append(new_point)
                    
            # Filter new samples for feasibility
            if new_samples:
                new_samples = np.array(new_samples)
                feasible_new = self._filter_feasible_points(new_samples)
                if len(feasible_new) > 0:
                    samples = np.vstack([samples, feasible_new])
                    
        return samples
        
    def solve_weighted_objectives(self, weight_vectors: List[List[float]], 
                                 objectives: List[str]) -> List[np.ndarray]:
        """
        Multi-objective optimization using weighted sum approach.
        
        Args:
            weight_vectors: List of weight vectors for objectives
            objectives: List of objective names
            
        Returns:
            List of optimal solutions for each weight vector
        """
        if len(weight_vectors[0]) != len(objectives):
            raise ValueError("Weight vector length must match number of objectives")
            
        solutions = []
        
        for weights in weight_vectors:
            # Define weighted objective function
            def weighted_objective(x):
                total = 0
                for i, obj_name in enumerate(objectives):
                    total += weights[i] * self.objectives[obj_name](x)
                return -total  # Minimize negative for maximization
                
            # Define constraints
            constraints = []
            
            # Inequality constraints
            if self.A_ineq is not None and self.b_ineq is not None:
                constraints.append({
                    'type': 'ineq',
                    'fun': lambda x: self.b_ineq - np.dot(self.A_ineq, x)
                })
                
            # Equality constraints
            if self.A_eq is not None and self.b_eq is not None:
                constraints.append({
                    'type': 'eq',
                    'fun': lambda x: np.dot(self.A_eq, x) - self.b_eq
                })
                
            # Bounds (assuming [0,1] for each variable)
            n_vars = len(self.translator.projects) * len(self.translator.criteria)
            bounds = [(0, 1) for _ in range(n_vars)]
            
            # Initial guess (center of feasible region)
            x0 = np.full(n_vars, 0.5)
            
            # Solve optimization problem
            try:
                result = minimize(
                    weighted_objective,
                    x0,
                    method='SLSQP',
                    bounds=bounds,
                    constraints=constraints,
                    options={'maxiter': 1000}
                )
                
                if result.success:
                    solutions.append(result.x)
                else:
                    # Fallback: use feasible sample closest to optimum
                    samples = self.sample_polytope(n_samples=100)
                    if len(samples) > 0:
                        obj_values = [weighted_objective(x) for x in samples]
                        best_idx = np.argmin(obj_values)
                        solutions.append(samples[best_idx])
                    else:
                        solutions.append(x0)  # Last resort
                        
            except Exception as e:
                warnings.warn(f"Optimization failed for weights {weights}: {e}")
                solutions.append(x0)
                
        return solutions


def create_example_objectives(translator) -> Dict[str, Callable]:
    """
    Create example objective functions for demonstration purposes.
    
    Args:
        translator: QualitativeEvaluationTranslator instance
        
    Returns:
        Dictionary of example objective functions
    """
    n_projects = len(translator.projects)
    n_criteria = len(translator.criteria)
    
    # Create some example weight vectors
    strategic_weights = np.random.uniform(0.5, 1.0, n_projects * n_criteria)
    cost_weights = np.random.uniform(0.3, 0.8, n_projects * n_criteria)
    risk_weights = np.random.uniform(0.2, 0.6, n_projects * n_criteria)
    
    objectives = {
        'strategic_value': lambda x: np.sum(x * strategic_weights),
        'development_cost': lambda x: -np.sum(x * cost_weights),  # Negative for minimization
        'technical_risk': lambda x: -np.sum(x * risk_weights),    # Negative for minimization
        'portfolio_balance': lambda x: -np.std(x),                # Negative std for balance
        'total_value': lambda x: np.sum(x)
    }
    
    return objectives


if __name__ == "__main__":
    # Example usage
    from polytope_visualization_demo import create_logos_nimbus_status_translator
    from polytope_visualizer import PolytopeVisualizer
    
    # Create translator and visualizer
    translator = create_logos_nimbus_status_translator()
    visualizer = PolytopeVisualizer(translator)
    
    # Create trade-off analyzer
    analyzer = TradeoffAnalyzer(visualizer)
    
    # Set up example objectives
    objectives = create_example_objectives(translator)
    analyzer.set_objectives(objectives)
    
    # Demonstrate trade-off analysis
    print("Generating samples...")
    samples = analyzer.sample_polytope(n_samples=1000, method='latin_hypercube')
    print(f"Generated {len(samples)} feasible samples")
    
    print("\nComputing Pareto frontier...")
    frontier = analyzer.compute_pareto_frontier(['strategic_value', 'development_cost'], resolution=100)
    print(f"Found {frontier['n_pareto_points']} Pareto optimal points")
    print(f"Pareto efficiency: {frontier['pareto_efficiency']:.3f}")
    
    print("\nAnalyzing trade-offs...")
    tradeoffs = analyzer.analyze_tradeoffs([
        ('strategic_value', 'development_cost'),
        ('strategic_value', 'technical_risk')
    ])
    
    for pair, metrics in tradeoffs.items():
        print(f"{pair}: correlation={metrics.correlation:.3f}, "
              f"exchange_rate={metrics.avg_exchange_rate:.3f}")
    
    print("\nCreating visualization...")
    fig = analyzer.create_tradeoff_visualization(['strategic_value', 'development_cost'])
    
    # Save to proper directory
    import os
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'visualizations', 'phase2')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "tradeoff_analysis_example.html")
    fig.write_html(output_path)
    print(f"Visualization saved to {output_path}")
