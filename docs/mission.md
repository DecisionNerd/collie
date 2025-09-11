# Mission

The goal of this repository is to provide a **developer‑friendly toolkit** for working with the CIDOC CRM v7.1.3 in modern data workflows. Instead of focusing on RDF/OWL or JSON‑LD, this repo implements:

* **Pydantic models → JSON**: canonical, schema‑driven representations of CRM entities and properties.
* **JSON → Markdown**: lightweight renderers that produce human‑readable entity cards, tables, and narratives optimized for LLM prompts and reports.
* **JSON → Cypher**: emitters that generate idempotent MERGE/UNWIND scripts for ingestion into labeled property graph databases such as Neo4j and Memgraph.

---

## Why This Matters

Cultural heritage and information extraction projects often need a **CRM‑compliant backbone** without the overhead of RDF stacks. This repo:

* Keeps the conceptual rigor of CIDOC CRM.
* Provides lean, open‑world Pydantic validation.
* Outputs formats directly usable by LLMs (Markdown) and LPGs (Cypher).
* Prioritizes ergonomics and performance for real‑world extraction pipelines.

---

## Core Outcomes

1. **Complete Pydantic coverage** for key CRM classes and properties.
2. **Canonical JSON schema** with stable IDs and explicit cross‑references.
3. **Markdown renderers** for concise cards, detailed narratives, and tabular summaries.
4. **Cypher emitters** for idempotent graph construction.
5. **Validation utilities** for cardinalities and type alignment, configurable from warnings to strict enforcement.
6. **Lean runtime**: no RDF/OWL/JSON‑LD dependencies.

---

## Guiding Principles

* **IDs first**: every entity has a stable `id` for cross‑linking across JSON, Markdown, and Cypher. Flexible UUID handling supports both string IDs and UUIDs with deterministic conversion.
* **Explicit over implicit**: relationships are IDs and P‑codes; shortcuts expand to full CRM semantics when exported.
* **Readable outputs**: Markdown is designed for LLM consumption and human comprehension.
* **Graph‑ready**: Cypher generation is idempotent, batched, and aligned to Pxx semantics.
* **Developer ergonomics**: flexible ID handling maintains backward compatibility while providing modern UUID benefits.
* **Extensible**: new CRM classes and properties can be added via curated YAML and codegen.

---

## Deliverables

* **Pydantic models**: core CRM classes (E‑classes) and property registry (Pxx).
* **JSON utilities**: canonical serialization and shorthand normalization.
* **Markdown utilities**: cards, narratives, tables with style profiles.
* **Cypher utilities**: node/relationship param builders, MERGE emitters, constraint helpers.
* **Examples**: golden JSON cases with verified Markdown and Cypher output.
* **Tests**: comprehensive unit tests and golden tests for validators, Markdown, and Cypher with 100% pass rate.

---

## Example Workflow

1. **Extract** entities from source text or structured data.
2. **Serialize** them as canonical JSON using Pydantic models.
3. **Render** them into Markdown for inclusion in LLM prompts or human review.
4. **Emit** Cypher scripts to build or update a labeled property graph.

---

## Mission Statement

> To make CIDOC CRM practical and ergonomic for information extraction, LLM workflows, and graph databases by providing Pydantic models, Markdown renderers, and Cypher emitters that bridge the gap between conceptual rigor and developer usability.
