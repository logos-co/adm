# Deep Learning Portfolio Optimization (dl-example)

## Overview

The `dl-example/` directory is a **standalone, independent experiment** containing a comprehensive system for converting human qualitative evaluations into mathematical constraints for robust project portfolio selection.

⚠️ **This is a self-contained research system** - it has its own project data, evaluation methods, and workflows. Do not reference or mix with other examples in this repository.

## Key Features

- **🔄 Qualitative-to-Mathematical Translation**: Converts human evaluations into linear constraints
- **📊 Interactive Polytope Visualization**: 2D/3D visualization of constraint spaces
- **🎯 Multi-Criteria Support**: Handles multiple evaluation criteria simultaneously
- **👥 Stakeholder Integration**: Processes evaluations from multiple stakeholders
- **📈 Constraint Sensitivity Analysis**: Analyzes impact of individual constraints
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

### 4. Input/Output Parser
**File**: `evaluation_input_parser.py`

- Natural language processing for free-form evaluation text
- Structured data import/export (CSV, JSON formats)
- Interactive evaluation collection interface

## Installation & Setup

### Prerequisites
```bash
pip install numpy pandas plotly scipy
```

### Optional Dependencies
```bash
pip install pypoman  # For enhanced polytope operations
pip install dash     # For interactive web applications
```

## Deep Learning Workflow

```bash
# Navigate to dl-example directory
cd dl-example

# Run basic demonstration
python demo.py

# Run portfolio optimization with real project data
python portfolio_optimization_demo.py

# Generate interactive polytope visualizations
python polytope_visualization_demo.py

# Run comprehensive tests
python test_qualitative_evaluation.py
python test_polytope_visualization.py
```

## Data Files

- **logos_nimbus_status_projects.json**: Real project portfolio data from ecosystem
- **stakeholder_evaluations.json**: Expert evaluation inputs
- **budget_constraints.json**: Financial and resource limitations
- **demo_evaluations.csv**: Example evaluation datasets

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
python test_qualitative_evaluation.py
python test_polytope_visualization.py
```

The deep learning test suite validates:
- Qualitative evaluation translation accuracy
- Constraint generation and validation
- Natural language parsing functionality
- Mathematical optimization integration
- Polytope visualization accuracy

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

## Performance Considerations

- **Vertex computation** scales exponentially with dimensions
- **Constraint generation** is linear in number of evaluations
- **Visualization** works best with ≤ 20 dimensions for interactive use
- **Large systems** (>100 constraints) may require specialized solvers

## Common Tasks

### Deep Learning Portfolio Optimization
- **Qualitative evaluation translation**: Convert human expert evaluations into mathematical constraints
- **Natural language processing**: Parse free-form text evaluations using `NaturalLanguageParser`
- **Constraint generation**: Create linear optimization constraints from subjective assessments
- **Portfolio optimization**: Integrate with robust human-machine project selection frameworks

### Working with Polytope Visualizations
- **Interactive visualization**: Use `PolytopeVisualizer` for 2D/3D constraint space exploration
- **Sensitivity analysis**: Analyze impact of individual constraints on feasible regions
- **Multi-stakeholder comparison**: Compare constraint spaces from different evaluators
- **Export capabilities**: Save visualizations and constraint data in multiple formats

## Research Context

This is an independent research experiment focused on:
- Converting qualitative human evaluations into mathematical constraints
- Interactive polytope visualization of constraint spaces
- Portfolio optimization using constraint-based approaches

**Status**: ✅ Phase 1 Complete - Interactive Polytope Visualization System Operational

## System Independence

This experiment is completely self-contained with:
- Its own project data (`logos_nimbus_status_projects.json`)
- Its own evaluation methods and workflows
- Its own mathematical framework and algorithms
- No dependencies on other repository examples