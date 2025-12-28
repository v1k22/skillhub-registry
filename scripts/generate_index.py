#!/usr/bin/env python3
"""
Generate index.json from all skills in the registry.
Run this after adding/updating skills.
"""
import os
import json
import yaml
from pathlib import Path
from datetime import datetime

def extract_metadata(skill_path):
    """Extract metadata from skill markdown file."""
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML frontmatter
        if not content.startswith('---'):
            print(f"⚠️  Warning: {skill_path} missing YAML frontmatter")
            return None

        parts = content.split('---', 2)
        if len(parts) < 3:
            print(f"⚠️  Warning: {skill_path} invalid YAML frontmatter structure")
            return None

        frontmatter = parts[1]
        data = yaml.safe_load(frontmatter)

        if not data or 'metadata' not in data:
            print(f"⚠️  Warning: {skill_path} missing metadata section")
            return None

        return data.get('metadata', {})

    except Exception as e:
        print(f"❌ Error processing {skill_path}: {e}")
        return None

def generate_index(base_url='https://raw.githubusercontent.com/v1k22/skillhub-registry/main'):
    """Generate search index from all skills."""
    skills_dir = Path('skills')

    if not skills_dir.exists():
        print(f"❌ Error: skills directory not found at {skills_dir}")
        return False

    index = {
        'version': '1.0.0',
        'generated': datetime.now().isoformat(),
        'skills': []
    }

    skill_count = 0
    error_count = 0

    print("=" * 60)
    print("Generating skill index...")
    print("=" * 60)

    # Find all .md files in skills directory
    for skill_file in sorted(skills_dir.rglob('*.md')):
        print(f"\nProcessing: {skill_file}")

        metadata = extract_metadata(skill_file)

        if metadata:
            # Get category from directory structure
            category = skill_file.parent.name

            # Build skill entry
            skill_entry = {
                'name': metadata.get('name', ''),
                'version': metadata.get('version', '1.0.0'),
                'description': metadata.get('description', ''),
                'category': metadata.get('category', category),
                'tags': metadata.get('tags', []),
                'author': metadata.get('author', 'unknown'),
                'created': metadata.get('created', ''),
                'updated': metadata.get('updated', ''),
                'difficulty': metadata.get('difficulty', ''),
                'estimated_time': metadata.get('estimated_time', ''),
                'path': str(skill_file),
                'url': f'{base_url}/{skill_file}'
            }

            # Validate required fields
            if not skill_entry['name']:
                print(f"  ⚠️  Warning: Missing 'name' field")
                error_count += 1
            elif not skill_entry['description']:
                print(f"  ⚠️  Warning: Missing 'description' field")
                error_count += 1
            else:
                index['skills'].append(skill_entry)
                skill_count += 1
                print(f"  ✅ Added: {skill_entry['name']}")
        else:
            error_count += 1

    # Write index
    index_file = Path('index.json')
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "=" * 60)
    print("INDEX GENERATION SUMMARY")
    print("=" * 60)
    print(f"✅ Skills indexed: {skill_count}")
    print(f"⚠️  Errors/Warnings: {error_count}")
    print(f"📄 Output file: {index_file}")
    print(f"📅 Generated: {index['generated']}")
    print("=" * 60)

    # Print skills by category
    skills_by_category = {}
    for skill in index['skills']:
        cat = skill['category']
        if cat not in skills_by_category:
            skills_by_category[cat] = []
        skills_by_category[cat].append(skill['name'])

    print("\nSkills by Category:")
    for category, skills in sorted(skills_by_category.items()):
        print(f"\n  {category.upper()} ({len(skills)})")
        for skill_name in sorted(skills):
            print(f"    - {skill_name}")

    return skill_count > 0

if __name__ == '__main__':
    success = generate_index()

    if success:
        print("\n✅ Index generated successfully!")
        exit(0)
    else:
        print("\n❌ Index generation failed!")
        exit(1)
