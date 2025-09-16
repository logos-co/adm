# Portfolio Strategic Visualizations

This project demonstrates interactive portfolio management visualizations using D3.js, built from toy data representing a project portfolio with dependencies, resource allocations, and strategic dimensions.

## Overview

The project creates six comprehensive visualizations to help stakeholders understand portfolio dynamics and make strategic decisions:

1. **Project Dependency Network** - Interactive force-directed graph showing project relationships
2. **Resource Allocation Heatmap** - Matrix visualization of resource distribution across projects  
3. **Strategic Impact vs Risk Matrix** - Bubble chart positioning projects by strategic value and risk
4. **Project Timeline & Dependencies** - Gantt chart with completion progress and dependency arrows
5. **Portfolio Management Dashboard** - Multi-panel KPI dashboard with comprehensive metrics
6. **Portfolio Investment Decision Tree** - Interactive decision support tool for investment decisions

## Project Structure

```
toy-example/
├── README.md                     # This file
├── core-data-flat.md            # Data schema documentation
├── visualization-options.md      # Visualization design patterns
├── data_preparation.py          # Python script for data processing
├── portfolio_visualizations.html # Main visualization dashboard
├── js/                          # JavaScript modules
│   ├── dependency-graph.js      # Dependency network implementation
│   ├── resource-matrix.js       # Resource heatmap implementation
│   ├── strategic-matrix.js      # Strategic positioning implementation
│   ├── timeline-gantt.js        # Timeline Gantt chart implementation
│   ├── portfolio-dashboard.js   # Portfolio dashboard implementation
│   └── decision-tree.js         # Decision tree implementation
└── visualization_data/          # Generated JSON data files
    ├── dependency_network.json  # Network nodes and links
    ├── resource_matrix.json     # Resource allocation matrix
    ├── strategic_positioning.json # Strategic scores and metrics
    ├── decision_tree.json       # Decision tree structure and data
    └── [additional processed files]
```

## Data Sources

The visualizations are built from CSV files in the `toy-data/` directory:

- **projects.csv** - Core project information (budget, status, timeline)
- **dependencies.csv** - Project interdependencies and relationships
- **resources.csv** - Available resources (teams, budget, facilities)
- **resource_allocations.csv** - Resource assignments to projects
- **strategic_dimensions.csv** - Strategic scoring across multiple dimensions
- **timeline_events.csv** - Project milestones and events
- **portfolio_metrics.csv** - Aggregated portfolio-level metrics
- **dependency_impacts.csv** - Impact analysis of dependency failures
- **time_series_snapshots.csv** - Historical project performance data

## Getting Started

### Prerequisites

- Python 3.7+ with pandas, numpy
- Modern web browser with JavaScript enabled
- HTTP server for local development

### Setup and Execution

1. **Prepare the data:**
   ```bash
   cd toy-example
   python data_preparation.py
   ```
   This script:
   - Loads and cleans all CSV data files
   - Combines related datasets using project IDs
   - Calculates derived metrics (strategic scores, budget utilization)
   - Exports optimized JSON files for D3.js visualizations

2. **Launch the visualizations:**
   ```bash
   # Start a local HTTP server (from toy-example directory)
   python -m http.server 8000
   
   # Open in browser
   http://localhost:8000/portfolio_visualizations.html
   ```

## Visualization Features

### 1. Project Dependency Network

**Purpose:** Understand project interdependencies and identify critical paths

**Features:**
- **Nodes:** Projects sized by budget allocation, colored by status
- **Edges:** Dependencies colored by type (resource/technical/timeline), thickness by strength
- **Interactivity:** 
  - Drag nodes to explore relationships
  - Hover for detailed project information
  - Filter by dependency type
- **Legend:** Project status and dependency type indicators

**Strategic Insights:**
- Identify bottleneck projects with many incoming dependencies
- Spot resource conflicts between connected projects
- Assess cascade risks from project delays or failures

### 2. Resource Allocation Heatmap

