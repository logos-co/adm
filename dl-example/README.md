# Qualitative Evaluation Translation Module

A comprehensive system for converting human qualitative evaluations into mathematical constraints for robust project portfolio selection, implementing the constraint space visualization framework described in the research requirements.

## Overview

This module implements the **Qualitative Evaluation Translation Module** from the Robust Human–Machine Framework for Project Portfolio Selection (PPSS). It converts subjective human evaluations into linear equality and inequality constraints that define a convex polytope representing the feasible space for project value matrices.

## Key Features

- **🔄 Qualitative-to-Mathematical Translation**: Converts human evaluations into linear constraints
- **📊 Interactive Polytope Visualization**: 2D/3D visualization of constraint spaces
- **🎯 Multi-Criteria Support**: Handles multiple evaluation criteria simultaneously
- **👥 Stakeholder Integration**: Processes evaluations from multiple stakeholders
- **📈 Constraint Sensitivity Analysis**: Analyzes impact of individual constraints
- **⚖️ Objective Trade-off Sampling**: Systematic exploration of trade-offs between competing objectives
- **🎲 Pareto Frontier Analysis**: Identification and visualization of optimal trade-off boundaries
- **🌐 Web-Based Dashboards**: Interactive HTML visualizations
- **📁 Data Export**: Multiple export formats (JSON, CSV, NPZ)

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Input Layer                              │
├─────────────────────────────────────────────────────────────┤
│ • Human Qualitative Evaluations                            │
│ • Project Data (costs, durations, values)                  │
│ • Stakeholder Preferences                                   │
│ • Objective Function Definitions                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Translation Engine                             │
├─────────────────────────────────────────────────────────────┤
│ • QualitativeEvaluationTranslator                         │
│ • Constraint Generation (A_ineq * x ≤ b_ineq)             │
│ • Polytope Definition                                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│             Visualization Layer                            │
├─────────────────────────────────────────────────────────────┤
│ • PolytopeVisualizer                                       │
│ • 2D/3D Interactive Plots                                  │
│ • Constraint Sensitivity Analysis                          │
│ • Stakeholder Comparison                                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│          Trade-off Analysis Layer (Phase 2)                │
├─────────────────────────────────────────────────────────────┤
│ • TradeoffAnalyzer                                         │
│ • Polytope Sampling (Uniform, Grid, Latin Hypercube)      │
│ • Pareto Frontier Computation                              │
│ • Multi-Objective Trade-off Quantification                │
│ • Interactive Trade-off Dashboards                        │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. QualitativeEvaluationTranslator
**File**: `qualitative_evaluation_translator.py`

Converts human evaluations into mathematical constraints:

```python
from qualitative_evaluation_translator import (
    QualitativeEvaluationTranslator, 
    QualitativeEvaluation, 
    EvaluationType,
    ComparisonOperator
)

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

**Supported Evaluation Types**:
- **COMPARISON**: "Project A > Project B"
- **RANGE**: "Project value between 0.3 and 0.7"
- **RANKING**: "A > B > C > D"
- **THRESHOLD**: "Project must have value ≥ 0.5"

### 2. PolytopeVisualizer
**File**: `polytope_visualizer.py`

Creates interactive visualizations of constraint polytopes:

```python
from polytope_visualizer import PolytopeVisualizer

# Create visualizer
visualizer = PolytopeVisualizer(translator)

# Generate 2D visualization
fig_2d = visualizer.create_2d_visualization(
    dim_x=0, dim_y=1,
    show_vertices=True,
    show_constraints=True,
    show_feasible_region=True
)

# Generate 3D visualization
fig_3d = visualizer.create_3d_visualization(
    dim_x=0, dim_y=1, dim_z=2,
    show_vertices=True,
    opacity=0.3
)

# Create interactive dashboard
dashboard = visualizer.create_dimension_selector_dashboard()
```

### 3. Project Data Integration
**File**: `logos_nimbus_status_projects.py`

Comprehensive project data for the Logos/Nimbus/Status ecosystem:

- **16 projects** across 5 ecosystems
- **Complete project attributes**: duration, cost, multiple values
- **Constraint relationships**: cooperation, precedence, exclusivity
- **12 stakeholder evaluations** from 6 different roles

### 4. Demonstration System
**File**: `polytope_visualization_demo.py`

Complete demonstration with real project data:

```python
from polytope_visualization_demo import create_logos_nimbus_status_translator

