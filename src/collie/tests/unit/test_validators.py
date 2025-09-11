"""
Unit tests for CRM validators.
"""

import pytest
from ..models.base import CRMEntity, E22_HumanMadeObject, E12_Production
from ..validators.quantifiers import (
    enforce_quantifier, 
    validate_entity_quantifiers,
    ValidationSeverity
)
from ..validators.typing_rules import (
    validate_domain_range_alignment,
    validate_batch_typing
)


class TestQuantifierValidation:
    """Test quantifier validation functionality."""
    
    def test_enforce_quantifier_valid(self):
        """Test quantifier enforcement with valid values."""
        entity = E22_HumanMadeObject(id="obj_001", class_code="E22")
        
        # P108 has quantifier "0..1" - should allow 0 or 1 values
        enforce_quantifier(entity, "P108", [], ValidationSeverity.WARN)
        enforce_quantifier(entity, "P108", ["prod_001"], ValidationSeverity.WARN)
    
    def test_enforce_quantifier_too_many(self):
        """Test quantifier enforcement with too many values."""
        entity = E22_HumanMadeObject(id="obj_001", class_code="E22")
        
        # P108 has quantifier "0..1" - should not allow 2 values
        with pytest.raises(Exception):  # Should raise CRMValidationError
            enforce_quantifier(entity, "P108", ["prod_001", "prod_002"], ValidationSeverity.RAISE)
    
    def test_enforce_quantifier_too_few(self):
        """Test quantifier enforcement with too few values."""
        entity = E12_Production(id="prod_001", class_code="E12")
        
        # P108i has quantifier "0..*" - should allow 0 values
        enforce_quantifier(entity, "P108i", [], ValidationSeverity.WARN)
    
    def test_validate_entity_quantifiers(self):
        """Test entity quantifier validation."""
        entity = E22_HumanMadeObject(
            id="obj_001",
            class_code="E22",
            produced_by="prod_001"  # This should be valid
        )
        
        messages = validate_entity_quantifiers(entity, ValidationSeverity.WARN)
        # Should not have validation errors for a valid entity
        assert len(messages) == 0


class TestTypingValidation:
    """Test typing validation functionality."""
    
    def test_validate_domain_range_alignment_valid(self):
        """Test domain/range alignment with valid entities."""
        source = E22_HumanMadeObject(id="obj_001", class_code="E22")
        target = E12_Production(id="prod_001", class_code="E12")
        
        # P108: E22 -> E12 should be valid
        validate_domain_range_alignment(source, target, "P108", ValidationSeverity.WARN)
    
    def test_validate_domain_range_alignment_invalid(self):
        """Test domain/range alignment with invalid entities."""
        source = E22_HumanMadeObject(id="obj_001", class_code="E22")
        target = E22_HumanMadeObject(id="obj_002", class_code="E22")
        
        # P108: E22 -> E12 should be invalid with E22 target
        with pytest.raises(Exception):  # Should raise CRMValidationError
            validate_domain_range_alignment(source, target, "P108", ValidationSeverity.RAISE)
    
    def test_validate_batch_typing(self):
        """Test batch typing validation."""
        entities = [
            E22_HumanMadeObject(id="obj_001", class_code="E22"),
            E12_Production(id="prod_001", class_code="E12")
        ]
        
        results = validate_batch_typing(entities, ValidationSeverity.WARN)
        # Should not have validation errors for valid entities
        assert len(results) == 0


class TestValidationSeverity:
    """Test validation severity handling."""
    
    def test_warn_severity(self):
        """Test that WARN severity issues warnings but doesn't raise."""
        entity = E22_HumanMadeObject(id="obj_001", class_code="E22")
        
        # This should issue a warning but not raise an exception
        enforce_quantifier(entity, "P108", ["prod_001", "prod_002"], ValidationSeverity.WARN)
    
    def test_raise_severity(self):
        """Test that RAISE severity raises exceptions."""
        entity = E22_HumanMadeObject(id="obj_001", class_code="E22")
        
        # This should raise an exception
        with pytest.raises(Exception):
            enforce_quantifier(entity, "P108", ["prod_001", "prod_002"], ValidationSeverity.RAISE)
    
    def test_ignore_severity(self):
        """Test that IGNORE severity doesn't validate."""
        entity = E22_HumanMadeObject(id="obj_001", class_code="E22")
        
        # This should not raise an exception or issue warnings
        enforce_quantifier(entity, "P108", ["prod_001", "prod_002"], ValidationSeverity.IGNORE)
