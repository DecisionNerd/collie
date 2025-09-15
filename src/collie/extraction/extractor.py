"""
LLM-powered information extractor for CIDOC CRM entities using PydanticAI.

This module provides intelligent extraction of CRM entities and relationships
from unstructured text using structured LLM output with CIDOC CRM standards enforcement.
"""

import asyncio
import os
from typing import List, Optional
import uuid

from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from .models import (
    ExtractionResult,
    ExtractedEntity,
    ExtractedRelationship,
    PersonExtraction,
    EventExtraction,
    PlaceExtraction,
    ObjectExtraction,
    TimeExtraction,
)
from .llm_models import (
    CIDOCExtractionResult,
    CIDOCPerson,
    CIDOCEvent,
    CIDOCPlace,
    CIDOCObject,
    CIDOCTime,
    CIDOCRelationship,
    CIDOC_PROPERTIES,
)


class InformationExtractor:
    """
    LLM-powered information extractor for CIDOC CRM entities.
    
    Uses PydanticAI with structured output to extract entities and relationships
    from unstructured text according to CIDOC CRM standards.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the information extractor.
        
        Args:
            api_key: Google API key for PydanticAI. If None, will try to get from environment.
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable.")
        
        self.provider = GoogleProvider(api_key=self.api_key)
        self.model = GoogleModel("gemini-2.5-flash", provider=self.provider)
        self.agent = Agent(
            self.model,
            output_type=CIDOCExtractionResult,
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for CIDOC CRM extraction."""
        return """
You are an expert in CIDOC CRM (Conceptual Reference Model) for cultural heritage information.
Your task is to extract structured entities and relationships from biographical and historical text.

CIDOC CRM Entity Types:
- E21 Person: Individuals with biographical information
- E5 Event: Things that happened (birth, death, marriage, achievements, etc.)
- E53 Place: Locations (cities, countries, institutions, buildings)
- E22 Object: Physical or conceptual objects (theories, awards, publications, artifacts)
- E52 Time-Span: Temporal references (dates, periods, eras)

Key CIDOC CRM Property Codes:
- P98: was born in (Person -> Place)
- P100: died in (Person -> Place)
- P108: has produced (Person -> Object/Event)
- P107: has current or former member (Person -> Institution)
- P7: took place at (Event -> Place)
- P4: has time-span (Event -> Time)
- P11: had participant (Event -> Person)
- P14: carried out by (Event -> Person)

Extraction Guidelines:
1. Extract factual, verifiable information only
2. Use high confidence scores (0.7-1.0) for clear facts
3. Use lower confidence scores (0.3-0.6) for inferred or uncertain information
4. Provide detailed descriptions with context
5. Include relevant source text snippets
6. Ensure proper CIDOC CRM property codes for relationships
7. Be thorough but accurate - quality over quantity

Date Format: Use YYYY-MM-DD format when possible, or YYYY for years only.
Confidence Scores: 0.0 (no confidence) to 1.0 (absolute certainty).
"""
    
    async def extract_from_text(self, text: str) -> ExtractionResult:
        """
        Extract CRM entities and relationships from text using LLM.
        
        Args:
            text: Input text to analyze
            
        Returns:
            ExtractionResult containing extracted entities and relationships
        """
        try:
            # Create extraction prompt
            prompt = self._create_extraction_prompt(text)
            
            # Use PydanticAI to extract structured data
            result = await self.agent.run(prompt)
            
            # Convert LLM result to internal format
            return self._convert_llm_result(result, text)
            
        except Exception as e:
            print(f"Error in LLM extraction: {e}")
            # Return empty result rather than falling back to patterns
            return ExtractionResult(
                entities=[],
                relationships=[],
                extraction_metadata={
                    "source_text_length": len(text),
                    "extraction_method": "llm_failed",
                    "model": "gemini-2.5-flash",
                    "error": str(e)
                }
            )
    
    def _create_extraction_prompt(self, text: str) -> str:
        """Create a detailed prompt for entity extraction."""
        return f"""
Analyze the following text and extract CIDOC CRM entities and relationships.

Text: {text}

Extract the following information:

1. **Persons (E21)**: All people mentioned with biographical details
   - Include birth/death dates and places when mentioned
   - Include nationality, occupation, and other biographical facts
   - Extract family relationships and professional connections

2. **Events (E5)**: All significant events mentioned
   - Births, deaths, marriages, graduations
   - Achievements, awards, publications, inventions
   - Work events, travel, meetings
   - Include dates, locations, and participants

3. **Places (E53)**: All geographical locations and institutions
   - Cities, countries, regions
   - Universities, institutes, organizations
   - Buildings, landmarks, specific locations

4. **Objects (E22)**: All physical and conceptual objects
   - Theories, formulas, concepts
   - Awards, publications, patents
   - Institutions, organizations
   - Artifacts, inventions

5. **Time Periods (E52)**: All temporal references
   - Specific dates, years, decades
   - Periods, eras, time spans
   - Duration references

6. **Relationships**: All connections between entities
   - Use proper CIDOC CRM property codes (P-codes)
   - Include person-place relationships (birth, death, work)
   - Include person-object relationships (created, won, published)
   - Include event relationships (participants, locations, times)

Focus on extracting factual, verifiable information with high confidence.
Be thorough but accurate - it's better to extract fewer high-confidence entities than many uncertain ones.
"""
    
    def _convert_llm_result(self, llm_result: CIDOCExtractionResult, source_text: str) -> ExtractionResult:
        """Convert LLM structured result to internal format."""
        entities = []
        relationships = []
        
        # Convert persons
        for person in llm_result.persons:
            entity = PersonExtraction(
                label=person.label,
                description=person.description,
                confidence=person.confidence,
                source_text=person.source_text,
                properties={
                    "birth_date": person.birth_date,
                    "death_date": person.death_date,
                    "birth_place": person.birth_place,
                    "death_place": person.death_place,
                    "nationality": person.nationality,
                    "occupation": person.occupation,
                    "extraction_method": "llm_structured",
                    "cidoc_class": "E21"
                }
            )
            entities.append(entity)
        
        # Convert events
        for event in llm_result.events:
            entity = EventExtraction(
                label=event.label,
                description=event.description,
                confidence=event.confidence,
                source_text=event.source_text,
                event_type=event.event_type,
                properties={
                    "start_date": event.start_date,
                    "end_date": event.end_date,
                    "location": event.location,
                    "participants": event.participants,
                    "extraction_method": "llm_structured",
                    "cidoc_class": "E5"
                }
            )
            entities.append(entity)
        
        # Convert places
        for place in llm_result.places:
            entity = PlaceExtraction(
                label=place.label,
                description=place.description,
                confidence=place.confidence,
                source_text=place.source_text,
                place_type=place.place_type,
                properties={
                    "coordinates": place.coordinates,
                    "country": place.country,
                    "region": place.region,
                    "extraction_method": "llm_structured",
                    "cidoc_class": "E53"
                }
            )
            entities.append(entity)
        
        # Convert objects
        for obj in llm_result.objects:
            entity = ObjectExtraction(
                label=obj.label,
                description=obj.description,
                confidence=obj.confidence,
                source_text=obj.source_text,
                object_type=obj.object_type,
                properties={
                    "creator": obj.creator,
                    "creation_date": obj.creation_date,
                    "location": obj.location,
                    "extraction_method": "llm_structured",
                    "cidoc_class": "E22"
                }
            )
            entities.append(entity)
        
        # Convert times
        for time in llm_result.times:
            entity = TimeExtraction(
                label=time.label,
                description=time.description,
                confidence=time.confidence,
                source_text=time.source_text,
                time_type=time.time_type,
                properties={
                    "start_date": time.start_date,
                    "end_date": time.end_date,
                    "extraction_method": "llm_structured",
                    "cidoc_class": "E52"
                }
            )
            entities.append(entity)
        
        # Convert relationships
        for rel in llm_result.relationships:
            # Find source and target entities
            source_entity = self._find_entity_by_label(entities, rel.source_label)
            target_entity = self._find_entity_by_label(entities, rel.target_label)
            
            if source_entity and target_entity:
                relationship = ExtractedRelationship(
                    source_id=source_entity.id,
                    target_id=target_entity.id,
                    property_code=rel.property_code,
                    property_label=rel.property_label,
                    confidence=rel.confidence,
                    source_text=rel.source_text,
                    properties={
                        "description": rel.description,
                        "extraction_method": "llm_structured",
                        "cidoc_property": rel.property_code
                    }
                )
                relationships.append(relationship)
        
        return ExtractionResult(
            entities=entities,
            relationships=relationships,
            extraction_metadata={
                "source_text_length": len(source_text),
                "extraction_method": "llm_structured",
                "model": "gemini-2.5-flash",
                "llm_confidence": llm_result.extraction_confidence,
                "total_entities": llm_result.total_entities,
                "total_relationships": llm_result.total_relationships,
                "entities_by_type": {
                    "persons": len(llm_result.persons),
                    "events": len(llm_result.events),
                    "places": len(llm_result.places),
                    "objects": len(llm_result.objects),
                    "times": len(llm_result.times)
                }
            }
        )
    
    def _find_entity_by_label(self, entities: List[ExtractedEntity], label: str) -> Optional[ExtractedEntity]:
        """Find entity by label with fuzzy matching."""
        label_lower = label.lower().strip()
        
        # First try exact match
        for entity in entities:
            if entity.label.lower() == label_lower:
                return entity
        
        # Try partial matching
        for entity in entities:
            if label_lower in entity.label.lower() or entity.label.lower() in label_lower:
                return entity
        
        return None
    
    def get_cidoc_property_info(self, property_code: str) -> dict:
        """Get information about a CIDOC CRM property code."""
        return {
            "code": property_code,
            "label": CIDOC_PROPERTIES.get(property_code, "Unknown"),
            "description": f"CIDOC CRM property {property_code}"
        }
    
    def validate_extraction(self, result: ExtractionResult) -> dict:
        """Validate extraction results against CIDOC CRM standards."""
        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "statistics": {
                "total_entities": len(result.entities),
                "total_relationships": len(result.relationships),
                "entity_types": {},
                "property_codes": set()
            }
        }
        
        # Validate entities
        for entity in result.entities:
            # Check for required fields
            if not entity.label or not entity.label.strip():
                validation_results["errors"].append(f"Entity missing label: {entity.id}")
            
            if not 0.0 <= entity.confidence <= 1.0:
                validation_results["errors"].append(f"Invalid confidence score: {entity.confidence}")
            
            # Count entity types
            entity_type = entity.properties.get("cidoc_class", "Unknown")
            validation_results["statistics"]["entity_types"][entity_type] = \
                validation_results["statistics"]["entity_types"].get(entity_type, 0) + 1
        
        # Validate relationships
        for rel in result.relationships:
            # Check property code format
            if not rel.property_code.startswith("P"):
                validation_results["errors"].append(f"Invalid property code: {rel.property_code}")
            
            # Check if property code exists in CIDOC standards
            if rel.property_code not in CIDOC_PROPERTIES:
                validation_results["warnings"].append(f"Unknown property code: {rel.property_code}")
            
            validation_results["statistics"]["property_codes"].add(rel.property_code)
        
        validation_results["statistics"]["property_codes"] = list(validation_results["statistics"]["property_codes"])
        
        if validation_results["errors"]:
            validation_results["valid"] = False
        
        return validation_results
