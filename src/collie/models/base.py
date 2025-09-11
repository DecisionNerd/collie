"""
Base CRM entity model and core wrappers.
Provides the foundation for all CIDOC CRM E-class models.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class CRMEntity(BaseModel):
    """
    Base class for all CIDOC CRM entities.
    
    Every CRM entity has:
    - id: unique identifier
    - class_code: E-number (e.g., "E22")
    - label: human-readable name
    - notes: additional textual information
    - type: list of type assignments
    """
    
    id: str = Field(..., description="Unique identifier for this entity")
    class_code: str = Field(..., description="CIDOC CRM E-class code")
    label: Optional[str] = Field(None, description="Human-readable label")
    notes: Optional[str] = Field(None, description="Additional textual notes")
    type: List[str] = Field(default_factory=list, description="Type assignments")
    
    class Config:
        json_schema_extra = {
            "description": "Base CIDOC CRM entity",
            "examples": [
                {
                    "id": "obj_001",
                    "class_code": "E22",
                    "label": "Ancient Vase",
                    "type": ["E55:Vessel", "E55:Ceramic"]
                }
            ]
        }


class CRMRelation(BaseModel):
    """
    Represents a relationship between two CRM entities.
    
    Used internally for relationship expansion and Cypher emission.
    """
    
    src: str = Field(..., description="Source entity ID")
    type: str = Field(..., description="P-property code (e.g., 'P108')")
    tgt: str = Field(..., description="Target entity ID")
    props: Optional[Dict[str, Any]] = Field(None, description="Additional relationship properties")
    
    class Config:
        json_schema_extra = {
            "description": "CRM relationship between entities",
            "examples": [
                {
                    "src": "obj_001",
                    "type": "P108",
                    "tgt": "prod_001",
                    "props": {"role": "E55:Painter"}
                }
            ]
        }


class CRMValidationError(Exception):
    """Raised when CRM validation rules are violated."""
    pass


class CRMValidationWarning(Warning):
    """Issued when CRM validation rules are violated but severity is set to warn."""
    pass


# Core wrapper classes for high-use E-classes
# These provide ergonomic shortcuts and additional methods

class E5_Event(CRMEntity):
    """Event - something that happened."""
    class_code: str = "E5"
    
    # Shortcut fields
    timespan: Optional[str] = Field(None, description="Time-span entity ID")
    took_place_at: Optional[str] = Field(None, description="Place entity ID")
    
    class Config:
        json_schema_extra = {
            "description": "CIDOC CRM E5: Event",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"]
        }


class E7_Activity(E5_Event):
    """Activity - an event that involves action."""
    class_code: str = "E7"
    
    class Config:
        json_schema_extra = {
            "description": "CIDOC CRM E7: Activity",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"]
        }


class E12_Production(E7_Activity):
    """Production - the creation of a human-made object."""
    class_code: str = "E12"
    
    class Config:
        json_schema_extra = {
            "description": "CIDOC CRM E12: Production",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"]
        }


class E8_Acquisition(E7_Activity):
    """Acquisition - the act of acquiring something."""
    class_code: str = "E8"
    
    class Config:
        json_schema_extra = {
            "description": "CIDOC CRM E8: Acquisition",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"]
        }


class E22_HumanMadeObject(CRMEntity):
    """Human-Made Object - a physical object created by humans."""
    class_code: str = "E22"
    
    # Shortcut fields
    current_location: Optional[str] = Field(None, description="Current location entity ID")
    produced_by: Optional[str] = Field(None, description="Production event entity ID")
    
    class Config:
        json_schema_extra = {
            "description": "CIDOC CRM E22: Human-Made Object",
            "canonical_fields": ["label", "type", "notes", "current_location", "produced_by"]
        }


class E21_Person(CRMEntity):
    """Person - a human individual."""
    class_code: str = "E21"
    
    # Shortcut fields
    current_location: Optional[str] = Field(None, description="Current location entity ID")
    
    class Config:
        json_schema_extra = {
            "description": "CIDOC CRM E21: Person",
            "canonical_fields": ["label", "type", "notes", "current_location"]
        }


class E74_Group(CRMEntity):
    """Group - a collection of actors."""
    class_code: str = "E74"
    
    class Config:
        json_schema_extra = {
            "description": "CIDOC CRM E74: Group",
            "canonical_fields": ["label", "type", "notes"]
        }


class E53_Place(CRMEntity):
    """Place - a spatial location."""
    class_code: str = "E53"
    
    class Config:
        json_schema_extra = {
            "description": "CIDOC CRM E53: Place",
            "canonical_fields": ["label", "type", "notes"]
        }


class E52_TimeSpan(CRMEntity):
    """Time-Span - a temporal extent."""
    class_code: str = "E52"
    
    # Shortcut fields
    begin_of_the_begin: Optional[str] = Field(None, description="Beginning time primitive ID")
    end_of_the_end: Optional[str] = Field(None, description="End time primitive ID")
    
    class Config:
        json_schema_extra = {
            "description": "CIDOC CRM E52: Time-Span",
            "canonical_fields": ["label", "type", "notes", "begin_of_the_begin", "end_of_the_end"]
        }


class E42_Identifier(CRMEntity):
    """Identifier - a unique identifier."""
    class_code: str = "E42"
    
    class Config:
        json_schema_extra = {
            "description": "CIDOC CRM E42: Identifier",
            "canonical_fields": ["label", "type", "notes"]
        }


class E35_Title(CRMEntity):
    """Title - a name or title."""
    class_code: str = "E35"
    
    class Config:
        json_schema_extra = {
            "description": "CIDOC CRM E35: Title",
            "canonical_fields": ["label", "type", "notes"]
        }