# Create translator with real project data
translator = create_logos_nimbus_status_translator()

# Generate visualizations and analysis
visualizer = PolytopeVisualizer(translator)
properties = visualizer.compute_polytope_properties()
```

## Directory Structure

This project is organized into a clean, maintainable directory structure:

```
dl-example/
├── README.md                           # This file
├── project_portfolio_index.html        # Main visualization dashboard
├── DIRECTORY_STRUCTURE.md             # Detailed directory documentation
├── src/                                # Source code modules
├── tests/                              # Test suite
├── examples/                           # Usage demonstrations
├── data/                               # Data files (JSON, CSV)
├── docs/                               # Documentation
└── visualizations/                     # Generated HTML visualizations
    ├── phase1/                         # Phase 1 polytope visualizations
    ├── phase2/                         # Phase 2 trade-off analysis
    └── portfolio/                      # Project portfolio visualizations
```

For detailed information about each directory and file, see [`DIRECTORY_STRUCTURE.md`](DIRECTORY_STRUCTURE.md).

## Installation & Setup

### Prerequisites
```bash
pip install numpy pandas plotly scipy networkx
```

### Optional Dependencies
```bash
pip install pypoman  # For enhanced polytope operations
pip install dash     # For interactive web applications
```

### Quick Start

#### 1. View Interactive Visualizations
Open `project_portfolio_index.html` in your web browser to explore all visualizations.

#### 2. Basic Usage Example
```python
# Add src directory to path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from qualitative_evaluation_translator import *
from polytope_visualizer import PolytopeVisualizer

# 1. Create translator
translator = QualitativeEvaluationTranslator(
    projects=["Project A", "Project B"],
    criteria=["Strategic Value"]
)

# 2. Add evaluations
eval1 = QualitativeEvaluation(
    evaluator_id="expert_1",
    evaluation_type=EvaluationType.RANGE,
    projects=["Project A"],
    values=[0.3, 0.7],
    criteria="Strategic Value"
)
translator.add_evaluation(eval1)

# 3. Create visualizer
visualizer = PolytopeVisualizer(translator)

# 4. Generate visualization
fig = visualizer.create_2d_visualization()
fig.show()
```

#### 3. Run Examples
```bash
# Phase 1 demonstration
python examples/polytope_visualization_demo.py

# Phase 2 demonstration  
python examples/tradeoff_analysis_demo.py

# Project portfolio visualization
python src/project_visualizer.py
```

#### 4. Run Tests
```bash
# Run all tests
python tests/test_qualitative_evaluation.py
python tests/test_polytope_visualization.py
python tests/test_tradeoff_analysis.py
```

## Usage Examples

### Example 1: Simple Project Comparison
```python
# Compare two projects on strategic value
comparison = QualitativeEvaluation(
    evaluator_id="ceo",
    evaluation_type=EvaluationType.COMPARISON,
    projects=["Logos Core", "Status App"],
    operator=ComparisonOperator.GREATER,
    criteria="Strategic Value"
)
```

### Example 2: Range Constraints
```python
# Set acceptable range for project value
range_constraint = QualitativeEvaluation(
    evaluator_id="expert",
    evaluation_type=EvaluationType.RANGE,
    projects=["Nimbus Client"],
    values=[0.6, 0.9],
    criteria="Technical Feasibility"
)
```

### Example 3: Multi-Project Ranking
```python
# Rank projects by preference
ranking = QualitativeEvaluation(
    evaluator_id="stakeholder",
    evaluation_type=EvaluationType.RANKING,
    projects=["Project A", "Project B", "Project C"],
    criteria="Market Impact"
)
```

## Testing

Run the comprehensive test suite:

```bash
cd dl-example
python test_polytope_visualization.py
```

Run basic functionality test:

```bash
python -c "
from polytope_visualization_demo import create_logos_nimbus_status_translator
from polytope_visualizer import PolytopeVisualizer

