# Implementation Plan

Comprehensive plan to deliver full Pydantic coverage of CIDOC CRM v7.1.3 with Markdown renderers and Cypher emitters, aligned with the repo mission (JSON ↔ Markdown ↔ Cypher; no RDF/OWL/JSON‑LD at runtime).

---

## 0) Scope & Non‑Goals

**In‑scope**

* Pydantic v2 models covering all CIDOC CRM **E‑classes** and **P‑properties** (7.1.3).
* Canonical JSON schema (stable keys, IDs, references).
* Markdown renderers: cards, narratives, tables.
* Cypher emitters: idempotent MERGE/UNWIND for nodes/relationships, optional indexes/constraints.
* Validators for cardinalities, domain/range alignment; configurable severity (warn/raise).
* Curated source-of-truth YAML to drive code generation (classes, properties, quantifiers, aliases).

**Out‑of‑scope**

* RDF/OWL/JSON‑LD interop.
* Inference/reasoning engines.
* SHACL or ontology validation.

---

## 1) Architecture & Packages

```
src/collie/
  codegen/
    specs/
      crm_classes.yaml        # E‑class metadata (code, label, parents, notes)
      crm_properties.yaml     # P‑property metadata (domain, range, inverse, quantifier, aliases)
      aliases.yaml            # human‑friendly labels for classes/properties (Markdown/Cypher)
    generate_models.py        # YAML → Pydantic .py
    generate_registry.py      # YAML → properties.py (P‑registry)
    generate_templates.py     # YAML → Markdown/Cypher template stubs
  models/
    base.py                   # CRMEntity + core wrappers (E5/E22/E21/E53/E52)
    generated/
      e_classes.py            # auto‑generated Pydantic models per E‑class
  properties.py               # auto‑generated P‑registry (domain, range, inverse, quantifier)
  io/
    to_markdown.py            # renderers + registry + profiles
    to_cypher.py              # emitters + helpers + batching
  validators/
    quantifiers.py            # enforcement utilities
    typing_rules.py           # domain/range/class alignment checks
  examples/
    *.json                    # golden cases across subdomains
  tests/
    unit/                     # validators, emitters, renderers
    golden/                   # snapshot tests (JSON → MD/Cypher)
  docs/
    HOWTOs.md                 # modeling patterns & tips
```

---

## 2) Source‑of‑Truth Specifications (YAML)

### 2.1 crm\_classes.yaml

* Fields: `code` (E‑number), `label`, `abstract: bool`, `parents: [E‑codes]`, `hints`, `canonical_fields` (ordered list), `shortcuts` (list of property aliases used in ergonomic wrappers), `markdown_template: optional` reference.
* Example (excerpt):

```yaml
- code: E22
  label: Human-Made Object
  abstract: false
  parents: [E19]
  canonical_fields: [label, type, produced_by, current_location, identifiers, titles]
  shortcuts:
    - property: P108
      alias_field: produced_by
    - property: P53
      alias_field: current_location
```

### 2.2 crm\_properties.yaml

* Fields: `code` (P‑number), `label`, `domain`, `range`, `inverse`, `quantifier` in {"0..1","0..*","1..1","1..*"}, `notes`, `aliases` (friendly name), `roles` (if event/participation roles apply), `is_transitive: bool?`.
* Example (excerpt):

```yaml
- code: P108
  label: was produced by
  domain: E22
  range: E12
  inverse: P108i
  quantifier: 0..1
  aliases: [WAS_PRODUCED_BY]
```

### 2.3 aliases.yaml

* Human‑friendly label map for classes/properties used in Markdown headers and optional Cypher type aliases.

---

## 3) Code Generation

### 3.1 Model Generation (YAML → Pydantic)

* Iterate `crm_classes.yaml` to emit a single `e_classes.py` with one Pydantic class per E‑class:

  * Every class extends `CRMEntity` (from `models/base.py`).
  * Add typed fields for ergonomic shortcuts defined in `shortcuts`.
  * Add docstrings with class label/definition.
  * Provide `__crm_meta__` (dataclass) with class metadata (parents, label, etc.).
