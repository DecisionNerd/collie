# COLLIE Quickstart Guide

Get up and running with COLLIE in minutes! This guide will walk you through the complete AI-powered cultural heritage information extraction and analysis workflow.

## 🚀 What is COLLIE?

COLLIE (Classful Ontology for Life-Events Information Extraction) is a comprehensive toolkit that combines:

- **AI-Powered Extraction**: Uses PydanticAI to extract entities and relationships from unstructured text
- **CIDOC CRM Compliance**: Full implementation of the CIDOC CRM v7.1.3 ontology (99 classes, 322 properties)
- **NetworkX Analysis**: Social network analysis with centrality measures and community detection
- **Interactive Visualizations**: Both static matplotlib plots and interactive Plotly visualizations
- **Multiple Output Formats**: JSON, Markdown, Cypher, and visualization files

## 📋 Prerequisites

- Python 3.13+
- Google API Key (for AI extraction)
- Git

## ⚡ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/decisionnerd/collie.git
   cd collie
   ```

2. **Install dependencies:**
   ```bash
   # Install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install COLLIE and dependencies
   uv sync
   ```

3. **Set up your API key:**
   ```bash
   # Create .env file
   echo "GOOGLE_API_KEY=your-api-key-here" > .env
   ```
   
   Get your Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## 🎯 Quick Start Examples

### 1. Interactive Jupyter Notebook Demo

> **🚀 Best for learning and experimentation: [`COLLIE_Demo_Notebook.ipynb`](COLLIE_Demo_Notebook.ipynb)**

The notebook provides a complete interactive walkthrough with:
- **Step-by-step execution** of all workflow components
- **Live visualizations** and network analysis
- **Canonical JSON serialization** demonstration
- **Advanced examples** including batch processing
- **Real-time output** generation

Perfect for understanding how COLLIE works and experimenting with different texts!

### 2. Run the Einstein Demo

The fastest way to see COLLIE in action:

```bash
uv run python -m collie.main demo --einstein
```

This will:
- Extract entities from Einstein's biography using AI
- Convert them to CIDOC CRM entities
- Generate Markdown reports
- Create NetworkX graphs
- Perform social network analysis
- Generate visualizations
- Export to Cypher scripts

### 2. Extract Entities from Your Own Text

```bash
uv run python -m collie.main extract --text "Albert Einstein was born in Ulm, Germany in 1879. He developed the theory of relativity and won the Nobel Prize in 1921." --output my_results/
```

### 3. Run Complete Workflow

```bash
uv run python -m collie.main workflow --text "Your text here" --all --output complete_analysis/
```

## 🔧 CLI Commands Reference

### Extract Command
Extract entities from text using AI:

```bash
collie extract [OPTIONS]

Options:
  --text TEXT              Text to extract entities from
  --file FILE              File containing text to extract entities from
  --output, -o OUTPUT       Output directory (default: output)
  --confidence CONFIDENCE  Minimum confidence threshold (default: 0.5)
  --format {json,markdown,both}  Output format (default: both)
```

**Examples:**
```bash
# Extract from text
collie extract --text "Einstein was born in Germany" --output results/

# Extract from file
collie extract --file biography.txt --format json --confidence 0.7

# Extract with high confidence
collie extract --text "Your text" --confidence 0.8 --format both
```

### Analyze Command
Analyze extracted entities with NetworkX:

```bash
collie analyze --input INPUT [OPTIONS]

Options:
  --input, -i INPUT        Input file with extracted entities
  --output, -o OUTPUT      Output directory (default: analysis)
  --visualize             Create visualizations
  --interactive           Create interactive plots
  --export-cypher         Export to Cypher script
  --centrality            Calculate centrality measures
  --communities           Find communities
```

**Examples:**
```bash
# Full analysis
collie analyze --input results/extraction_result.json --all

# Just visualization
collie analyze --input results/extraction_result.json --visualize --interactive

# Centrality analysis
collie analyze --input results/extraction_result.json --centrality --communities
```

### Workflow Command
Run complete end-to-end pipeline:

```bash
collie workflow [OPTIONS]

Options:
  --text TEXT              Text to process
  --file FILE              File containing text to process
  --output, -o OUTPUT      Output directory (default: workflow_output)
  --all                    Run all analysis steps
  --visualize              Create visualizations
  --interactive            Create interactive plots
  --export-cypher          Export to Cypher script
  --confidence CONFIDENCE  Minimum confidence threshold (default: 0.5)
```

**Examples:**
```bash
# Complete workflow
collie workflow --text "Your text" --all --output complete_results/

# Workflow with custom confidence
collie workflow --file document.txt --confidence 0.8 --visualize

# Minimal workflow (just extraction)
collie workflow --text "Your text" --output minimal_results/
```

### Demo Command
Run demo examples:

```bash
collie demo [OPTIONS]

Options:
  --einstein              Run Einstein biography demo
  --sample                Run sample text demo
  --output, -o OUTPUT     Output directory (default: demo_output)
```

**Examples:**
```bash
# Einstein demo
collie demo --einstein