translator = create_logos_nimbus_status_translator()
visualizer = PolytopeVisualizer(translator)
properties = visualizer.compute_polytope_properties()
print(f'System working: {properties[\"n_constraints\"]} constraints generated')
"
```

## Demo & Visualization

### Generate Interactive Visualizations
```bash
python polytope_visualization_demo.py
```

This creates:
- `polytope_2d_*.html` - 2D constraint visualizations
- `polytope_3d_*.html` - 3D polytope visualizations  
- `polytope_dashboard.html` - Interactive dashboard
- `polytope_data.json` - Exported polytope data

### View Results
Open the generated HTML files in a web browser to explore:
- **Feasible regions** defined by constraints
- **Polytope vertices** and boundaries
- **Interactive dimension selection**
- **Constraint sensitivity analysis**

## Mathematical Foundation

The system implements the mathematical framework where:

- **x** = project value vector (n_projects × n_criteria dimensions)
- **A_ineq * x ≤ b_ineq** = inequality constraints from evaluations
- **A_eq * x = b_eq** = equality constraints from evaluations
- **Polytope P** = {x : A_ineq * x ≤ b_ineq, A_eq * x = b_eq}

### Constraint Types Generated

1. **Comparison Constraints**: v_A - v_B ≥ ε (for A > B)
2. **Range Constraints**: min ≤ v_i ≤ max
3. **Threshold Constraints**: v_i ≥ threshold
4. **Ranking Constraints**: v_1 ≥ v_2 ≥ ... ≥ v_n

## API Reference

### QualitativeEvaluationTranslator

#### Methods
- `add_evaluation(evaluation)` - Add qualitative evaluation
- `translate_evaluations()` - Convert to linear constraints
- `get_constraint_matrices()` - Get A_ineq, b_ineq, A_eq, b_eq
- `validate_constraints()` - Check system consistency
- `export_constraints(format)` - Export in various formats

### PolytopeVisualizer

#### Methods
- `compute_vertices()` - Calculate polytope vertices
- `compute_polytope_properties()` - Get polytope statistics
- `create_2d_visualization()` - Generate 2D plots
- `create_3d_visualization()` - Generate 3D plots
- `create_dimension_selector_dashboard()` - Interactive dashboard
- `export_polytope_data()` - Export polytope data

### TradeoffAnalyzer

#### Methods
- `set_objectives(objectives)` - Define objective functions for analysis
- `sample_polytope(n_samples, method)` - Generate sample points within polytope
- `compute_pareto_frontier(objectives, resolution)` - Calculate Pareto optimal solutions
- `analyze_tradeoffs(objective_pairs, sample_points)` - Quantify trade-off relationships
- `create_tradeoff_visualization(objectives, interactive)` - Generate trade-off plots
- `create_tradeoff_dashboard(objectives, options)` - Create comprehensive analysis dashboard
- `adaptive_sample_pareto_regions(objectives, params)` - Focus sampling on Pareto regions
- `solve_weighted_objectives(weight_vectors, objectives)` - Multi-objective optimization

## Objective Trade-off Sampling and Analysis (Phase 2)

### Overview

The objective trade-off sampling and analysis module enables systematic exploration of competing objectives within the feasible polytope space. This capability allows decision-makers to understand the fundamental trade-offs between different project portfolio objectives and identify optimal compromise solutions.

### Key Capabilities

- **Systematic Sampling**: Generate representative sample points throughout the feasible polytope
- **Pareto Frontier Identification**: Discover optimal trade-off boundaries between objectives
- **Trade-off Quantification**: Measure the cost of improving one objective relative to others
- **Interactive Exploration**: Navigate trade-off spaces with dynamic objective weighting
- **Sensitivity Analysis**: Understand how constraint changes affect trade-off relationships

### Mathematical Foundation

The trade-off analysis operates on the feasible polytope **P** defined by constraints, exploring the objective space:

- **Objective Functions**: f₁(x), f₂(x), ..., fₖ(x) representing different portfolio goals
- **Pareto Optimal Set**: {x ∈ P : ∄ y ∈ P such that fᵢ(y) ≥ fᵢ(x) ∀i and fⱼ(y) > fⱼ(x) for some j}
- **Trade-off Rate**: ∂fᵢ/∂fⱼ measuring the exchange rate between objectives
- **Weighted Objectives**: Σᵢ wᵢfᵢ(x) for exploring preference-based solutions

### API Methods

#### TradeoffAnalyzer Class

```python
from polytope_visualizer import PolytopeVisualizer
from tradeoff_analyzer import TradeoffAnalyzer

# Create analyzer from existing visualizer
analyzer = TradeoffAnalyzer(visualizer)

