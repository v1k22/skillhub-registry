#!/usr/bin/env python3
"""
Process skill submission from GitHub Issue.
Extracts skill content, validates it, and outputs metadata for PR creation.
"""

import sys
import re
import json
import yaml
from pathlib import Path


def extract_field(body: str, field_name: str) -> str:
    """Extract content from a GitHub issue form field."""
    # GitHub issue forms use ### Field Name format
    pattern = rf'### {re.escape(field_name)}\s*\n+(.*?)(?=\n### |\Z)'
    match = re.search(pattern, body, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def extract_skill_content(body: str) -> str:
    """Extract the skill markdown content from issue body."""
    content = extract_field(body, "Skill Markdown")
    # Remove any markdown code block wrappers if present
    content = re.sub(r'^```(?:markdown|md|yaml)?\s*\n', '', content)
    content = re.sub(r'\n```\s*$', '', content)
    return content.strip()


def extract_category(body: str) -> str:
    """Extract category from issue body."""
    category = extract_field(body, "Category")
    if category.lower() == "other":
        custom = extract_field(body, "Custom Category (if \"Other\" selected above)")
        if custom:
            return custom.lower().replace(" ", "-")
    return category.lower()


def parse_yaml_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from skill content."""
    if not content.startswith('---'):
        return None

    # Find the closing ---
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return None

    yaml_content = content[3:end_match.start() + 3]
    try:
        return yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        print(f"YAML parsing error: {e}", file=sys.stderr)
        return None


def validate_skill(content: str) -> tuple[bool, list[str], list[str]]:
    """
    Validate skill content.
    Returns (is_valid, list_of_errors, list_of_warnings)

    Only essential fields for index.json are required:
    - name, version, description, category, tags, author
    """
    errors = []
    warnings = []

    # Check YAML frontmatter exists
    if not content.startswith('---'):
        errors.append("Skill must start with YAML frontmatter (---)")
        return False, errors, warnings

    # Parse frontmatter
    frontmatter = parse_yaml_frontmatter(content)
    if frontmatter is None:
        errors.append("Invalid YAML frontmatter format. Make sure you have closing --- after the metadata.")
        return False, errors, warnings

    # Check metadata section
    metadata = frontmatter.get('metadata', {})
    if not metadata:
        errors.append("Missing 'metadata' section in frontmatter")
        return False, errors, warnings

    # Required metadata fields (essential for index.json)
    required_fields = ['name', 'description', 'category', 'tags', 'author']
    for field in required_fields:
        if field not in metadata or not metadata[field]:
            errors.append(f"Missing required metadata field: {field}")

    # Optional but recommended
    if 'version' not in metadata:
        warnings.append("Missing 'version' field - defaulting to 1.0.0")

    # Validate name format (kebab-case) - be lenient
    name = metadata.get('name', '')
    if name:
        # Allow alphanumeric and hyphens, just no spaces or special chars
        if not re.match(r'^[a-zA-Z0-9-]+$', name):
            errors.append(f"Skill name should only contain letters, numbers, and hyphens. Got: {name}")
        elif ' ' in name:
            errors.append(f"Skill name cannot contain spaces. Use hyphens instead. Got: {name}")

    # Validate tags is a list
    tags = metadata.get('tags', [])
    if tags and not isinstance(tags, list):
        errors.append("Tags must be a list/array (e.g., [\"tag1\", \"tag2\"])")

    # Content sections are now optional - just warn if missing
    recommended_sections = ['Overview', 'Steps']
    for section in recommended_sections:
        # Look for ## Section Name (case insensitive, allowing content after)
        if not re.search(rf'^##\s+{re.escape(section)}', content, re.MULTILINE | re.IGNORECASE):
            warnings.append(f"Recommended section missing: ## {section}")

    return len(errors) == 0, errors, warnings


def check_duplicate(skill_name: str, category: str) -> bool:
    """Check if a skill with this name already exists."""
    skills_dir = Path('skills')
    if not skills_dir.exists():
        return False

    # Normalize skill name for comparison
    skill_name_lower = skill_name.lower()

    # Check in all categories
    for skill_file in skills_dir.rglob("*.md"):
        if skill_file.stem.lower() == skill_name_lower:
            return True

    return False


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: process_skill_submission.py <issue_body_file>", file=sys.stderr)
        sys.exit(1)

    # Read issue body from file
    body_file = sys.argv[1]
    with open(body_file, 'r', encoding='utf-8') as f:
        issue_body = f.read()

    # Extract skill content
    skill_content = extract_skill_content(issue_body)
    if not skill_content:
        print("::error::Could not extract skill content from issue body. Make sure you pasted the skill markdown in the 'Skill Markdown' field.")
        sys.exit(1)

    # Debug: print first 200 chars of extracted content
    print(f"Extracted skill content (first 200 chars): {skill_content[:200]}...")

    # Extract category from form (fallback)
    form_category = extract_category(issue_body)

    # Validate skill
    is_valid, errors, warnings = validate_skill(skill_content)

    # Print warnings (non-fatal)
    for warning in warnings:
        print(f"::warning::{warning}")

    if not is_valid:
        error_msg = "Skill validation failed:\\n" + "\\n".join(f"- {e}" for e in errors)
        print(f"::error::{error_msg}")
        # Output errors for workflow to use
        print(f"validation_errors={json.dumps(errors)}")
        sys.exit(1)

    # Parse metadata
    frontmatter = parse_yaml_frontmatter(skill_content)
    metadata = frontmatter.get('metadata', {})
    skill_name = metadata.get('name', 'unknown-skill')

    # Use category from metadata if available, otherwise from form
    skill_category = metadata.get('category', form_category)
    if skill_category:
        skill_category = skill_category.lower().replace(" ", "-")
    else:
        skill_category = 'uncategorized'

    # Check for duplicates
    if check_duplicate(skill_name, skill_category):
        print(f"::warning::A skill named '{skill_name}' already exists. The PR will update the existing skill.")

    # Get version with default
    skill_version = metadata.get('version', '1.0.0')

    # Output results for GitHub Actions
    import os

    github_output = os.environ.get('GITHUB_OUTPUT', '')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"skill_name={skill_name}\n")
            f.write(f"skill_category={skill_category}\n")
            f.write(f"skill_version={skill_version}\n")
            f.write(f"skill_description={metadata.get('description', '')}\n")
            f.write(f"skill_author={metadata.get('author', 'unknown')}\n")
            f.write(f"file_path=skills/{skill_category}/{skill_name}.md\n")
    else:
        # Fallback for local testing
        print(f"skill_name={skill_name}")
        print(f"skill_category={skill_category}")
        print(f"skill_version={skill_version}")
        print(f"skill_description={metadata.get('description', '')}")
        print(f"skill_author={metadata.get('author', 'unknown')}")
        print(f"file_path=skills/{skill_category}/{skill_name}.md")

    # Save skill content to a temp file for the workflow
    with open('/tmp/skill_content.md', 'w', encoding='utf-8') as f:
        f.write(skill_content)

    print(f"Successfully validated skill: {skill_name}")
    print(f"Category: {skill_category}")
    print(f"File will be created at: skills/{skill_category}/{skill_name}.md")


if __name__ == '__main__':
    main()
