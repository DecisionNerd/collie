"""
AI-powered information extraction module for CIDOC CRM entities.

This module provides PydanticAI-powered extraction of CRM entities and relationships
from unstructured text, supporting biographical, historical, and cultural content.
"""

from .extractor import InformationExtractor
from .models import (
    ExtractedEntity,
    ExtractedRelationship,
    ExtractionResult,
    PersonExtraction,
    EventExtraction,
    PlaceExtraction,
    ObjectExtraction,
    TimeExtraction,
)

__all__ = [
    "InformationExtractor",
    "ExtractedEntity",
    "ExtractedRelationship", 
    "ExtractionResult",
    "PersonExtraction",
    "EventExtraction",
    "PlaceExtraction",
    "ObjectExtraction",
    "TimeExtraction",
]