# Define objective functions
objectives = {
    'strategic_value': lambda x: np.sum(x * strategic_weights),
    'technical_risk': lambda x: np.sum(x * risk_weights),
    'resource_cost': lambda x: np.sum(x * cost_weights)
}
analyzer.set_objectives(objectives)
```

#### Core Methods

**`sample_polytope(n_samples=1000, method='uniform')`**
- **Purpose**: Generate representative sample points within the feasible polytope
- **Parameters**:
  - `n_samples`: Number of sample points to generate
  - `method`: Sampling strategy ('uniform', 'grid', 'monte_carlo', 'latin_hypercube')
- **Returns**: Array of sample points (n_samples × n_dimensions)

```python
# Generate uniform samples
samples = analyzer.sample_polytope(n_samples=5000, method='uniform')

# Generate structured grid samples
grid_samples = analyzer.sample_polytope(n_samples=1000, method='grid')
```

**`compute_pareto_frontier(objectives, resolution=100)`**
- **Purpose**: Identify Pareto optimal solutions for given objectives
- **Parameters**:
  - `objectives`: List of objective function names
  - `resolution`: Number of points to compute along frontier
- **Returns**: Dictionary with frontier points, objective values, and trade-off rates

```python
# Compute 2D Pareto frontier
frontier_2d = analyzer.compute_pareto_frontier(
    objectives=['strategic_value', 'technical_risk'],
    resolution=200
)

# Compute 3D Pareto surface
frontier_3d = analyzer.compute_pareto_frontier(
    objectives=['strategic_value', 'technical_risk', 'resource_cost'],
    resolution=50
)
```

**`analyze_tradeoffs(objective_pairs, sample_points=None)`**
- **Purpose**: Quantify trade-off relationships between objective pairs
- **Parameters**:
  - `objective_pairs`: List of (obj1, obj2) tuples to analyze
  - `sample_points`: Optional pre-computed sample points
- **Returns**: Trade-off analysis results including correlation, exchange rates, and efficiency metrics

```python
# Analyze all pairwise trade-offs
tradeoff_analysis = analyzer.analyze_tradeoffs([
    ('strategic_value', 'technical_risk'),
    ('strategic_value', 'resource_cost'),
    ('technical_risk', 'resource_cost')
])

# Access trade-off metrics
for pair, metrics in tradeoff_analysis.items():
    print(f"{pair}: correlation={metrics['correlation']:.3f}, "
          f"exchange_rate={metrics['avg_exchange_rate']:.3f}")
```

**`create_tradeoff_visualization(objectives, interactive=True)`**
- **Purpose**: Generate interactive visualizations of trade-off relationships
- **Parameters**:
  - `objectives`: List of 2-3 objectives to visualize
  - `interactive`: Whether to create interactive Plotly plots
- **Returns**: Plotly figure object with trade-off visualization

```python
# Create 2D trade-off plot
fig_2d = analyzer.create_tradeoff_visualization(
    objectives=['strategic_value', 'technical_risk'],
    interactive=True
)

# Create 3D trade-off surface
fig_3d = analyzer.create_tradeoff_visualization(
    objectives=['strategic_value', 'technical_risk', 'resource_cost'],
    interactive=True
)
```

### Usage Examples

#### Example 1: Basic Trade-off Analysis

```python
from polytope_visualization_demo import create_logos_nimbus_status_translator
from polytope_visualizer import PolytopeVisualizer
from tradeoff_analyzer import TradeoffAnalyzer

# Setup
translator = create_logos_nimbus_status_translator()
visualizer = PolytopeVisualizer(translator)
analyzer = TradeoffAnalyzer(visualizer)

# Define objectives
objectives = {
    'strategic_value': lambda x: np.sum(x[:16]),  # Sum of strategic values
    'development_cost': lambda x: -np.sum(x[16:32]),  # Negative cost (minimize)
    'time_to_market': lambda x: -np.sum(x[32:48])  # Negative time (minimize)
}
analyzer.set_objectives(objectives)

# Generate samples and analyze
samples = analyzer.sample_polytope(n_samples=2000)
tradeoffs = analyzer.analyze_tradeoffs([
    ('strategic_value', 'development_cost'),
    ('strategic_value', 'time_to_market')
])

