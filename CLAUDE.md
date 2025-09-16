# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains **two completely independent portfolio management experiments**:

- **toy-data/**: Shared sample CSV datasets (used by toy-example only)
- **toy-example/**: **INDEPENDENT** - D3.js interactive visualization experiment
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
A standalone qualitative evaluation translation experiment.
```bash
cd dl-example
python demo.py
python portfolio_optimization_demo.py
python polytope_visualization_demo.py
```

### Testing Each Example
```bash
# Test ONLY the visualization experiment
cd toy-example && python test_visualizations.py

# Test ONLY the deep learning experiment  
cd dl-example && python test_qualitative_evaluation.py
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
- Self-contained qualitative evaluation system
- Uses its own internal project data
- See [dl-example-docs.md](./dl-example-docs.md) for complete details

## Repository Structure

```
Repository Structure:
├── toy-example/        # INDEPENDENT visualization experiment
│   ├── toy-data/      # CSV datasets for this experiment only
│   ├── js/            # D3.js visualization modules  
│   ├── data_preparation.py
│   └── portfolio_visualizations.html
├── dl-example/         # INDEPENDENT deep learning experiment
│   ├── qualitative_evaluation_translator.py
│   ├── polytope_visualizer.py
│   ├── portfolio_optimization_demo.py
│   └── *.json         # Self-contained project data
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