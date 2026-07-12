# Contributing to Photonic Volumetric Computing

Thank you for your interest in contributing to this groundbreaking research project! We welcome contributions from researchers, engineers, and enthusiasts in optical computing, photonics, and neural networks.

## How to Contribute

### 1. Report Issues
- Found a bug? Open an issue with:
  - Clear description of the problem
  - Steps to reproduce
  - Expected vs. actual behavior
  - Python version and dependencies

### 2. Suggest Features
- Have an idea? Create an issue with:
  - Feature description
  - Use case and motivation
  - Proposed implementation approach (if applicable)
  - References to relevant research papers

### 3. Submit Code

#### Setup Development Environment
```bash
git clone https://github.com/yasarhotmailes/photonic-volumetric-compute.git
cd photonic-volumetric-compute
pip install -e ".[dev]"
```

#### Code Style
- Follow PEP 8
- Use `black` for formatting: `black src/ tests/`
- Use `flake8` for linting: `flake8 src/ tests/`
- Document with docstrings (Google style)

#### Testing
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_layer.py::test_layer_creation
```

#### Creating a Pull Request
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make changes with clear commit messages
4. Add tests for new functionality
5. Update documentation
6. Push to your fork
7. Open a pull request with:
   - Clear description of changes
   - References to related issues
   - Explanation of testing
   - Any breaking changes noted

## Research Contribution Areas

We particularly welcome contributions in these areas:

### Optical Physics & Simulation
- [ ] Ray tracing through multilayer glass stacks
- [ ] FDTD (Finite-Difference Time-Domain) electromagnetic solver
- [ ] Fresnel equations and refraction modeling
- [ ] Aberration analysis
- [ ] Quantum effects simulation

### Optical VMM (Vector-Matrix Multiplication)
- [ ] Efficient algorithms for optical matrix operations
- [ ] Numerical stability analysis
- [ ] Precision/noise trade-offs
- [ ] Comparison with electronic VMM

### Neural Network Architectures
- [ ] Optical convolutional layers
- [ ] Optical pooling operations
- [ ] Optical attention mechanisms
- [ ] Quantization-aware optical networks

### Hardware Design
- [ ] ITO material property models
- [ ] Laser specifications and optimization
- [ ] Photodetector sensitivity analysis
- [ ] Thermal management
- [ ] Power consumption calculations

### Machine Learning Training
- [ ] Backpropagation adapted for optical domain
- [ ] Calibration procedures
- [ ] Error compensation algorithms
- [ ] Model optimization for photonic hardware

### Benchmarking & Validation
- [ ] Performance metrics and comparison frameworks
- [ ] Energy consumption profiling
- [ ] Latency analysis
- [ ] Accuracy vs. silicon neural networks

### Documentation
- [ ] Tutorial notebooks
- [ ] API documentation
- [ ] Physics explanations
- [ ] Hardware interface guides
- [ ] Performance guides

## Code Organization Guidelines

### File Naming
- `module_name.py` for modules
- `test_module_name.py` for tests
- Use underscores for multi-word names

### Function/Class Naming
- Classes: `PascalCase` (e.g., `PhotonicStack`)
- Functions: `snake_case` (e.g., `calculate_refraction`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `SPEED_OF_LIGHT`)

### Docstring Format
```python
def optical_vmm(matrix: np.ndarray, vector: np.ndarray) -> np.ndarray:
    """Perform optical vector-matrix multiplication.
    
    Simulates multiplication of a vector by a weight matrix using
    optical diffraction and interference principles.
    
    Args:
        matrix: Weight matrix of shape (m, n), representing optical phase/amplitude
        vector: Input vector of shape (n,), representing input light field
        
    Returns:
        Output vector of shape (m,), representing output light intensity
        
    Raises:
        ValueError: If dimensions are incompatible
        
    Examples:
        >>> W = np.random.randn(10, 20)
        >>> x = np.random.randn(20)
        >>> y = optical_vmm(W, x)
        >>> y.shape
        (10,)
        
    References:
        - Lin et al. (2018). "All-optical machine learning using diffractive deep neural networks"
    """
    # Implementation
```

## Commit Message Guidelines

Follow conventional commits format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without feature changes
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(optics): implement Fresnel equations for multilayer reflection
fix(ito_controller): correct ITO transparency calculation for layer addressing
docs(architecture): add detailed explanation of optical VMM principle
test(layer): add tests for glass layer creation and properties
```

## Review Process

1. **Automated Checks**: All PRs must pass:
   - Linting (flake8)
   - Formatting (black)
   - Tests (pytest with >80% coverage)
   - Type checking (if applicable)

2. **Code Review**: At least one maintainer review
   - Correctness of physics/algorithms
   - Code quality and clarity
   - Test adequacy
   - Documentation completeness

3. **Scientific Review**: For contributions to core algorithms or physics
   - Validation against academic literature
   - Experimental methodology review (if applicable)
   - Performance claims verification

## Communication

- **Issues**: Use GitHub issues for bug reports and feature requests
- **Discussions**: Use GitHub discussions for broader topics
- **Email**: For sensitive or private matters
- **Research Collaboration**: Contact maintainers for large collaborative projects

## Code of Conduct

All contributors are expected to:
- Be respectful and inclusive
- Provide constructive feedback
- Acknowledge and respect different perspectives
- Focus on scientific integrity and accuracy
- Avoid discrimination and harassment

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Academic papers (if applicable)
- Project acknowledgments

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to the future of photonic computing!** 🌟