#!/usr/bin/env python3
"""
Schema Generator Tool for Narrative Gravity Analysis

Generates JSON Schema skeletons from example records and refines them with
descriptions and required field flags. This tool helps create new framework
extension schemas and update existing schemas.
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, List, Set, Union
from datetime import datetime
import jsonschema
import re

class SchemaGenerator:
    """Generate and refine JSON schemas from example data"""
    
    def __init__(self):
        self.basic_types = {
            'string': str,
            'integer': int,
            'number': (int, float),
            'boolean': bool,
            'array': list,
            'object': dict,
            'null': type(None)
        }
    
    def infer_type(self, value: Any) -> str:
        """Infer JSON Schema type from Python value"""
        if value is None:
            return 'null'
        elif isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, int):
            return 'integer'
        elif isinstance(value, float):
            return 'number'
        elif isinstance(value, str):
            return 'string'
        elif isinstance(value, list):
            return 'array'
        elif isinstance(value, dict):
            return 'object'
        else:
            return 'string'  # Default fallback
    
    def detect_format(self, value: str) -> str:
        """Detect common string formats"""
        if not isinstance(value, str):
            return None
            
        # Date/time patterns
        if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', value):
            return 'date-time'
        elif re.match(r'^\d{4}-\d{2}-\d{2}$', value):
            return 'date'
        elif re.match(r'^\d{2}:\d{2}:\d{2}$', value):
            return 'time'
        
        # URI pattern
        if re.match(r'^https?://', value):
            return 'uri'
        
        # Email pattern
        if re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
            return 'email'
        
        return None
    
    def detect_enum_values(self, values: List[Any]) -> List[Any]:
        """Detect if values should be an enum (limited set of values)"""
        unique_values = list(set(values))
        
        # If we have 5 or fewer unique values from 3+ examples, suggest enum
        if len(values) >= 3 and len(unique_values) <= 5:
            return unique_values
        
        return None
    
    def generate_property_schema(self, key: str, values: List[Any]) -> Dict[str, Any]:
        """Generate schema for a single property from example values"""
        non_null_values = [v for v in values if v is not None]
        has_nulls = len(non_null_values) != len(values)
        
        if not non_null_values:
            return {"type": "null", "description": f"Property {key}"}
        
        # Determine primary type
        types = [self.infer_type(v) for v in non_null_values]
        primary_type = max(set(types), key=types.count)
        
        property_schema = {
            "description": f"Property {key} (auto-generated)"
        }
        
        # Handle type specification
        if has_nulls:
            property_schema["type"] = [primary_type, "null"]
        else:
            property_schema["type"] = primary_type
        
        # Add format for strings
        if primary_type == 'string' and non_null_values:
            format_type = self.detect_format(non_null_values[0])
            if format_type:
                property_schema["format"] = format_type
        
        # Check for enum values
        if primary_type in ['string', 'integer', 'number']:
            enum_values = self.detect_enum_values(non_null_values)
            if enum_values:
                property_schema["enum"] = enum_values
                if has_nulls:
                    property_schema["enum"].append(None)
        
        # Add constraints based on type
        if primary_type == 'string' and non_null_values:
            min_len = min(len(str(v)) for v in non_null_values)
            max_len = max(len(str(v)) for v in non_null_values)
            if min_len > 0:
                property_schema["minLength"] = min_len
            if max_len < 1000:  # Only add maxLength for reasonable sizes
                property_schema["maxLength"] = max_len
        
        elif primary_type in ['integer', 'number'] and non_null_values:
            min_val = min(non_null_values)
            max_val = max(non_null_values)
            if min_val >= 0:
                property_schema["minimum"] = min_val
            if max_val <= 1000000:  # Only add maximum for reasonable sizes
                property_schema["maximum"] = max_val
        
        elif primary_type == 'array' and non_null_values:
            # Analyze array items
            all_items = []
            for arr in non_null_values:
                if isinstance(arr, list):
                    all_items.extend(arr)
            
            if all_items:
                item_schema = self.generate_property_schema(f"{key}_item", all_items)
                property_schema["items"] = item_schema
        
        elif primary_type == 'object' and non_null_values:
            # Recursively analyze object properties
            all_keys = set()
            for obj in non_null_values:
                if isinstance(obj, dict):
                    all_keys.update(obj.keys())
            
            if all_keys:
                properties = {}
                for obj_key in all_keys:
                    obj_values = []
                    for obj in non_null_values:
                        if isinstance(obj, dict) and obj_key in obj:
                            obj_values.append(obj[obj_key])
                    
                    if obj_values:
                        properties[obj_key] = self.generate_property_schema(obj_key, obj_values)
                
                property_schema["type"] = "object"
                property_schema["properties"] = properties
                property_schema["additionalProperties"] = True
        
        return property_schema
    
    def analyze_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze a list of records to generate a schema"""
        if not records:
            raise ValueError("No records provided for analysis")
        
        # Collect all keys and their values
        all_keys = set()
        for record in records:
            if isinstance(record, dict):
                all_keys.update(record.keys())
        
        properties = {}
        required_fields = []
        
        for key in all_keys:
            values = []
            present_count = 0
            
            for record in records:
                if isinstance(record, dict):
                    if key in record:
                        values.append(record[key])
                        present_count += 1
                    else:
                        values.append(None)
            
            # Field is required if present in 80% or more of records
            if present_count / len(records) >= 0.8:
                required_fields.append(key)
            
            properties[key] = self.generate_property_schema(key, values)
        
        # Generate the complete schema
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://narrative-gravity.github.io/schemas/generated_schema.json",
            "title": "Generated Schema",
            "description": "Auto-generated schema from example records",
            "version": "1.0.0",
            "type": "object",
            "properties": properties,
            "required": sorted(required_fields),
            "additionalProperties": False
        }
        
        return schema
    
    def refine_schema_with_metadata(self, schema: Dict[str, Any], 
                                  title: str = None,
                                  description: str = None,
                                  schema_id: str = None,
                                  version: str = None) -> Dict[str, Any]:
        """Refine a generated schema with human-provided metadata"""
        if title:
            schema["title"] = title
        if description:
            schema["description"] = description
        if schema_id:
            schema["$id"] = schema_id
        if version:
            schema["version"] = version
        
        return schema
    
    def validate_against_schema(self, records: List[Dict[str, Any]], 
                              schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Validate records against a schema and return validation errors"""
        errors = []
        
        for i, record in enumerate(records):
            try:
                jsonschema.validate(record, schema)
            except jsonschema.ValidationError as e:
                errors.append({
                    "record_index": i,
                    "error": str(e),
                    "path": list(e.absolute_path),
                    "failed_value": e.instance
                })
        
        return errors
    
    def generate_schema_from_jsonl(self, jsonl_path: Path) -> Dict[str, Any]:
        """Generate schema from a JSONL file"""
        records = []
        
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    try:
                        record = json.loads(line)
                        records.append(record)
                    except json.JSONDecodeError as e:
                        print(f"Warning: Invalid JSON on line {line_num}: {e}")
        
        if not records:
            raise ValueError(f"No valid JSON records found in {jsonl_path}")
        
        return self.analyze_records(records)
    
    def save_schema(self, schema: Dict[str, Any], output_path: Path):
        """Save schema to a JSON file with pretty formatting"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)
        
        print(f"Schema saved to: {output_path}")


def main():
    """CLI interface for the schema generator"""
    parser = argparse.ArgumentParser(
        description="Generate JSON Schema skeletons from example records",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate schema from JSONL file
  python schema_generator.py --input sample.jsonl --output schema.json

  # Generate schema with custom metadata
  python schema_generator.py --input sample.jsonl --output schema.json \\
    --title "My Schema" --description "Schema for my data" --version "1.0.0"

  # Validate records against existing schema
  python schema_generator.py --input data.jsonl --validate-against existing_schema.json
        """
    )
    
    parser.add_argument('--input', '-i', required=True, type=Path,
                       help='Input JSONL file with example records')
    parser.add_argument('--output', '-o', type=Path,
                       help='Output JSON schema file')
    parser.add_argument('--title', help='Schema title')
    parser.add_argument('--description', help='Schema description')
    parser.add_argument('--schema-id', help='Schema $id URL')
    parser.add_argument('--version', default='1.0.0', help='Schema version')
    parser.add_argument('--validate-against', type=Path,
                       help='Validate input records against existing schema')
    parser.add_argument('--show-errors', action='store_true',
                       help='Show detailed validation errors')
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: Input file {args.input} does not exist")
        sys.exit(1)
    
    generator = SchemaGenerator()
    
    try:
        if args.validate_against:
            # Validation mode
            if not args.validate_against.exists():
                print(f"Error: Schema file {args.validate_against} does not exist")
                sys.exit(1)
            
            with open(args.validate_against, 'r') as f:
                schema = json.load(f)
            
            # Load records
            records = []
            with open(args.input, 'r') as f:
                for line in f:
                    if line.strip():
                        records.append(json.loads(line))
            
            errors = generator.validate_against_schema(records, schema)
            
            if not errors:
                print(f"✅ All {len(records)} records are valid against the schema")
            else:
                print(f"❌ Found {len(errors)} validation errors in {len(records)} records")
                if args.show_errors:
                    for error in errors:
                        print(f"  Record {error['record_index']}: {error['error']}")
        
        else:
            # Schema generation mode
            schema = generator.generate_schema_from_jsonl(args.input)
            
            # Refine with metadata
            schema = generator.refine_schema_with_metadata(
                schema,
                title=args.title,
                description=args.description,
                schema_id=args.schema_id,
                version=args.version
            )
            
            if args.output:
                generator.save_schema(schema, args.output)
                print(f"Generated schema with {len(schema['properties'])} properties")
                print(f"Required fields: {', '.join(schema['required'])}")
            else:
                print(json.dumps(schema, indent=2))
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 