#!/usr/bin/env python3
"""
Generate tasks-data.js from all JSON task files for GitHub Pages deployment
"""

import os
import json
import re
from pathlib import Path

def extract_servers(task_json, task_id):
    """Extract server names from task JSON"""
    servers = []
    
    # Check mcp_servers field
    if 'mcp_servers' in task_json:
        mcp_servers = task_json['mcp_servers']
        if isinstance(mcp_servers, list):
            for server in mcp_servers:
                if isinstance(server, str):
                    servers.append(server)
                elif isinstance(server, dict) and 'name' in server:
                    servers.append(server['name'])
        elif isinstance(mcp_servers, str):
            servers.append(mcp_servers)
        elif isinstance(mcp_servers, dict) and 'name' in mcp_servers:
            servers.append(mcp_servers['name'])
    
    # Infer from category
    category = task_json.get('category', '').lower()
    if 'blender' in category and 'blender' not in servers:
        servers.append('blender')
    elif 'github' in category and 'github' not in servers:
        servers.append('github')
    elif 'yfinance' in category and 'yfinance' not in servers:
        servers.append('yfinance')
    
    # Infer from task ID
    if 'google_maps' in task_id and 'google-maps' not in servers:
        servers.append('google-maps')
    elif 'playwright' in task_id and 'playwright' not in servers:
        servers.append('playwright')
    elif 'info_search' in task_id and 'web-search' not in servers:
        servers.append('web-search')
    elif 'blender' in task_id and 'blender' not in servers:
        servers.append('blender')
    elif 'github' in task_id and 'github' not in servers:
        servers.append('github')
    elif 'yfinance' in task_id and 'yfinance' not in servers:
        servers.append('yfinance')
    
    # Fallback: if no servers found, infer from task_id
    if not servers:
        if 'google_maps' in task_id:
            servers.append('google-maps')
        elif 'playwright' in task_id:
            servers.append('playwright')
        elif 'info_search' in task_id:
            servers.append('web-search')
        elif 'blender' in task_id:
            servers.append('blender')
        elif 'github' in task_id:
            servers.append('github')
        elif 'yfinance' in task_id:
            servers.append('yfinance')
        else:
            servers.append('unknown')
    
    return list(set(servers))  # Remove duplicates

def main():
    # Domain mappings
    domain_mapping = {
        'location_navigation': 'location-navigation',
        'web_search': 'web-search',
        'browser_automation': 'browser-automation',
        'financial_analysis': 'financial-analysis',
        'repository_management': 'repository-management',
        '3d_design': '3d-design'
    }
    
    tasks_data = {
        'location-navigation': [],
        'web-search': [],
        'browser-automation': [],
        'financial-analysis': [],
        'repository-management': [],
        '3d-design': []
    }
    
    total_tasks = 0
    
    # Process each domain directory
    for domain_dir, domain_key in domain_mapping.items():
        domain_path = Path(f'tasks/{domain_dir}')
        if not domain_path.exists():
            print(f"Warning: {domain_path} does not exist")
            continue
            
        print(f"Processing {domain_dir}...")
        domain_count = 0
        
        # Find all JSON files in this domain
        json_files = list(domain_path.glob('*.json'))
        json_files.sort()  # Sort for consistent ordering
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    task_json = json.load(f)
                
                # Create task object
                task_id = json_file.stem  # filename without extension
                
                task = {
                    'id': task_id,
                    'category': task_json.get('category', 'general'),
                    'question': task_json.get('question', 'No description available'),
                    'servers': extract_servers(task_json, task_id),
                    'evaluators': len(task_json.get('evaluators', [])),
                    'fullData': task_json
                }
                
                tasks_data[domain_key].append(task)
                domain_count += 1
                total_tasks += 1
                
            except Exception as e:
                print(f"Error processing {json_file}: {e}")
        
        print(f"  Loaded {domain_count} tasks for {domain_key}")
    
    print(f"Total tasks loaded: {total_tasks}")
    
    # Generate JavaScript file
    js_content = """// Task data for GitHub Pages deployment
// This file contains all task information to avoid CORS issues with JSON files
// Auto-generated from JSON files

window.TASKS_DATA = """
    
    js_content += json.dumps(tasks_data, indent=2, ensure_ascii=False)
    js_content += ";\n\n"
    js_content += f"// Total task count\nwindow.TOTAL_TASKS = {total_tasks};\n"
    
    # Write to file
    with open('tasks-data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"Generated tasks-data.js with {total_tasks} tasks")
    
    # Print summary
    print("\nSummary by domain:")
    for domain_key, tasks in tasks_data.items():
        print(f"  {domain_key}: {len(tasks)} tasks")

if __name__ == '__main__':
    main()
