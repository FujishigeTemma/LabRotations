# Technical Context: CHAOS

## Technologies Used

### Core Technologies
- **Python**: Primary programming language
- **NumPy/SciPy**: Likely used for numerical computations
- **Jupyter**: Interactive notebooks for analysis and demonstration
- **Matplotlib/Seaborn**: Likely used for visualization
- **NetworkX**: Possibly used for graph/network analysis

### Development Tools
- **pyenv**: Python version management (indicated by .python-version files)
- **pyproject.toml**: Modern Python packaging
- **ruff**: Python linter (indicated by ruff.toml)
- **uv**: Likely used for dependency management (indicated by uv.lock)
- **Git**: Version control

## Development Setup

### Project Structure
```
CHAOS/
├── data/                  # Data storage
├── libs/                  # Core libraries
│   ├── edmkit/            # Empirical Dynamic Modeling toolkit
│   └── generate/          # Data generation library
├── notebooks/             # Jupyter notebooks
├── outputs/               # Generated outputs
└── openssl/               # SSL certificates (possibly for secure connections)
```

### Library Structure
```
edmkit/
├── __init__.py
├── ccm.py                # Convergent Cross Mapping
├── embedding.py          # Time series embedding
├── graph.py              # Graph construction and analysis
├── heap.py               # Heap data structure
├── simplex_projection.py # Simplex projection algorithm
├── smap.py               # S-Map algorithm
├── tensor.py             # Tensor operations
└── util.py               # Utility functions

generate/
├── __init__.py
├── double_pendulum.py    # Double pendulum system
├── lorenz.py             # Lorenz system
├── mackey_glass.py       # Mackey-Glass equation
└── network.py            # Network-based systems
```

### Installation & Setup
1. Clone the repository
2. Install Python (version likely specified in .python-version)
3. Install dependencies using uv or pip
4. Run notebooks from the notebooks/ directory

## Technical Constraints

### Performance Considerations
- Algorithms may have high computational complexity
- Large datasets may require significant memory
- Some algorithms may benefit from parallelization

### Numerical Precision
- Chaotic systems are sensitive to initial conditions
- Floating-point precision may affect results
- Stability of numerical algorithms is critical

### Visualization Challenges
- High-dimensional data visualization
- Network/graph visualization layout algorithms
- Interactive visualization performance

## Dependencies

### Core Dependencies (Inferred)
- **NumPy**: Numerical computing
- **SciPy**: Scientific computing
- **Matplotlib/Seaborn**: Visualization
- **Jupyter**: Interactive notebooks
- **NetworkX**: Graph algorithms (possibly)
- **pandas**: Data manipulation (possibly)

### Development Dependencies (Inferred)
- **pytest**: Testing framework
- **ruff**: Linting
- **uv**: Dependency management
- **pyenv**: Python version management

## Environment Setup

### Python Environment
- Specific Python version likely managed via pyenv
- Virtual environments likely used for isolation
- Dependencies managed via pyproject.toml

### Data Management
- Data directory structure suggests organized data storage
- .gitignore in data/ suggests large data files aren't versioned
- Outputs directory for generated results

## Build & Test Process

### Building
- Python packages built using modern pyproject.toml configuration
- Libraries installable via pip/uv

### Testing
- Unit tests in libs/edmkit/tests/
- Test files follow naming convention test_*.py
- Tests likely run using pytest

### Documentation
- Documentation likely in docstrings
- Notebooks serve as executable documentation
- README.md files provide overview information