**Purpose:** Visualize resource distribution and identify allocation conflicts

**Features:**
- **Matrix Layout:** Projects (rows) vs Resources (columns)
- **Color Intensity:** Represents allocation amount
- **Interactivity:** Hover for allocation details
- **Axis Labels:** Truncated names for readability

**Strategic Insights:**
- Identify over-allocated resources
- Spot projects competing for the same resources
- Balance resource distribution across portfolio

### 3. Strategic Impact vs Risk Matrix

**Purpose:** Position projects in strategic space for portfolio optimization

**Features:**
- **Bubble Chart:** X-axis (Strategic Score), Y-axis (Risk Score)
- **Bubble Size:** Represents budget allocation
- **Color Coding:** Project status (Active/Planning/Complete)
- **Interactivity:** 
  - Hover for comprehensive project details
  - Filter by project status
- **Quadrant Analysis:** High/Low strategic value vs High/Low risk

**Strategic Insights:**
- Prioritize high-value, low-risk projects
- Identify projects requiring risk mitigation
- Balance portfolio across strategic dimensions

### 4. Project Timeline & Dependencies

**Purpose:** Visualize project schedules and temporal relationships

**Features:**
- **Gantt Bars:** Project timelines with start/end dates
- **Completion Progress:** Green overlay bars showing completion percentage
- **Dependency Arrows:** Visual connections between dependent projects
- **Time Scale:** Horizontal axis with month/year labels
- **Status Colors:** Projects colored by current status
- **Interactivity:** Hover for timeline details and project information

**Strategic Insights:**
- Identify scheduling conflicts and bottlenecks
- Track project progress against planned timelines
- Visualize critical path dependencies
- Plan resource allocation over time

### 5. Portfolio Management Dashboard

**Purpose:** Comprehensive overview of portfolio health and performance

**Features:**
- **KPI Cards:** Total projects, active projects, total budget
- **Budget Distribution:** Pie chart showing budget allocation by project
- **Risk Analysis:** Bar chart displaying risk levels across projects
- **Completion Tracking:** Progress bars for each project
- **Resource Utilization:** Line chart showing utilization trends over time
- **Timeline Overview:** Condensed view of project schedules

**Strategic Insights:**
- Monitor overall portfolio health at a glance
- Track budget utilization and distribution
- Identify projects at risk or behind schedule
- Analyze resource utilization patterns
- Make data-driven portfolio decisions

### 6. Portfolio Investment Decision Tree

**Purpose:** Structured decision support for portfolio investment choices

**Features:**
- **Decision Nodes:** Blue rectangles with strategic questions/criteria
- **Outcome Nodes:** Color-coded rectangles with investment recommendations
- **Interactive Tree:** Click outcome nodes to view detailed project information
- **Project Mapping:** Real portfolio projects categorized by decision paths
- **Recommendation Colors:**
  - Green: "Strongly Recommend" - High value, low risk
  - Light Green: "Recommend" - Good returns, manageable risk
  - Orange: "Proceed with Caution" - High value but significant investment
  - Dark Orange: "Evaluate Alternatives" - Good ROI but elevated risk
  - Red: "Do Not Recommend" - Poor strategic/financial returns

**Decision Criteria:**
- **Strategic Priority:** Critical/High vs Medium/Low priority assessment
- **Risk Assessment:** Risk score thresholds (≤5 for high priority, ≤4 for medium/low)
- **ROI Analysis:** Projected return thresholds (≥1.5 for attractive returns)
- **Budget Impact:** Investment size thresholds ($300K for significant investment)
- **Strategic Score:** Strategic value validation (≥8.0 for high strategic value)

**Strategic Insights:**
- Standardize investment decision processes
- Ensure consistent evaluation criteria across portfolio
- Identify optimal investment opportunities
- Balance risk and return considerations
- Support data-driven investment decisions

## Technical Implementation

### Data Processing Pipeline

The `data_preparation.py` script implements a robust ETL pipeline:

