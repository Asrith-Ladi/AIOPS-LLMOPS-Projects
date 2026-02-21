# Setup.py Documentation

## Overview
The `setup.py` file is the configuration file for Python package distribution and installation. It defines how the AIOPS project is packaged, installed, and what dependencies it requires. This file is used by setuptools to create installable distributions.

## What This File Does

- **Defines package metadata** (name, version, author)
- **Automatically discovers all packages** in the project
- **Manages dependencies** from requirements.txt
- **Enables installation** via `pip install -e .`
- **Prepares distribution** for sharing or deployment

## File Components Explained

### Imports
```python
from setuptools import setup, find_packages
```
- **setuptools**: Tools for building and distributing Python packages
- **find_packages()**: Automatically locates all Python packages in your project

### Requirements Loading
```python
with open("requirements.txt") as f:
    requirements = f.read().splitlines()
```
- Reads the `requirements.txt` file
- Converts it into a list of dependency strings
- Each line becomes a separate requirement

### Setup Configuration

| Parameter | Value | Purpose |
|-----------|-------|---------|
| **name** | YT SEO Insights Generator | Display name of the project |
| **version** | 1.0.0 | Current version (semantic versioning) |
| **author** | Ladi Asrith | Package maintainer/creator |
| **packages** | find_packages() | All packages with `__init__.py` files |
| **install_requires** | requirements list | Dependencies to install |

## How It Works

### Package Discovery with `find_packages()`
The `find_packages()` function automatically discovers all directories containing an `__init__.py` file:

```
project_root/
├── setup.py
├── requirements.txt
├── common/                  ← Found as a package
│   ├── __init__.py         ← Marker file
│   ├── logger.py
│   └── custom_exception.py
└── other_module/           ← Found as a package
    └── __init__.py                ← Marker file
```

**Result**: `packages = ['common', 'other_module']`

### Dependency Installation
The `install_requires` parameter ensures all dependencies are installed:
- Reads from `requirements.txt`
- Each line is a dependency (e.g., `flask==2.0.0`, `requests>=2.25.0`)
- Installed automatically when project is installed

## Common Use Cases

### Installation for Development
```bash
pip install -e .
```
- `-e` = editable mode (changes to code reflect immediately)
- `.` = current directory (where setup.py is located)
- Installs all dependencies from requirements.txt

### Installation for Distribution
```bash
pip install .
```
- Regular installation (not editable)
- Suitable for end users

### Building Distribution Packages
```bash
python setup.py sdist bdist_wheel
```
- Creates source distribution and wheel
- Ready to upload to PyPI

## Configuration Reference

### Version Format (Semantic Versioning)
```
MAJOR.MINOR.PATCH
1.0.0
│   │  └─ Patch (bug fixes)
│   └──── Minor (new features, backward compatible)
└─────── Major (breaking changes)
```

### When to Update Version
- **Patch (1.0.X)**: Bug fixes, minor improvements
- **Minor (1.X.0)**: New features, backward compatible
- **Major (X.0.0)**: Breaking changes, API changes

## Best Practices

### 1. Always Include requirements.txt
```python
with open("requirements.txt") as f:
    requirements = f.read().splitlines()
```
✓ Centralized dependency management
✓ Easy to update dependencies
✓ Human-readable format

### 2. Use Meaningful Metadata
```python
name="YT SEO Insights Generator"     # Clear, descriptive name
version="1.0.0"                      # Semantic versioning
author="Your Name"                   # Who maintains this
```

### 3. Don't Hardcode Dependencies
❌ BAD:
```python
install_requires=['flask==2.0.0', 'requests>=2.25.0']
```

✓ GOOD:
```python
with open("requirements.txt") as f:
    requirements = f.read().splitlines()
install_requires=requirements
```

## Example requirements.txt
```
flask==2.0.0
requests>=2.25.0
python-dotenv==0.19.0
```

Each dependency is installed when `pip install .` is run.

## Common Issues & Solutions

### Issue: Packages not found
**Problem**: `find_packages()` doesn't discover your modules
**Solution**: Ensure all package directories have `__init__.py` file

```
├── common/
│   ├── __init__.py     ← Required!
│   └── logger.py
```

### Issue: Dependencies not installing
**Problem**: `pip install .` doesn't install requirements
**Solution**: Check that `requirements.txt` exists and is in project root

### Issue: Version conflicts
**Problem**: Installed version differs from expected
**Solution**: Use version specifiers in requirements.txt:
- `==` for exact versions
- `>=` for minimum versions
- `~=` for compatible versions

## Project Metadata

| Field | Current Value |
|-------|---------------|
| Project Name | YT SEO Insights Generator |
| Version | 1.0.0 |
| Author | Ladi Asrith |
| Package Discovery | Automatic (find_packages) |
| Dependencies | From requirements.txt |

## Next Steps

1. **Ensure all packages have `__init__.py`** - Required for discovery
2. **Maintain requirements.txt** - Update whenever dependencies change
3. **Update version** - When releasing new versions
4. **Document in README** - Installation instructions for users

## Advanced Features (Optional)

If you want to enhance setup.py later:

```python
# Add description
description="A tool for YouTube SEO insights",

# Add URL
url="https://github.com/username/repo",

# Add classification
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
],

# Add long description from README
long_description=open("README.md").read(),
long_description_content_type="text/markdown",
```
