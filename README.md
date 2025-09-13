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

> **📖 For a comprehensive getting started guide, see [QUICKSTART.md](QUICKSTART.md)**

### Installation

```bash
# Using uv (recommended)
uv add collie

# Or with pip
pip install collie
```

### Basic Usage

```python
from collie.models.generated.e_classes import EE22_HumanMadeObject
from collie.io.to_markdown import to_markdown, MarkdownStyle
from collie.io.to_cypher import generate_cypher_script

# Create a CRM entity (string IDs are automatically converted to UUIDs)
vase = EE22_HumanMadeObject(
    id="obj_001",  # Automatically converted to deterministic UUID
    label="Ancient Greek Vase",
    type=["E55:Vessel", "E55:Ceramic"]
)

# Render as Markdown for LLM consumption
markdown = to_markdown(vase, MarkdownStyle.CARD)
print(markdown)

# Generate Cypher for Neo4j/Memgraph
cypher = generate_cypher_script([vase])
print(cypher)
```

## 📋 Core Features

### 🤖 **AI-Powered Information Extraction**
- PydanticAI-powered text analysis for automatic entity extraction
- Intelligent parsing of biographical, historical, and cultural texts
- Automatic relationship detection between entities
- Support for complex narrative structures and temporal relationships

### 🏗️ **Pydantic Models**
- Complete CIDOC CRM v7.1.3 coverage (99 E-classes, 322 P-properties)
- Flexible UUID handling with automatic string-to-UUID conversion
- Canonical JSON schema with stable IDs and explicit cross-references
- Auto-generated from curated YAML specifications
- Deterministic UUID generation maintains consistency across runs

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

### 🔗 **NetworkX Integration**
- Direct conversion from CRM entities to NetworkX graphs
- Built-in social network analysis algorithms
- Community detection and centrality measures
- Temporal network analysis for historical data
- Interactive visualization capabilities

### 📊 **Visualization & Analysis**
- Interactive network plots with matplotlib and plotly
- Customizable node and edge styling based on CRM classes
- Timeline visualization for temporal relationships
- Export capabilities for presentations and reports

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

## 📓 Interactive Jupyter Notebook Demo

> **🎯 For hands-on exploration, try our comprehensive Jupyter notebook: [`COLLIE_Demo_Notebook.ipynb`](COLLIE_Demo_Notebook.ipynb)**

The notebook provides an interactive walkthrough of the complete COLLIE workflow with:
- **Step-by-step execution** of all 10 workflow steps
- **Live visualizations** and network analysis
- **Canonical JSON serialization** demonstration
- **Advanced examples** including batch processing
- **Real-time output** generation and file management

Perfect for learning, experimentation, and understanding how COLLIE enables async/future processing workflows!

## 🔄 Complete Workflow

```python
from collie.extraction import InformationExtractor
from collie.io.to_networkx import to_networkx_graph
from collie.visualization import plot_network_graph

# 1. Extract entities from source text using PydanticAI
extractor = InformationExtractor()
extraction_result = await extractor.extract_from_text("""
Albert Einstein was born on March 14, 1879, in Ulm, Germany. 
He developed the theory of relativity and won the Nobel Prize in 1921.
""")

# 2. Convert to CRM entities
from collie.models.base import CRMEntity
crm_entities = []
for entity in extraction_result.entities:
    crm_entity = CRMEntity(
        id=str(entity.id),
        class_code=entity.class_code,
        label=entity.label,
        notes=entity.description
    )
    crm_entities.append(crm_entity)

# 3. Serialize as canonical JSON (important for async/future processing)
json_data = [entity.model_dump(mode='json') for entity in crm_entities]

# 4. Render into Markdown for analysis and reporting
markdown_report = render_table(crm_entities)

# 5. Convert to NetworkX graph for social network analysis
graph = to_networkx_graph(crm_entities)

# 6. Perform network analysis
centrality = nx.degree_centrality(graph)
communities = nx.community.greedy_modularity_communities(graph)

# 7. Visualize the network
plot_network_graph(graph, title="Einstein's Life Network")

# 8. Export to Cypher for graph database persistence (optional)
cypher_script = generate_cypher_script(crm_entities)
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
# Run all tests (32 tests, all passing)
uv run pytest

# Run specific test suites
uv run pytest src/collie/tests/unit/
uv run pytest src/collie/tests/golden/

# Format and lint with modern tooling
uv run ruff format
uv run ruff check --fix

# Check code quality
uv run ruff check
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
- **Phase 2**: ✅ Complete - Advanced validation, performance, complete CRM coverage, and robust testing
- **Phase 3**: 📋 Planned - Profile packs and additional analysis tools

**Current Coverage**: 99 E-classes, 322 P-properties (complete CRM 7.1.3)  
**Test Status**: 32 tests passing (100% success rate)  
**CI/CD**: Modern GitHub Actions workflow with uv and ruff

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- CIDOC CRM Working Group for the foundational ontology
- Pydantic team for the excellent validation framework
- Neo4j community for Cypher language inspiration

---

**Made with ❤️ for the cultural heritage and information extraction community**