* **Naming**: `class E22_HumanMadeObject(CRMEntity)` with `class_code="E22"` defaulted.

### 3.2 Property Registry Generation

* Emit `properties.py` from `crm_properties.yaml`:

```python
P = {
  "P108": {"label": "was produced by", "domain": "E22", "range": "E12", "inverse": "P108i", "quantifier": "0..1"},
  # ... all Pxx
}
```

* Include reverse lookup tables for performance: `DOMAIN["E22"] → [P108, ...]`, `RANGE["E12"] → [...]`.

### 3.3 Template Generation (optional)

* Stub Markdown and Cypher templates per class/property (Jinja strings) to enable custom formatting beyond defaults.

---

## 4) Pydantic Base & Ergonomic Wrappers

### 4.1 Base

```python
class CRMEntity(BaseModel):
    id: str
    class_code: str
    label: Optional[str] = None
    notes: Optional[str] = None
    type: List[str] = Field(default_factory=list)
```

### 4.2 High‑Use Wrappers (hand‑written)

* `E5_Event`, `E7_Activity`, `E12_Production`, `E8_Acquisition`, `E22_HumanMadeObject`, `E21_Person`, `E74_Group`, `E53_Place`, `E52_TimeSpan`, `E42_Identifier`, `E35_Title`.
* Add shortcut fields (e.g., `produced_by`, `current_location`) that map to P‑relations via emitters.

### 4.3 Autogenerated Classes

* For all remaining E‑classes, generate lean classes with no logic aside from field definitions and `class_code` constant.

---

## 5) Validation Utilities

### 5.1 Cardinality

* Implement `enforce_quantifier(entity, pcode, values)` to warn/raise based on configured severity.
* Apply during:

  * `expand_shortcuts()` (when turning fields into relations)
  * `emit_relationships()` (final check)

### 5.2 Domain/Range Typing

* Validate that relations align with `P[pcode]['domain']` and `['range']` based on `class_code` of source/target IDs when both ends are present in the batch. If unknown (open world), skip with INFO log.

### 5.3 Completeness Profiles

* Per class, optional `profile.json` requiring a minimal set of fields (e.g., E22 needs ≥1 of {title, identifier, production}).

---

## 6) Markdown Renderers

### 6.1 Public API

```python
from enum import Enum
class MarkdownStyle(str, Enum):
    CARD = "card"
    DETAILED = "detailed"
    TABLE = "table"

def to_markdown(entity: CRMEntity, style: MarkdownStyle = MarkdownStyle.CARD, *,
                aliases: dict | None = None,
                show_codes: bool = True) -> str:
    ...
```

### 6.2 Card Templates (default)

* Header: `### {E‑code} · {FriendlyLabel} — {label or id} ({id})`
* Body bullets derived from `canonical_fields` for the class.
* Human‑friendly property names from `aliases.yaml`.

### 6.3 Detailed Templates

* Dump non‑empty fields in labeled bullet list with friendly names.
* Optional inclusion of cross‑reference previews (e.g., show linked labels if available in a provided `lookup: Dict[id → label]`).

### 6.4 Table Renderer (batch)

* Produce a Markdown table with configurable columns.
* `render_table(entities: list[CRMEntity], columns: list[str]) -> str`.

### 6.5 Narrative Renderer (events)

* For E5/E7/E8/E12: render a concise storyline (who, what, when, where, roles) using `TimeSpan` and `Place` lookups when available.

---

## 7) Cypher Emitters

### 7.1 Node Emission

```python
def emit_nodes(entities: Iterable[CRMEntity]) -> dict:
    return {"nodes": [{"id": e.id, "class_code": e.class_code, "label": e.label, "notes": e.notes} for e in entities]}
```

### 7.2 Relationship Expansion & Emission

* `expand_shortcuts(entity)` → list of `{"src","type","tgt"}` based on shortcut fields and `crm_properties.yaml` mapping.
* Also consume explicit relation collections if present (e.g., `participants` → `P11`).

