#!/usr/bin/env python3
"""
Validate skill file format and content.
Returns exit code 0 for valid, 1 for invalid.
"""
import sys
import yaml
from pathlib import Path
import re

# Required fields in metadata
REQUIRED_FIELDS = ['name', 'version', 'description', 'category', 'tags', 'author']

# Required sections in skill body
REQUIRED_SECTIONS = [
    '## Overview',
    '## Task Description',
    '## Steps',
    '## Expected Output',
    '## Success Criteria'
]

# Optional but recommended sections
RECOMMENDED_SECTIONS = [
    '## Prerequisites',
    '## Troubleshooting',
    '## Related Skills',
    '## References'
]

# Valid categories
VALID_CATEGORIES = [
    'benchmarking',
    'data-engineering',
    'web-development',
    'automation',
    'ml-ops',
    'devops',
    'testing',
    'database',
    'security'
]

# Valid difficulty levels
VALID_DIFFICULTIES = ['beginner', 'intermediate', 'advanced']

def validate_skill(skill_path):
    """Validate a single skill file."""
    errors = []
    warnings = []

    skill_path = Path(skill_path)

    # Check file exists
    if not skill_path.exists():
        errors.append(f"File not found: {skill_path}")
        return errors, warnings

    # Read file
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        errors.append(f"Failed to read file: {e}")
        return errors, warnings

    # Check frontmatter exists
    if not content.startswith('---'):
        errors.append("Missing YAML frontmatter (must start with '---')")
        return errors, warnings

    # Parse frontmatter
    try:
        parts = content.split('---', 2)
        if len(parts) < 3:
            errors.append("Invalid YAML frontmatter structure (must have closing '---')")
            return errors, warnings

        frontmatter = parts[1]
        body = parts[2]

        data = yaml.safe_load(frontmatter)
        if not data:
            errors.append("Empty YAML frontmatter")
            return errors, warnings

        metadata = data.get('metadata', {})
        if not metadata:
            errors.append("Missing 'metadata' section in YAML frontmatter")
            return errors, warnings

    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML syntax: {e}")
        return errors, warnings
    except Exception as e:
        errors.append(f"Failed to parse frontmatter: {e}")
        return errors, warnings

    # Validate required metadata fields
    for field in REQUIRED_FIELDS:
        if field not in metadata:
            errors.append(f"Missing required metadata field: '{field}'")
        elif not metadata[field]:
            errors.append(f"Empty required metadata field: '{field}'")

    # Validate specific fields
    if 'name' in metadata:
        name = metadata['name']

        # Check naming convention (kebab-case)
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
            errors.append(f"Name must be kebab-case (lowercase with hyphens): '{name}'")

        # Check filename matches name
        expected_filename = f"{name}.md"
        if skill_path.name != expected_filename:
            errors.append(f"Filename '{skill_path.name}' should match name '{expected_filename}'")

    # Validate version format (semver)
    if 'version' in metadata:
        version = metadata['version']
        if not re.match(r'^\d+\.\d+\.\d+$', version):
            errors.append(f"Version must follow semantic versioning (X.Y.Z): '{version}'")

    # Validate description length
    if 'description' in metadata:
        desc_len = len(metadata['description'])
        if desc_len < 50:
            warnings.append(f"Description is too short ({desc_len} chars, recommended: 50-200)")
        elif desc_len > 200:
            warnings.append(f"Description is too long ({desc_len} chars, recommended: 50-200)")

    # Validate category
    if 'category' in metadata:
        category = metadata['category']
        if category not in VALID_CATEGORIES:
            warnings.append(f"Category '{category}' not in standard list: {VALID_CATEGORIES}")

        # Check file is in correct category directory
        if skill_path.parent.name != category:
            warnings.append(f"File in '{skill_path.parent.name}' directory but category is '{category}'")

    # Validate tags
    if 'tags' in metadata:
        tags = metadata['tags']
        if not isinstance(tags, list):
            errors.append("Tags must be a list")
        elif len(tags) < 3:
            warnings.append(f"Should have at least 3 tags (found {len(tags)})")
        elif len(tags) > 10:
            warnings.append(f"Should have at most 10 tags (found {len(tags)})")

    # Validate difficulty
    if 'difficulty' in metadata:
        difficulty = metadata['difficulty']
        if difficulty and difficulty not in VALID_DIFFICULTIES:
            warnings.append(f"Difficulty '{difficulty}' should be one of: {VALID_DIFFICULTIES}")

    # Validate date format
    for date_field in ['created', 'updated']:
        if date_field in metadata and metadata[date_field]:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', metadata[date_field]):
                warnings.append(f"{date_field} should be in YYYY-MM-DD format")

    # Validate required sections
    for section in REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f"Missing required section: '{section}'")

    # Check for recommended sections
    for section in RECOMMENDED_SECTIONS:
        if section not in body:
            warnings.append(f"Missing recommended section: '{section}'")

    # Check for code blocks
    if '```' not in body:
        warnings.append("No code blocks found - consider adding code examples")

    # Check for proper step numbering
    if '## Steps' in body:
        steps_section = body.split('## Steps', 1)[1].split('##', 1)[0]
        step_pattern = r'###\s+\d+\.'
        steps_found = re.findall(step_pattern, steps_section)
        if not steps_found:
            warnings.append("Steps section should use numbered subsections (### 1., ### 2., etc.)")

    # Check body length
    body_length = len(body.strip())
    if body_length < 1000:
        warnings.append(f"Skill content seems short ({body_length} chars) - consider adding more detail")

    return errors, warnings

def print_results(skill_path, errors, warnings):
    """Print validation results."""
    print("=" * 70)
    print(f"Validating: {skill_path}")
    print("=" * 70)

    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")

    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")

    if not errors and not warnings:
        print("\n✅ Perfect! No issues found.")
    elif not errors:
        print(f"\n✅ Valid skill (with {len(warnings)} warning(s))")
    else:
        print(f"\n❌ Invalid skill - please fix {len(errors)} error(s)")

    print("=" * 70)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: validate_skill.py <skill_file.md>")
        print("\nExample:")
        print("  python validate_skill.py skills/benchmarking/benchmark-qwen.md")
        sys.exit(1)

    skill_path = sys.argv[1]
    errors, warnings = validate_skill(skill_path)

    print_results(skill_path, errors, warnings)

    # Exit code: 0 if valid (no errors), 1 if invalid (has errors)
    if errors:
        sys.exit(1)
    else:
        sys.exit(0)
