# Testing Guide for React Newsletter Application

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setting Up the Testing Environment](#setting-up-the-testing-environment)
- [Running Tests](#running-tests)
- [Types of Tests](#types-of-tests)
- [Writing New Tests](#writing-new-tests)
- [Continuous Integration](#continuous-integration)
- [Best Practices](#best-practices)

## Prerequisites

Before running tests, ensure you have:
- Python 3.9+ installed
- Virtual environment created and activated
- All dependencies installed from requirements.txt and test-requirements.txt

## Setting Up the Testing Environment

1. Create and activate a virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Unix/MacOS
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r test-requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your test configuration
```

## Running Tests

### Running All Tests
```bash
python -m pytest
```

### Running Specific Test Files
```bash
python -m pytest tests/test_newsletter.py
```

### Running Tests with Coverage Report
```bash
python -m pytest --cov=src tests/
```

### Running Tests with Verbose Output
```bash
python -m pytest -v
```

## Types of Tests

### Unit Tests
Located in `tests/unit/`
- Test individual components and functions
- Should be quick to run
- No external dependencies

```bash
python -m pytest tests/unit/
```

### Integration Tests
Located in `tests/integration/`
- Test interaction between components
- May require test database
- Slower than unit tests

```bash
python -m pytest tests/integration/
```

### E2E Tests
Located in `tests/e2e/`
- Test complete user workflows
- Require full test environment
- Slowest to run

```bash
python -m pytest tests/e2e/
```

## Writing New Tests

### Test File Structure
```python
# test_component.py
import pytest
from src.component import Component

def test_component_functionality():
    # Arrange
    component = Component()
    
    # Act
    result = component.do_something()
    
    # Assert
    assert result == expected_result
```

### Using Fixtures
```python
# conftest.py
import pytest

@pytest.fixture
def test_database():
    # Setup test database
    db = setup_test_db()
    yield db
    # Teardown
    db.cleanup()
```

### Mocking Dependencies
```python
from unittest.mock import Mock, patch

@patch('src.component.external_service')
def test_with_mock(mock_service):
    mock_service.return_value = expected_value
    # Test code here
```

## Continuous Integration

### GitHub Actions
Tests automatically run on:
- Push to main branch
- Pull request to main branch
- Daily scheduled runs

Configuration file: `.github/workflows/tests.yml`

### Local CI Checks
Run before committing:
```bash
# Run linting
flake8 src tests

# Run type checking
mypy src

# Run all tests
python -m pytest
```

## Best Practices

1. **Test Isolation**: Each test should be independent and not rely on other tests.

2. **Naming Conventions**:
   - Test files: `test_*.py`
   - Test functions: `test_*`
   - Clear, descriptive names

3. **Arrange-Act-Assert Pattern**:
   ```python
   def test_example():
       # Arrange
       data = setup_test_data()
       
       # Act
       result = process_data(data)
       
       # Assert
       assert result.is_valid()
   ```

4. **Use Meaningful Assertions**:
   ```python
   # Good
   assert user.is_active, "User should be active after activation"
   
   # Avoid
   assert user.is_active == True
   ```

5. **Test Edge Cases**:
   - Empty inputs
   - Boundary conditions
   - Error conditions
   - Invalid inputs

6. **Keep Tests Fast**:
   - Mock external services
   - Use test databases
   - Avoid unnecessary setup

## Troubleshooting

Common Issues and Solutions:

1. **Tests Hanging**:
   - Check for infinite loops
   - Verify timeouts
   - Check resource cleanup

2. **Random Failures**:
   - Look for race conditions
   - Check for test interdependencies
   - Verify cleanup procedures

3. **Import Errors**:
   - Verify PYTHONPATH
   - Check virtual environment
   - Verify package installation

## Getting Help

If you encounter issues:
1. Check the test logs
2. Review the documentation
3. Contact the development team
4. Create an issue in the repository

## Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Maintain test coverage
3. Follow existing patterns
4. Update documentation

---

For more information, contact the development team or refer to the project documentation.