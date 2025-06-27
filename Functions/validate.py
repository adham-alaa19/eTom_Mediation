from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

def validate(
    usage_record_data: Dict[str, Any],
    service_usage_spec_data: Optional[Dict[str, Any]]
) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    
    record_spec_id = usage_record_data.get("usage_specification_id")
    if not record_spec_id:
        errors.append("'usage_specification_id' is missing in the usage record.")
    
    if record_spec_id and not service_usage_spec_data:
        errors.append(f"ServiceUsageSpecification data for ID '{record_spec_id}' was not provided or not found.")
    
    elif service_usage_spec_data:
        spec_json = service_usage_spec_data.get("spec_json")
        if isinstance(spec_json, dict):
            required_base_fields = spec_json.get("requiredBaseFields")
            if isinstance(required_base_fields, list):
                for field_name in required_base_fields:
                    if usage_record_data.get(field_name) is None:
                        errors.append(f"Required base field '{field_name}' (defined in spec) is missing or null in the usage record.")
        elif record_spec_id:
             errors.append(f"'spec_json' is missing or not a dictionary in the provided ServiceUsageSpecification data for ID '{record_spec_id}'.")

    characteristics = usage_record_data.get("usage_characteristics")
    if characteristics is not None:
        if not isinstance(characteristics, list):
            errors.append("'usage_characteristics', if present, should be a list.")
        else:
            for i, char_dict in enumerate(characteristics):
                if not isinstance(char_dict, dict):
                    errors.append(f"Item at index {i} in 'usage_characteristics' is not a dictionary.")
                    continue
                if char_dict.get("name") is None:
                     errors.append(f"Characteristic at index {i} in 'usage_characteristics' is missing a 'name' or its name is null.")
    
    if errors:
        print("Validation errors:")
        for err in errors:
            print(f" - {err}")

    is_valid = not errors
    return is_valid, errors
