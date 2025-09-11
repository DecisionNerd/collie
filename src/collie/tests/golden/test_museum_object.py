"""
Golden test for museum object example.
Tests the complete workflow from JSON to Markdown to Cypher.
"""

import json
from pathlib import Path
from ..models.generated.e_classes import EE1_CRMEntity, EE22_HumanMadeObject, EE12_Production, EE53_Place, EE52_TimeSpan, EE61_TimePrimitive
from ..io.to_markdown import to_markdown, MarkdownStyle
from ..io.to_cypher import generate_cypher_script, generate_cypher_parameters


def test_museum_object_workflow():
    """Test the complete museum object workflow."""
    # Load the example data
    example_file = Path(__file__).parent.parent.parent / "examples" / "museum_object.json"
    with open(example_file, 'r') as f:
        data = json.load(f)
    
    # Create entities from JSON
    entities = []
    for entity_data in data["entities"]:
        if entity_data["class_code"] == "E22":
            entity = EE22_HumanMadeObject(**entity_data)
        elif entity_data["class_code"] == "E12":
            entity = EE12_Production(**entity_data)
        elif entity_data["class_code"] == "E53":
            entity = EE53_Place(**entity_data)
        elif entity_data["class_code"] == "E52":
            entity = EE52_TimeSpan(**entity_data)
        elif entity_data["class_code"] == "E61":
            entity = EE61_TimePrimitive(**entity_data)
        else:
            entity = EE1_CRMEntity(**entity_data)
        
        entities.append(entity)
    
    # Test Markdown rendering
    vase = entities[0]  # EE22_HumanMadeObject
    markdown_card = to_markdown(vase, MarkdownStyle.CARD)
    markdown_detailed = to_markdown(vase, MarkdownStyle.DETAILED)
    markdown_table = to_markdown(entities, MarkdownStyle.TABLE)
    markdown_narrative = to_markdown(entities[1], MarkdownStyle.NARRATIVE)  # EE12_Production
    
    # Verify Markdown output contains expected elements
    assert "### E22 · Human-Made Object · Ancient Greek Vase (obj_001)" in markdown_card
    assert "**Location** (`current_location`): place_001" in markdown_card
    assert "**Produced By** (`produced_by`): prod_001" in markdown_card
    
    assert "## E22 · Human-Made Object — Ancient Greek Vase (obj_001)" in markdown_detailed
    assert "**Notes** (`notes`): A beautifully preserved amphora" in markdown_detailed
    
    assert "| id | class_code | label | type |" in markdown_table
    assert "| obj_001 | E22 | Ancient Greek Vase |" in markdown_table
    
    assert "**Vase Production**" in markdown_narrative
    assert "is a production" in markdown_narrative
    assert "that occurred during timespan_001" in markdown_narrative
    
    # Test Cypher generation
    cypher_script = generate_cypher_script(entities)
    cypher_params = generate_cypher_parameters(entities)
    
    # Verify Cypher output contains expected elements
    assert "-- Create constraints" in cypher_script
    assert "CREATE CONSTRAINT crm_id IF NOT EXISTS FOR (n:CRM) REQUIRE n.id IS UNIQUE;" in cypher_script
    assert "-- Create nodes" in cypher_script
    assert "UNWIND $nodes_0 AS n" in cypher_script
    assert "MERGE (x:CRM {id: n.id})" in cypher_script
    assert "SET x.class_code = n.class_code" in cypher_script
    
    # Verify relationship creation
    assert "-- Create relationships" in cypher_script
    assert "UNWIND $rels_P53_HAS_CURRENT_LOCATION_0 AS r" in cypher_script
    assert "MERGE (s)-[:`P53_HAS_CURRENT_LOCATION`]->(t);" in cypher_script
    
    # Verify parameters
    assert "nodes_0" in cypher_params
    assert len(cypher_params["nodes_0"]) == 7  # All 7 entities
    
    # Check specific node data
    node_data = cypher_params["nodes_0"]
    vase_node = next(node for node in node_data if node["id"] == "obj_001")
    assert vase_node["class_code"] == "E22"
    assert vase_node["label"] == "Ancient Greek Vase"
    assert vase_node["type"] == ["E55:Vessel", "E55:Ceramic"]
    
    # Check relationship parameters
    assert "rels_P53_HAS_CURRENT_LOCATION_0" in cypher_params
    assert "rels_P108_WAS_PRODUCED_BY_0" in cypher_params
    assert "rels_P4_HAS_TIME_SPAN_0" in cypher_params
    assert "rels_P7_TOOK_PLACE_AT_0" in cypher_params
    assert "rels_P79_BEGIN_OF_THE_BEGIN_0" in cypher_params
    assert "rels_P80_END_OF_THE_END_0" in cypher_params
    
    # Verify relationship data
    location_rels = cypher_params["rels_P53_HAS_CURRENT_LOCATION_0"]
    assert len(location_rels) == 1
    assert location_rels[0]["src"] == "obj_001"
    assert location_rels[0]["tgt"] == "place_001"
    
    production_rels = cypher_params["rels_P108_WAS_PRODUCED_BY_0"]
    assert len(production_rels) == 1
    assert production_rels[0]["src"] == "obj_001"
    assert production_rels[0]["tgt"] == "prod_001"


