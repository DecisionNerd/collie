#!/usr/bin/env python3
"""
Code generator for CIDOC CRM Pydantic models from YAML specifications.
Generates e_classes.py with all E-class models.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any


def load_yaml_specs(specs_dir: Path) -> Dict[str, Any]:
    """Load YAML specifications from the specs directory."""
    classes_file = specs_dir / "crm_classes.yaml"
    properties_file = specs_dir / "crm_properties.yaml"
    aliases_file = specs_dir / "aliases.yaml"
    
    with open(classes_file, 'r') as f:
        classes = yaml.safe_load(f)
    
    with open(properties_file, 'r') as f:
        properties = yaml.safe_load(f)
    
    with open(aliases_file, 'r') as f:
        aliases = yaml.safe_load(f)
    
    return {
        "classes": classes,
        "properties": properties,
        "aliases": aliases
    }


def generate_class_model(class_spec: Dict[str, Any]) -> str:
    """Generate Pydantic model code for a single E-class."""
    code = class_spec["code"]
    label = class_spec["label"]
    abstract = class_spec.get("abstract", False)
    parents = class_spec.get("parents", [])
    canonical_fields = class_spec.get("canonical_fields", [])
    shortcuts = class_spec.get("shortcuts", [])
    
    # Convert label to Python class name
    class_name = f"E{code}_{label.replace(' ', '').replace('-', '')}"
    
    # Determine parent class
    if parents:
        parent_class = f"E{parents[0]}_{label.replace(' ', '').replace('-', '')}"
    else:
        parent_class = "CRMEntity"
    
    # Generate shortcut fields
    shortcut_fields = []
    for shortcut in shortcuts:
        prop_code = shortcut["property"]
        alias_field = shortcut["alias_field"]
        shortcut_fields.append(f'    {alias_field}: Optional[str] = None')
    
    shortcut_fields_str = "\n".join(shortcut_fields) if shortcut_fields else "    pass"
    
    # Generate docstring
    docstring = f'    """CIDOC CRM {code}: {label}'
    if abstract:
        docstring += " (Abstract)"
    docstring += '"""'
    
    model_code = f'''class {class_name}({parent_class}):
{docstring}
    class_code: str = "{code}"
    
{shortcut_fields_str}
    
    class Config:
        json_schema_extra = {{
            "description": "{label}",
            "canonical_fields": {canonical_fields}
        }}
'''
    
    return model_code


def generate_models_file(specs: Dict[str, Any], output_path: Path) -> None:
    """Generate the complete e_classes.py file."""
    classes = specs["classes"]
    
    # Generate imports and base class
    header = '''"""
Auto-generated CIDOC CRM E-class models.
Generated from YAML specifications in codegen/specs/
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from ..models.base import CRMEntity


'''
    
    # Generate all class models
    class_models = []
    for class_spec in classes:
        model_code = generate_class_model(class_spec)
        class_models.append(model_code)
    
    # Combine header and models
    full_content = header + "\n\n".join(class_models)
    
    # Write to file
    with open(output_path, 'w') as f:
        f.write(full_content)


def main():
    """Main code generation function."""
    # Get paths
    current_dir = Path(__file__).parent
    specs_dir = current_dir / "specs"
    output_path = current_dir.parent / "models" / "generated" / "e_classes.py"
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load specifications
    specs = load_yaml_specs(specs_dir)
    
    # Generate models
    generate_models_file(specs, output_path)
    
    print(f"Generated {output_path}")
    print(f"Created {len(specs['classes'])} E-class models")


if __name__ == "__main__":
    main()
