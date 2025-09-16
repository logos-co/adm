# Interactive Data Visualizations (toy-example)

## Overview

The `toy-example/` directory is a **standalone, independent experiment** containing a complete D3.js visualization system for portfolio management and strategic decision-making.

⚠️ **This is a self-contained system** - it has its own data, workflows, and documentation. Do not reference or mix with other examples in this repository.

## Development Workflow

### Data Processing
```bash
# Navigate to example directory
cd toy-example

# Process raw CSV data into visualization-ready JSON format
python data_preparation.py

# Run data validation tests
python test_visualizations.py
```

### Development Server
```bash
# Start local HTTP server for development (from toy-example directory)
python -m http.server 8000

# Access visualizations at:
# http://localhost:8000/portfolio_visualizations.html
```

### Testing
```bash
# Run comprehensive test suite
cd toy-example
python test_visualizations.py
```

The test suite validates:
- Data file integrity (CSV and JSON)
- Visualization file presence
- Data relationship consistency
- Decision tree structure
- Server accessibility

## Architecture

### Data Pipeline
1. **Raw Data**: CSV files in `toy-example/toy-data/` directory with normalized schema
2. **ETL Process**: `data_preparation.py` loads, cleans, and transforms data
3. **Output**: JSON files in `visualization_data/` optimized for D3.js consumption

### Visualization Framework
- **HTML Container**: `portfolio_visualizations.html` with responsive layout
- **JavaScript Modules**: Separate files in `js/` directory for each visualization type
- **D3.js Framework**: Interactive SVG-based visualizations with force simulations, matrices, and dashboards

### Core Visualizations
1. **Dependency Network** (`js/dependency-graph.js`) - Force-directed graph of project relationships
2. **Resource Heatmap** (`js/resource-matrix.js`) - Matrix visualization of resource allocation
3. **Strategic Matrix** (`js/strategic-matrix.js`) - Risk vs. impact bubble chart positioning
4. **Timeline Gantt** (`js/timeline-gantt.js`) - Project schedules with dependency arrows
5. **Portfolio Dashboard** (`js/portfolio-dashboard.js`) - Multi-panel KPI overview
6. **Decision Tree** (`js/decision-tree.js`) - Interactive investment decision support tool

### Supporting Tools
7. **Export Utils** (`js/export-utils.js`) - Export visualizations as PNG/SVG images
8. **Filter Controls** (`js/filter-controls.js`) - Cross-visualization filtering and data exploration
9. **Scenario Comparison** (`js/scenario-comparison.js`) - Create and compare portfolio scenarios

## Data Schema

The system uses a normalized relational schema across CSV files:

- **projects.csv**: Core project information (IDs, budgets, timelines, status)
- **dependencies.csv**: Project interdependencies with strength and impact metrics
- **resources.csv**: Available resources (teams, budget, facilities)
- **resource_allocations.csv**: Resource assignments to projects
- **strategic_dimensions.csv**: Multi-dimensional strategic scoring
- **timeline_events.csv**: Project milestones and events
- **portfolio_metrics.csv**: Aggregated portfolio-level KPIs

## Key Technical Patterns

### Data Processing Pipeline
- Pandas for CSV loading with proper date parsing
- Foreign key joins between related datasets
- Derived metric calculation (strategic scores, utilization rates)
- JSON serialization with datetime string conversion

### D3.js Visualization Patterns
- Modular design with separate files for each chart type
- Data binding and enter/update/exit patterns
- Force simulations for network layouts
- Interactive tooltips and filtering
- Responsive SVG containers

### Decision Tree Structure
- Hierarchical JSON structure with decision and outcome nodes
- Real project data mapped to decision paths
- Color-coded recommendations based on strategic criteria
- Interactive exploration of investment decision logic

## Common Tasks

### Adding New Data
1. Update CSV files in `toy-example/toy-data/` following existing schema
2. Run `python data_preparation.py` to regenerate JSON files
3. Test with `python test_visualizations.py`

### Creating New Visualizations
1. Create new JavaScript module in `js/` directory
2. Follow D3.js patterns from existing modules
3. Add container div to `portfolio_visualizations.html`
4. Update data preparation script if new data formats needed

### Modifying Existing Visualizations
- Update JavaScript files in `js/` directory
- Modify color scales, layouts, or interactions
- Test changes with local HTTP server

### Working with Supporting Tools
- **Export functionality**: Use `ExportUtils` class to add export buttons to new visualizations
- **Filtering**: Leverage `FilterControls` to add cross-visualization filtering capabilities
- **Scenario analysis**: Integrate `ScenarioComparison` for portfolio modeling and comparison features