# Visualize results
fig = analyzer.create_tradeoff_visualization(['strategic_value', 'development_cost'])
fig.show()
```

#### Example 2: Pareto Frontier Exploration

```python
# Compute Pareto frontier
frontier = analyzer.compute_pareto_frontier(
    objectives=['strategic_value', 'development_cost'],
    resolution=150
)

# Analyze frontier properties
print(f"Frontier contains {len(frontier['points'])} optimal solutions")
print(f"Strategic value range: {frontier['objective_ranges']['strategic_value']}")
print(f"Average trade-off rate: {frontier['avg_tradeoff_rate']:.3f}")

# Find specific trade-off points
high_value_solutions = frontier['points'][frontier['objectives']['strategic_value'] > 0.8]
balanced_solutions = frontier['points'][
    (frontier['objectives']['strategic_value'] > 0.6) & 
    (frontier['objectives']['development_cost'] > -0.6)
]
```

#### Example 3: Interactive Trade-off Dashboard

```python
# Create comprehensive trade-off dashboard
dashboard = analyzer.create_tradeoff_dashboard(
    objectives=['strategic_value', 'development_cost', 'time_to_market'],
    include_pareto=True,
    include_samples=True,
    include_sensitivity=True
)

# Export dashboard
dashboard.write_html("tradeoff_analysis_dashboard.html")
```

### Interpreting Trade-off Analysis Results

#### Key Metrics

1. **Correlation Coefficient**: Measures linear relationship between objectives
   - Values near +1: Objectives align (improving one improves the other)
   - Values near -1: Objectives conflict (improving one worsens the other)
   - Values near 0: Objectives are independent

2. **Exchange Rate**: Quantifies trade-off intensity
   - High rates: Small improvements in one objective require large sacrifices in another
   - Low rates: Objectives can be improved simultaneously with minimal trade-offs

3. **Pareto Efficiency**: Percentage of feasible solutions that are Pareto optimal
   - High efficiency: Many good compromise solutions available
   - Low efficiency: Few optimal solutions, difficult trade-offs

#### Decision Support Guidelines

- **Identify Knee Points**: Look for regions where trade-off rates change dramatically
- **Explore Dominated Solutions**: Sometimes slightly suboptimal solutions offer better robustness
- **Weight Sensitivity**: Test how different objective weights affect optimal solutions
- **Constraint Impact**: Understand which constraints most limit trade-off flexibility

### Performance Considerations

- **Sampling Complexity**: O(n_samples × n_dimensions) for uniform sampling
- **Pareto Computation**: O(n_samples × n_objectives × log(n_samples)) for frontier identification
- **Visualization Rendering**: Scales with number of sample points and objectives
- **Memory Usage**: Large sample sets (>10K points) may require memory management for high-dimensional spaces

### Advanced Features

#### Custom Sampling Strategies

```python
# Latin Hypercube sampling for better space coverage
lhs_samples = analyzer.sample_polytope(method='latin_hypercube', n_samples=1000)

# Adaptive sampling focusing on Pareto regions
adaptive_samples = analyzer.adaptive_sample_pareto_regions(
    objectives=['strategic_value', 'development_cost'],
    initial_samples=500,
    refinement_iterations=3
)
```

#### Multi-Objective Optimization Integration

```python
# Integration with scipy.optimize for precise Pareto solutions
from scipy.optimize import minimize