1. **Data Loading:** Reads CSV files with proper date parsing
2. **Data Integration:** Joins related tables using foreign keys
3. **Metric Calculation:** Derives strategic scores and utilization rates
4. **Data Validation:** Filters invalid dependencies and handles missing values
5. **Export Optimization:** Creates visualization-specific JSON datasets

### Visualization Architecture

- **Modular Design:** Separate JavaScript files for each visualization
- **D3.js Framework:** Leverages data binding and SVG rendering
- **Responsive Layout:** Adapts to different screen sizes
- **Interactive Elements:** Tooltips, filters, and dynamic updates
- **Force Simulation:** Physics-based layout for dependency network

### Key Technical Features

- **Data Integrity:** Validates project relationships before visualization
- **Performance:** Optimized JSON structure for fast loading
- **Scalability:** Modular code supports additional visualizations
- **Cross-browser:** Compatible with modern web browsers
- **Accessibility:** Proper color contrast and keyboard navigation

## Customization and Extension

### Adding New Visualizations

1. Create new JavaScript module in `js/` directory
2. Follow existing patterns for data loading and D3.js setup
3. Add visualization container to `portfolio_visualizations.html`
4. Update data preparation script if new data formats needed

### Modifying Existing Visualizations

- **Colors:** Update color scales in JavaScript files
- **Layout:** Adjust dimensions and margins in visualization functions
- **Interactions:** Modify event handlers for different behaviors
- **Filters:** Add new filter controls and update functions

### Data Schema Changes

1. Update CSV files in `toy-data/` directory
2. Modify `data_preparation.py` to handle new fields
3. Update visualization code to use new data attributes
4. Test data pipeline and visualizations

## Performance Considerations

- **Data Size:** Current implementation optimized for 10-100 projects
- **Browser Memory:** Large datasets may require data pagination
- **Rendering Speed:** Force simulation performance depends on node/link count
- **Network Loading:** JSON files cached by browser for repeat visits

## Testing and Validation

### Test Suite

The project includes a comprehensive test suite (`test_visualizations.py`) that validates:

- **Data File Integrity:** Checks all CSV and JSON files exist and are valid
- **Visualization Files:** Validates all JavaScript modules are present and functional
- **Data Relationships:** Tests referential integrity between related data tables
- **Decision Tree Structure:** Validates the decision tree data structure and logic
- **Server Accessibility:** Tests HTTP server functionality and file accessibility

**Running Tests:**
```bash
cd toy-example
python test_visualizations.py
```

**Expected Output:**
- All data files should be accessible and valid
- All 6 JavaScript visualization files should be present
- Data integrity checks should pass (no orphaned references)
- Decision tree should contain 13 nodes with valid structure
- HTTP server should be accessible on localhost:8000

### Validation Results

Current test results show:
- ✓ 9 CSV data files with complete data (4 projects, 3 dependencies, 4 resources)
- ✓ 4 JSON visualization data files with valid structure
- ✓ 6 JavaScript visualization modules with D3.js implementations
- ✓ Complete data integrity with no orphaned references
- ✓ Valid decision tree with 13 nodes and proper structure
- ✓ HTTP server accessibility for all required files

## Advanced Features

### Export Functionality

The portfolio suite includes comprehensive export capabilities:

- **Individual Visualization Export:** Each visualization has an export button (📥) in the top-right corner
- **Bulk Export:** "Export All Visualizations" button exports all charts as PNG files
- **High-Quality Output:** Exports include white backgrounds and proper sizing for presentations
- **Staggered Downloads:** Multiple exports are automatically staggered to prevent browser issues

**Usage:**
- Click individual export buttons on each visualization
- Use the global "Export All Visualizations" button for complete portfolio export
- Files are automatically downloaded with descriptive names

### Advanced Portfolio Filtering

Cross-visualization filtering system allows dynamic exploration of portfolio data:

