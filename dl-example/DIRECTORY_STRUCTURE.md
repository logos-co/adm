# Directory Structure

This document describes the organized directory structure of the Qualitative Evaluation Translation Module project.

## Overview

```
dl-example/
├── README.md                           # Main project documentation
├── project_portfolio_index.html        # Main visualization dashboard
├── DIRECTORY_STRUCTURE.md             # This file
├── src/                                # Source code
├── tests/                              # Test files
├── examples/                           # Example scripts and demos
├── data/                               # Data files (JSON, CSV)
├── docs/                               # Documentation files
└── visualizations/                     # Generated HTML visualizations
    ├── phase1/                         # Phase 1 polytope visualizations
    ├── phase2/                         # Phase 2 trade-off analysis
    └── portfolio/                      # Project portfolio visualizations
```

## Directory Details

### `/src/` - Source Code
Core implementation files for the project:

- **`qualitative_evaluation_translator.py`** - Main translation engine
- **`polytope_visualizer.py`** - Phase 1 polytope visualization system
- **`tradeoff_analyzer.py`** - Phase 2 trade-off analysis system
- **`project_visualizer.py`** - Project portfolio visualization system
- **`evaluation_input_parser.py`** - Input parsing utilities
- **`logos_nimbus_status_projects.py`** - Project data definitions

### `/tests/` - Test Suite
Comprehensive test files for validation:

- **`test_qualitative_evaluation.py`** - Core translation tests
- **`test_polytope_visualization.py`** - Phase 1 visualization tests
- **`test_tradeoff_analysis.py`** - Phase 2 trade-off analysis tests
- **`simple_polytope_test.py`** - Basic functionality tests

### `/examples/` - Demonstrations
Example scripts and demonstrations:

- **`demo.py`** - Basic usage demonstration
- **`polytope_visualization_demo.py`** - Phase 1 demo
- **`tradeoff_analysis_demo.py`** - Phase 2 demo
- **`portfolio_optimization_demo.py`** - Portfolio optimization examples

### `/data/` - Data Files
Project data and generated datasets:

- **`logos_nimbus_status_projects.json/csv`** - Main project dataset
- **`stakeholder_evaluations.json/csv`** - Evaluation data
- **`budget_constraints.json`** - Budget constraint data
- **`polytope_data.json`** - Generated polytope data
- **`demo_evaluations.json/csv`** - Demo evaluation data
- **`simple_test_data.json`** - Test data

### `/docs/` - Documentation
Comprehensive project documentation:

- **`API_DOCUMENTATION.md`** - Complete API reference
- **`IMPLEMENTATION_SUMMARY.md`** - Implementation overview
- **`constraint_space_analysis_roadmap.md`** - Analysis roadmap
- **`chen-summary.md`** - Research summary
- **`required-resources.md`** - Resource requirements

### `/visualizations/` - Generated Visualizations
Interactive HTML visualizations organized by phase:

#### `/visualizations/phase1/` - Phase 1 Polytope Visualizations
- **`polytope_2d_sample.html`** - 2D polytope visualization
- **`polytope_dashboard.html`** - Interactive polytope dashboard
- **`simple_test_2d.html`** - Simple 2D test visualization
- **`simple_test_dashboard.html`** - Simple test dashboard

#### `/visualizations/phase2/` - Phase 2 Trade-off Analysis
- **`phase2_demo_tradeoff_2d.html`** - 2D trade-off demonstration
- **`phase2_demo_tradeoff_3d.html`** - 3D trade-off demonstration
- **`test_tradeoff_2d.html`** - 2D trade-off test visualization
- **`test_tradeoff_3d.html`** - 3D trade-off test visualization
- **`test_tradeoff_dashboard.html`** - Trade-off analysis dashboard

#### `/visualizations/portfolio/` - Project Portfolio Visualizations
- **`project_portfolio_ecosystem_overview.html`** - Ecosystem analysis
- **`project_portfolio_project_timeline.html`** - Project timeline
- **`project_portfolio_project_relationships.html`** - Relationship network
- **`project_portfolio_metrics_radar.html`** - Metrics comparison
- **`project_portfolio_project_table.html`** - Detailed project table
- **`project_portfolio_budget_analysis.html`** - Budget analysis
- **`project_portfolio_comprehensive_dashboard.html`** - Complete dashboard

## Quick Start

1. **View Main Dashboard**: Open `project_portfolio_index.html` in a web browser
2. **Run Examples**: Execute scripts in `/examples/` directory
3. **Run Tests**: Execute test files in `/tests/` directory
4. **Explore Visualizations**: Browse HTML files in `/visualizations/` subdirectories

## File Organization Principles

- **Source code** (`/src/`) contains only implementation files
- **Tests** (`/tests/`) are separated from source code
- **Examples** (`/examples/`) provide usage demonstrations
- **Data** (`/data/`) contains all JSON/CSV files
- **Documentation** (`/docs/`) centralizes all markdown documentation
- **Visualizations** (`/visualizations/`) are organized by project phase

## Import Paths

When importing modules from different directories, use relative imports:

```python
# From examples/ or tests/
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from qualitative_evaluation_translator import QualitativeEvaluationTranslator
from polytope_visualizer import PolytopeVisualizer
from tradeoff_analyzer import TradeoffAnalyzer
```

## Development Workflow

1. **Source code changes**: Edit files in `/src/`
2. **Add tests**: Create corresponding tests in `/tests/`
3. **Create examples**: Add demonstrations in `/examples/`
4. **Update documentation**: Modify files in `/docs/`
5. **Generate visualizations**: Run visualization scripts to update `/visualizations/`

This organized structure makes the project more maintainable, easier to navigate, and follows standard software development practices.
