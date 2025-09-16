# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains **two completely independent portfolio management experiments**:

- **toy-example/**: **INDEPENDENT** - D3.js interactive visualization experiment (includes toy-data/)
- **dl-example/**: **INDEPENDENT** - Deep learning qualitative evaluation experiment

⚠️ **IMPORTANT**: These are separate, unrelated experiments. Do not mix concepts, data, or approaches between them.

## Independent Examples

### Example 1: Interactive Visualizations (toy-example)
A standalone D3.js visualization system experiment.
```bash
cd toy-example
python data_preparation.py
python -m http.server 8000
# Access at http://localhost:8000/portfolio_visualizations.html
```

### Example 2: Deep Learning Optimization (dl-example)
A standalone qualitative evaluation translation experiment with organized directory structure.
```bash
cd dl-example
# View main dashboard
open project_portfolio_index.html
# Run examples
python examples/demo.py
python examples/portfolio_optimization_demo.py
python examples/polytope_visualization_demo.py
```

### Testing Each Example
```bash
# Test ONLY the visualization experiment
cd toy-example && python test_visualizations.py

# Test ONLY the deep learning experiment  
cd dl-example && python tests/test_qualitative_evaluation.py
```

## Documentation

Each example has completely separate documentation:

- **📊 Visualization Experiment**: See [toy-example-docs.md](./toy-example-docs.md) - D3.js visualization system (uses toy-data)
- **🧠 Deep Learning Experiment**: See [dl-example-docs.md](./dl-example-docs.md) - Qualitative evaluation translation system (self-contained)

## Example Details

⚠️ **Work on ONE example at a time. Do not mix or cross-reference between examples.**

### Visualization Experiment (toy-example/)
- Self-contained D3.js visualization system
- Has its own toy-data/ subdirectory with CSV datasets
- See [toy-example-docs.md](./toy-example-docs.md) for complete details

### Deep Learning Experiment (dl-example/)  
- Self-contained qualitative evaluation system with organized directory structure
- Includes Phase 1 polytope visualization, Phase 2 trade-off analysis, and DPbQN integration
- Uses its own internal project data in data/ directory
- Generated visualizations organized in visualizations/ subdirectories
- See [dl-example-docs.md](./dl-example-docs.md) and [dl-example/README.md](./dl-example/README.md) for complete details

## Repository Structure

```
Repository Structure:
├── toy-example/        # INDEPENDENT visualization experiment
│   ├── toy-data/      # CSV datasets for this experiment only
│   ├── js/            # D3.js visualization modules  
│   ├── data_preparation.py
│   └── portfolio_visualizations.html
├── dl-example/         # INDEPENDENT deep learning experiment
│   ├── README.md                     # Main documentation
│   ├── project_portfolio_index.html  # Main dashboard
│   ├── DIRECTORY_STRUCTURE.md       # Directory documentation
│   ├── src/                         # Source code modules
│   ├── tests/                       # Test suite
│   ├── examples/                    # Usage demonstrations
│   ├── data/                        # Data files (JSON, CSV)
│   ├── docs/                        # Documentation
│   └── visualizations/              # Generated HTML visualizations
│       ├── phase1/                  # Phase 1 polytope visualizations
│       ├── phase2/                  # Phase 2 trade-off analysis
│       └── portfolio/               # Project portfolio visualizations
├── toy-example-docs.md # Documentation for visualization experiment
├── dl-example-docs.md  # Documentation for deep learning experiment
└── CLAUDE.md          # This file
```

## Important Instructions

- **File Creation**: NEVER create files unless absolutely necessary; always prefer editing existing files
- **Documentation**: Do not proactively create documentation files unless explicitly requested
- **Code Style**: Follow existing patterns and conventions in each module
- **Security**: Never expose or log secrets; follow security best practices
- **Testing**: Always run appropriate test suites after making changes