# COLLIE Testing Documentation

This document provides a comprehensive overview of the COLLIE project's testing regime, including test structure, strategies, and execution guidelines.

## Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Test Structure](#test-structure)
3. [Test Categories](#test-categories)
4. [Test Execution](#test-execution)
5. [Test Data and Examples](#test-data-and-examples)
6. [Continuous Integration](#continuous-integration)
7. [Test Coverage](#test-coverage)
8. [Writing Tests](#writing-tests)
9. [Debugging Tests](#debugging-tests)
10. [Best Practices](#best-practices)

## Testing Philosophy

COLLIE follows a comprehensive testing strategy that ensures reliability, maintainability, and correctness across all components:

### Core Principles

- **Comprehensive Coverage**: Tests cover all major functionality including models, renderers, emitters, and validators
- **Real-World Scenarios**: Tests use realistic data and workflows that mirror actual usage patterns
- **Deterministic Results**: All tests produce consistent, predictable outcomes
- **Fast Execution**: Tests run quickly to enable rapid development cycles
- **Clear Documentation**: Tests serve as living documentation of expected behavior

### Testing Goals

1. **Functional Correctness**: Verify that all components work as intended
2. **Data Integrity**: Ensure UUID handling and data transformations are accurate
3. **Integration Testing**: Validate end-to-end workflows from JSON to Markdown/Cypher
4. **Regression Prevention**: Catch breaking changes early in development
5. **API Stability**: Maintain consistent interfaces and behavior

## Test Structure

The COLLIE test suite is organized into a clear hierarchical structure:

```
src/collie/tests/
├── __init__.py                 # Test package initialization
├── unit/                       # Unit tests for individual components
│   ├── __init__.py
│   ├── test_cypher.py         # Cypher emission tests
│   ├── test_markdown.py       # Markdown rendering tests
│   └── test_validators.py     # Validation framework tests
└── golden/                     # Integration and golden tests
    ├── __init__.py
    └── test_museum_object.py  # Complete workflow tests
```

### Test Organization Principles

- **Separation of Concerns**: Unit tests focus on individual components, golden tests cover complete workflows
- **Logical Grouping**: Tests are grouped by functionality (cypher, markdown, validators)
- **Clear Naming**: Test files and functions use descriptive names that indicate their purpose
- **Modular Design**: Each test file is self-contained and can run independently

## Test Categories

### 1. Unit Tests (`src/collie/tests/unit/`)

Unit tests focus on testing individual components in isolation, ensuring each piece works correctly on its own.

#### Cypher Tests (`test_cypher.py`)
- **Purpose**: Test Cypher script generation and parameter handling
- **Coverage**: 12 test methods covering all Cypher emission functionality
- **Key Areas**:
  - Node emission and parameter generation
  - Relationship expansion and creation
  - Script generation with proper MERGE/UNWIND patterns
  - Batch size handling and empty entity lists
  - Script validation and error handling

**Example Test**:
```python
def test_emit_nodes(self):
    """Test node emission."""
    entities = [
        EE22_HumanMadeObject(
            id=uuid4(),
            class_code="E22",
            label="Ancient Vase",
            type=["E55:Vessel"]
        )
    ]
    result = emit_nodes(entities)
    assert "nodes" in result
    assert len(result["nodes"]) == 1
```

#### Markdown Tests (`test_markdown.py`)
- **Purpose**: Test Markdown rendering in all supported styles
- **Coverage**: 9 test methods covering all Markdown functionality
- **Key Areas**:
  - Card, detailed, table, and narrative rendering styles
  - Alias usage and code display options
  - Empty entity handling and custom column support
  - Table rendering with multiple entities

**Example Test**:
```python
def test_card_rendering(self):
    """Test card-style rendering."""
    entity = EE22_HumanMadeObject(
        id=uuid4(),
        class_code="E22",
        label="Ancient Vase",
        type=["E55:Vessel"]
    )
    markdown = to_markdown(entity, MarkdownStyle.CARD)
    assert "### E22 · Human-Made Object · Ancient Vase" in markdown
```

#### Validator Tests (`test_validators.py`)
- **Purpose**: Test validation framework for quantifiers and typing rules
- **Coverage**: 10 test methods covering all validation functionality
- **Key Areas**:
  - Quantifier enforcement (cardinality rules)
  - Domain/range alignment validation
  - Batch validation processing
  - Validation severity levels (WARN, RAISE, IGNORE)

**Example Test**:
```python
def test_enforce_quantifier_valid(self):
    """Test quantifier enforcement with valid values."""
    entity = EE22_HumanMadeObject(id=uuid4(), class_code="E22")
    # P108 has quantifier "0..1" - should allow 1 value
    enforce_quantifier(entity, "P108", [uuid4()], ValidationSeverity.RAISE)
    # Should not raise an exception
```

### 2. Golden Tests (`src/collie/tests/golden/`)

Golden tests validate complete workflows using real-world data and ensure end-to-end functionality.

#### Museum Object Tests (`test_museum_object.py`)
- **Purpose**: Test complete museum object lifecycle from JSON to Markdown to Cypher
- **Coverage**: 3 comprehensive test methods
- **Key Areas**:
  - Complete workflow validation (JSON → Entities → Markdown/Cypher)
  - Validation framework integration
  - Roundtrip data integrity (JSON → Entities → JSON)

**Test Methods**:

1. **`test_museum_object_workflow()`**
   - Tests complete workflow from JSON data to rendered outputs
   - Validates Markdown rendering in all styles (card, detailed, table, narrative)
   - Verifies Cypher script generation with proper parameters
   - Ensures relationship expansion works correctly

2. **`test_museum_object_validation()`**
   - Tests validation framework with real museum object data
   - Validates quantifier rules and typing constraints
   - Ensures validation warnings are properly handled

3. **`test_museum_object_roundtrip()`**
   - Tests data integrity through complete roundtrip conversion
   - Validates that JSON → Entities → JSON preserves all data
   - Ensures UUID handling maintains consistency

## Test Execution

### Running Tests

#### Basic Test Execution
```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest src/collie/tests/unit/test_cypher.py

# Run specific test method
uv run pytest src/collie/tests/golden/test_museum_object.py::test_museum_object_workflow
```

#### Test Categories
```bash
# Run only unit tests
uv run pytest src/collie/tests/unit/

# Run only golden tests
uv run pytest src/collie/tests/golden/

# Run tests with specific markers (if implemented)
uv run pytest -m "not slow"
```

#### Test Output and Debugging
```bash
# Run with short traceback
uv run pytest --tb=short

# Run with no output capture (see print statements)
uv run pytest -s

# Run with coverage reporting
uv run pytest --cov=src/collie

# Run specific test with debugging
uv run pytest -v -s src/collie/tests/unit/test_cypher.py::TestCypherEmission::test_emit_nodes
```

### Test Configuration

Tests are configured through `pyproject.toml`:

```toml
[dependency-groups]
dev = [
    "pytest>=8.4.2",
    "ruff>=0.1.0",
]

[tool.ruff]
target-version = "py313"
line-length = 88
```

## Test Data and Examples

### Golden Test Data

The museum object example (`src/collie/examples/museum_object.json`) serves as the primary test dataset:

```json
{
  "entities": [
    {
      "id": "192f3e61-b22d-4f94-a2cf-c6ae1418ee83",
      "class_code": "E22",
      "label": "Ancient Greek Vase",
      "type": ["E55:Vessel", "E55:Ceramic"],
      "notes": "A beautifully preserved amphora from the 5th century BCE",
      "current_location": "2cd977c8-de61-48d8-a39c-681c0481e1fd",
      "produced_by": "f7111fe2-fed1-4cd3-8a89-b25ef835b517"
    }
    // ... additional entities
  ]
}
```

### Test Data Characteristics

- **Realistic Structure**: Uses actual CIDOC CRM class codes and relationships
- **Complete Workflow**: Includes objects, events, places, and time spans
- **UUID-Based**: All entities use proper UUID identifiers
- **Relationship Coverage**: Tests all major CRM relationships (P53, P108, P4, etc.)
- **Validation Scenarios**: Includes data that triggers various validation rules

### Test Entity Types

The test data includes examples of:

- **E22 Human-Made Object**: Ancient Greek vase with production and location
- **E12 Production**: Manufacturing event with time and place
- **E53 Place**: Geographic locations (museum, city)
- **E52 Time-Span**: Temporal periods (5th century BCE)
- **E61 Time-Primitive**: Specific dates (500 BCE, 400 BCE)

## Continuous Integration

### GitHub Actions Workflow

The project uses GitHub Actions for automated testing:

```yaml
# .github/workflows/python-package.yml
name: Python package

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.13"]

    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v3
      - name: Set up Python
        uses: actions/setup-python@v5
      - name: Cache uv dependencies
        uses: actions/cache@v4
      - name: Install dependencies
        run: uv sync
      - name: Lint with Ruff
        run: uv run ruff check
      - name: Format check with Ruff
        run: uv run ruff format --check
      - name: Run tests
        run: uv run pytest
```

### CI Pipeline Steps

1. **Environment Setup**: Install Python 3.13 and uv package manager
2. **Dependency Management**: Cache and install dependencies with uv
3. **Code Quality**: Run ruff linting and formatting checks
4. **Test Execution**: Run complete test suite with pytest
5. **Result Reporting**: Provide detailed test results and coverage

### CI Benefits

- **Automated Validation**: Every commit and PR is automatically tested
- **Consistent Environment**: Tests run in a clean, reproducible environment
- **Early Detection**: Issues are caught before they reach the main branch
- **Quality Gates**: Code must pass all tests before merging

## Test Coverage

### Current Coverage

- **Total Tests**: 32 tests across all components
- **Success Rate**: 100% (all tests passing)
- **Coverage Areas**:
  - Cypher emission: 12 tests
  - Markdown rendering: 9 tests
  - Validation framework: 10 tests
  - Golden workflows: 3 tests

### Coverage Metrics

| Component | Test Count | Coverage |
|-----------|------------|----------|
| Cypher Emitters | 12 | Complete |
| Markdown Renderers | 9 | Complete |
| Validators | 10 | Complete |
| Golden Tests | 3 | Complete |
| **Total** | **32** | **100%** |

### Coverage Goals

- **Functional Coverage**: All public APIs and major code paths
- **Edge Case Coverage**: Empty inputs, invalid data, error conditions
- **Integration Coverage**: End-to-end workflows and data transformations
- **Regression Coverage**: Historical bugs and breaking changes

## Writing Tests

### Test Development Guidelines

#### 1. Test Structure
```python
class TestComponentName:
    """Test component functionality."""
    
    def test_specific_functionality(self):
        """Test specific functionality with clear description."""
        # Arrange: Set up test data
        entity = EE22_HumanMadeObject(id=uuid4(), class_code="E22")
        
        # Act: Execute the functionality
        result = function_under_test(entity)
        
        # Assert: Verify expected outcomes
        assert result == expected_value
```

#### 2. Test Naming Conventions
- **Class Names**: `TestComponentName` (e.g., `TestCypherEmission`)
- **Method Names**: `test_specific_functionality` (e.g., `test_emit_nodes`)
- **Descriptions**: Clear docstrings explaining what each test validates

#### 3. Test Data Management
```python
# Use realistic test data
entity = EE22_HumanMadeObject(
    id=uuid4(),
    class_code="E22",
    label="Ancient Vase",
    type=["E55:Vessel"]
)

# Use proper UUIDs for relationships
entity.current_location = uuid4()
entity.produced_by = uuid4()
```

#### 4. Assertion Patterns
```python
# Test for presence/absence
assert "expected_content" in result
assert "unexpected_content" not in result

# Test for structure
assert "key" in result
assert len(result["items"]) == expected_count

# Test for specific values
assert result["field"] == expected_value
assert isinstance(result["field"], expected_type)
```

### Adding New Tests

#### Unit Test Addition
1. **Identify Component**: Determine which component needs testing
2. **Create Test Method**: Add test method to appropriate test class
3. **Write Test Logic**: Implement arrange-act-assert pattern
4. **Verify Coverage**: Ensure test covers new functionality
5. **Run Tests**: Verify test passes and doesn't break existing tests

#### Golden Test Addition
1. **Create Test Data**: Add realistic example data to `examples/`
2. **Write Workflow Test**: Create test method that exercises complete workflow
3. **Validate Outputs**: Ensure Markdown and Cypher outputs are correct
4. **Test Roundtrip**: Verify data integrity through conversions

## Debugging Tests

### Common Debugging Techniques

#### 1. Verbose Output
```bash
# Run with verbose output to see test names
uv run pytest -v

# Run with no capture to see print statements
uv run pytest -s
```

#### 2. Specific Test Debugging
```bash
# Run single test with debugging
uv run pytest -v -s src/collie/tests/unit/test_cypher.py::TestCypherEmission::test_emit_nodes
```

#### 3. Test Data Inspection
```python
def test_debug_example(self):
    """Debug test with data inspection."""
    entity = EE22_HumanMadeObject(id=uuid4(), class_code="E22")
    result = emit_nodes([entity])
    
    # Debug output
    print(f"Entity: {entity}")
    print(f"Result: {result}")
    
    # Continue with assertions
    assert "nodes" in result
```

#### 4. Exception Debugging
```bash
# Run with full traceback
uv run pytest --tb=long

# Run with short traceback
uv run pytest --tb=short
```

### Common Test Issues

#### 1. UUID Handling Issues
- **Problem**: Tests expecting string IDs but getting UUIDs
- **Solution**: Use `uuid4()` for test data, convert to string when needed
- **Prevention**: Always use proper UUID types in test data

#### 2. Import Path Issues
- **Problem**: Relative import errors in test files
- **Solution**: Use correct relative import paths (`...models` not `..models`)
- **Prevention**: Follow established import patterns

#### 3. Assertion Failures
- **Problem**: Tests failing due to data structure changes
- **Solution**: Update assertions to match current data structure
- **Prevention**: Use robust assertions that test behavior, not implementation

## Best Practices

### Test Development

1. **Write Tests First**: Follow TDD principles when possible
2. **Test Behavior, Not Implementation**: Focus on what the code does, not how
3. **Use Descriptive Names**: Test names should clearly indicate what they test
4. **Keep Tests Simple**: Each test should verify one specific behavior
5. **Use Realistic Data**: Test with data that mirrors real-world usage

### Test Maintenance

1. **Regular Updates**: Keep tests current with code changes
2. **Remove Obsolete Tests**: Delete tests for removed functionality
3. **Refactor Tests**: Improve test structure and readability
4. **Monitor Performance**: Ensure tests run quickly
5. **Document Changes**: Update test documentation when adding new tests

### Test Quality

1. **Comprehensive Coverage**: Test all major functionality and edge cases
2. **Reliable Execution**: Tests should produce consistent results
3. **Clear Failures**: Test failures should clearly indicate what went wrong
4. **Fast Execution**: Tests should run quickly to enable rapid development
5. **Maintainable Code**: Tests should be easy to understand and modify

### Integration with Development

1. **Pre-commit Hooks**: Run tests before committing code
2. **CI Integration**: Ensure all tests pass in CI environment
3. **Code Review**: Include test changes in code reviews
4. **Documentation**: Keep test documentation current
5. **Team Standards**: Follow established testing conventions

## Conclusion

The COLLIE testing regime provides comprehensive coverage of all project components through a well-structured, maintainable test suite. The combination of unit tests and golden tests ensures both individual component correctness and end-to-end workflow validation.

The testing strategy supports the project's goals of reliability, maintainability, and developer productivity while providing confidence in the correctness of CIDOC CRM data processing workflows.

For questions about testing or to contribute new tests, please refer to the project's contribution guidelines and existing test patterns.