# API Documentation - Qualitative Evaluation Translation Module

This document provides comprehensive API documentation for the Qualitative Evaluation Translation Module and Polytope Visualization System.

## Table of Contents

1. [Core Classes](#core-classes)
2. [Data Structures](#data-structures)
3. [Enumerations](#enumerations)
4. [Main APIs](#main-apis)
5. [Visualization APIs](#visualization-apis)
6. [Utility Functions](#utility-functions)
7. [Examples](#examples)
8. [Error Handling](#error-handling)

## Core Classes

### QualitativeEvaluationTranslator

Main class for translating qualitative evaluations into mathematical constraints.

#### Constructor

```python
QualitativeEvaluationTranslator(projects: List[str], criteria: List[str] = None)
```

**Parameters:**
- `projects` (List[str]): List of project identifiers
- `criteria` (List[str], optional): List of evaluation criteria. Defaults to `['value']`

**Attributes:**
- `projects`: List of project names
- `criteria`: List of evaluation criteria
- `n_projects`: Number of projects
- `n_criteria`: Number of criteria
- `evaluations`: List of stored evaluations
- `constraints`: List of generated linear constraints

#### Methods

##### add_evaluation()
```python
add_evaluation(evaluation: QualitativeEvaluation) -> None
```
Add a qualitative evaluation to the system.

**Parameters:**
- `evaluation`: QualitativeEvaluation instance

##### translate_evaluations()
```python
translate_evaluations() -> List[LinearConstraint]
```
Convert all stored evaluations into linear constraints.

**Returns:**
- List of LinearConstraint objects

##### get_constraint_matrices()
```python
get_constraint_matrices() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
```
Get constraint matrices in standard optimization form.

**Returns:**
- `A_ineq`: Inequality constraint matrix (A_ineq * x ≤ b_ineq)
- `b_ineq`: Inequality constraint bounds
- `A_eq`: Equality constraint matrix (A_eq * x = b_eq)
- `b_eq`: Equality constraint bounds

##### validate_constraints()
```python
validate_constraints() -> Dict[str, Any]
```
Validate constraint system for consistency and feasibility.

**Returns:**
- Dictionary with validation results including:
  - `n_inequality_constraints`: Number of inequality constraints
  - `n_equality_constraints`: Number of equality constraints
  - `total_constraints`: Total number of constraints
  - `n_variables`: Number of variables
  - `is_overconstrained`: Boolean indicating if system is overconstrained
  - `warnings`: List of warning messages

##### export_constraints()
```python
export_constraints(format: str = 'dict') -> Union[Dict, pd.DataFrame]
```
Export constraints in various formats.

**Parameters:**
- `format`: Export format ('dict', 'dataframe', or 'matrices')

**Returns:**
- Constraints in specified format

### PolytopeVisualizer

Interactive visualization class for constraint polytopes.

#### Constructor

```python
PolytopeVisualizer(translator: QualitativeEvaluationTranslator)
```

**Parameters:**
- `translator`: QualitativeEvaluationTranslator instance with constraints

**Attributes:**
- `translator`: Reference to translator
- `constraints`: List of linear constraints
- `A_ineq`, `b_ineq`, `A_eq`, `b_eq`: Constraint matrices
- `dimension_names`: Names of all dimensions
- `n_dimensions`: Total number of dimensions

#### Methods

##### compute_vertices()
```python
compute_vertices(bounds: Optional[List[Tuple[float, float]]] = None) -> np.ndarray
```
Compute vertices of the constraint polytope.

**Parameters:**
- `bounds`: Optional bounds for each dimension as (min, max) tuples

**Returns:**
- Array of polytope vertices, shape (n_vertices, n_dimensions)

##### compute_polytope_properties()
```python
compute_polytope_properties() -> Dict[str, Any]
```
Compute various properties of the polytope.

**Returns:**
- Dictionary containing:
  - `n_vertices`: Number of vertices
  - `n_constraints`: Number of constraints
  - `n_dimensions`: Number of dimensions
  - `dimension_names`: List of dimension names
  - `centroid`: Centroid coordinates (if vertices exist)
  - `bounding_box`: Min/max bounds (if vertices exist)
  - `volume`: Polytope volume (for low dimensions)
  - `surface_area`: Surface area (for low dimensions)

##### create_2d_visualization()
```python
create_2d_visualization(
    dim_x: int = 0, 
    dim_y: int = 1,
    show_vertices: bool = True,
    show_constraints: bool = True,
    show_feasible_region: bool = True,
    resolution: int = 100
) -> go.Figure
```
Create 2D visualization of the polytope.

**Parameters:**
- `dim_x`: Index of dimension for x-axis
- `dim_y`: Index of dimension for y-axis
- `show_vertices`: Whether to show polytope vertices
- `show_constraints`: Whether to show constraint boundaries
- `show_feasible_region`: Whether to shade feasible region
- `resolution`: Resolution for constraint boundary plotting

**Returns:**
- Plotly Figure object

##### create_3d_visualization()
```python
create_3d_visualization(
    dim_x: int = 0,
    dim_y: int = 1, 
    dim_z: int = 2,
    show_vertices: bool = True,
    show_wireframe: bool = True,
    opacity: float = 0.3
) -> go.Figure
```
Create 3D visualization of the polytope.

**Parameters:**
- `dim_x`: Index of dimension for x-axis
- `dim_y`: Index of dimension for y-axis
- `dim_z`: Index of dimension for z-axis
- `show_vertices`: Whether to show polytope vertices
- `show_wireframe`: Whether to show polytope edges
- `opacity`: Opacity of polytope surface

**Returns:**
- Plotly Figure object

##### create_dimension_selector_dashboard()
```python
create_dimension_selector_dashboard() -> go.Figure
```
Create interactive dashboard with dimension selectors.

**Returns:**
- Plotly Figure with subplots for different projections

##### export_polytope_data()
```python
export_polytope_data(filename: str, format: str = 'json') -> None
```
Export polytope data to file.

**Parameters:**
- `filename`: Output filename
- `format`: Export format ('json', 'csv', 'npz')

## Data Structures

### QualitativeEvaluation

Dataclass representing a single qualitative evaluation.

```python
@dataclass
class QualitativeEvaluation:
    evaluator_id: str
    evaluation_type: EvaluationType
    projects: List[str]
    operator: Optional[ComparisonOperator] = None
    values: Optional[List[float]] = None
    confidence: float = 1.0
    criteria: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Optional[Dict] = None
```

**Fields:**
- `evaluator_id`: Unique identifier for the evaluator
- `evaluation_type`: Type of evaluation (see EvaluationType)
- `projects`: List of projects involved in evaluation
- `operator`: Comparison operator (for comparison/threshold evaluations)
- `values`: Numeric values (for range/threshold evaluations)
- `confidence`: Confidence level (0.0 to 1.0)
- `criteria`: Evaluation criterion name
- `timestamp`: Timestamp of evaluation
- `metadata`: Additional metadata dictionary

### LinearConstraint

Dataclass representing a linear constraint.

```python
@dataclass
class LinearConstraint:
    coefficients: np.ndarray
    bound: float
    is_equality: bool = False
    constraint_id: str = ""
    source_evaluation: Optional[QualitativeEvaluation] = None
```

**Fields:**
- `coefficients`: Coefficient vector 'a' in constraint a^T * x ≤ b
- `bound`: Bound value 'b'
- `is_equality`: True for equality constraints, False for inequality
- `constraint_id`: Unique identifier for the constraint
- `source_evaluation`: Reference to source evaluation

## Enumerations

### EvaluationType

```python
class EvaluationType(Enum):
    COMPARISON = "comparison"  # Project A > Project B
    RANGE = "range"           # Project value between X and Y
    RANKING = "ranking"       # Ordered list of projects
    PREFERENCE = "preference" # Preference weights
    THRESHOLD = "threshold"   # Minimum/maximum constraints
```

### ComparisonOperator

```python
class ComparisonOperator(Enum):
    GREATER = ">"
    LESS = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    EQUAL = "="
    NOT_EQUAL = "!="
```

## Main APIs

### Basic Usage Pattern

```python
# 1. Create translator
translator = QualitativeEvaluationTranslator(
    projects=["Project A", "Project B", "Project C"],
    criteria=["Strategic Value", "Technical Feasibility"]
)

# 2. Add evaluations
evaluation = QualitativeEvaluation(
    evaluator_id="expert_1",
    evaluation_type=EvaluationType.COMPARISON,
    projects=["Project A", "Project B"],
    operator=ComparisonOperator.GREATER,
    criteria="Strategic Value"
)
translator.add_evaluation(evaluation)

# 3. Generate constraints
constraints = translator.translate_evaluations()

# 4. Get constraint matrices
A_ineq, b_ineq, A_eq, b_eq = translator.get_constraint_matrices()

# 5. Create visualizer
visualizer = PolytopeVisualizer(translator)

# 6. Generate visualizations
fig_2d = visualizer.create_2d_visualization()
fig_3d = visualizer.create_3d_visualization()
```

### Evaluation Type Examples

#### Comparison Evaluation
```python
comparison = QualitativeEvaluation(
    evaluator_id="expert_1",
    evaluation_type=EvaluationType.COMPARISON,
    projects=["Project A", "Project B"],
    operator=ComparisonOperator.GREATER,
    criteria="Strategic Value"
)
```

#### Range Evaluation
```python
range_eval = QualitativeEvaluation(
    evaluator_id="expert_2",
    evaluation_type=EvaluationType.RANGE,
    projects=["Project A"],
    values=[0.3, 0.7],  # min, max
    criteria="Technical Feasibility"
)
```

#### Ranking Evaluation
```python
ranking = QualitativeEvaluation(
    evaluator_id="expert_3",
    evaluation_type=EvaluationType.RANKING,
    projects=["Project A", "Project B", "Project C"],  # Ordered by preference
    criteria="Market Impact"
)
```

#### Threshold Evaluation
```python
threshold = QualitativeEvaluation(
    evaluator_id="expert_4",
    evaluation_type=EvaluationType.THRESHOLD,
    projects=["Project A"],
    operator=ComparisonOperator.GREATER_EQUAL,
    values=[0.5],  # threshold value
    criteria="Strategic Value"
)
```

## Visualization APIs

### 2D Visualization Options

```python
# Basic 2D plot
fig = visualizer.create_2d_visualization(
    dim_x=0,  # First dimension
    dim_y=1,  # Second dimension
    show_vertices=True,
    show_constraints=True,
    show_feasible_region=True
)

# Save to file
fig.write_html("polytope_2d.html")
fig.show()  # Display in browser
```

### 3D Visualization Options

```python
# Basic 3D plot
fig = visualizer.create_3d_visualization(
    dim_x=0,  # X dimension
    dim_y=1,  # Y dimension
    dim_z=2,  # Z dimension
    show_vertices=True,
    opacity=0.3
)

# Save to file
fig.write_html("polytope_3d.html")
```

### Dashboard Creation

```python
# Create comprehensive dashboard
dashboard = visualizer.create_dimension_selector_dashboard()
dashboard.write_html("polytope_dashboard.html")
```

## Utility Functions

### Data Export

```python
# Export polytope data
visualizer.export_polytope_data("polytope.json", format="json")
visualizer.export_polytope_data("vertices.csv", format="csv")
visualizer.export_polytope_data("polytope.npz", format="npz")

# Export constraints
constraint_dict = translator.export_constraints("dict")
constraint_df = translator.export_constraints("dataframe")
A_ineq, b_ineq, A_eq, b_eq = translator.export_constraints("matrices")
```

### Validation

```python
# Validate constraint system
validation = translator.validate_constraints()
print(f"Total constraints: {validation['total_constraints']}")
print(f"Variables: {validation['n_variables']}")
print(f"Warnings: {validation['warnings']}")
```

### Properties Computation

```python
# Get polytope properties
properties = visualizer.compute_polytope_properties()
print(f"Vertices: {properties['n_vertices']}")
print(f"Volume: {properties.get('volume', 'N/A')}")
print(f"Centroid: {properties.get('centroid', 'N/A')}")
```

## Examples

### Complete Workflow Example

```python
from qualitative_evaluation_translator import *
from polytope_visualizer import PolytopeVisualizer

# Define projects and criteria
projects = ["Logos Core", "Nimbus Client", "Status App"]
criteria = ["Strategic Value", "Technical Feasibility", "Market Impact"]

# Create translator
translator = QualitativeEvaluationTranslator(projects, criteria)

# Add multiple evaluations
evaluations = [
    QualitativeEvaluation(
        evaluator_id="ceo",
        evaluation_type=EvaluationType.RANKING,
        projects=["Logos Core", "Status App", "Nimbus Client"],
        criteria="Strategic Value"
    ),
    QualitativeEvaluation(
        evaluator_id="cto",
        evaluation_type=EvaluationType.RANGE,
        projects=["Nimbus Client"],
        values=[0.8, 1.0],
        criteria="Technical Feasibility"
    ),
    QualitativeEvaluation(
        evaluator_id="pm",
        evaluation_type=EvaluationType.THRESHOLD,
        projects=["Status App"],
        operator=ComparisonOperator.GREATER_EQUAL,
        values=[0.6],
        criteria="Market Impact"
    )
]

for eval in evaluations:
    translator.add_evaluation(eval)

# Generate constraints and validate
constraints = translator.translate_evaluations()
validation = translator.validate_constraints()

# Create visualizations
visualizer = PolytopeVisualizer(translator)
properties = visualizer.compute_polytope_properties()

# Generate 2D and 3D plots
fig_2d = visualizer.create_2d_visualization(0, 1)
fig_3d = visualizer.create_3d_visualization(0, 1, 2)
dashboard = visualizer.create_dimension_selector_dashboard()

# Save results
fig_2d.write_html("strategic_vs_technical.html")
fig_3d.write_html("3d_polytope.html")
dashboard.write_html("dashboard.html")
visualizer.export_polytope_data("polytope_data.json")
```

### Real Project Data Example

```python
from polytope_visualization_demo import create_logos_nimbus_status_translator

# Load real project data
translator = create_logos_nimbus_status_translator()
print(f"Loaded {len(translator.projects)} projects with {len(translator.evaluations)} evaluations")

# Create visualizer
visualizer = PolytopeVisualizer(translator)
properties = visualizer.compute_polytope_properties()

print(f"Generated polytope with {properties['n_constraints']} constraints")
print(f"Polytope has {properties['n_vertices']} vertices in {properties['n_dimensions']} dimensions")

# Create comprehensive dashboard
dashboard = visualizer.create_dimension_selector_dashboard()
dashboard.write_html("logos_nimbus_status_dashboard.html")
```

## Error Handling

### Common Exceptions

#### ValueError
- Raised for invalid evaluation parameters
- Raised for unsupported export formats
- Raised for invalid constraint specifications

```python
try:
    evaluation = QualitativeEvaluation(
        evaluator_id="expert",
        evaluation_type=EvaluationType.COMPARISON,
        projects=["Project A"],  # Error: comparison needs 2 projects
        operator=ComparisonOperator.GREATER,
        criteria="Value"
    )
    translator.add_evaluation(evaluation)
except ValueError as e:
    print(f"Invalid evaluation: {e}")
```

#### LinAlgError
- Raised during vertex computation for singular matrices
- Handled internally with fallback methods

#### ImportError
- Raised when optional dependencies are missing
- Gracefully handled with warnings

```python
# Check for optional dependencies
try:
    import pypoman
    print("pypoman available for enhanced polytope operations")
except ImportError:
    print("pypoman not available - using fallback methods")
```

### Best Practices

1. **Always validate constraints** after adding evaluations:
```python
validation = translator.validate_constraints()
if validation['warnings']:
    print("Warnings:", validation['warnings'])
```

2. **Handle empty polytopes** gracefully:
```python
vertices = visualizer.compute_vertices()
if len(vertices) == 0:
    print("No feasible region found - constraints may be contradictory")
```

3. **Use appropriate bounds** for vertex computation:
```python
# Set reasonable bounds for your problem domain
bounds = [(0, 1) for _ in range(visualizer.n_dimensions)]
vertices = visualizer.compute_vertices(bounds=bounds)
```

4. **Check dimension limits** for visualization:
```python
if visualizer.n_dimensions > 20:
    print("Warning: High-dimensional polytope may be slow to visualize")
```

---

**Version**: 1.0.0  
**Last Updated**: September 2025  
**Status**: Phase 1 Complete - Core API Stable

For additional examples and advanced usage, see the demo scripts and test files in the repository.
