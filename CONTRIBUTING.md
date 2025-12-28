# Contributing to SkillHub Registry

Thank you for your interest in contributing to SkillHub! This document provides guidelines and instructions for contributing new skills to the registry.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Skill Requirements](#skill-requirements)
- [Skill Format Specification](#skill-format-specification)
- [Submission Process](#submission-process)
- [Review Process](#review-process)
- [Best Practices](#best-practices)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone. We expect all contributors to:

- Be respectful and considerate
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Trolling or insulting/derogatory comments
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## How to Contribute

There are several ways to contribute to SkillHub:

### 1. Submit a New Skill

Create a skill that solves a real problem you've encountered. See [Skill Requirements](#skill-requirements) below.

### 2. Improve Existing Skills

Found a bug or have an improvement? Submit a PR to update an existing skill.

### 3. Report Issues

Found a problem with a skill? [Open an issue](https://github.com/v1k22/skillhub-registry/issues/new).

### 4. Suggest New Categories

Think we need a new skill category? Start a discussion!

## Skill Requirements

### Required Elements

Every skill must include:

1. **Metadata Section**
   - Name (unique, kebab-case)
   - Version (semantic versioning)
   - Description (50-200 characters)
   - Category
   - Tags (3-10 relevant tags)
   - Author (your GitHub username)

2. **Content Sections**
   - Overview
   - Task Description
   - Prerequisites
   - Steps (detailed, numbered)
   - Expected Output
   - Troubleshooting
   - Success Criteria

3. **Quality Standards**
   - Must be tested and working
   - Code examples must be complete and runnable
   - Must handle common errors
   - Should be reproducible across environments

### Optional but Recommended

- Related Skills section
- References section
- Next Steps section
- Diagrams or screenshots
- Time estimates
- Difficulty level

## Skill Format Specification

### Metadata Format

```yaml
---
metadata:
  name: "skill-name"              # Required: kebab-case, unique
  version: "1.0.0"                # Required: semver (major.minor.patch)
  description: "Brief description" # Required: 50-200 chars
  category: "category-name"       # Required: see categories below
  tags: ["tag1", "tag2", "tag3"]  # Required: 3-10 tags
  author: "github_username"       # Required: your GitHub username
  created: "2024-01-15"           # Required: YYYY-MM-DD
  updated: "2024-01-15"           # Required: YYYY-MM-DD

requirements:                     # Optional but recommended
  os: ["linux", "macos", "windows"]
  python: ">=3.9"                 # If applicable
  node: ">=18.0.0"                # If applicable
  packages:
    - package1>=1.0.0
    - package2
  hardware:
    - ram: ">=8GB"
    - gpu: "optional"

estimated_time: "30-45 minutes"   # Optional
difficulty: "intermediate"        # Optional: beginner/intermediate/advanced
---
```

### Available Categories

- `benchmarking` - Performance testing and benchmarks
- `data-engineering` - ETL, pipelines, data processing
- `web-development` - Web apps, APIs, frontend
- `automation` - Scripts, bots, scrapers
- `ml-ops` - ML deployment and operations
- `devops` - Infrastructure, CI/CD, deployment
- `testing` - Test setup, frameworks, automation
- `database` - Database setup, migrations, queries
- `security` - Security tools, audits, hardening

Don't see your category? [Suggest a new one](https://github.com/v1k22/skillhub-registry/discussions)!

### Naming Convention

- Use kebab-case: `my-skill-name`
- Be descriptive: `setup-react-typescript` not `setup-react`
- Avoid redundancy: `benchmark-qwen` not `benchmark-qwen-model`
- Keep it short: 2-4 words maximum

### File Naming

- Filename must match metadata name
- Format: `{category}/{skill-name}.md`
- Example: `benchmarking/benchmark-qwen.md`

## Submission Process

### Step 1: Fork the Repository

```bash
# Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/skillhub-registry.git
cd skillhub-registry
```

### Step 2: Create a Branch

```bash
# Create a new branch for your skill
git checkout -b add-my-skill-name
```

### Step 3: Create Your Skill

```bash
# Copy the template
cp templates/skill-template.md skills/category/my-skill.md

# Edit the skill file
# Replace all placeholder content
# Ensure all code examples are tested
```

### Step 4: Validate Your Skill

```bash
# Install dependencies
pip install pyyaml

# Validate your skill
python scripts/validate_skill.py skills/category/my-skill.md

# If validation fails, fix the errors and run again
```

### Step 5: Test Your Skill

**IMPORTANT**: You must test your skill before submitting!

- Follow every step in your skill
- Run all code examples
- Verify the expected output
- Test troubleshooting steps
- Confirm success criteria are met

### Step 6: Commit and Push

```bash
# Add your skill
git add skills/category/my-skill.md

# Commit with a clear message
git commit -m "Add: my-skill for doing X"

# Push to your fork
git push origin add-my-skill-name
```

### Step 7: Create Pull Request

1. Go to your fork on GitHub
2. Click "Pull Request"
3. Fill out the PR template
4. Submit the PR

## Review Process

### Automated Checks

When you submit a PR, our GitHub Actions will:

1. **Validate Format**: Check YAML frontmatter and required sections
2. **Check Naming**: Verify filename matches metadata name
3. **Lint Markdown**: Check for formatting issues
4. **Generate Index**: Update the search index

All automated checks must pass before review.

### Manual Review

A maintainer will review your skill for:

- **Accuracy**: Does it work as described?
- **Completeness**: Are all steps clear and detailed?
- **Quality**: Is the code production-ready?
- **Originality**: Does this duplicate an existing skill?
- **Usefulness**: Does this solve a real problem?

### Feedback and Revisions

- Reviewers may request changes
- Update your PR branch with the changes
- Automated checks will run again
- Once approved, your skill will be merged!

## Best Practices

### Writing Clear Steps

**Good:**
```markdown
### 1. Install Dependencies
\`\`\`bash
pip install requests beautifulsoup4
\`\`\`

This installs the required libraries for web scraping.
```

**Bad:**
```markdown
### 1. Setup
Install stuff
```

### Providing Complete Code

**Good:**
```python
import requests

def fetch_data(url):
    """Fetch data from URL with error handling."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
```

**Bad:**
```python
# Fetch data
data = requests.get(url).json()
```

### Including Error Handling

Always include:
- Try/except blocks
- Timeout parameters
- Validation checks
- Helpful error messages

### Testing Across Environments

Test your skill on:
- Different OS (if applicable)
- Fresh virtual environments
- Minimum required versions
- Clean installation

### Documentation Quality

- Use proper grammar and spelling
- Be concise but complete
- Include examples
- Explain the "why" not just the "what"

### Code Quality

- Follow language-specific best practices
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

## Example PR Template

When submitting a PR, please include:

```markdown
## Description
Brief description of what this skill does.

## Category
- [ ] benchmarking
- [ ] data-engineering
- [ ] web-development
- [ ] automation
- [ ] ml-ops
- [ ] other: _______

## Checklist
- [ ] Skill follows the template structure
- [ ] All code examples have been tested
- [ ] Validation script passes
- [ ] Troubleshooting section includes common issues
- [ ] Success criteria are clear and measurable
- [ ] Related skills are linked (if applicable)

## Testing
Describe how you tested this skill:
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11]
- Date tested: [e.g., 2024-01-15]

## Additional Notes
Any additional context or notes for reviewers.
```

## Updating Existing Skills

To update an existing skill:

1. Increment the version number:
   - **Patch** (1.0.0 → 1.0.1): Bug fixes, typos
   - **Minor** (1.0.0 → 1.1.0): New sections, improvements
   - **Major** (1.0.0 → 2.0.0): Breaking changes

2. Update the `updated` date in metadata

3. Add a note at the top explaining what changed

4. Follow the same submission process

## Questions?

- Check [existing skills](skills/) for examples
- Read the [FAQ](README.md#faq)
- [Open a discussion](https://github.com/v1k22/skillhub-registry/discussions)
- [Ask in Discord](#) (coming soon)

## License

By contributing to SkillHub, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to SkillHub! Your skills help developers around the world. 🚀
