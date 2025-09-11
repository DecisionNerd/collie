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
- [ ] Implement advanced validation features (completeness profiles)
- [ ] Add performance testing for large batches
- [ ] Create additional example datasets
- [ ] Add CLI tools for code generation and validation

### Future Enhancements (Phase 3)
- [ ] Profile packs (Linked.Art-like profiles)
- [ ] Graph diff utilities
- [ ] LLM prompt packs for extraction tasks
- [ ] Importers for common museum/archive formats
- [ ] Web interface for entity browsing
- [ ] API endpoints for programmatic access

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

## Project Status
- **Phase 1 Complete**: Core CIDOC CRM implementation is scaffolded and ready for development
- **Phase 2 Major Progress**: Comprehensive YAML coverage, code generation, and UUID refactoring implemented
- **Architecture**: Follows plan.md exactly with codegen/, models/, io/, validators/, tests/, examples/
- **Coverage**: Now covers 99 E-classes and 64 P-properties (comprehensive CRM 7.1.3 coverage)
- **Code Generation**: Automated YAML → Pydantic model generation working
- **UUID Support**: All entities now use UUIDs for better uniqueness and data integrity
- **Testing**: Unit tests, golden tests, and validation tests implemented and updated for UUIDs
- **Documentation**: HOWTOs.md provides comprehensive modeling guide
- **Examples**: Museum object lifecycle example demonstrates complete workflow with UUIDs

## Notes
- Project has evolved from simple pydantic_ai demo to full CIDOC CRM toolkit
- All scaffolding follows the comprehensive plan in docs/plan.md
- Successfully refactored from string IDs to UUIDs for better data integrity
- UUIDs provide better uniqueness guarantees and follow best practices for entity identification
- All components (models, renderers, emitters, validators, tests) updated for UUID support
- Core functionality: JSON ↔ Markdown ↔ Cypher with CRM validation
- No RDF/OWL/JSON-LD dependencies as per mission