```python
def emit_relationships(entities: Iterable[CRMEntity]) -> dict:
    rels = []
    for e in entities:
        rels.extend(expand_shortcuts(e))
        # class-specific collections
        if hasattr(e, "participants"):
            for a in e.participants:
                rels.append({"src": e.id, "type": "P11_HAD_PARTICIPANT", "tgt": a})
    return {"rels": rels}
```

### 7.3 Script Generation

* Group relationships by `type` and emit per‑type UNWIND blocks:

```cypher
UNWIND $nodes AS n
MERGE (x:CRM {id:n.id})
SET x.label = coalesce(n.label, x.label), x.class_code = n.class_code;

UNWIND $rels_P108_WAS_PRODUCED_BY AS r
MATCH (s:CRM {id:r.src}) MATCH (t:CRM {id:r.tgt})
MERGE (s)-[:`P108_WAS_PRODUCED_BY`]->(t);
```

* Emit `CREATE CONSTRAINT crm_id IF NOT EXISTS ...` once per script.

### 7.4 Role & Qualifier Handling

* Edge properties supported via extended relation items: `{src, type, tgt, props: {role: 'E55:Painter'}}`.
* Provide optional schema to whitelist allowed edge properties per `P` relation.

---

## 8) Testing Strategy

### 8.1 Unit Tests

* Validators: quantifier and domain/range behavior.
* Emitters: nodes/relationships from samples.
* Renderers: card/detailed/table outputs (snapshot testing).

### 8.2 Golden Examples (snapshot)

* Domains: museum object lifecycle, excavation, archival record creation, custody transfer, movement, condition assessment, measurement, identifier assignment, type assignment.
* Ensure coverage matrix: each major `P` appears ≥1 time; each major `E` instantiated ≥1 time.

### 8.3 Performance/Scale Tests

* Large batch UNWIND (10k nodes / 50k rels) to validate generation speed and memory.

---

## 9) Milestones & Timeline

1. **Specs & Codegen (Days 1–4)**

   * Draft YAML specs (classes/properties/aliases) for top 40 classes & 60 properties; design generators.
   * Deliver first `e_classes.py` + `properties.py`.
2. **Wrappers & Validators (Days 5–7)**

   * Implement base + ergonomic wrappers; quantifier and typing validators.
3. **Markdown & Cypher (Days 8–10)**

   * Implement renderers (card/detailed/table/narrative); implement emitters with per‑type UNWIND blocks.
4. **Full Coverage Expansion (Days 11–16)**

   * Complete YAML for all CRM 7.1.3 classes/properties; regenerate; add missing shortcuts.
5. **Golden Suite & Docs (Days 17–20)**

   * Author examples; add snapshot tests; write HOWTOs.

---

## 10) Acceptance Criteria (Definition of Done)

* ✅ All CIDOC CRM 7.1.3 E‑classes represented as Pydantic models (generated or wrapped).
* ✅ `properties.py` contains all P‑properties with `domain`, `range`, `inverse`, `quantifier`.
* ✅ `expand_shortcuts()` and emitters cover the standard CRM shortcuts (location, production, identifiers, titles, custody, acquisition).
* ✅ Markdown: card/detailed/table/narrative renderers produce clean, friendly output using aliases and canonical fields.
* ✅ Cypher: generator outputs idempotent scripts grouping by relationship type; example payloads run on Neo4j/Memgraph.
* ✅ Validators enforce quantifiers and basic domain/range alignment with configurable severity.
* ✅ Golden examples cover the object/event/actor/time/place patterns and pass snapshot tests.

---

## 11) Risks & Mitigations

* **Ambiguous quantifiers in prose spec** → Curate quantifiers in YAML with inline citations; treat unknowns as warnings.
* **Circular references / deep graphs** → Use ID references only; avoid recursive expansion by default.
* **Parameterizable labels in Cypher** → Group by relationship type and emit static type tokens.
* **Scale** → Batch UNWIND; avoid per‑row queries; prefer client‑side grouping.

---

## 12) Future Enhancements

* Profile packs (e.g., Linked.Art‑like profiles) to toggle field visibility and renderer verbosity.
* Graph diff utilities to emit update/delete scripts.
* Prompt packs for LLM extraction tasks (per E‑class and event patterns).
* Importers for common museum/archive CSVs to canonical JSON.
