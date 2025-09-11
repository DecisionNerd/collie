# Mission

The goal of this repository is to provide a **developer‑friendly toolkit** for working with the CIDOC CRM v7.1.3 in modern social network analysis workflows. Instead of focusing on RDF/OWL or JSON‑LD, this repo implements:

* **Pydantic models → JSON**: canonical, schema‑driven representations of CRM entities and properties.
* **JSON → NetworkX**: direct integration with NetworkX for in-memory graph analysis without external database dependencies.
* **JSON → Markdown**: lightweight renderers that produce human‑readable entity cards, tables, and narratives optimized for LLM prompts and reports.
* **JSON → Cypher**: emitters that generate idempotent MERGE/UNWIND scripts for ingestion into labeled property graph databases such as Neo4j and Memgraph when persistence is needed.

---

## Why This Matters

Cultural heritage and information extraction projects often need a **CRM‑compliant backbone** for social network analysis without the overhead of external graph databases or RDF stacks. This repo:

* Keeps the conceptual rigor of CIDOC CRM.
* Provides lean, open‑world Pydantic validation.
* Enables NetworkX-based graph analysis for rapid prototyping and pure Python workflows.
* Outputs formats directly usable by LLMs (Markdown), graph analysis libraries (NetworkX), and LPGs (Cypher) when persistence is required.
* Prioritizes ergonomics and performance for database-agnostic extraction pipelines.

---

## Core Outcomes

1. **Complete Pydantic coverage** for key CRM classes and properties.
2. **Canonical JSON schema** with stable IDs and explicit cross‑references.
3. **NetworkX integration** for in-memory graph construction and analysis algorithms.
4. **Markdown renderers** for concise cards, detailed narratives, and tabular summaries.
5. **Cypher emitters** for idempotent graph construction when database persistence is needed.
6. **Validation utilities** for cardinalities and type alignment, configurable from warnings to strict enforcement.
7. **Database-agnostic workflow**: NetworkX-first with optional LPG export capabilities.
8. **Lean runtime**: no RDF/OWL/JSON‑LD dependencies, minimal external graph database dependencies.

---

## Guiding Principles

* **IDs first**: every entity has a stable `id` for cross‑linking across JSON, NetworkX, Markdown, and Cypher. Flexible UUID handling supports both string IDs and UUIDs with deterministic conversion.
* **NetworkX-first**: primary graph analysis workflows use NetworkX for in-memory processing, avoiding external database dependencies.
* **Explicit over implicit**: relationships are IDs and P‑codes; shortcuts expand to full CRM semantics when exported.
* **Readable outputs**: Markdown is designed for LLM consumption and human comprehension.
* **Graph‑ready**: NetworkX integration provides immediate analysis capabilities; Cypher generation is idempotent, batched, and aligned to Pxx semantics for optional persistence.
* **Database-agnostic**: workflows remain portable between NetworkX and external graph databases without tight coupling.
* **Developer ergonomics**: flexible ID handling maintains backward compatibility while providing modern UUID benefits.
* **Extensible**: new CRM classes and properties can be added via curated YAML and codegen.

---

## Deliverables

* **Pydantic models**: core CRM classes (E‑classes) and property registry (Pxx).
* **JSON utilities**: canonical serialization and shorthand normalization.
* **NetworkX utilities**: graph construction from JSON, analysis algorithms, and visualization helpers.
* **Markdown utilities**: cards, narratives, tables with style profiles.
* **Cypher utilities**: node/relationship param builders, MERGE emitters, constraint helpers for optional database persistence.
* **Examples**: golden JSON cases with verified NetworkX, Markdown, and Cypher output.
* **Tests**: comprehensive unit tests and golden tests for validators, NetworkX integration, Markdown, and Cypher with 100% pass rate.

---

## Example Workflow

1. **Extract** entities from source text or structured data.
2. **Serialize** them as canonical JSON using Pydantic models.
3. **Analyze** relationships and patterns using NetworkX algorithms for social network analysis.
4. **Render** them into Markdown for inclusion in LLM prompts or human review.
5. **Emit** Cypher scripts to build or update a labeled property graph (optional, when persistence is needed).

---

## Mission Statement

> To make CIDOC CRM practical and ergonomic for social network analysis workflows by providing Pydantic models, NetworkX integration, Markdown renderers, and optional Cypher emitters that bridge the gap between conceptual rigor and database-agnostic developer usability.
