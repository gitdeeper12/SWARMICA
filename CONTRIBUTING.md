# Contributing to SWARMICA v1.0.0

Thank you for your interest in contributing to **SWARMICA**!

## How to Contribute

### 1. Report Bugs
- Use GitHub/GitLab Issues
- Include: Python version, OS, swarm modality (aerial/ground/underwater/mixed)
- Label: `bug`

### 2. Suggest Features
- Open an issue with label `enhancement`
- Describe the use case and expected behavior
- New target formations or coupling manifolds are welcome

### 3. Submit Code Changes

#### Prerequisites
```bash
pip install -e .[dev]
pre-commit install
```

Development Workflow

```bash
git clone https://github.com/gitedeeper12/SWARMICA
cd SWARMICA
git checkout -b feature/your-feature-name
pytest tests/ -v
git commit -m "feat: add new formation type"
git push origin feature/your-feature-name
```

4. Update Documentation

· Edit README.md, docs/, or docstrings
· Ensure documentation builds correctly

Code Style

· Python: PEP 8 (use black)
· Type hints: Required for all public functions
· Docstrings: Google style

Testing Requirements

· All tests must pass: pytest tests/ -v
· Coverage should not decrease: pytest --cov=swarmica
· New features require tests
· Jacobian stability certification must hold

Commit Convention

Type Description
feat New feature
fix Bug fix
docs Documentation
test Testing
refactor Code refactor
perf Performance improvement

Questions?

Open an issue or email: gitdeeper@gmail.com

---

Thank you for contributing to collective swarm stability! 🐝
