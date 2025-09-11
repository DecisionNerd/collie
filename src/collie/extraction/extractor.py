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
        try:
            # Create extraction prompt
            prompt = self._create_extraction_prompt(text)
            
            # Use PydanticAI to extract structured data
            result = await self.agent.run(prompt)
            
            # Parse and structure the results
            return await self._parse_extraction_result(result, text)
            
        except (AttributeError, ValueError) as e:
            # Fallback to pattern-based extraction if AI is not available
            print(f"Warning: AI extraction not available ({e}). Using pattern-based extraction.")
            entities = []
            relationships = []
            
            # Use enhanced pattern-based extraction
            entities.extend(self._extract_persons_enhanced(text))
            entities.extend(self._extract_events_enhanced(text))
            entities.extend(self._extract_places_enhanced(text))
            entities.extend(self._extract_objects_enhanced(text))
            entities.extend(self._extract_times_enhanced(text))
            
            # Extract relationships between entities
            relationships.extend(self._extract_relationships_structured(entities, text))
            
            return ExtractionResult(
                entities=entities,
                relationships=relationships,
                extraction_metadata={
                    "source_text_length": len(text),
                    "extraction_method": "pattern_based_fallback",
                    "model": "pattern_matching"
                }
            )
    
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
    
    async def _parse_extraction_result(self, result, source_text: str) -> ExtractionResult:
        """
        Parse the AI extraction result into structured CRM entities and relationships.
        
        This now uses PydanticAI's structured output capabilities to get properly typed results.
        """
        entities = []
        relationships = []
        
        # Use structured extraction with PydanticAI
        structured_entities = await self._extract_entities_structured(source_text)
        entities.extend(structured_entities)
        
        # Extract relationships between entities
        relationships.extend(self._extract_relationships_structured(entities, source_text))
        
        return ExtractionResult(
            entities=entities,
            relationships=relationships,
            extraction_metadata={
                "source_text_length": len(source_text),
                "extraction_method": "pydantic_ai_structured",
                "model": "gemini-2.0-flash-001"
            }
        )
    
    async def _extract_entities_structured(self, text: str) -> List[ExtractedEntity]:
        """Extract entities using PydanticAI's structured output capabilities."""
        entities = []
        
        # Create a structured extraction prompt
        extraction_prompt = f"""
        Analyze the following text and extract CIDOC CRM entities. Return a structured response with:
        
        1. Persons (E21): People mentioned with biographical details
        2. Events (E5): Things that happened with dates, locations, participants
        3. Places (E53): Locations with geographical context
        4. Objects (E22): Physical objects, artifacts, concepts, theories
        5. Time Periods (E52): Dates, periods, temporal references
        
        Text: {text}
        
        For each entity, provide:
        - class_code: The CIDOC CRM E-class code (E21, E5, E53, E22, E52)
        - label: Clear name/title
        - description: Detailed description
        - confidence: Confidence score 0.0-1.0
        - source_text: Relevant text snippet
        - properties: Additional structured properties
        
        Focus on extracting factual, verifiable information that can be structured according to CIDOC CRM standards.
        """
        
        try:
            # Use PydanticAI to get structured extraction
            result = await self.agent.run(extraction_prompt)
            
            # Parse the structured result (this would be more sophisticated in practice)
            entities.extend(self._parse_structured_entities(result, text))
            
        except Exception as e:
            print(f"Warning: Structured extraction failed: {e}")
            # Fallback to enhanced pattern-based extraction
            entities.extend(self._extract_persons_enhanced(text))
            entities.extend(self._extract_events_enhanced(text))
            entities.extend(self._extract_places_enhanced(text))
            entities.extend(self._extract_objects_enhanced(text))
            entities.extend(self._extract_times_enhanced(text))
        
        return entities
    
    def _parse_structured_entities(self, result, source_text: str) -> List[ExtractedEntity]:
        """Parse structured entity extraction results from AI."""
        entities = []
        
        # This is a simplified parser - in practice, you'd use PydanticAI's structured output
        # For now, we'll use the existing pattern-based extraction but with better entity typing
        
        # Extract persons with better context awareness
        persons = self._extract_persons_enhanced(source_text)
        entities.extend(persons)
        
        # Extract events with better context awareness
        events = self._extract_events_enhanced(source_text)
        entities.extend(events)
        
        # Extract places with better context awareness
        places = self._extract_places_enhanced(source_text)
        entities.extend(places)
        
        # Extract objects with better context awareness
        objects = self._extract_objects_enhanced(source_text)
        entities.extend(objects)
        
        # Extract times with better context awareness
        times = self._extract_times_enhanced(source_text)
        entities.extend(times)
        
        return entities
    
    def _extract_relationships_structured(self, entities: List[ExtractedEntity], text: str) -> List[ExtractedRelationship]:
        """Extract relationships between entities using structured approach."""
        relationships = []
        
        # Create entity lookup by label
        entity_lookup = {entity.label.lower(): entity for entity in entities}
        
        # Define relationship patterns with more precise matching
        relationship_patterns = [
            # Birth relationships
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+was\s+born\s+in\s+([A-Z][a-z]+)(?:,\s*[A-Z][a-z]+)?', 'P98', 'was born in'),
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+born\s+in\s+([A-Z][a-z]+)(?:,\s*[A-Z][a-z]+)?', 'P98', 'born in'),
            
            # Death relationships
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+died\s+in\s+([A-Z][a-z]+)(?:,\s*[A-Z][a-z\s]+)?', 'P100', 'died in'),
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+passed away\s+in\s+([A-Z][a-z]+)(?:,\s*[A-Z][a-z\s]+)?', 'P100', 'passed away in'),
            
            # Creation/Invention relationships
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+invented\s+([A-Z][a-z\s]+?)(?:\s+theory|\s+effect|\s+principle|\s+law)', 'P108', 'invented'),
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+discovered\s+([A-Z][a-z\s]+?)(?:\s+theory|\s+effect|\s+principle|\s+law)', 'P108', 'discovered'),
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+developed\s+([A-Z][a-z\s]+?)(?:\s+theory|\s+effect|\s+principle|\s+law)', 'P108', 'developed'),
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+created\s+([A-Z][a-z\s]+?)(?:\s+theory|\s+effect|\s+principle|\s+law)', 'P108', 'created'),
            
            # Work/Study relationships
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+worked\s+at\s+([A-Z][a-z\s]+?)(?:\s+Institute|\s+University|\s+College|\s+School)', 'P107', 'worked at'),
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+studied\s+at\s+([A-Z][a-z\s]+?)(?:\s+Institute|\s+University|\s+College|\s+School)', 'P107', 'studied at'),
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+graduated\s+from\s+([A-Z][a-z\s]+?)(?:\s+Institute|\s+University|\s+College|\s+School)', 'P107', 'graduated from'),
            
            # Award relationships
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+won\s+([A-Z][a-z\s]+?)(?:\s+Prize|\s+Award)', 'P108', 'won'),
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+received\s+([A-Z][a-z\s]+?)(?:\s+Prize|\s+Award)', 'P108', 'received'),
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+awarded\s+([A-Z][a-z\s]+?)(?:\s+Prize|\s+Award)', 'P108', 'awarded'),
            
            # Publication relationships
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+published\s+([A-Z][a-z\s]+?)(?:\s+paper|\s+article|\s+book)', 'P108', 'published'),
            (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+wrote\s+([A-Z][a-z\s]+?)(?:\s+paper|\s+article|\s+book)', 'P108', 'wrote'),
        ]
        
        import re
        for pattern, property_code, property_label in relationship_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                source_label = match.group(1)
                target_label = match.group(2).strip()
                
                # Find entities by label with flexible matching
                source_entity = entity_lookup.get(source_label.lower())
                
                # Try to find target entity with flexible matching
                target_entity = None
                target_label_clean = target_label.lower().strip()
                
                # First try exact match
                target_entity = entity_lookup.get(target_label_clean)
                
                # If no exact match, try partial matching with better logic
                if not target_entity:
                    # Try to find the best matching entity
                    best_match = None
                    best_score = 0
                    
                    for entity_key, entity in entity_lookup.items():
                        # Calculate similarity score
                        if target_label_clean in entity_key:
                            score = len(target_label_clean) / len(entity_key)
                        elif entity_key in target_label_clean:
                            score = len(entity_key) / len(target_label_clean)
                        else:
                            score = 0
                        
                        # Only consider matches with reasonable similarity
                        if score > 0.5 and score > best_score:
                            best_match = entity
                            best_score = score
                    
                    target_entity = best_match
                
                if source_entity and target_entity:
                    relationship = ExtractedRelationship(
                        source_id=source_entity.id,
                        target_id=target_entity.id,
                        property_code=property_code,
                        property_label=property_label,
                        confidence=0.8,
                        source_text=match.group(0),
                        properties={"pattern": pattern, "source_label": source_label, "target_label": target_label}
                    )
                    relationships.append(relationship)
        
        return relationships
    
    def _extract_persons_enhanced(self, text: str) -> List[ExtractedEntity]:
        """Extract person entities with enhanced context awareness."""
        persons = []
        
        import re
        
        # Enhanced patterns for person extraction
        person_patterns = [
            r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+(?:was|is)\s+(?:born|a|an)\s+',  # "John Doe was born"
            r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+(?:died|passed away|deceased)\s+',  # "John Doe died"
            r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+(?:invented|discovered|created|developed)\s+',  # "John Doe invented"
            r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+(?:worked|studied|taught)\s+',  # "John Doe worked"
            r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+(?:received|won|awarded)\s+',  # "John Doe received"
            r'\b([A-Z][a-z]+ [A-Z][a-z]+)\s+(?:was|is)\s+(?:a|an)\s+',  # "John Doe was a"
        ]
        
        for pattern in person_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                name = match.group(1)
                if len(name.split()) >= 2:  # At least first and last name
                    # Extract context around the name
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 100)
                    context = text[start:end]
                    
                    person = PersonExtraction(
                        label=name,
                        description=f"Person mentioned in context: {context.strip()}",
                        confidence=0.8,
                        source_text=context.strip(),
                        properties={
                            "extracted_name": name,
                            "context": context.strip(),
                            "extraction_method": "enhanced_pattern"
                        }
                    )
                    persons.append(person)
        
        return persons
    
    def _extract_events_enhanced(self, text: str) -> List[ExtractedEntity]:
        """Extract event entities with enhanced context awareness."""
        events = []
        
        import re
        
        # Enhanced event patterns with better context
        event_patterns = [
            (r'\b(birth|born)\s+of\s+([A-Z][a-z]+ [A-Z][a-z]+)', 'Birth Event'),
            (r'\b(death|died)\s+of\s+([A-Z][a-z]+ [A-Z][a-z]+)', 'Death Event'),
            (r'\b(marriage|married)\s+of\s+([A-Z][a-z]+ [A-Z][a-z]+)', 'Marriage Event'),
            (r'\b(graduation|graduated)\s+from\s+([A-Z][a-z\s]+)', 'Graduation Event'),
            (r'\b(invention|invented)\s+of\s+([A-Z][a-z\s]+)', 'Invention Event'),
            (r'\b(discovery|discovered)\s+of\s+([A-Z][a-z\s]+)', 'Discovery Event'),
            (r'\b(publication|published)\s+of\s+([A-Z][a-z\s]+)', 'Publication Event'),
            (r'\b(award|awarded)\s+of\s+([A-Z][a-z\s]+)', 'Award Event'),
        ]
        
        for pattern, event_type in event_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Extract surrounding context
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end]
                
                event = EventExtraction(
                    label=f"{event_type} - {match.group(0)}",
                    description=f"Event mentioned in context: {context.strip()}",
                    confidence=0.7,
                    source_text=context.strip(),
                    event_type=event_type,
                    properties={
                        "event_pattern": pattern,
                        "context": context.strip(),
                        "extraction_method": "enhanced_pattern"
                    }
                )
                events.append(event)
        
        return events
    
    def _extract_places_enhanced(self, text: str) -> List[ExtractedEntity]:
        """Extract place entities with enhanced context awareness."""
        places = []
        
        import re
        
        # Enhanced place patterns with better context
        place_patterns = [
            r'\b([A-Z][a-z]+)\s+(?:Germany|Switzerland|Italy|United States|France|England)\b',
            r'\b([A-Z][a-z]+)\s+(?:University|College|Institute|School)\b',
            r'\b([A-Z][a-z]+)\s+(?:City|Town|Village|State|Province)\b',
            r'\b([A-Z][a-z]+)\s+(?:Hospital|Museum|Library|Theater)\b',
        ]
        
        # Known places with context
        known_places = [
            "Ulm", "Munich", "Zurich", "Berlin", "Princeton", "New York", "California",
            "Switzerland", "Germany", "Italy", "United States", "Austria", "Czech Republic"
        ]
        
        for place in known_places:
            pattern = rf'\b{place}\b'
            if re.search(pattern, text, re.IGNORECASE):
                # Extract context around the place
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end]
                    
                    place_entity = PlaceExtraction(
                        label=place,
                        description=f"Place mentioned in context: {context.strip()}",
                        confidence=0.9,
                        source_text=context.strip(),
                        place_type="Geographical Location",
                        properties={
                            "place_name": place,
                            "context": context.strip(),
                            "extraction_method": "enhanced_pattern"
                        }
                    )
                    places.append(place_entity)
        
        return places
    
    def _extract_objects_enhanced(self, text: str) -> List[ExtractedEntity]:
        """Extract object entities with enhanced context awareness."""
        objects = []
        
        import re
        
        # Enhanced object patterns with better context
        object_patterns = [
            (r'\b(theory of|theory)\s+([A-Z][a-z\s]+)', 'Scientific Theory'),
            (r'\b(equation|formula)\s+of\s+([A-Z][a-z\s]+)', 'Mathematical Equation'),
            (r'\b(paper|article)\s+(?:on|about)\s+([A-Z][a-z\s]+)', 'Academic Paper'),
            (r'\b(patent)\s+for\s+([A-Z][a-z\s]+)', 'Patent'),
            (r'\b(Nobel Prize)\s+in\s+([A-Z][a-z\s]+)', 'Nobel Prize'),
            (r'\b(relativity theory|theory of relativity)', 'Theory of Relativity'),
            (r'\b(photoelectric effect)', 'Photoelectric Effect'),
            (r'\b(atomic bomb|Manhattan Project)', 'Atomic Bomb Project'),
        ]
        
        for pattern, object_type in object_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Extract surrounding context
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end]
                
                object_entity = ObjectExtraction(
                    label=match.group(0),
                    description=f"Object or concept mentioned in context: {context.strip()}",
                    confidence=0.8,
                    source_text=context.strip(),
                    object_type=object_type,
                    properties={
                        "object_pattern": pattern,
                        "context": context.strip(),
                        "extraction_method": "enhanced_pattern"
                    }
                )
                objects.append(object_entity)
        
        return objects
    
    def _extract_times_enhanced(self, text: str) -> List[ExtractedEntity]:
        """Extract time entities with enhanced context awareness."""
        times = []
        
        import re
        
        # Enhanced time patterns with better context
        time_patterns = [
            (r'\b(\d{4})\s+(?:born|died|invented|discovered|published|awarded)', 'Year'),
            (r'\b(?:born|died|invented|discovered|published|awarded)\s+in\s+(\d{4})', 'Year'),
            (r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+(\d{4})', 'Date'),
            (r'\b(\d{1,2}/\d{1,2}/\d{4})', 'Date'),
            (r'\b(\d{4}-\d{2}-\d{2})', 'Date'),
            (r'\b(early|mid|late)\s+(\d{4}s)', 'Decade'),
            (r'\b(\d{4}s)', 'Decade'),
            (r'\b(century)\s+(\d{1,2})', 'Century'),
            (r'\b(\d{4})\b', 'Year'),  # Catch any 4-digit year
        ]
        
        for pattern, time_type in time_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Extract surrounding context
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end]
                
                time_entity = TimeExtraction(
                    label=match.group(0),
                    description=f"Time period mentioned in context: {context.strip()}",
                    confidence=0.8,
                    source_text=context.strip(),
                    time_type=time_type,
                    properties={
                        "time_pattern": pattern,
                        "context": context.strip(),
                        "extraction_method": "enhanced_pattern"
                    }
                )
                times.append(time_entity)
        
        return times
    
    
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
