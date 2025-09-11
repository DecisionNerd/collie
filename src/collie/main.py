"""
COLLIE - Complete workflow demonstration.

This module demonstrates the complete COLLIE workflow:
Text → PydanticAI Extraction → CRM Entities → Markdown → NetworkX → Visualization
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from collie.extraction import InformationExtractor
from collie.io.to_markdown import to_markdown, MarkdownStyle, render_table
from collie.io.to_networkx import to_networkx_graph, calculate_centrality_measures, find_communities
from collie.visualization import plot_network_graph, create_interactive_plot, create_network_summary
from collie.io.to_cypher import generate_cypher_script

# Load environment variables from .env file
load_dotenv()


def check_api_key():
    """Check if GOOGLE_API_KEY is set and provide helpful error message if not."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable is required.")
        print("Please set your Google API key:")
        print("  export GOOGLE_API_KEY='your-api-key-here'")
        print("Or create a .env file with:")
        print("  GOOGLE_API_KEY=your-api-key-here")
        sys.exit(1)
    return api_key


async def complete_workflow_demo(text: str, output_dir: str = "output", 
                              visualize: bool = True, interactive: bool = True, 
                              export_cypher: bool = True, confidence_threshold: float = 0.5):
    """
    Demonstrate the complete COLLIE workflow.
    
    Args:
        text: Input text to analyze
        output_dir: Directory to save outputs
        visualize: Whether to create static visualizations
        interactive: Whether to create interactive plots
        export_cypher: Whether to export Cypher scripts
        confidence_threshold: Minimum confidence for entities/relationships
    """
    print("🚀 Starting COLLIE Complete Workflow Demo")
    print("=" * 50)
    
    # Step 1: AI-powered Information Extraction
    print("\n📝 Step 1: AI-powered Information Extraction")
    print("-" * 40)
    
    extractor = InformationExtractor()
    extraction_result = await extractor.extract_from_text(text)
    
    print(f"✅ Extracted {len(extraction_result.entities)} entities")
    print(f"✅ Extracted {len(extraction_result.relationships)} relationships")
    
    # Step 2: Convert to CRM Entities
    print("\n🏗️ Step 2: Convert to CRM Entities")
    print("-" * 40)
    
    # Convert extracted entities to CRM entities
    from collie.models.base import CRMEntity
    from uuid import uuid4
    
    crm_entities = []
    for entity in extraction_result.entities:
        crm_entity = CRMEntity(
            id=str(entity.id),
            class_code=entity.class_code,
            label=entity.label,
            notes=entity.description,
            type=[entity.class_code]
        )
        crm_entities.append(crm_entity)
    
    print(f"✅ Created {len(crm_entities)} CRM entities")
    
    # Step 3: Serialize as Canonical JSON
    print("\n💾 Step 3: Serialize as Canonical JSON")
    print("-" * 40)
    
    # Serialize as canonical JSON using Pydantic models
    json_data = [entity.model_dump(mode='json') for entity in crm_entities]
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save canonical JSON
    import json
    json_file = output_path / "canonical_entities.json"
    with open(json_file, "w") as f:
        json.dump(json_data, f, indent=2)
    
    print(f"✅ Serialized {len(json_data)} entities to canonical JSON: {json_file}")
    
    # Step 4: Render to Markdown
    print("\n📄 Step 4: Render to Markdown")
    print("-" * 40)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Generate Markdown reports
    markdown_dir = output_path / "markdown"
    markdown_dir.mkdir(exist_ok=True)
    
    # Individual entity cards
    for i, entity in enumerate(crm_entities[:5]):  # Show first 5 entities
        markdown_card = to_markdown(entity, MarkdownStyle.CARD)
        card_file = markdown_dir / f"entity_{i+1}_{entity.class_code}.md"
        with open(card_file, "w") as f:
            f.write(markdown_card)
    
    # Summary table
    table_markdown = render_table(crm_entities)
    table_file = markdown_dir / "entities_summary.md"
    with open(table_file, "w") as f:
        f.write("# CRM Entities Summary\n\n" + table_markdown)
    
    print(f"✅ Generated Markdown reports in {markdown_dir}")
    
    # Step 5: Convert to NetworkX Graph
    print("\n🕸️ Step 5: Convert to NetworkX Graph")
    print("-" * 40)
    
    # Convert to NetworkX graph
    graph = to_networkx_graph(crm_entities)
    
    print(f"✅ Created NetworkX graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
    
    # Step 6: Network Analysis
    print("\n📊 Step 6: Network Analysis")
    print("-" * 40)
    
    # Calculate centrality measures
    centrality_measures = calculate_centrality_measures(graph)
    
    # Find communities
    communities = find_communities(graph)
    
    # Get network statistics
    network_stats = create_network_summary(graph)
    
    print(f"✅ Calculated centrality measures: {list(centrality_measures.keys())}")
    print(f"✅ Found {len(communities)} communities")
    print(f"✅ Network density: {network_stats['network_info']['density']:.3f}")
    
    # Step 7: Visualization
    if visualize or interactive:
        print("\n🎨 Step 7: Visualization")
        print("-" * 40)
        
        plots_dir = output_path / "plots"
        plots_dir.mkdir(exist_ok=True)
        
        if visualize:
            # Static network plot
            fig = plot_network_graph(
                graph,
                title="COLLIE Network Analysis",
                figsize=(14, 10),
                show_plot=False,
                save_path=str(plots_dir / "network_overview.png")
            )
            print(f"✅ Generated static plot: {plots_dir / 'network_overview.png'}")
        
        if interactive:
            # Interactive plot
            interactive_fig = create_interactive_plot(
                graph,
                title="Interactive COLLIE Network"
            )
            
            # Save interactive plot
            interactive_file = plots_dir / "interactive_network.html"
            interactive_fig.write_html(str(interactive_file))
            print(f"✅ Generated interactive plot: {interactive_file}")
    
    # Step 8: Export to Cypher (Optional)
    if export_cypher:
        print("\n🔗 Step 8: Export to Cypher")
        print("-" * 40)
        
        cypher_script = generate_cypher_script(crm_entities)
        cypher_file = output_path / "network.cypher"
        with open(cypher_file, "w") as f:
            f.write(cypher_script)
        
        print(f"✅ Generated Cypher script: {cypher_file}")
    
    # Step 9: Create Summary Report
    print("\n📋 Step 9: Create Summary Report")
    print("-" * 40)
    
    summary_file = output_path / "workflow_summary.md"
    with open(summary_file, "w") as f:
        f.write("# COLLIE Workflow Summary\n\n")
        f.write(f"## Input Text\n\n{text[:200]}...\n\n")
        f.write(f"## Extracted Entities\n\n")
        f.write(f"- Total entities: {len(extraction_result.entities)}\n")
        f.write(f"- Total relationships: {len(extraction_result.relationships)}\n\n")
        f.write(f"## Network Analysis\n\n")
        f.write(f"- Nodes: {graph.number_of_nodes()}\n")
        f.write(f"- Edges: {graph.number_of_edges()}\n")
        f.write(f"- Density: {network_stats['network_info']['density']:.3f}\n")
        f.write(f"- Communities: {len(communities)}\n\n")
        f.write(f"## Output Files\n\n")
        f.write(f"- Canonical JSON: {json_file}\n")
        f.write(f"- Markdown reports: {markdown_dir}\n")
        if visualize or interactive:
            f.write(f"- Network plots: {plots_dir}\n")
        if export_cypher:
            f.write(f"- Cypher script: {cypher_file}\n")
    
    print(f"✅ Created summary report: {summary_file}")
    
    print("\n🎉 Complete Workflow Demo Finished!")
    print("=" * 50)
    print(f"📁 All outputs saved to: {output_path.absolute()}")


async def einstein_demo():
    """Run the Einstein biography demo."""
    print("🧠 Running Einstein Biography Demo")
    print("=" * 50)
    
    # Read Einstein biography
    einstein_file = Path("src/collie/examples/einstein.md")
    if not einstein_file.exists():
        print(f"❌ Einstein file not found: {einstein_file}")
        return
    
    with open(einstein_file, "r") as f:
        einstein_text = f.read()
    
    # Run complete workflow
    await complete_workflow_demo(einstein_text, "einstein_output")


async def handle_extract_command(args):
    """Handle the extract command."""
    if not args.text and not args.file:
        print("Error: Either --text or --file must be provided")
        return
    
    if args.text and args.file:
        print("Error: Provide either --text or --file, not both")
        return
    
    # Get input text
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            return
        with open(file_path, "r") as f:
            text = f.read()
    else:
        text = args.text
    
    print(f"🔍 Extracting entities from {'file' if args.file else 'text'}...")
    
    # Extract entities
    extractor = InformationExtractor()
    extraction_result = await extractor.extract_from_text(text)
    
    # Filter by confidence
    filtered_entities = [e for e in extraction_result.entities if e.confidence >= args.confidence]
    filtered_relationships = [r for r in extraction_result.relationships if r.confidence >= args.confidence]
    
    print(f"✅ Extracted {len(filtered_entities)} entities and {len(filtered_relationships)} relationships")
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # Convert to CRM entities first
    from collie.models.base import CRMEntity
    crm_entities = []
    for entity in filtered_entities:
        crm_entity = CRMEntity(
            id=str(entity.id),
            class_code=entity.class_code,
            label=entity.label,
            notes=entity.description
        )
        crm_entities.append(crm_entity)
    
    # Save results
    if args.format in ["json", "both"]:
        import json
        
        # Save raw extraction results
        result_data = {
            "entities": [e.model_dump() for e in filtered_entities],
            "relationships": [r.model_dump() for r in filtered_relationships]
        }
        with open(output_dir / "extraction_result.json", "w") as f:
            json.dump(result_data, f, indent=2)
        print(f"📄 Saved raw extraction results to {output_dir / 'extraction_result.json'}")
        
        # Save canonical JSON (important for async/future processing)
        canonical_json = [entity.model_dump(mode='json') for entity in crm_entities]
        with open(output_dir / "canonical_entities.json", "w") as f:
            json.dump(canonical_json, f, indent=2)
        print(f"💾 Saved canonical JSON to {output_dir / 'canonical_entities.json'}")
    
    if args.format in ["markdown", "both"]:
        markdown_content = render_table(crm_entities)
        with open(output_dir / "extraction_result.md", "w") as f:
            f.write(markdown_content)
        print(f"📄 Saved Markdown results to {output_dir / 'extraction_result.md'}")


async def handle_analyze_command(args):
    """Handle the analyze command."""
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        return
    
    print(f"📊 Analyzing entities from {input_file}...")
    
    # Load entities
    import json
    with open(input_file, "r") as f:
        data = json.load(f)
    
    # Convert to CRM entities
    from collie.models.base import CRMEntity
    entities = []
    
    # Handle both canonical JSON format and raw extraction format
    if isinstance(data, list):
        # Canonical JSON format: [{"id": "...", "class_code": "...", ...}, ...]
        for entity_data in data:
            entity = CRMEntity(**entity_data)
            entities.append(entity)
    elif isinstance(data, dict) and "entities" in data:
        # Raw extraction format: {"entities": [...], "relationships": [...]}
        for entity_data in data["entities"]:
            entity = CRMEntity(
                id=entity_data["id"],
                class_code=entity_data["class_code"],
                label=entity_data["label"],
                notes=entity_data.get("description", "")
            )
            entities.append(entity)
    else:
        print(f"Error: Unrecognized JSON format in {input_file}")
        return
    
    print(f"✅ Loaded {len(entities)} entities")
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # Convert to NetworkX graph
    graph = to_networkx_graph(entities)
    print(f"📈 Created NetworkX graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
    
    # Run analysis based on flags
    if args.centrality or args.all:
        print("🔍 Calculating centrality measures...")
        centrality_measures = calculate_centrality_measures(graph)
        
        # Save centrality results
        with open(output_dir / "centrality_measures.json", "w") as f:
            json.dump(centrality_measures, f, indent=2)
        print(f"📄 Saved centrality measures to {output_dir / 'centrality_measures.json'}")
    
    if args.communities or args.all:
        print("🔍 Finding communities...")
        communities = find_communities(graph)
        
        # Save community results
        community_data = {
            "num_communities": len(communities),
            "communities": [list(community) for community in communities]
        }
        with open(output_dir / "communities.json", "w") as f:
            json.dump(community_data, f, indent=2)
        print(f"📄 Saved community analysis to {output_dir / 'communities.json'}")
    
    if args.visualize or args.all:
        print("🎨 Creating visualizations...")
        plot_network_graph(
            graph,
            title="CRM Entity Network",
            save_path=str(output_dir / "network_plot.png"),
            show_plot=False
        )
        print(f"📄 Saved static plot to {output_dir / 'network_plot.png'}")
    
    if args.interactive or args.all:
        print("🎨 Creating interactive plot...")
        interactive_fig = create_interactive_plot(graph, title="Interactive CRM Network")
        interactive_fig.write_html(str(output_dir / "interactive_network.html"))
        print(f"📄 Saved interactive plot to {output_dir / 'interactive_network.html'}")
    
    if args.export_cypher or args.all:
        print("🔗 Exporting to Cypher...")
        cypher_script = generate_cypher_script(entities)
        with open(output_dir / "entities.cypher", "w") as f:
            f.write(cypher_script)
        print(f"📄 Saved Cypher script to {output_dir / 'entities.cypher'}")


async def handle_workflow_command(args):
    """Handle the workflow command."""
    if not args.text and not args.file:
        print("Error: Either --text or --file must be provided")
        return
    
    if args.text and args.file:
        print("Error: Provide either --text or --file, not both")
        return
    
    # Get input text
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            return
        with open(file_path, "r") as f:
            text = f.read()
    else:
        text = args.text
    
    # Determine which steps to run
    run_all = args.all
    run_visualize = args.visualize or run_all
    run_interactive = args.interactive or run_all
    run_cypher = args.export_cypher or run_all
    
    # Run the complete workflow
    await complete_workflow_demo(text, args.output, 
                               visualize=run_visualize,
                               interactive=run_interactive,
                               export_cypher=run_cypher,
                               confidence_threshold=args.confidence)


async def handle_demo_command(args):
    """Handle the demo command."""
    if args.einstein:
        await einstein_demo()
    elif args.sample:
        sample_text = """
        Albert Einstein was born on March 14, 1879, in Ulm, Germany. 
        He developed the theory of relativity and won the Nobel Prize in Physics in 1921.
        Einstein worked at the Institute for Advanced Study in Princeton, New Jersey.
        He died on April 18, 1955, at Princeton Hospital.
        """
        await complete_workflow_demo(sample_text, args.output)
    else:
        print("Error: Specify either --einstein or --sample")


async def main():
    """Main function for CLI."""
    parser = argparse.ArgumentParser(
        description="COLLIE - Complete workflow for cultural heritage information extraction and analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  collie extract --text "Albert Einstein was born in Ulm, Germany"
  collie extract --file einstein.md --output results/
  collie analyze --input entities.json --visualize --export-cypher
  collie workflow --file einstein.md --all --output einstein_results/
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract entities from text using AI")
    extract_parser.add_argument("--text", help="Text to extract entities from")
    extract_parser.add_argument("--file", help="File containing text to extract entities from")
    extract_parser.add_argument("--output", "-o", default="output", help="Output directory")
    extract_parser.add_argument("--confidence", type=float, default=0.5, help="Minimum confidence threshold")
    extract_parser.add_argument("--format", choices=["json", "markdown", "both"], default="both", help="Output format")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze extracted entities")
    analyze_parser.add_argument("--input", "-i", required=True, help="Input file with extracted entities")
    analyze_parser.add_argument("--output", "-o", default="analysis", help="Output directory")
    analyze_parser.add_argument("--visualize", action="store_true", help="Create visualizations")
    analyze_parser.add_argument("--interactive", action="store_true", help="Create interactive plots")
    analyze_parser.add_argument("--export-cypher", action="store_true", help="Export to Cypher script")
    analyze_parser.add_argument("--centrality", action="store_true", help="Calculate centrality measures")
    analyze_parser.add_argument("--communities", action="store_true", help="Find communities")
    
    # Workflow command (complete pipeline)
    workflow_parser = subparsers.add_parser("workflow", help="Run complete workflow")
    workflow_parser.add_argument("--text", help="Text to process")
    workflow_parser.add_argument("--file", help="File containing text to process")
    workflow_parser.add_argument("--output", "-o", default="workflow_output", help="Output directory")
    workflow_parser.add_argument("--all", action="store_true", help="Run all analysis steps")
    workflow_parser.add_argument("--visualize", action="store_true", help="Create visualizations")
    workflow_parser.add_argument("--interactive", action="store_true", help="Create interactive plots")
    workflow_parser.add_argument("--export-cypher", action="store_true", help="Export to Cypher script")
    workflow_parser.add_argument("--confidence", type=float, default=0.5, help="Minimum confidence threshold")
    
    # Demo commands
    demo_parser = subparsers.add_parser("demo", help="Run demo examples")
    demo_parser.add_argument("--einstein", action="store_true", help="Run Einstein biography demo")
    demo_parser.add_argument("--sample", action="store_true", help="Run sample text demo")
    demo_parser.add_argument("--output", "-o", default="demo_output", help="Output directory")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Check API key for commands that need it
    if args.command in ["extract", "workflow"]:
        check_api_key()
    
    if args.command == "extract":
        await handle_extract_command(args)
    elif args.command == "analyze":
        await handle_analyze_command(args)
    elif args.command == "workflow":
        await handle_workflow_command(args)
    elif args.command == "demo":
        await handle_demo_command(args)


def cli():
    """Command line interface entry point."""
    asyncio.run(main())


if __name__ == "__main__":
    cli()
