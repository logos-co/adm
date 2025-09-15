# 🎯 Interactive Decision Space Viewer with Backend Integration

A comprehensive web-based system for visualizing project decision spaces with real-time constraint analysis using your research framework.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Flask (`pip install flask flask-cors`)
- Your existing qualitative evaluation research framework

### Launch the System

1. **Start both servers**:
   ```bash
   # Terminal 1: Launch web interface
   python start_decision_space_viewer.py

   # Terminal 2: Launch backend API
   python decision_space_backend.py
   ```

2. **Open your browser** to http://localhost:8080/decision_space_viewer.html

## 🌟 Features

### Real-time Integration with Your Research Framework

✅ **Live Backend Connection**: Frontend automatically detects and connects to the Python backend
✅ **Qualitative Evaluation Translator**: Uses your existing translator for constraint conversion
✅ **Polytope Visualization Engine**: Integrates with your advanced visualization system
✅ **Constraint Validation**: Real feasibility checking using your research algorithms
✅ **Sensitivity Analysis**: Live impact assessment of constraint changes

### Interactive Decision Space Exploration

🎯 **Real-time Visualization**: Watch decision space update instantly as you add projects and constraints
📊 **Multi-dimensional Views**: Switch between different criteria pairs (Strategic Value vs Technical Complexity)
🔗 **Constraint Management**: Add, modify, and remove constraints with immediate visual feedback
📈 **Project Portfolio Analysis**: Interactive portolio building with live optimization scoring

### Advanced Analysis Capabilities

🔬 **Research-Grade Integration**:
- Full integration with your `qualitative_evaluation_translator.py`
- Compatible with your existing polytope visualization system
- Supports all constraint types from your research framework

🧮 **Real-time Analytics**:
- Live constraint matrix generation
- Feasibility validation using your algorithms
- Sensitivity analysis and impact assessment

## 📋 Usage Guide

### 1. Initial Setup

When you first open the viewer, you'll see:
- Welcome screen with demo button
- Backend status notification (Advanced analysis enabled/unavailable)
- Clean, modern interface ready for your data

### 2. Loading Demo Data

Click **"Try the Demo"** or **"Load Demo Data"** to see real examples:
- **Logos Core**: Research platform project
- **Nimbus ETH2**: Blockchain client project
- **VAC Research**: Advanced research initiative
- **Status Desktop**: User interface project

### 3. Adding Projects

1. Click **"Add Project"**
2. Enter Project ID (e.g., `PRJ001`)
3. Enter descriptive project name
4. Projects are added instantly to your portfolio

### 4. Creating Constraints

1. **Select Projects**: Click "Select" next to projects you want to compare
2. **Choose Constraint Type**:
   - `Project A > Project B`: Make one project take priority
   - `Project A < Project B`: Reverse priority direction
   - `Project A = Project B`: Equal importance
   - `Set Range`: Define acceptable score ranges (0.0-1.0)
3. **Add Constraint**: Click to apply and see immediate visualization update

### 5. Analyzing Results

Use the right panel to:
- **Test Feasibility**: Check if constraints are solvable
- **Sensitivity Analysis**: See how individual constraints affect results
- **Portfolio Optimization**: Get optimization recommendations
- **Export Data**: Save your analysis in JSON format

### 6. Exploring Visualizations

Switch between different dimension combinations:
- **Strategic Value vs Market Impact** (Default)
- **Technical Complexity vs Innovation Level**
- **Resource Requirement vs Strategic Value**
- And any other criteria combinations

## 🔧 Backend Integration Details

### API Endpoints

The backend provides RESTful APIs:

```javascript
// Check backend availability
GET /api/status

// Update projects
POST /api/projects
{
  "projects": [...]
}

// Add constraint
POST /api/constraints
{
  "evaluator_id": "user_123",
  "evaluation_type": "COMPARISON",
  "projects": ["PROJ_1", "PROJ_2"],
  "operator": "GREATER",
  "criteria": "Strategic Value"
}

// Get constraint matrices
GET /api/constraints/matrices

// Validate constraints
GET /api/constraints/validate

// Run portfolio optimization
POST /api/optimize
{
  "type": "max_benefit"
}
```

### Integration with Your Framework

The system automatically integrates with your existing research code:

```python
# From your qualitative_evaluation_translator.py
from qualitative_evaluation_translator import (
    QualitativeEvaluationTranslator,
    QualitativeEvaluation,
    EvaluationType,
    ComparisonOperator
)

# From your polytope_visualizer.py
from polytope_visualizer import PolytopeVisualizer
```

## 🎨 Visualization Features

### Interactive Elements

- **Hover Tooltips**: Detailed project information on hover
- **Real-time Updates**: Visualization updates immediately after changes
- **Constraint Regions**: Visual regions showing constraint boundaries
- **Project Positioning**: Bubble size represents resource requirements
- **Color Coding**: Different colors for project statuses