# Sample text demo
collie demo --sample --output my_demo/
```

## 📊 Understanding the Output

### Directory Structure
```
output/
├── extraction_result.json      # Raw AI extraction results
├── canonical_entities.json     # Canonical JSON for async/future processing
├── extraction_result.md        # Human-readable entity table
├── markdown/                   # Individual entity cards
│   ├── entity_1_E21.md
│   ├── entity_2_E53.md
│   └── ...
├── plots/                      # Visualizations
│   ├── network_overview.png    # Static network plot
│   └── network_overview.png # Static network plot
├── network.cypher             # Cypher script for graph databases
└── workflow_summary.md         # Complete analysis summary
```

### Key Files Explained

- **`extraction_result.json`**: Raw AI extraction with confidence scores
- **`canonical_entities.json`**: Canonical JSON format for async/future processing (UUIDs as strings, ready for graph databases)
- **`extraction_result.md`**: Clean table of extracted entities
- **`network_overview.png`**: Static visualization of entity relationships
- **`network_overview.png`**: Static network visualization
- **`network.cypher`**: Ready-to-run script for Neo4j or Memgraph
- **`workflow_summary.md`**: Complete analysis report

## 🧠 AI-Powered Extraction

COLLIE uses PydanticAI to intelligently extract:

### Entity Types (CIDOC CRM Classes)
- **E21 Person**: People mentioned in the text
- **E53 Place**: Locations and geographical entities
- **E5 Event**: Events, activities, and occurrences
- **E22 Man-Made Object**: Artifacts, documents, artworks
- **E52 Time-Span**: Temporal periods and dates
- **E41 Appellation**: Names, titles, and identifiers

### Relationship Types (CIDOC CRM Properties)
- **P74**: has residence (person → place)
- **P7**: took place at (event → place)
- **P4**: has time-span (event → time-span)
- **P108**: produced by (object → person)
- **P11**: had participant (event → person)

## 📈 Network Analysis Features

### Centrality Measures
- **Degree Centrality**: Most connected entities
- **Betweenness Centrality**: Entities that bridge different parts of the network
- **Closeness Centrality**: Entities closest to all others
- **PageRank**: Importance based on network structure

### Community Detection
- **Greedy Modularity**: Find natural groupings in the network
- **Louvain Algorithm**: Optimize community structure

### Network Statistics
- **Density**: How connected the network is
- **Clustering**: How tightly connected local neighborhoods are
- **Path Length**: Average distance between entities

## 🎨 Visualization Options

### Static Plots (matplotlib)
- Clean, publication-ready network diagrams
- Color-coded by entity type
- Node sizes based on centrality
- Edge thickness based on relationship strength

### Static Plots (Matplotlib)
- High-quality network visualizations
- Clear entity and relationship display
- Customizable styling and layouts
- Export to PNG for sharing

## 🔗 Integration with Graph Databases

The generated Cypher scripts work with:

- **Neo4j**: Most popular graph database
- **Memgraph**: High-performance graph database
- **Amazon Neptune**: Cloud-based graph database

Example Cypher output:
```cypher
// Create entities
CREATE (e1:E21 {id: "person-1", label: "Albert Einstein"})
CREATE (e2:E53 {id: "place-1", label: "Ulm"})

// Create relationships
CREATE (e1)-[:P74]->(e2)  // Einstein has residence in Ulm
```

## 🧪 Testing Your Setup

Run the test suite to verify everything works:

```bash
uv run pytest src/collie/tests/ -v
```

You should see all 47 tests pass, including:
- Unit tests for core functionality
- NetworkX integration tests
- Visualization tests
- Complete workflow tests

## 🚨 Troubleshooting

### Common Issues

1. **"GOOGLE_API_KEY environment variable is required"**
   - Make sure you've created a `.env` file with your API key
   - Verify the key is valid and has the right permissions

2. **"ModuleNotFoundError: No module named 'scipy'"**
   - Run `uv sync` to install all dependencies
   - Make sure you're using the virtual environment

3. **Tests failing**
   - Check that all dependencies are installed: `uv sync`
   - Verify Python version is 3.13+

4. **Empty extraction results**
   - Try lowering the confidence threshold: `--confidence 0.3`
   - Check that your text contains recognizable entities
   - Verify your API key has sufficient quota

### Getting Help

- Check the [README.md](README.md) for detailed documentation
- Review [docs/mission.md](docs/mission.md) for project philosophy
- Look at [docs/plan.md](docs/plan.md) for technical architecture
- Run `collie --help` for command reference

## 🎯 Next Steps

Now that you're up and running:

1. **Try your own data**: Extract entities from your own texts
2. **Explore visualizations**: View the static PNG plots
3. **Import to graph databases**: Use the Cypher scripts with Neo4j
4. **Customize analysis**: Adjust confidence thresholds and analysis parameters
5. **Integrate with workflows**: Use COLLIE in your data processing pipelines

## 📚 Additional Resources

- **Complete Documentation**: [README.md](README.md)
- **Project Mission**: [docs/mission.md](docs/mission.md)
- **Technical Plan**: [docs/plan.md](docs/plan.md)
- **Testing Guide**: [docs/testing.md](docs/testing.md)
- **CIDOC CRM Specification**: [Official CIDOC CRM Documentation](https://cidoc-crm.org/)

Happy analyzing! 🎉