**Filter Controls:**
- **Project Status:** Filter by Active, Planning, Complete, or On Hold
- **Strategic Priority:** Filter by Critical, High, Medium, or Low priority
- **Risk Level:** Filter by Low (1-3), Medium (4-6), or High (7-10) risk scores
- **Budget Range:** Dual-slider for minimum and maximum budget allocation
- **Completion Range:** Filter by project completion percentage

**Features:**
- **Real-time Updates:** Filters apply instantly across all visualizations
- **Cross-Visualization Sync:** Changes affect dependency network, strategic matrix, and other charts
- **Filter Summary:** Active filters are clearly displayed with current criteria
- **Reset Functionality:** One-click reset to clear all filters

**Usage:**
1. Use the Portfolio Filters panel on the left side of the screen
2. Adjust any combination of filters using dropdowns and sliders
3. Click "Apply Filters" to update all visualizations
4. Use "Reset" to clear all filters and return to full portfolio view

### Scenario Planning & Comparison

Interactive scenario planning tool for strategic portfolio analysis:

**Scenario Configuration:**
- **Current Portfolio:** Baseline scenario with actual portfolio metrics
- **Scenario 1 & 2:** Customizable alternative scenarios
- **Budget Adjustments:** Apply percentage changes (+/-20%, +50%, no change)
- **Project Selection:** Include/exclude specific projects from scenarios
- **Custom Naming:** Rename scenarios for clarity (e.g., "High Growth Strategy", "Risk Mitigation Focus")

**Scenario Metrics:**
- Total project count and budget allocation
- Average risk and strategic scores
- Average completion percentage
- Projected ROI calculations

**Comparison Features:**
- **Side-by-side Metrics:** Compare key indicators across all scenarios
- **Recommendation Engine:** Automated analysis highlighting scenario advantages
- **Interactive Comparison Modal:** Detailed comparison table with strategic insights
- **What-if Analysis:** Test different portfolio compositions and budget allocations

**Usage:**
1. Use the Scenario Planning panel on the right side of the screen
2. Switch between Current, Scenario 1, and Scenario 2 tabs
3. Configure scenario parameters (budget, project selection)
4. Click "Calculate Scenario" to generate metrics
5. Use "Compare All Scenarios" for comprehensive analysis

### Integration Features

**Cross-Feature Integration:**
- **Filter + Export:** Export filtered views of visualizations
- **Scenario + Filter:** Apply filters within scenario planning
- **Real-time Sync:** All features work together seamlessly

**Performance Optimizations:**
- **Efficient Rendering:** Smooth transitions and updates
- **Memory Management:** Optimized for large portfolios
- **Browser Compatibility:** Works across modern browsers

## Future Enhancements

### Potential Additions

- **Portfolio Optimization:** Algorithmic project selection tools
- **Real-time Updates:** WebSocket integration for live data
- **Mobile Support:** Touch-optimized interactions
- **Advanced Analytics:** Machine learning for project success prediction
- **Collaboration Features:** Multi-user scenario sharing
- **API Integration:** Connect to external project management systems

### Advanced Analytics

- **Network Analysis:** Centrality measures and community detection
- **Risk Modeling:** Monte Carlo simulation of project outcomes
- **Resource Optimization:** Linear programming for allocation
- **Predictive Analytics:** Machine learning for project success prediction

## Troubleshooting

### Common Issues

1. **Blank Visualizations:** Check browser console for JavaScript errors
2. **Data Loading Errors:** Verify HTTP server is running and JSON files exist
3. **Layout Problems:** Ensure browser supports SVG and modern JavaScript
4. **Performance Issues:** Reduce dataset size or simplify visualizations

### Browser Compatibility

- **Recommended:** Chrome 80+, Firefox 75+, Safari 13+, Edge 80+
- **Required Features:** ES6 JavaScript, SVG, CSS3 transforms
- **Known Issues:** Internet Explorer not supported

## Contributing

To contribute improvements or bug fixes:

1. Test changes with sample data
2. Ensure cross-browser compatibility
3. Update documentation for new features
4. Follow existing code style and patterns

## License

This project is provided as an educational example for portfolio visualization techniques.