### Advanced Visualizations

- **2D Scatter Plots**: Show projects across any two dimensions
- **Constraint Boundaries**: Highlight feasible regions
- **Grid Background**: Easy value estimation
- **Responsive Design**: Works on different screen sizes

## 🧪 Testing with Your Research Framework

### Sample Usage

```bash
# Start the backend
python decision_space_backend.py

# In another terminal, or via API calls:
curl http://localhost:5001/api/status
curl -X POST http://localhost:5001/api/demo \
  -H "Content-Type: application/json"

# Then open the web interface
python start_decision_space_viewer.py
```

### Integration Testing

1. **Add Projects** via the web interface
2. **Create Constraints** and observe real-time updates
3. **Monitor Backend Logs** to see constraint processing
4. **Export Results** for further analysis in your research framework

## 🔍 Advanced Features

### Constraint Analysis

- **Real Feasibility Checking**: Uses your translator's validation algorithms
- **Matrix Generation**: Creates A_ineq, b_ineq matrices for optimization
- **Conflict Detection**: Identifies contradictory constraints
- **Sensitivity Analysis**: Measures impact of individual constraints

### Portfolio Optimization

- **Integration Ready**: Connects with your optimization algorithms
- **Multiple Objectives**: Support for different optimization criteria
- **Real-time Scoring**: Live optimization score updates
- **Solution Export**: Results compatible with further analysis

### Data Export

- **JSON Format**: Complete project and constraint data
- **Research Compatibility**: Format matches your framework inputs
- **Analysis Results**: Includes polytope data and validation results

## 🛠 Troubleshooting

### Backend Connection Issues

**Problem**: "Backend not connected" notification
**Solution**:
1. Ensure `decision_space_backend.py` is running on port 5001
2. Check firewall settings
3. Verify Python path includes `dl-example/` directory

**Problem**: "Advanced features unavailable"
**Solution**:
1. Install required dependencies: `pip install flask flask-cors`
2. Ensure `dl-example/` modules are accessible
3. Check Python import paths

### Visualization Issues

**Problem**: Visualization not updating
**Solution**:
1. Check browser console for JavaScript errors
2. Verify D3.js is loading correctly
3. Try refreshing the page

**Problem**: No demo data loading
**Solution**:
1. Check network connectivity
2. Verify backend API is responding
3. Check browser developer tools for failed API calls

### Performance Considerations

- **Large Portfolios**: Systems handles up to 50+ projects efficiently
- **Constraint Complexity**: Scales well with constraint density
- **Browser Requirements**: Modern browsers with ES6+ support recommended

## 🔄 Integration Examples

### Using Exported Data

```python
import json

# Load exported data
with open('decision_space_analysis_20241209.json') as f:
    data = json.load(f)

# Process with your research framework
from dl_example.qualitative_evaluation_translator import QualitativeEvaluationTranslator

projects = [p['id'] for p in data['projects']]
translator = QualitativeEvaluationTranslator(projects, ['Strategic Value', 'Market Impact'])

# Add constraints
for constraint in data['constraints']:
    eval_data = constraint['evaluation']
    evaluation = translator.convert_evaluation(eval_data)
    translator.add_evaluation(evaluation)
```

## 🎯 Benefits for Your Research

### Real-time Feedback Loop

- **Immediate Visualization**: See constraint impacts instantly
- **Iterative Refinement**: Quickly modify and test constraints
- **Validation Feedback**: Get real analysis results as you work
- **Educational Tool**: Demonstrate concepts interactively

### Research Integration

- **Framework Validation**: Test your algorithms with real data
- **User Experience Studies**: Evaluate interface effectiveness
- **Algorithm Comparison**: Compare different constraint handling approaches
- **Data Collection**: Gather real qualification patterns

## 🚀 Future Enhancements

### Planned Features

- **3D Visualization**: Interactive 3D decision space exploration
- **Multi-user Collaboration**: Shared decision spaces
- **Advanced Animation**: Smooth transitions and constraint morphing
- **Machine Learning Integration**: Automated constraint suggestions
- **Historical Analysis**: Track decision space evolution

### Research Extensions

- **Uncertainty Modeling**: Stochastic constraint visualization
- **Dynamic Constraints**: Time-varying decision spaces
- **Preference Learning**: User preference inference
- **Advanced Optimization**: NSGA-II, MOEA/D integration

---

## 🎉 Getting Started

1. **Launch the system** using the commands above
2. **Click "Load Demo Data"** to see working examples
3. **Add your own projects** and start creating constraints
4. **Watch the decision space** evolve in real-time
5. **Export results** for integration with your research framework

This system provides a powerful interface between your advanced research algorithms and interactive data exploration, enabling you to see your decision spaces come to life as you develop project constraints! 🎯
