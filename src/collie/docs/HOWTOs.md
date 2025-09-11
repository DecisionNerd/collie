# CIDOC CRM Modeling Guide

This guide provides practical examples and patterns for modeling cultural heritage data using the Collie toolkit.

## Table of Contents

1. [Basic Entity Creation](#basic-entity-creation)
2. [Modeling Events](#modeling-events)
3. [Modeling Objects](#modeling-objects)
4. [Modeling People and Groups](#modeling-people-and-groups)
5. [Modeling Places and Time](#modeling-places-and-time)
6. [Working with Relationships](#working-with-relationships)
7. [Validation and Quality Control](#validation-and-quality-control)
8. [Exporting to Markdown](#exporting-to-markdown)
9. [Exporting to Cypher](#exporting-to-cypher)

## Basic Entity Creation

### Creating a Simple Entity

```python
from collie.models.base import CRMEntity

# Create a basic CRM entity
entity = CRMEntity(
    id="obj_001",
    class_code="E22",
    label="Ancient Vase",
    type=["E55:Vessel", "E55:Ceramic"],
    notes="A beautifully preserved amphora"
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
# Render as a table
table_md = to_markdown([vase, painting], MarkdownStyle.TABLE)
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

### 3. Validate Early and Often

Run validation during development:

```python
# Validate after creating entities
messages = validate_entity_quantifiers(entity, ValidationSeverity.RAISE)
if messages:
    print("Validation failed:", messages)
```

### 4. Use Appropriate Class Codes

Choose the most specific class code available:

```python
# Good - specific
person = E21_Person(id="person_001", label="Leonardo da Vinci")

# Avoid - too generic
person = CRMEntity(id="person_001", class_code="E1", label="Leonardo da Vinci")
```

### 5. Document with Notes

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

This guide should help you get started with modeling cultural heritage data using the Collie toolkit. For more advanced patterns and examples, refer to the test cases in the `tests/` directory.