pareto_solutions = analyzer.solve_weighted_objectives(
    weight_vectors=[[0.7, 0.3], [0.5, 0.5], [0.3, 0.7]],
    objectives=['strategic_value', 'development_cost']
)
```

## Performance Considerations

- **Vertex computation** scales exponentially with dimensions
- **Constraint generation** is linear in number of evaluations
- **Polytope sampling** complexity depends on method: O(n) for uniform, O(n log n) for structured
- **Pareto frontier computation** scales as O(n_samples × n_objectives × log(n_samples))
- **Visualization** works best with ≤ 20 dimensions for interactive use
- **Large systems** (>100 constraints) may require specialized solvers
- **Trade-off analysis** memory usage scales with sample size and number of objectives

## Limitations & Future Work

### Current Limitations
- Vertex computation limited without pypoman for high-dimensional spaces
- Visualization complexity increases with dimension count
- No automatic constraint conflict resolution

### Completed Enhancements (Phases 2-5)
- **Phase 2**: ✅ Deep Preference-based Q Network (DPbQN) Algorithm Implementation
- **Phase 3**: ✅ Human Preference Collection Interfaces (CLI/GUI)
- **Phase 4**: ✅ Integrated PPSS Framework with Human-in-the-Loop Training
- **Phase 5**: ✅ Complete End-to-End Portfolio Optimization System

## Deep Preference-based Q Network (DPbQN) System

The system now includes the complete implementation of the second part of the human-machine framework: **Preference-Based Deep Reinforcement Learning for Optimization**.

### Key Components Added

#### 1. DPbQN Algorithm (`src/dpbqn_algorithm.py`)
- Deep neural network that learns from human preferences instead of scalar rewards
- Handles high-dimensional state and action spaces for project portfolio optimization
- Integrates constraint data from qualitative evaluations
- Includes preference replay buffer and target network for stable learning

#### 2. Human Preference Interface (`src/human_preference_interface.py`)
- **CLI Interface**: Command-line preference collection
- **GUI Interface**: Graphical interface for solution comparison
- **Batch Collector**: Efficient collection of multiple preferences
- **Preference Analysis**: Pattern analysis and solution suggestions

#### 3. Integrated Framework (`src/integrated_ppss_framework.py`)
- Combines qualitative evaluation translation with DPbQN optimization
- Manages training with periodic human feedback
- Provides solution generation and analysis tools
- Includes visualization and export capabilities

### New Usage Examples

#### Quick Start with DPbQN
```python
from integrated_ppss_framework import create_sample_framework

# Create pre-configured framework
framework = create_sample_framework()

# Train with human preferences (interactive)
framework.train(episodes=100)

# Generate optimized portfolio
solution = framework.generate_optimized_portfolio()
print(f"Selected projects: {solution.selected_projects}")
```

#### Enterprise Portfolio Optimization
```python
# Run comprehensive demo
python examples/dpbqn_integration_demo.py

# Quick automated demo (no human interaction)
python examples/dpbqn_integration_demo.py --quick
```

### Features Demonstrated

✅ **Human-Machine Collaboration**: Stakeholders provide preferences to guide AI optimization  
✅ **Preference-Based Learning**: System learns without requiring exact numerical rewards  
✅ **Constraint Integration**: Qualitative evaluations become mathematical constraints  
✅ **Interactive Training**: Periodic human feedback improves solution quality  
✅ **Solution Analysis**: Trade-off analysis and visualization tools  
✅ **Scalable Architecture**: Handles enterprise-scale project portfolios  

### Testing and Validation

Comprehensive test suite available:
```bash
python tests/test_dpbqn_system.py
```

Tests cover:
- DPbQN algorithm functionality
- Preference collection interfaces  
- Integrated framework operations
- Performance benchmarks
- Edge cases and error handling

### Documentation

Complete documentation available at:
- **System Documentation**: `docs/dpbqn_system_documentation.md`
- **API Reference**: Detailed method documentation
- **Usage Examples**: Multiple real-world scenarios
- **Troubleshooting Guide**: Common issues and solutions

### Research Impact

This implementation demonstrates:
1. **Novel Algorithm**: First implementation of preference-based Q-learning for project portfolio optimization
2. **Human-AI Collaboration**: Effective integration of human expertise with machine learning
3. **Practical Application**: Ready-to-use system for enterprise project portfolio selection
4. **Theoretical Validation**: Proof-of-concept for robust human-machine optimization frameworks

## Contributing

The system is designed for extensibility:

1. **New Evaluation Types**: Add to `EvaluationType` enum and implement parser
2. **Visualization Modes**: Extend `PolytopeVisualizer` with new plot types
3. **Export Formats**: Add new formats to `export_polytope_data()`
4. **Constraint Solvers**: Integrate additional optimization libraries

## Research Context

This implementation supports the research described in:
- "Robust Human–Machine Framework for Project Portfolio Selection"
- Requirements document: `required-resources.md`
- Constraint space analysis roadmap: `constraint_space_analysis_roadmap.md`

## License

This module is part of the Logos/Nimbus/Status ecosystem research project.

---

**Status**: 
- ✅ **Phase 1 Complete** - Interactive Polytope Visualization System Operational
- ✅ **Phase 2 Complete** - Objective Trade-off Sampling and Analysis Framework

For questions or support, refer to the test files and demo scripts for usage examples.
