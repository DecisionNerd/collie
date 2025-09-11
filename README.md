# COLLIE

**Classful Ontology for Life-Events Information Extraction**

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Tests](https://img.shields.io/badge/tests-pytest-blue.svg)](https://pytest.org/)
[![Package: uv](https://img.shields.io/badge/package%20manager-uv-orange.svg)](https://github.com/astral-sh/uv)
[![CIDOC CRM](https://img.shields.io/badge/CIDOC%20CRM-v7.1.3-green.svg)](https://www.cidoc-crm.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.0+-red.svg)](https://pydantic.dev/)
[![Neo4j Compatible](https://img.shields.io/badge/Neo4j-Compatible-blue.svg)](https://neo4j.com/)
[![Memgraph Compatible](https://img.shields.io/badge/Memgraph-Compatible-purple.svg)](https://memgraph.com/)

![COLLIE logo](collie-logo.png)

A developer-friendly toolkit for working with the **CIDOC CRM v7.1.3** in modern data workflows. COLLIE provides complete Pydantic models (99 classes, 322 properties), Markdown renderers, and Cypher emitters that bridge the gap between conceptual rigor and developer usability.

## 🎯 Why COLLIE?

Cultural heritage and information extraction projects often need a **CRM-compliant backbone** without the overhead of RDF stacks. COLLIE:

- ✅ Keeps the conceptual rigor of CIDOC CRM
- ✅ Provides lean, open-world Pydantic validation  
- ✅ Outputs formats directly usable by LLMs (Markdown) and LPGs (Cypher)
- ✅ Prioritizes ergonomics and performance for real-world extraction pipelines
- ✅ Zero RDF/OWL/JSON-LD dependencies

## 🚀 Quick Start

### Installation

```bash
# Using uv (recommended)
uv add collie

# Or with pip
pip install collie
```

### Basic Usage

```python
from collie.models.generated.e_classes import E22_Man_Made_Object
from collie.io.to_markdown import render_entity_card
from collie.io.to_cypher import emit_cypher_script

# Create a CRM entity
vase = E22_Man_Made_Object(
    id="192f3e61-b22d-4f94-a2cf-c6ae1418ee83",
    label="Ancient Greek Vase",
    type=["E55:Vessel", "E55:Ceramic"]
)

# Render as Markdown for LLM consumption
markdown = render_entity_card(vase)
print(markdown)

# Generate Cypher for Neo4j/Memgraph
cypher = emit_cypher_script([vase])
print(cypher)
```

## 📋 Core Features

### 🏗️ **Pydantic Models**
- Complete CIDOC CRM v7.1.3 coverage (99 E-classes, 322 P-properties)
- UUID-based entity identification
- Canonical JSON schema with stable IDs and explicit cross-references
- Auto-generated from curated YAML specifications

#### Class Naming Convention

Collie uses a consistent naming pattern for generated Python classes:

- **Official CIDOC CRM**: `E1`, `E2`, `E22`, `E96` (class codes)
- **Collie Python Classes**: `EE1_CRMEntity`, `EE2_TemporalEntity`, `EE22_HumanMadeObject`, `EE96_Purchase`
- **Pattern**: `E{code}_{label_without_spaces}`

**Examples:**
- `E1` "CRM Entity" → `EE1_CRMEntity`
- `E22` "Human-Made Object" → `EE22_HumanMadeObject`  
- `E96` "Purchase" → `EE96_Purchase`

The `EE` prefix identifies Collie-generated Python classes for CIDOC CRM Entities, making them easily distinguishable from the official CRM class codes.

### 📝 **Markdown Renderers**
- **Entity Cards**: Concise summaries optimized for LLM prompts
- **Detailed Narratives**: Rich descriptions with full context
- **Tabular Summaries**: Structured data presentation
- **Style Profiles**: Configurable output formatting

### 🔗 **Cypher Emitters**
- Idempotent MERGE/UNWIND scripts for graph databases
- Neo4j and Memgraph compatible
- Batched operations for performance
- Constraint helpers and relationship builders

### ✅ **Validation Framework**
- Cardinality enforcement (configurable from warnings to strict)
- Type alignment validation
- Quantifier rules and typing constraints
- Extensible validation profiles

## 🔄 Complete Workflow

```python
# 1. Extract entities from source data
entities = extract_from_text("Ancient Greek vase from 5th century BCE...")

# 2. Serialize as canonical JSON using Pydantic models
json_data = [entity.model_dump() for entity in entities]

# 3. Render into Markdown for LLM prompts
markdown_report = render_narrative(entities)

# 4. Emit Cypher scripts for graph database
cypher_script = emit_cypher_script(entities)
```

## 📊 Example Output

### Markdown Card
```markdown
## 🏺 Ancient Greek Vase
**Type**: E22 Man-Made Object  
**Categories**: Vessel, Ceramic  
**Current Location**: Metropolitan Museum of Art  
**Production**: 5th Century BCE, Athens, Greece  

A beautifully preserved amphora from the 5th century BCE...
```

### Cypher Script
```cypher
MERGE (e22:E22_Man_Made_Object {id: "192f3e61-b22d-4f94-a2cf-c6ae1418ee83"})
SET e22.label = "Ancient Greek Vase",
    e22.type = ["E55:Vessel", "E55:Ceramic"]
```

## 🏛️ CIDOC CRM Background

The CIDOC Conceptual Reference Model (CIDOC CRM) is a formal ontology designed to facilitate the integration, mediation and interchange of heterogeneous cultural heritage information. COLLIE implements CRM v7.1.3 with a focus on:

- **Semantic interoperability** across different data sources
- **Formal ontology** for cultural heritage documentation
- **Extensible framework** for specialized communities
- **Developer-friendly** implementation without RDF complexity

## 📁 Project Structure

```
collie/
├── models/           # Pydantic CRM models
│   ├── base.py      # Base classes and utilities
│   └── generated/   # Auto-generated E-classes
├── io/              # Input/output modules
│   ├── to_markdown.py  # Markdown renderers
│   └── to_cypher.py    # Cypher emitters
├── validators/      # Validation framework
├── codegen/         # YAML → Pydantic generation
├── examples/        # Sample data and workflows
└── tests/           # Comprehensive test suite
```

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run specific test suites
uv run pytest tests/unit/
uv run pytest tests/golden/

# Format and lint
uv run ruff format
uv run ruff check --fix
```

## 📚 Documentation

- **[Mission Statement](docs/mission.md)** - Project goals and philosophy
- **[Development Plan](docs/plan.md)** - Technical roadmap and architecture
- **[HOWTOs](src/collie/docs/HOWTOs.md)** - Comprehensive modeling guide
- **[CIDOC CRM Standard](docs/cidoc-crm-standard.md)** - Official specification

## 🤝 Contributing

We welcome contributions! Please see our [development guidelines](docs/plan.md) and:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## 📈 Project Status

- **Phase 1**: ✅ Complete - Core CIDOC CRM implementation
- **Phase 2**: ✅ Complete - Advanced validation, performance, and complete CRM coverage
- **Phase 3**: 📋 Planned - Profile packs and web interface

**Current Coverage**: 99 E-classes, 322 P-properties (complete CRM 7.1.3)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- CIDOC CRM Working Group for the foundational ontology
- Pydantic team for the excellent validation framework
- Neo4j community for Cypher language inspiration

---

**Made with ❤️ for the cultural heritage and information extraction community**