"""
Pydantic models for structured LLM output in CIDOC CRM extraction.

These models define the exact structure that the LLM should return,
ensuring compliance with CIDOC CRM standards.
"""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, validator
import uuid


class CIDOCPerson(BaseModel):
    """CIDOC CRM E21 Person entity."""
    label: str = Field(..., description="Full name of the person")
    description: str = Field(..., description="Biographical description")
    birth_date: Optional[str] = Field(None, description="Birth date (YYYY-MM-DD format)")
    death_date: Optional[str] = Field(None, description="Death date (YYYY-MM-DD format)")
    birth_place: Optional[str] = Field(None, description="Birth place name")
    death_place: Optional[str] = Field(None, description="Death place name")
    nationality: Optional[str] = Field(None, description="Nationality or citizenship")
    occupation: Optional[str] = Field(None, description="Primary occupation or profession")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    source_text: str = Field(..., description="Relevant text snippet")
    
    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v


class CIDOCEvent(BaseModel):
    """CIDOC CRM E5 Event entity."""
    label: str = Field(..., description="Event name or description")
    description: str = Field(..., description="Detailed event description")
    event_type: Literal["Birth", "Death", "Marriage", "Graduation", "Invention", "Discovery", 
                       "Publication", "Award", "Employment", "Travel", "Other"] = Field(..., description="Type of event")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD format)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD format)")
    location: Optional[str] = Field(None, description="Event location")
    participants: List[str] = Field(default_factory=list, description="List of participant names")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    source_text: str = Field(..., description="Relevant text snippet")
    
    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v


class CIDOCPlace(BaseModel):
    """CIDOC CRM E53 Place entity."""
    label: str = Field(..., description="Place name")
    description: str = Field(..., description="Place description")
    place_type: Literal["City", "Country", "Region", "Institution", "Building", "Geographic Feature", "Other"] = Field(..., description="Type of place")
    coordinates: Optional[str] = Field(None, description="Geographic coordinates if available")
    country: Optional[str] = Field(None, description="Country name")
    region: Optional[str] = Field(None, description="Region or state")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    source_text: str = Field(..., description="Relevant text snippet")
    
    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v


class CIDOCObject(BaseModel):
    """CIDOC CRM E22 Object entity."""
    label: str = Field(..., description="Object name or title")
    description: str = Field(..., description="Object description")
    object_type: Literal["Theory", "Formula", "Award", "Institution", "Publication", "Artifact", "Concept", "Other"] = Field(..., description="Type of object")
    creator: Optional[str] = Field(None, description="Creator or inventor name")
    creation_date: Optional[str] = Field(None, description="Creation date (YYYY-MM-DD format)")
    location: Optional[str] = Field(None, description="Current or original location")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    source_text: str = Field(..., description="Relevant text snippet")
    
    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v


class CIDOCTime(BaseModel):
    """CIDOC CRM E52 Time-Span entity."""
    label: str = Field(..., description="Time period description")
    description: str = Field(..., description="Detailed time description")
    time_type: Literal["Date", "Year", "Decade", "Century", "Period", "Era", "Other"] = Field(..., description="Type of time reference")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD format)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD format)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    source_text: str = Field(..., description="Relevant text snippet")
    
    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v


class CIDOCRelationship(BaseModel):
    """CIDOC CRM Relationship entity."""
    source_label: str = Field(..., description="Source entity label")
    target_label: str = Field(..., description="Target entity label")
    property_code: str = Field(..., description="CIDOC CRM property code (P-code)")
    property_label: str = Field(..., description="Human-readable property label")
    description: str = Field(..., description="Relationship description")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    source_text: str = Field(..., description="Relevant text snippet")
    
    @validator('property_code')
    def validate_property_code(cls, v):
        if not v.startswith('P'):
            raise ValueError('Property code must start with P')
        return v
    
    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v


class CIDOCExtractionResult(BaseModel):
    """Complete structured extraction result from LLM."""
    persons: List[CIDOCPerson] = Field(default_factory=list, description="List of extracted persons (E21)")
    events: List[CIDOCEvent] = Field(default_factory=list, description="List of extracted events (E5)")
    places: List[CIDOCPlace] = Field(default_factory=list, description="List of extracted places (E53)")
    objects: List[CIDOCObject] = Field(default_factory=list, description="List of extracted objects (E22)")
    times: List[CIDOCTime] = Field(default_factory=list, description="List of extracted time periods (E52)")
    relationships: List[CIDOCRelationship] = Field(default_factory=list, description="List of extracted relationships")
    
    # Metadata
    extraction_confidence: float = Field(..., ge=0.0, le=1.0, description="Overall extraction confidence")
    total_entities: int = Field(..., description="Total number of entities extracted")
    total_relationships: int = Field(..., description="Total number of relationships extracted")
    
    @validator('extraction_confidence')
    def validate_confidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v


# CIDOC CRM Property Code Mappings
CIDOC_PROPERTIES = {
    # Person properties
    "P98": "was born in",
    "P100": "died in", 
    "P107": "has current or former member",
    "P131": "is identified by",
    "P132": "spatially overlaps with",
    
    # Event properties
    "P4": "has time-span",
    "P7": "took place at",
    "P11": "had participant",
    "P14": "carried out by",
    
    # Object properties
    "P108": "has produced",
    "P62": "depicts",
    "P65": "shows visual item",
    "P102": "has title",
    
    # Place properties
    "P89": "falls within",
    "P87": "is identified by",
    "P168": "place is defined by",
    
    # Time properties
    "P82": "at some time within",
    "P83": "before",
    "P84": "after",
    "P86": "falls within",
    
    # General relationship properties
    "P1": "is identified by",
    "P2": "has type",
    "P3": "has note",
    "P48": "has preferred identifier",
    "P138": "represents",
}
