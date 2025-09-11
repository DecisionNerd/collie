# Collie Project Todo List

## Current Tasks

### CIDOC CRM Implementation (Phase 1)
- [x] Scaffold complete folder structure according to plan.md
- [x] Create YAML specifications (crm_classes.yaml, crm_properties.yaml, aliases.yaml)
- [x] Implement base CRM entity models and ergonomic wrappers
- [x] Create auto-generated properties registry
- [x] Implement Markdown renderers (card, detailed, table, narrative)
- [x] Implement Cypher emitters with idempotent MERGE/UNWIND
- [x] Create validation utilities (quantifiers, typing rules)
- [x] Add comprehensive test suite (unit tests, golden tests)
- [x] Create example data and documentation

### Next Steps (Phase 2)
- [x] Run code generation scripts to update models from YAML
- [x] Add more comprehensive YAML coverage for all CRM 7.1.3 classes/properties
- [x] Complete CIDOC CRM v7.1.3 coverage (99 classes, 322 properties)
- [x] Fix duplicate class definitions and regenerate models
- [x] Test generated code for correctness
- [x] Fix all test failures and improve test robustness
- [x] Implement flexible UUID handling for better developer ergonomics
- [x] Modernize GitHub Actions workflow with uv and ruff
- [x] Refactor mission to emphasize NetworkX for social network analysis workflows
- [x] Implement NetworkX integration utilities (JSON → NetworkX graph construction)
- [x] Add NetworkX analysis examples and algorithms
- [x] Implement AI-powered information extraction with PydanticAI
- [x] Create comprehensive visualization utilities (matplotlib + Plotly)
- [x] Implement complete workflow: text → AI extraction → CRM entities → Markdown → NetworkX → visualization
- [x] Add comprehensive CLI with multiple commands (extract, analyze, workflow, demo)
- [x] Create Einstein biography demo showcasing complete workflow
- [x] Add comprehensive test suite for NetworkX integration and visualization
- [ ] Implement advanced validation features (completeness profiles)
- [ ] Add performance testing for large batches
- [ ] Create additional example datasets
- [ ] Add CLI tools for code generation and validation

### Future Enhancements (Phase 3)
- [x] NetworkX visualization utilities and interactive plots
- [ ] Profile packs (Linked.Art-like profiles)
- [ ] Graph diff utilities
- [ ] LLM prompt packs for extraction tasks
- [ ] Importers for common museum/archive formats
- [ ] Web interface for entity browsing with NetworkX visualizations
- [ ] API endpoints for programmatic access
- [x] Advanced NetworkX algorithms integration (community detection, centrality measures)

## Completed Tasks
- [x] Create agent workflow rule for documentation-driven development
- [x] Fix missing `os` import in main.py
- [x] Fix async main() function call
- [x] Handle missing GOOGLE_API_KEY environment variable gracefully
- [x] Add .env file loading capability (python-dotenv)
- [x] Fix asyncio event loop issue in async calls
- [x] Move code into src folder structure
- [x] Scaffold complete CIDOC CRM project structure
- [x] Create comprehensive YAML specifications
- [x] Implement core Pydantic models and base classes
- [x] Create properties registry with domain/range lookups
- [x] Implement Markdown rendering system
- [x] Implement Cypher emission system
- [x] Create validation framework
- [x] Add comprehensive test suite
- [x] Create example data and documentation
- [x] Refactor GitHub Actions workflow to use modern uv and ruff tooling
- [x] Add ruff as development dependency with proper configuration
- [x] Fix all test failures and improve test robustness
- [x] Implement flexible UUID validator for better developer ergonomics
- [x] Fix import path issues in test files
- [x] Add missing __init__.py files to test directories
- [x] Update test assertions to work with UUID formatting
- [x] Fix entity lookup logic in tests to use actual data
- [x] Update Cypher tests to use proper UUIDs
- [x] Fix table rendering to use correct render_table() function

## Project Status
- **Phase 1 Complete**: Core CIDOC CRM implementation is scaffolded and ready for development
- **Phase 2 Complete**: Comprehensive YAML coverage, code generation, UUID refactoring, complete CIDOC CRM v7.1.3 coverage, robust testing, AI-powered extraction, NetworkX integration, and visualization implemented
- **Architecture**: Follows plan.md exactly with codegen/, models/, io/, validators/, tests/, examples/, extraction/, visualization/
- **Coverage**: Now covers 99 E-classes and 322 P-properties (complete CRM 7.1.3 coverage)
- **Code Generation**: Automated YAML → Pydantic model generation working
- **UUID Support**: Flexible UUID handling with deterministic generation from string IDs for better developer ergonomics
- **AI Integration**: PydanticAI-powered information extraction from unstructured text
- **NetworkX Integration**: Complete graph analysis with centrality measures, community detection, and visualization
- **Visualization**: Both static (matplotlib) and interactive (Plotly) network visualizations
- **CLI**: Comprehensive command-line interface with extract, analyze, workflow, and demo commands
- **Testing**: All 47 tests passing (unit tests, golden tests, validation tests, NetworkX integration tests) with robust assertions
- **CI/CD**: Modern GitHub Actions workflow with uv package management and ruff linting/formatting
- **Documentation**: Comprehensive guides including QUICKSTART.md for rapid onboarding and interactive Jupyter notebook demo
- **Examples**: Einstein biography demo showcases complete AI-powered workflow
- **Interactive Learning**: Comprehensive Jupyter notebook (`COLLIE_Demo_Notebook.ipynb`) with 31 cells covering complete workflow

## Notes
- Project has evolved from simple pydantic_ai demo to full CIDOC CRM toolkit
- All scaffolding follows the comprehensive plan in docs/plan.md
- Successfully implemented flexible UUID handling that maintains "IDs first" principle while supporting developer ergonomics
- All components (models, renderers, emitters, validators, tests) updated for robust UUID support
- Core functionality: JSON ↔ NetworkX ↔ Markdown ↔ Cypher with CRM validation
- Mission refactored to emphasize NetworkX as primary graph analysis framework for database-agnostic workflows
- No RDF/OWL/JSON-LD dependencies as per mission
- Modern development workflow with uv package management and ruff code quality tools
- All tests passing with comprehensive coverage of core functionality
- Ready for NetworkX integration implementation as next priority
