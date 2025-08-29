#!/usr/bin/env python3
"""
Simple Postman Collection Validator
Works without Node.js/Newman - validates JSON and provides basic checks
"""

import json
import os
from pathlib import Path

def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent.parent

def validate_json_file(file_path, file_type):
    """Validate that a file contains valid JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ {file_type} is valid JSON: {file_path.name}")
        return True, data
    except FileNotFoundError:
        print(f"✗ {file_type} not found: {file_path}")
        return False, None
    except json.JSONDecodeError as e:
        print(f"✗ {file_type} contains invalid JSON: {e}")
        return False, None
    except Exception as e:
        print(f"✗ Error reading {file_type}: {e}")
        return False, None

def validate_collection(collection_data):
    """Validate Postman collection structure"""
    if not collection_data:
        return False
    
    checks_passed = 0
    total_checks = 5
    
    # Check basic structure
    if 'info' in collection_data:
        print("✓ Collection has info section")
        checks_passed += 1
        
        if 'name' in collection_data['info']:
            print(f"✓ Collection name: {collection_data['info']['name']}")
        if 'version' in collection_data['info']:
            print(f"✓ Collection version: {collection_data['info']['version']}")
    else:
        print("✗ Collection missing info section")
    
    # Check for items (requests)
    if 'item' in collection_data:
        items = collection_data['item']
        if isinstance(items, list) and len(items) > 0:
            print(f"✓ Collection has {len(items)} main folders/requests")
            checks_passed += 1
            
            # Count total requests
            total_requests = 0
            for item in items:
                if 'item' in item:  # This is a folder
                    total_requests += len(item['item'])
                else:  # This is a direct request
                    total_requests += 1
            print(f"✓ Total requests in collection: {total_requests}")
            checks_passed += 1
        else:
            print("✗ Collection has no items/requests")
    else:
        print("✗ Collection missing item section")
    
    # Check for variables
    if 'variable' in collection_data:
        print(f"✓ Collection has {len(collection_data['variable'])} variables")
        checks_passed += 1
    else:
        print("⚠️ Collection has no variables defined")
    
    # Check for events (tests/scripts)
    if 'event' in collection_data:
        print(f"✓ Collection has {len(collection_data['event'])} global events")
        checks_passed += 1
    else:
        print("⚠️ Collection has no global events/scripts")
    
    success_rate = (checks_passed / total_checks) * 100
    print(f"Collection validation: {checks_passed}/{total_checks} checks passed ({success_rate:.0f}%)")
    
    return checks_passed >= 3  # Pass if at least 3 out of 5 checks pass

def validate_environment(env_data, env_name):
    """Validate Postman environment structure"""
    if not env_data:
        return False
    
    checks_passed = 0
    total_checks = 3
    
    if 'name' in env_data:
        print(f"✓ Environment name: {env_data['name']}")
        checks_passed += 1
    else:
        print(f"✗ {env_name} missing name")
    
    if 'values' in env_data and isinstance(env_data['values'], list):
        variables = env_data['values']
        print(f"✓ {env_name} has {len(variables)} variables")
        checks_passed += 1
        
        # Check for BASE_URL
        base_url_found = False
        for var in variables:
            if var.get('key') == 'BASE_URL':
                base_url_found = True
                print(f"✓ BASE_URL configured: {var.get('value')}")
                break
        
        if base_url_found:
            checks_passed += 1
        else:
            print("✗ BASE_URL variable not found")
    else:
        print(f"✗ {env_name} missing variables")
    
    return checks_passed >= 2

def main():
    print("🔍 Validating Postman Integration (No Node.js required)")
    print("=" * 55)
    
    project_root = get_project_root()
    postman_dir = project_root / 'postman'
    
    if not postman_dir.exists():
        print(f"✗ Postman directory not found: {postman_dir}")
        return False
    
    print(f"📁 Checking directory: {postman_dir}")
    
    # Validate collection
    collection_path = postman_dir / 'Sustainability_Actions_API.postman_collection.json'
    collection_valid, collection_data = validate_json_file(collection_path, "Collection")
    
    if collection_valid:
        collection_structure_valid = validate_collection(collection_data)
    else:
        collection_structure_valid = False
    
    # Validate environments
    dev_env_path = postman_dir / 'Development.postman_environment.json'
    dev_valid, dev_data = validate_json_file(dev_env_path, "Development Environment")
    
    if dev_valid:
        dev_structure_valid = validate_environment(dev_data, "Development")
    else:
        dev_structure_valid = False
    
    prod_env_path = postman_dir / 'Production.postman_environment.json'
    prod_valid, prod_data = validate_json_file(prod_env_path, "Production Environment")
    
    if prod_valid:
        prod_structure_valid = validate_environment(prod_data, "Production")
    else:
        prod_structure_valid = False
    
    print("\n" + "=" * 55)
    
    all_valid = collection_structure_valid and dev_structure_valid and prod_structure_valid
    
    if all_valid:
        print("✅ All Postman files are valid and ready to use!")
        print("\n📋 Manual Import Instructions:")
        print("1. Open Postman application")
        print("2. Click Import → File → Select collection file")
        print(f"   📄 {collection_path}")
        print("3. Click Import → File → Select environment file")
        print(f"   🌍 {dev_env_path}")
        print("4. Select 'Development Environment' from dropdown")
        print("5. Start Django server: python manage.py runserver")
        print("6. Test the endpoints!")
    else:
        print("⚠️ Some validation issues found, but files may still work")
        print("💡 Check the errors above and fix any JSON syntax issues")
    
    return all_valid

if __name__ == '__main__':
    main()