def test_museum_object_validation():
    """Test validation of the museum object example."""
    from ..validators.quantifiers import validate_batch_quantifiers, ValidationSeverity
    from ..validators.typing_rules import validate_batch_typing
    
    # Load and create entities
    example_file = Path(__file__).parent.parent.parent / "examples" / "museum_object.json"
    with open(example_file, 'r') as f:
        data = json.load(f)
    
    entities = []
    for entity_data in data["entities"]:
        if entity_data["class_code"] == "E22":
            entity = EE22_HumanMadeObject(**entity_data)
        elif entity_data["class_code"] == "E12":
            entity = EE12_Production(**entity_data)
        elif entity_data["class_code"] == "E53":
            entity = EE53_Place(**entity_data)
        elif entity_data["class_code"] == "E52":
            entity = EE52_TimeSpan(**entity_data)
        elif entity_data["class_code"] == "E61":
            entity = EE61_TimePrimitive(**entity_data)
        else:
            entity = EE1_CRMEntity(**entity_data)
        
        entities.append(entity)
    
    # Test quantifier validation
    quantifier_results = validate_batch_quantifiers(entities, ValidationSeverity.WARN)
    assert len(quantifier_results) == 0  # Should have no validation issues
    
    # Test typing validation
    typing_results = validate_batch_typing(entities, ValidationSeverity.WARN)
    assert len(typing_results) == 0  # Should have no validation issues


def test_museum_object_roundtrip():
    """Test roundtrip conversion from JSON to entities and back."""
    # Load the example data
    example_file = Path(__file__).parent.parent.parent / "examples" / "museum_object.json"
    with open(example_file, 'r') as f:
        original_data = json.load(f)
    
    # Create entities from JSON
    entities = []
    for entity_data in original_data["entities"]:
        if entity_data["class_code"] == "E22":
            entity = EE22_HumanMadeObject(**entity_data)
        elif entity_data["class_code"] == "E12":
            entity = EE12_Production(**entity_data)
        elif entity_data["class_code"] == "E53":
            entity = EE53_Place(**entity_data)
        elif entity_data["class_code"] == "E52":
            entity = EE52_TimeSpan(**entity_data)
        elif entity_data["class_code"] == "E61":
            entity = EE61_TimePrimitive(**entity_data)
        else:
            entity = EE1_CRMEntity(**entity_data)
        
        entities.append(entity)
    
    # Convert back to JSON
    converted_data = {"entities": [entity.dict() for entity in entities]}
    
    # Verify that key data is preserved
    assert len(converted_data["entities"]) == len(original_data["entities"])
    
    # Check specific entity
    original_vase = next(e for e in original_data["entities"] if e["id"] == "obj_001")
    converted_vase = next(e for e in converted_data["entities"] if e["id"] == "obj_001")
    
    assert original_vase["class_code"] == converted_vase["class_code"]
    assert original_vase["label"] == converted_vase["label"]
    assert original_vase["type"] == converted_vase["type"]
    assert original_vase["current_location"] == converted_vase["current_location"]
    assert original_vase["produced_by"] == converted_vase["produced_by"]
