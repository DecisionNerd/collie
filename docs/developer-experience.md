# COLLIE Developer Experience Guide

This comprehensive guide covers everything you need to know about contributing to the COLLIE project and using it as a Python package. Whether you're a contributor, maintainer, or end user, this guide will help you get the most out of COLLIE.

## Table of Contents

1. [For Contributors](#for-contributors)
   - [Getting Started](#getting-started)
   - [Development Environment](#development-environment)
   - [Project Structure](#project-structure)
   - [Code Generation](#code-generation)
   - [Testing](#testing)
   - [Code Quality](#code-quality)
   - [Contributing Guidelines](#contributing-guidelines)
2. [For Users](#for-users)
   - [Installation](#installation)
   - [Basic Usage](#basic-usage)
   - [Advanced Features](#advanced-features)
   - [API Reference](#api-reference)
   - [Examples](#examples)
3. [Troubleshooting](#troubleshooting)
4. [Resources](#resources)

---

## For Contributors

### Getting Started

COLLIE is a developer-friendly toolkit for working with CIDOC CRM v7.1.3. Before contributing, familiarize yourself with:

- **CIDOC CRM**: The conceptual reference model we implement
- **Pydantic**: Our data validation framework
- **Modern Python**: We use Python 3.13+ with modern tooling

#### Prerequisites

- Python 3.13 or higher
- `uv` package manager (recommended) or `pip`
- Git for version control
- Basic understanding of CIDOC CRM concepts

### Development Environment

#### 1. Clone the Repository

```bash
git clone https://github.com/decisionnerd/collie.git
cd collie
```

#### 2. Set Up Development Environment

```bash
# Using uv (recommended)
uv sync --dev

# Or with pip
pip install -e ".[dev]"
```

#### 3. Verify Installation

```bash
# Run tests to ensure everything works
uv run pytest

# Check code quality
uv run ruff check
uv run ruff format --check
```

### Project Structure

Understanding the project structure is crucial for effective contribution:

```
collie/
├── src/collie/                    # Main package
│   ├── __init__.py               # Package initialization
│   ├── main.py                   # CLI entry point
│   ├── models/                   # Pydantic models
│   │   ├── base.py              # Base classes and utilities
│   │   ├── generated/           # Auto-generated E-classes
│   │   │   ├── __init__.py
│   │   │   └── e_classes.py     # 99 CIDOC CRM classes
│   │   └── __init__.py
│   ├── io/                      # Input/output modules
│   │   ├── to_markdown.py       # Markdown renderers
│   │   └── to_cypher.py         # Cypher emitters
│   ├── validators/              # Validation framework
│   │   ├── __init__.py
│   │   ├── quantifiers.py       # Cardinality validation
│   │   └── typing_rules.py      # Type alignment validation
│   ├── codegen/                 # Code generation tools
│   │   ├── generate_models.py   # YAML → Pydantic models
│   │   ├── generate_registry.py # YAML → property registry
│   │   ├── generate_templates.py # Jinja2 templates
│   │   └── specs/              # YAML specifications
│   │       ├── crm_classes.yaml # CRM class definitions
│   │       ├── crm_properties.yaml # CRM property definitions
│   │       └── aliases.yaml    # Human-readable aliases
│   ├── tests/                   # Test suite
│   │   ├── unit/               # Unit tests
│   │   └── golden/             # Integration tests
│   ├── examples/               # Sample data
│   └── docs/                   # Documentation
├── docs/                       # Project documentation
├── pyproject.toml              # Project configuration
└── README.md                   # Project overview
```

#### Key Components

- **`models/`**: Pydantic models for CIDOC CRM entities
- **`io/`**: Renderers for Markdown and Cypher output
- **`validators/`**: Framework for CRM compliance validation
- **`codegen/`**: Tools for generating models from YAML specs
- **`tests/`**: Comprehensive test suite (32 tests, 100% pass rate)

### Code Generation

COLLIE uses automated code generation to maintain consistency between YAML specifications and Python models.

#### Regenerating Models

When you modify YAML specifications, regenerate the Python models:

```bash
# Generate E-class models
uv run python src/collie/codegen/generate_models.py

# Generate property registry
uv run python src/collie/codegen/generate_registry.py
```

#### Adding New CRM Classes

1. **Edit YAML specifications** in `src/collie/codegen/specs/`
2. **Regenerate models** using the codegen scripts
3. **Update tests** to cover new functionality
4. **Update documentation** as needed

#### YAML Structure

```yaml
# Example from crm_classes.yaml
E22:
  code: "E22"
  label: "Human-Made Object"
  parent: "E19"
  description: "Physical objects created by human activity"
  canonical_fields: ["label", "type", "notes", "current_location", "produced_by"]
```

### Testing

COLLIE has a comprehensive testing strategy with 32 tests covering all major functionality.

#### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test suites
uv run pytest src/collie/tests/unit/      # Unit tests
uv run pytest src/collie/tests/golden/    # Integration tests

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=src/collie
```

#### Test Categories

1. **Unit Tests** (`tests/unit/`):
   - Individual component testing
   - Cypher emission validation
   - Markdown rendering verification
   - Validator framework testing

2. **Golden Tests** (`tests/golden/`):
   - End-to-end workflow testing
   - Real-world data scenarios
   - UUID handling verification
   - Integration testing

#### Writing Tests

Follow these patterns when adding tests:

```python
def test_new_feature():
    """Test description explaining what is being tested."""
    # Arrange
    entity = EE22_HumanMadeObject(id="test_001", label="Test Object")
    
    # Act
    result = some_function(entity)
    
    # Assert
    assert result is not None
    assert "expected_value" in result
```

#### Test Data

- **Golden test data**: `src/collie/examples/museum_object.json`
- **Test fixtures**: Use realistic CRM entities
- **UUID handling**: Test both string IDs and UUID objects

### Code Quality

COLLIE uses modern Python tooling for code quality:

#### Ruff Configuration

```bash
# Format code
uv run ruff format

# Check for issues
uv run ruff check

# Auto-fix issues
uv run ruff check --fix
```

#### Code Standards

- **Python 3.13+**: Use modern Python features
- **Type hints**: All functions should have type annotations
- **Docstrings**: Document all public functions and classes
- **Line length**: 88 characters (Black-compatible)
- **Import style**: Absolute imports preferred

#### Pre-commit Hooks

Set up pre-commit hooks for automatic code quality checks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

### Contributing Guidelines

#### 1. Fork and Branch

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/collie.git
cd collie

# Create feature branch
git checkout -b feature/your-feature-name
```

#### 2. Make Changes

- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

#### 3. Commit and Push

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add feature: brief description"

# Push to your fork
git push origin feature/your-feature-name
```

#### 4. Create Pull Request

- Provide clear description of changes
- Reference any related issues
- Ensure CI passes
- Request review from maintainers

#### Pull Request Checklist

- [ ] All tests pass
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages are clear and descriptive

---

## For Users

### Installation

#### Using uv (Recommended)

```bash
# Add to your project
uv add collie

# Or install globally
uv add --global collie
```

#### Using pip

```bash
# Install from PyPI
pip install collie

# Install with development dependencies
pip install collie[dev]
```

#### From Source

```bash
# Clone and install
git clone https://github.com/decisionnerd/collie.git
cd collie
pip install -e .
```

### Basic Usage

#### Creating CRM Entities

```python
from collie.models.generated.e_classes import EE22_HumanMadeObject, EE12_Production
from collie.models.base import E53_Place

# Create entities with string IDs (automatically converted to UUIDs)
vase = EE22_HumanMadeObject(
    id="obj_001",
    label="Ancient Greek Amphora",
    type=["E55:Vessel", "E55:Ceramic"]
)

production = EE12_Production(
    id="prod_001", 
    label="Vase Production",
    type=["E55:Manufacturing"]
)

location = E53_Place(
    id="place_001",
    label="Athens, Greece"
)
```

#### Rendering to Markdown

```python
from collie.io.to_markdown import to_markdown, MarkdownStyle

# Card style (concise, LLM-friendly)
card = to_markdown(vase, MarkdownStyle.CARD)
print(card)

# Detailed style (comprehensive information)
detailed = to_markdown(vase, MarkdownStyle.DETAILED)
print(detailed)

# Table style (structured data)
table = to_markdown([vase, production], MarkdownStyle.TABLE)
print(table)

# Narrative style (storytelling)
narrative = to_markdown(vase, MarkdownStyle.NARRATIVE)
print(narrative)
```

#### Generating Cypher Scripts

```python
from collie.io.to_cypher import generate_cypher_script, generate_cypher_parameters

# Generate Cypher script
entities = [vase, production, location]
cypher_script = generate_cypher_script(entities)
print(cypher_script)

# Generate parameters for batch operations
params = generate_cypher_parameters(entities)
print(params)
```

#### Validation

```python
from collie.validators import validate_batch_quantifiers, ValidationSeverity

# Validate entities for CRM compliance
results = validate_batch_quantifiers(entities, ValidationSeverity.WARN)
print(f"Validation issues: {results['total_issues']}")
```

### Advanced Features

#### UUID Handling

COLLIE provides flexible UUID handling:

```python
from uuid import UUID
from collie.models.generated.e_classes import EE22_HumanMadeObject

# String IDs (automatically converted to deterministic UUIDs)
entity1 = EE22_HumanMadeObject(id="obj_001", label="Object 1")

# UUID objects (used as-is)
entity2 = EE22_HumanMadeObject(id=UUID("12345678-1234-5678-9012-123456789012"), label="Object 2")

# Both approaches work seamlessly
print(entity1.id)  # UUID object
print(entity2.id)  # UUID object
```

#### Custom Validation

```python
from collie.validators import ValidationSeverity, enforce_quantifier

# Custom validation with different severity levels
enforce_quantifier(entity, "P108", [production.id], ValidationSeverity.RAISE)
```

#### Batch Operations

```python
# Process large datasets efficiently
entities = load_large_dataset()  # Your data loading function

# Batch validation
validation_results = validate_batch_quantifiers(entities)

# Batch Cypher generation
cypher_script = generate_cypher_script(entities, batch_size=1000)
```

### API Reference

#### Core Models

- **`CRMEntity`**: Base class for all CRM entities
- **`CRMRelation`**: Base class for relationships
- **`EE22_HumanMadeObject`**: Human-made objects
- **`EE12_Production`**: Production events
- **`E53_Place`**: Spatial locations

#### Markdown Renderers

- **`to_markdown()`**: Main rendering function
- **`MarkdownStyle`**: Enum for output styles
  - `CARD`: Concise summaries
  - `DETAILED`: Comprehensive information
  - `TABLE`: Structured data
  - `NARRATIVE`: Storytelling format

#### Cypher Emitters

- **`generate_cypher_script()`**: Generate MERGE/UNWIND scripts
- **`generate_cypher_parameters()`**: Generate parameter dictionaries
- **`emit_nodes()`**: Extract node data
- **`emit_relationships()`**: Extract relationship data

#### Validators

- **`validate_batch_quantifiers()`**: Cardinality validation
- **`validate_batch_typing()`**: Type alignment validation
- **`ValidationSeverity`**: Validation strictness levels
  - `WARN`: Log warnings (default)
  - `RAISE`: Raise exceptions
  - `IGNORE`: Skip validation

### Examples

#### Complete Workflow Example

```python
from collie.models.generated.e_classes import EE22_HumanMadeObject, EE12_Production
from collie.models.base import E53_Place, E52_TimeSpan
from collie.io.to_markdown import to_markdown, MarkdownStyle
from collie.io.to_cypher import generate_cypher_script
from collie.validators import validate_batch_quantifiers, ValidationSeverity

# 1. Create a complete museum object scenario
time_period = E52_TimeSpan(
    id="time_001",
    label="5th Century BCE",
    begin_of_the_begin="time_primitive_001",
    end_of_the_end="time_primitive_002"
)

location = E53_Place(
    id="place_001", 
    label="Athens, Greece"
)

production = EE12_Production(
    id="prod_001",
    label="Amphora Production",
    type=["E55:Manufacturing"],
    timespan=time_period.id,
    took_place_at=location.id
)

vase = EE22_HumanMadeObject(
    id="obj_001",
    label="Ancient Greek Amphora",
    type=["E55:Vessel", "E55:Ceramic"],
    produced_by=production.id,
    current_location=location.id
)

entities = [vase, production, location, time_period]

# 2. Validate for CRM compliance
validation_results = validate_batch_quantifiers(entities, ValidationSeverity.WARN)
print(f"Validation issues found: {validation_results['total_issues']}")

# 3. Generate Markdown report
markdown_report = to_markdown(entities, MarkdownStyle.NARRATIVE)
print("=== Markdown Report ===")
print(markdown_report)

# 4. Generate Cypher for Neo4j/Memgraph
cypher_script = generate_cypher_script(entities)
print("\n=== Cypher Script ===")
print(cypher_script)
```

#### Integration with LLMs

```python
# Use COLLIE output in LLM prompts
markdown_summary = to_markdown(entities, MarkdownStyle.CARD)

prompt = f"""
Based on this cultural heritage data:

{markdown_summary}

Please analyze the relationships between these entities and provide insights about their historical significance.
"""

# Send to your LLM of choice
response = llm_client.generate(prompt)
```

#### Graph Database Integration

```python
# Neo4j integration example
from neo4j import GraphDatabase

cypher_script = generate_cypher_script(entities)
params = generate_cypher_parameters(entities)

# Connect to Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

with driver.session() as session:
    # Execute the generated Cypher
    session.run(cypher_script, params)

driver.close()
```

---

## Troubleshooting

### Common Issues

#### Import Errors

```python
# Problem: ModuleNotFoundError
from collie.models.generated.e_classes import EE22_HumanMadeObject

# Solution: Ensure COLLIE is installed
pip install collie
# Or if developing locally:
pip install -e .
```

#### UUID Conversion Issues

```python
# Problem: UUID validation errors
entity = EE22_HumanMadeObject(id="invalid-uuid", label="Test")

# Solution: Use valid UUIDs or let COLLIE handle conversion
entity = EE22_HumanMadeObject(id="obj_001", label="Test")  # Auto-converted
# Or
from uuid import UUID
entity = EE22_HumanMadeObject(id=UUID("12345678-1234-5678-9012-123456789012"), label="Test")
```

#### Validation Warnings

```python
# Problem: Too many validation warnings
results = validate_batch_quantifiers(entities, ValidationSeverity.RAISE)

# Solution: Adjust validation severity or fix data
results = validate_batch_quantifiers(entities, ValidationSeverity.WARN)  # Less strict
# Or fix the underlying data issues
```

#### Performance Issues

```python
# Problem: Slow processing of large datasets
cypher_script = generate_cypher_script(large_entity_list)

# Solution: Use batch processing
cypher_script = generate_cypher_script(large_entity_list, batch_size=1000)
```

### Getting Help

1. **Check the documentation**: Start with this guide and the README
2. **Search issues**: Look for similar problems in GitHub issues
3. **Create an issue**: Provide detailed information about your problem
4. **Join discussions**: Participate in GitHub Discussions for community help

### Debugging Tips

#### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your COLLIE code here
```

#### Test with Simple Examples

```python
# Start with minimal examples
from collie.models.generated.e_classes import EE22_HumanMadeObject

entity = EE22_HumanMadeObject(id="test", label="Test Object")
print(entity.model_dump())
```

#### Validate Step by Step

```python
# Test each step of your workflow
entities = [entity1, entity2]

# Test validation
validation_results = validate_batch_quantifiers(entities)
print(validation_results)

# Test rendering
markdown = to_markdown(entities[0], MarkdownStyle.CARD)
print(markdown)

# Test Cypher generation
cypher = generate_cypher_script(entities)
print(cypher)
```

---

## Resources

### Documentation

- **[Mission Statement](mission.md)**: Project goals and philosophy
- **[Development Plan](plan.md)**: Technical roadmap and architecture
- **[Testing Guide](testing.md)**: Comprehensive testing documentation
- **[HOWTOs](src/collie/docs/HOWTOs.md)**: Detailed modeling guide
- **[CIDOC CRM Standard](cidoc-crm-standard.md)**: Official specification

### External Resources

- **[CIDOC CRM Official Site](https://www.cidoc-crm.org/)**: The official CIDOC CRM specification
- **[Pydantic Documentation](https://pydantic.dev/)**: Data validation framework
- **[Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/)**: Cypher query language
- **[uv Documentation](https://github.com/astral-sh/uv)**: Modern Python package manager

### Community

- **[GitHub Repository](https://github.com/decisionnerd/collie)**: Source code and issues
- **[GitHub Discussions](https://github.com/decisionnerd/collie/discussions)**: Community discussions
- **[Issues](https://github.com/decisionnerd/collie/issues)**: Bug reports and feature requests

### Contributing

- **Code of Conduct**: Be respectful and inclusive
- **Contributing Guidelines**: Follow the guidelines in this document
- **Pull Request Process**: Submit PRs with clear descriptions
- **Issue Templates**: Use provided templates for bugs and features

---

## Conclusion

COLLIE provides a powerful, developer-friendly toolkit for working with CIDOC CRM in modern Python applications. Whether you're contributing to the project or using it in your own work, this guide should help you get the most out of COLLIE.

For questions, suggestions, or contributions, please don't hesitate to reach out through GitHub issues or discussions. We're committed to making COLLIE the best possible tool for the cultural heritage and information extraction community.

**Happy coding! 🎉**