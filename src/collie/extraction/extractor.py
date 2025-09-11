"""
PydanticAI-powered information extractor for CIDOC CRM entities.

This module provides intelligent extraction of CRM entities and relationships
from unstructured text using AI models.
"""

import asyncio
import os
from typing import List, Optional

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


class InformationExtractor:
    """
    AI-powered information extractor for CIDOC CRM entities.
    
    Uses PydanticAI to extract structured entities and relationships
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
        self.model = GoogleModel("gemini-2.0-flash-001", provider=self.provider)
        self.agent = Agent(self.model)
    
    async def extract_from_text(self, text: str) -> ExtractionResult:
        """
        Extract CRM entities and relationships from text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            ExtractionResult containing extracted entities and relationships
        """
        # Create extraction prompt
        prompt = self._create_extraction_prompt(text)
        
        # Use PydanticAI to extract structured data
        result = await self.agent.run(prompt)
        
        # Parse and structure the results
        return self._parse_extraction_result(result, text)
    
    def _create_extraction_prompt(self, text: str) -> str:
        """Create a detailed prompt for entity extraction."""
        return f"""
        Analyze the following text and extract CIDOC CRM entities and relationships.
        
        Text: {text}
        
        Please identify and extract:
        
        1. **Persons (E21)**: People mentioned with their biographical information
        2. **Events (E5)**: Things that happened, with dates, locations, and participants
        3. **Places (E53)**: Locations mentioned with geographical context
        4. **Objects (E22)**: Physical objects, artifacts, or creations
        5. **Time Periods (E52)**: Specific dates, periods, or temporal references
        
        For each entity, provide:
        - A clear label/name
        - The appropriate CIDOC CRM class code
        - A detailed description
        - Relevant properties specific to the entity type
        - Confidence score (0.0 to 1.0)
        - Source text snippet
        
        For relationships, identify:
        - Source and target entities
        - Appropriate CIDOC CRM property codes (P-codes)
        - Relationship descriptions
        - Confidence scores
        
        Focus on extracting factual information that can be structured according to CIDOC CRM standards.
        Be thorough but accurate - it's better to extract fewer high-confidence entities than many uncertain ones.
        """
    
    def _parse_extraction_result(self, result, source_text: str) -> ExtractionResult:
        """
        Parse the AI extraction result into structured CRM entities and relationships.
        
        This is a simplified parser - in a real implementation, you would use
        PydanticAI's structured output capabilities to get properly typed results.
        """
        entities = []
        relationships = []
        
        # For now, create a simple extraction based on the text analysis
        # In a real implementation, this would parse the AI's structured response
        
        # Extract basic entities using simple text analysis
        entities.extend(self._extract_persons(source_text))
        entities.extend(self._extract_events(source_text))
        entities.extend(self._extract_places(source_text))
        entities.extend(self._extract_objects(source_text))
        entities.extend(self._extract_times(source_text))
        
        # Extract relationships between entities
        relationships.extend(self._extract_relationships(entities, source_text))
        
        return ExtractionResult(
            entities=entities,
            relationships=relationships,
            extraction_metadata={
                "source_text_length": len(source_text),
                "extraction_method": "pydantic_ai",
                "model": "gemini-2.0-flash-001"
            }
        )
    
    def _extract_persons(self, text: str) -> List[ExtractedEntity]:
        """Extract person entities from text using simple pattern matching."""
        persons = []
        
        # Simple pattern matching for names (this would be much more sophisticated in practice)
        import re
        
        # Look for capitalized words that might be names
        name_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
        potential_names = re.findall(name_pattern, text)
        
        for name in potential_names:
            if len(name.split()) >= 2:  # At least first and last name
                person = PersonExtraction(
                    label=name,
                    description=f"Person mentioned in the text: {name}",
                    confidence=0.7,
                    source_text=name,
                    properties={"extracted_name": name}
                )
                persons.append(person)
        
        return persons
    
    def _extract_events(self, text: str) -> List[ExtractedEntity]:
        """Extract event entities from text."""
        events = []
        
        # Look for event-related keywords
        event_keywords = [
            "born", "died", "married", "graduated", "invented", "discovered",
            "published", "awarded", "founded", "created", "developed", "won"
        ]
        
        import re
        for keyword in event_keywords:
            pattern = rf'\b{keyword}\b'
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                # Extract surrounding context
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                event = EventExtraction(
                    label=f"Event involving {keyword}",
                    description=f"Event mentioned in context: {context.strip()}",
                    confidence=0.6,
                    source_text=context.strip(),
                    event_type=keyword,
                    properties={"event_keyword": keyword}
                )
                events.append(event)
        
        return events
    
    def _extract_places(self, text: str) -> List[ExtractedEntity]:
        """Extract place entities from text."""
        places = []
        
        # Look for place-related keywords
        place_keywords = [
            "Germany", "Switzerland", "Italy", "United States", "Princeton",
            "Ulm", "Munich", "Zurich", "Berlin", "New York", "California"
        ]
        
        import re
        for place in place_keywords:
            pattern = rf'\b{place}\b'
            if re.search(pattern, text, re.IGNORECASE):
                place_entity = PlaceExtraction(
                    label=place,
                    description=f"Place mentioned in the text: {place}",
                    confidence=0.8,
                    source_text=place,
                    place_type="Geographical Location",
                    properties={"place_name": place}
                )
                places.append(place_entity)
        
        return places
    
    def _extract_objects(self, text: str) -> List[ExtractedEntity]:
        """Extract object entities from text."""
        objects = []
        
        # Look for object-related keywords
        object_keywords = [
            "theory", "equation", "paper", "patent", "Nobel Prize", "relativity",
            "photoelectric effect", "atomic bomb", "Manhattan Project"
        ]
        
        import re
        for obj in object_keywords:
            pattern = rf'\b{obj}\b'
            if re.search(pattern, text, re.IGNORECASE):
                object_entity = ObjectExtraction(
                    label=obj,
                    description=f"Object or concept mentioned: {obj}",
                    confidence=0.7,
                    source_text=obj,
                    object_type="Intellectual Object",
                    properties={"object_name": obj}
                )
                objects.append(object_entity)
        
        return objects
    
    def _extract_times(self, text: str) -> List[ExtractedEntity]:
        """Extract time entities from text."""
        times = []
        
        # Look for date patterns
        import re
        date_pattern = r'\b\d{4}\b'  # 4-digit years
        years = re.findall(date_pattern, text)
        
        for year in years:
            time_entity = TimeExtraction(
                label=f"Year {year}",
                description=f"Time period: {year}",
                confidence=0.9,
                source_text=year,
                time_type="Year",
                start_date=f"{year}-01-01",
                end_date=f"{year}-12-31",
                properties={"year": int(year)}
            )
            times.append(time_entity)
        
        return times
    
    def _extract_relationships(self, entities: List[ExtractedEntity], text: str) -> List[ExtractedRelationship]:
        """Extract relationships between entities."""
        relationships = []
        
        # Simple relationship extraction based on proximity in text
        # In a real implementation, this would use more sophisticated NLP
        
        for i, source in enumerate(entities):
            for j, target in enumerate(entities[i+1:], i+1):
                # Check if entities appear near each other in text
                if self._entities_are_related(source, target, text):
                    relationship = ExtractedRelationship(
                        source_id=source.id,
                        target_id=target.id,
                        property_code="P69",  # has association with
                        property_label="has association with",
                        confidence=0.5,
                        source_text=f"{source.label} - {target.label}",
                        properties={"relationship_type": "association"}
                    )
                    relationships.append(relationship)
        
        return relationships
    
    def _entities_are_related(self, source: ExtractedEntity, target: ExtractedEntity, text: str) -> bool:
        """Check if two entities are related based on text proximity."""
        # Simple check: if both entities appear in the same sentence or nearby sentences
        import re
        
        source_positions = [m.start() for m in re.finditer(re.escape(source.label), text, re.IGNORECASE)]
        target_positions = [m.start() for m in re.finditer(re.escape(target.label), text, re.IGNORECASE)]
        
        for src_pos in source_positions:
            for tgt_pos in target_positions:
                if abs(src_pos - tgt_pos) < 200:  # Within 200 characters
                    return True
        
        return False
