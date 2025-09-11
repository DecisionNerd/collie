# CIDOC CRM Modeling Guide

This guide provides practical examples and patterns for modeling cultural heritage data using the Collie toolkit with NetworkX integration for social network analysis.

## Table of Contents

1. [Interactive Jupyter Notebook Demo](#interactive-jupyter-notebook-demo)
2. [Understanding Class Naming](#understanding-class-naming)
3. [Basic Entity Creation](#basic-entity-creation)
4. [Modeling Events](#modeling-events)
5. [Modeling Objects](#modeling-objects)
6. [Modeling People and Groups](#modeling-people-and-groups)
7. [Modeling Places and Time](#modeling-places-and-time)
8. [Working with Relationships](#working-with-relationships)
9. [AI-Powered Information Extraction](#ai-powered-information-extraction)
10. [NetworkX Integration](#networkx-integration)
11. [Validation and Quality Control](#validation-and-quality-control)
12. [Exporting to Markdown](#exporting-to-markdown)
13. [Exporting to Cypher](#exporting-to-cypher)

## Interactive Jupyter Notebook Demo

> **🎯 For hands-on exploration: [`COLLIE_Demo_Notebook.ipynb`](../COLLIE_Demo_Notebook.ipynb)**

The best way to learn COLLIE is through our comprehensive Jupyter notebook that provides an interactive walkthrough of the complete workflow. The notebook includes:

### What You'll Learn

- **Complete Workflow**: All 10 steps from AI extraction to graph database export
- **Canonical JSON Serialization**: The crucial step for async/future processing
- **Live Visualizations**: Interactive network plots and analysis
- **Advanced Examples**: Batch processing, custom entities, and data loading
- **Real-time Output**: See results as you execute each step

### Notebook Features

- **31 Interactive Cells**: Step-by-step execution with detailed explanations
- **Sample Data**: Albert Einstein biography for demonstration
- **Output Generation**: Creates `notebook_output/` directory with all results
- **Educational**: Perfect for learning and experimentation
- **Comprehensive**: Covers the entire COLLIE ecosystem

### Getting Started

1. **Open the notebook** in Jupyter Lab or Jupyter Notebook
2. **Run cells sequentially** to follow the complete workflow
3. **Experiment** with different texts and parameters
4. **Explore** the generated visualizations and data
5. **Use outputs** for further analysis or graph database import

The notebook emphasizes the **canonical JSON serialization step** as the crucial bridge between AI extraction and future processing, making it perfect for understanding how COLLIE enables async workflows and graph database integration!

## Understanding Class Naming

### The E vs EE Convention

Collie uses a specific naming convention to distinguish between official CIDOC CRM class codes and generated Python classes:

#### Official CIDOC CRM Classes
- **Format**: `E1`, `E2`, `E22`, `E96`, etc.
- **Purpose**: Official class codes from CIDOC CRM v7.1.3 specification
- **Usage**: Referenced in documentation, YAML specifications, and as `class_code` field values

#### Collie Generated Python Classes  
- **Format**: `EE1_CRMEntity`, `EE2_TemporalEntity`, `EE22_HumanMadeObject`, `EE96_Purchase`
- **Pattern**: `E{code}_{label_without_spaces}`
- **Purpose**: Actual Python classes you import and instantiate

#### Naming Breakdown

```python
# Official CIDOC CRM class code
E22 = "Human-Made Object"

# Collie generated Python class
EE22_HumanMadeObject = class EE22_HumanMadeObject(EE19_PhysicalObject):
    """CIDOC CRM E22: Human-Made Object"""
    class_code: str = "E22"
```

**Components:**
- `E` = Python class prefix
- `22` = CIDOC CRM class code  
- `_` = Separator
- `HumanMadeObject` = Label with spaces/hyphens removed

#### Common Examples

| CIDOC CRM Code | CIDOC CRM Label | Collie Python Class |
|----------------|-----------------|-------------------|
| `E1` | CRM Entity | `EE1_CRMEntity` |
| `E2` | Temporal Entity | `EE2_TemporalEntity` |
| `E5` | Event | `EE5_Event` |
| `E7` | Activity | `EE7_Activity` |
| `E8` | Acquisition | `EE8_Acquisition` |
| `E12` | Production | `EE12_Production` |
| `E18` | Physical Thing | `EE18_PhysicalThing` |
| `E19` | Physical Object | `EE19_PhysicalObject` |
| `E20` | Biological Object | `EE20_BiologicalObject` |
| `E21` | Person | `EE21_Person` |
| `E22` | Human-Made Object | `EE22_HumanMadeObject` |
| `E39` | Actor | `EE39_Actor` |
| `E40` | Legal Body | `EE40_LegalBody` |
| `E53` | Place | `EE53_Place` |
| `E96` | Purchase | `EE96_Purchase` |

#### Why This Convention?

1. **Clear Distinction**: Immediately identifies Collie-generated classes vs official CRM codes
2. **Python Compatibility**: Creates valid Python class names
3. **Official Compliance**: Preserves official CIDOC CRM class codes
4. **Developer Friendly**: Human-readable class names with clear purpose

#### Importing Classes

```python
# Import specific classes
from collie.models.generated.e_classes import (
    EE1_CRMEntity,
    EE22_HumanMadeObject, 
    EE21_Person,
    EE53_Place
)

# Import all classes
from collie.models.generated.e_classes import *
```

#### Historical Note: The EEE Bug

During development, there was a bug that generated classes with `EEE` prefix (e.g., `EEE1_CRMEntity`). This was caused by the code generation script incorrectly adding an extra "E" prefix. This has been fixed, and all classes now use the correct `EE` prefix.

## Basic Entity Creation

### Understanding UUID Handling

Collie uses flexible UUID handling that maintains the "IDs first" principle while supporting developer ergonomics:

#### Automatic UUID Conversion
- **String IDs**: Automatically converted to deterministic UUIDs using MD5 hashing
- **UUID Objects**: Used directly without conversion
- **Deterministic**: Same string always produces the same UUID
- **Backward Compatible**: Works with existing string-based ID systems

```python
# These will produce the same UUID every time
entity1 = CRMEntity(id="obj_001", class_code="E22")
entity2 = CRMEntity(id="obj_001", class_code="E22")
assert entity1.id == entity2.id  # True - same UUID

# UUIDs are displayed in shortened format for readability
print(entity1.id)  # Shows: 192f3e61... (first 8 chars + "...")
```

#### UUID Benefits
- **Uniqueness**: Better uniqueness guarantees than string IDs
- **Consistency**: Same string always produces the same UUID
- **Performance**: UUIDs are more efficient for database operations
- **Standards**: Follows best practices for entity identification

### Creating a Simple Entity

```python
from collie.models.base import CRMEntity

# Create a basic CRM entity
entity = CRMEntity(
    id="obj_001",  # String IDs are automatically converted to deterministic UUIDs
    class_code="E22",
    label="Ancient Vase",
    type=["E55:Vessel", "E55:Ceramic"],
    notes="A beautifully preserved amphora"
)

# You can also use actual UUIDs
import uuid
entity_with_uuid = CRMEntity(
    id=uuid.uuid4(),  # Or use a specific UUID string
    class_code="E22",
    label="Ancient Vase"
)
```

### Using Ergonomic Wrappers

```python
from collie.models.base import E22_HumanMadeObject

# Use the ergonomic wrapper for human-made objects
vase = E22_HumanMadeObject(
    id="obj_001",
    label="Ancient Vase",
    type=["E55:Vessel", "E55:Ceramic"],
    current_location="place_001",
    produced_by="prod_001"
)
```

## Modeling Events

### Production Events

```python
from collie.models.base import E12_Production

# Create a production event
production = E12_Production(
    id="prod_001",
    label="Vase Production",
    type=["E55:Manufacturing"],
    timespan="timespan_001",
    took_place_at="place_002"
)
```

### Acquisition Events

```python
from collie.models.base import E8_Acquisition

# Create an acquisition event
acquisition = E8_Acquisition(
    id="acq_001",
    label="Museum Acquisition",
    type=["E55:Purchase"],
    timespan="timespan_002",
    took_place_at="place_001"
)
```

## Modeling Objects

### Human-Made Objects

```python
from collie.models.base import E22_HumanMadeObject

# Create a human-made object with production link
painting = E22_HumanMadeObject(
    id="obj_002",
    label="Mona Lisa",
    type=["E55:Painting", "E55:OilPainting"],
    current_location="place_003",
    produced_by="prod_002"
)
```

### Documents

```python
from collie.models.base import E31_Document

# Create a document
document = E31_Document(
    id="doc_001",
    label="Exhibition Catalog",
    type=["E55:Catalog", "E55:Publication"],
    notes="Official catalog for the 2023 exhibition"
)
```

## Modeling People and Groups

### Individuals

```python
from collie.models.base import E21_Person

# Create a person
artist = E21_Person(
    id="person_001",
    label="Leonardo da Vinci",
    type=["E55:Artist", "E55:Painter"],
    current_location="place_004"  # Current residence
)
```

### Groups

```python
from collie.models.base import E74_Group

# Create a group
museum = E74_Group(
    id="group_001",
    label="Louvre Museum",
    type=["E55:Museum", "E55:Institution"]
)
```

## Modeling Places and Time

### Places

```python
from collie.models.base import E53_Place

# Create a place
place = E53_Place(
    id="place_001",
    label="Paris, France",
    type=["E55:City", "E55:Capital"]
)
```

### Time-Spans

```python
from collie.models.base import E52_TimeSpan

# Create a time-span
timespan = E52_TimeSpan(
    id="timespan_001",
    label="Renaissance Period",
    type=["E55:TimePeriod"],
    begin_of_the_begin="time_001",
    end_of_the_end="time_002"
)
```

## Working with Relationships

### Expanding Shortcuts

```python
from collie.io.to_cypher import expand_shortcuts

# Expand shortcut fields to relationships
vase = E22_HumanMadeObject(
    id="obj_001",
    label="Ancient Vase",
    current_location="place_001",
    produced_by="prod_001"
)

# Get relationships from shortcuts
relationships = expand_shortcuts(vase)
# Returns: [
#   {"src": "obj_001", "type": "P53_HAS_CURRENT_LOCATION", "tgt": "place_001"},
#   {"src": "obj_001", "type": "P108_WAS_PRODUCED_BY", "tgt": "prod_001"}
# ]
```

### Creating Explicit Relationships

```python
from collie.models.base import CRMRelation

# Create explicit relationships
relationship = CRMRelation(
    src="obj_001",
    type="P53",
    tgt="place_001",
    props={"role": "E55:CurrentLocation"}
)
```

## AI-Powered Information Extraction

### Using PydanticAI for Entity Extraction

COLLIE includes AI-powered information extraction using PydanticAI to automatically identify CIDOC CRM entities and relationships from unstructured text.

```python
import asyncio
from collie.extraction import InformationExtractor

async def extract_entities():
    # Initialize the extractor
    extractor = InformationExtractor()
    
    # Extract from text
    text = """
    Albert Einstein was born on March 14, 1879, in Ulm, Germany.
    He developed the theory of relativity and won the Nobel Prize in Physics in 1921.
    Einstein worked at the Institute for Advanced Study in Princeton, New Jersey.
    """
    
    # Extract entities and relationships
    result = await extractor.extract_from_text(text)
    
    print(f"Extracted {len(result.entities)} entities")
    print(f"Extracted {len(result.relationships)} relationships")
    
    # Filter by confidence
    high_confidence_entities = [
        e for e in result.entities if e.confidence >= 0.8
    ]
    
    return result

# Run the extraction
result = asyncio.run(extract_entities())
```

### Converting Extracted Data to CRM Entities

```python
from collie.models.base import CRMEntity

# Convert extracted entities to CRM entities
crm_entities = []
for entity in result.entities:
    crm_entity = CRMEntity(
        id=str(entity.id),
        class_code=entity.class_code,
        label=entity.label,
        notes=entity.description
    )
    crm_entities.append(crm_entity)

# Now you can use all COLLIE features
from collie.io.to_markdown import render_table
markdown_table = render_table(crm_entities)
print(markdown_table)
```

### Complete AI-Powered Workflow

```python
import asyncio
from collie.extraction import InformationExtractor
from collie.io.to_networkx import to_networkx_graph, calculate_centrality_measures
from collie.visualization import plot_network_graph

async def complete_ai_workflow(text: str):
    # Step 1: Extract entities using AI
    extractor = InformationExtractor()
    extraction_result = await extractor.extract_from_text(text)
    
    # Step 2: Convert to CRM entities
    crm_entities = []
    for entity in extraction_result.entities:
        crm_entity = CRMEntity(
            id=str(entity.id),
            class_code=entity.class_code,
            label=entity.label,
            notes=entity.description
        )
        crm_entities.append(crm_entity)
    
    # Step 3: Serialize as canonical JSON (important for async/future processing)
    json_data = [entity.model_dump(mode='json') for entity in crm_entities]
    
    # Step 4: Convert to NetworkX graph
    graph = to_networkx_graph(crm_entities)
    
    # Step 5: Perform network analysis
    centrality_measures = calculate_centrality_measures(graph)
    
    # Step 6: Create visualization
    plot_network_graph(
        graph,
        title="AI-Extracted Entity Network",
        save_path="ai_network.png",
        show_plot=False
    )
    
    return {
        "entities": crm_entities,
        "graph": graph,
        "centrality": centrality_measures
    }

# Example usage
text = "Your unstructured text here..."
results = asyncio.run(complete_ai_workflow(text))
```

### Using the CLI for AI Extraction

```bash
# Extract entities from text
collie extract --text "Albert Einstein was born in Ulm, Germany" --output results/

# Extract from file with high confidence
collie extract --file biography.txt --confidence 0.8 --format both

# Run complete AI-powered workflow
collie workflow --text "Your text here" --all --output complete_analysis/
```

## NetworkX Integration

### Converting to NetworkX Graph

```python
import networkx as nx
from collie.io.to_networkx import to_networkx_graph

# Create entities
entities = [vase, production, place, artist]

# Convert to NetworkX graph
G = to_networkx_graph(entities)

# Now you can use all NetworkX algorithms
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")
```

### Social Network Analysis

```python
# Calculate centrality measures
centrality = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)
closeness = nx.closeness_centrality(G)

# Find communities
communities = nx.community.greedy_modularity_communities(G)

# Calculate shortest paths
shortest_path = nx.shortest_path(G, source="obj_001", target="person_001")
```

### Graph Visualization

```python
import matplotlib.pyplot as plt

# Basic visualization
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=1000, font_size=8)
plt.title("Cultural Heritage Network")
plt.show()

# Advanced visualization with attributes
node_colors = [G.nodes[node].get('class_code', 'E1') for node in G.nodes()]
nx.draw(G, pos, node_color=node_colors, with_labels=True)
plt.show()
```

### NetworkX Export/Import

```python
# Export to various formats
nx.write_graphml(G, "cultural_network.graphml")
nx.write_gexf(G, "cultural_network.gexf")
nx.write_edgelist(G, "cultural_network.edgelist")

# Import from formats
G_imported = nx.read_graphml("cultural_network.graphml")
```

## Validation and Quality Control

### Quantifier Validation

```python
from collie.validators.quantifiers import validate_entity_quantifiers, ValidationSeverity

# Validate quantifier rules
messages = validate_entity_quantifiers(vase, ValidationSeverity.WARN)
for message in messages:
    print(f"Validation issue: {message}")
```

### Typing Validation

```python
from collie.validators.typing_rules import validate_batch_typing

# Validate typing rules for a batch of entities
entities = [vase, production, place]
results = validate_batch_typing(entities, ValidationSeverity.WARN)

for entity_id, messages in results.items():
    print(f"Entity {entity_id}: {messages}")
```

## Exporting to Markdown

### Card Style

```python
from collie.io.to_markdown import to_markdown, MarkdownStyle

# Render as a card
card_md = to_markdown(vase, MarkdownStyle.CARD)
print(card_md)
```

### Detailed Style

```python
# Render in detailed format
detailed_md = to_markdown(vase, MarkdownStyle.DETAILED)
print(detailed_md)
```

### Table Style

```python
from collie.io.to_markdown import render_table

# Render multiple entities as a table
entities = [vase, painting]
table_md = render_table(entities)
print(table_md)

# Or use the single-entity function
table_md = to_markdown(vase, MarkdownStyle.TABLE)
print(table_md)
```

### Narrative Style

```python
# Render as narrative
narrative_md = to_markdown(production, MarkdownStyle.NARRATIVE)
print(narrative_md)
```

## Exporting to Cypher

### Basic Cypher Generation

```python
from collie.io.to_cypher import generate_cypher_script, generate_cypher_parameters

# Generate Cypher script
entities = [vase, production, place]
script = generate_cypher_script(entities)
print(script)

# Generate parameters
params = generate_cypher_parameters(entities)
print(params)
```

### Customizing Cypher Output

```python
# Generate script without constraints
script = generate_cypher_script(entities, include_constraints=False)

# Use custom batch size
script = generate_cypher_script(entities, batch_size=500)
```

## Best Practices

### 1. Use Stable IDs

Always use stable, meaningful IDs for your entities:

```python
# Good
entity = CRMEntity(id="museum_001", class_code="E74", label="Metropolitan Museum")

# Avoid
entity = CRMEntity(id="temp_123", class_code="E74", label="Metropolitan Museum")
```

### 2. Leverage Shortcut Fields

Use shortcut fields for common relationships:

```python
# Good - uses shortcut
vase = E22_HumanMadeObject(
    id="obj_001",
    current_location="place_001",  # Shortcut for P53
    produced_by="prod_001"        # Shortcut for P108
)

# Avoid - manual relationship creation
vase = E22_HumanMadeObject(id="obj_001")
relationship = CRMRelation(src="obj_001", type="P53", tgt="place_001")
```

### 3. NetworkX-First Workflow

Prioritize NetworkX for analysis, use Cypher only when persistence is needed:

```python
# Good - NetworkX for analysis
G = to_networkx_graph(entities)
analysis_results = nx.pagerank(G)

# Optional - Cypher for persistence
cypher_script = generate_cypher_script(entities)
```

### 4. Validate Early and Often

Run validation during development:

```python
# Validate after creating entities
messages = validate_entity_quantifiers(entity, ValidationSeverity.RAISE)
if messages:
    print("Validation failed:", messages)
```

### 5. Use Appropriate Class Codes

Choose the most specific class code available:

```python
# Good - specific
person = E21_Person(id="person_001", label="Leonardo da Vinci")

# Avoid - too generic
person = CRMEntity(id="person_001", class_code="E1", label="Leonardo da Vinci")
```

### 6. Document with Notes

Add meaningful notes to entities:

```python
entity = CRMEntity(
    id="obj_001",
    class_code="E22",
    label="Ancient Vase",
    notes="Discovered in 1923 during archaeological excavation of the Acropolis"
)
```

## Common Patterns

### Museum Object Lifecycle

```python
# 1. Production
production = E12_Production(
    id="prod_001",
    label="Vase Production",
    timespan="timespan_001",
    took_place_at="place_002"
)

# 2. Object
vase = E22_HumanMadeObject(
    id="obj_001",
    label="Ancient Vase",
    produced_by="prod_001"
)

# 3. Acquisition
acquisition = E8_Acquisition(
    id="acq_001",
    label="Museum Acquisition",
    timespan="timespan_002",
    took_place_at="place_001"
)

# 4. Current Location
place = E53_Place(
    id="place_001",
    label="Metropolitan Museum of Art"
)
```

### Social Network Analysis Workflow

```python
# 1. Create entities with relationships
entities = [vase, production, place, artist, museum]

# 2. Convert to NetworkX graph
G = to_networkx_graph(entities)

# 3. Perform social network analysis
centrality = nx.degree_centrality(G)
communities = nx.community.greedy_modularity_communities(G)

# 4. Visualize results
nx.draw(G, with_labels=True)
plt.show()

# 5. Export for persistence (optional)
cypher_script = generate_cypher_script(entities)
```

### Event Participation

```python
# Event with participants
exhibition = E7_Activity(
    id="event_001",
    label="Renaissance Art Exhibition",
    timespan="timespan_003",
    took_place_at="place_001"
)

# Add participants (this would be handled in the relationship expansion)
# participants = ["person_001", "person_002", "group_001"]
```

This guide should help you get started with modeling cultural heritage data using the Collie toolkit with NetworkX integration for social network analysis. For more advanced patterns and examples, refer to the test cases in the `tests/` directory.
