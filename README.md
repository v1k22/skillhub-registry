# SkillHub Registry

> A community-driven registry of reusable AI agent workflows

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/skills-5-blue.svg)](./skills)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

## What is SkillHub?

SkillHub is a package manager for AI agent workflows, similar to how Homebrew manages packages or npm manages JavaScript libraries. When AI coding agents (like Claude Code, GitHub Copilot, or ChatGPT) complete complex tasks, they follow specific sequences of steps. SkillHub allows you to:

- **Store** completed AI agent workflows as reusable "skills"
- **Search** and discover relevant skills for your tasks
- **Pull** and execute skills on different environments/hardware
- **Contribute** new skills via GitHub Pull Requests

## The Problem

When AI agents complete complex tasks (like benchmarking a model, setting up a development environment, or deploying an application), the workflow is lost after completion. Users must re-prompt similar tasks from scratch, wasting time and effort.

## The Solution

SkillHub stores these workflows as structured markdown files with:
- Step-by-step instructions
- Code examples
- Troubleshooting guides
- Success criteria
- Metadata for searchability

## Quick Start

### Using Skills

```bash
# Install the SkillHub CLI
pip install skillhub

# Search for skills
skillhub search "benchmark model"

# Pull a skill to your local directory
skillhub pull benchmark-qwen

# List all available skills
skillhub list

# View skill details
cat benchmark-qwen.md
```

### Contributing Skills

**Easy Way (Recommended):** Submit via GitHub Issue - no setup required!

1. Go to [Submit a Skill](https://github.com/v1k22/skillhub-registry/issues/new?template=submit-skill.yml)
2. Paste your skill markdown
3. Submit the issue
4. A Pull Request is created automatically!

**Alternative:** Manual PR submission

```bash
# Fork this repository
# Create a new skill using the template
cp templates/skill-template.md skills/category/my-skill.md

# Edit the skill file
# Validate your skill
python scripts/validate_skill.py skills/category/my-skill.md

# Submit a Pull Request
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Available Skills

### Benchmarking
- **[benchmark-qwen](skills/benchmarking/benchmark-qwen.md)** - Benchmark Qwen 3B model on custom hardware with comprehensive performance metrics

### Data Engineering
- **[etl-pipeline](skills/data-engineering/etl-pipeline.md)** - Set up a production-ready ETL pipeline with data validation and monitoring

### Web Development
- **[react-app-setup](skills/web-development/react-app-setup.md)** - Set up a modern React application with TypeScript, Tailwind CSS, and best practices

### Automation
- **[web-scraper](skills/automation/web-scraper.md)** - Build a robust web scraper with rate limiting, error handling, and data export

### ML Ops
- **[model-deployment](skills/ml-ops/model-deployment.md)** - Deploy ML model as REST API using FastAPI with Docker containerization

## Skill Format

Skills are structured markdown files with:

```markdown
---
metadata:
  name: "skill-name"
  version: "1.0.0"
  description: "What this skill does"
  category: "category-name"
  tags: ["tag1", "tag2"]
  author: "github_username"

requirements:
  os: ["linux", "macos"]
  python: ">=3.9"
  packages:
    - package1>=1.0.0
---

# Skill Title

## Overview
Brief overview

## Task Description
What gets accomplished

## Steps
1. Step one
2. Step two
...

## Expected Output
What you'll get

## Troubleshooting
Common issues and solutions

## Success Criteria
How to know it worked
```

See [templates/skill-template.md](templates/skill-template.md) for the full template.

## How It Works

1. **Registry**: This GitHub repository stores all skills as markdown files
2. **Index**: An auto-generated `index.json` makes skills searchable
3. **CLI Tool**: The `skillhub` command-line tool lets users search and pull skills
4. **Validation**: GitHub Actions automatically validate new skill submissions
5. **Community**: Anyone can contribute skills via Pull Requests

## Architecture

![SkillHub Architecture](skillhub.png)

```
skillhub-registry/
├── skills/              # All skills organized by category
│   ├── benchmarking/
│   ├── data-engineering/
│   ├── web-development/
│   ├── automation/
│   └── ml-ops/
├── templates/           # Skill template for contributors
├── scripts/             # Automation scripts
│   ├── generate_index.py
│   └── validate_skill.py
├── .github/workflows/   # GitHub Actions
└── index.json          # Auto-generated search index
```

## CLI Installation

```bash
# Install from PyPI
pip install skillhub

# Or install from source
git clone https://github.com/v1k22/skillhub-cli.git
cd skillhub-cli
pip install -e .
```

## CLI Usage

```bash
# Search for skills
skillhub search "react setup"

# List all skills
skillhub list

# List skills in a category
skillhub list --category web-development

# Pull a skill
skillhub pull react-app-setup

# Get CLI info
skillhub info

# Validate a skill file
skillhub validate my-skill.md
```

## Use Cases

### 1. Reproducible Benchmarks
Run the same benchmark across different hardware:
```bash
skillhub pull benchmark-qwen
# Run on hardware A, save results
# Run on hardware B, compare results
```

### 2. Onboarding New Developers
New team member needs a dev environment:
```bash
skillhub search "react setup"
skillhub pull react-app-setup
# Follow the steps to set up identical environment
```

### 3. Standardized Workflows
Ensure consistency across team:
```bash
skillhub pull etl-pipeline
# Everyone uses the same ETL structure
```

### 4. Learning and Education
Learn best practices by example:
```bash
skillhub search "deployment"
skillhub pull model-deployment
# See production-ready deployment setup
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to create a skill
- Skill format requirements
- Submission process
- Code of conduct

## Roadmap

### Phase 1 (Current)
- [x] Basic registry structure
- [x] 5 example skills
- [x] Skill template
- [x] Validation scripts
- [x] CLI tool (basic)

### Phase 2 (Next)
- [ ] 20+ community skills
- [ ] Vector search for semantic matching
- [ ] Skill versioning system
- [ ] Dependency resolution
- [ ] Web UI for browsing

### Phase 3 (Future)
- [ ] Skill execution engine (`skillhub run`)
- [ ] Analytics dashboard
- [ ] VSCode extension
- [ ] AI-powered skill generation
- [ ] Skill marketplace

## Community

- **GitHub Issues**: Report bugs or request skills
- **Discussions**: Share ideas and ask questions
- **Twitter**: Follow [@skillhub](https://twitter.com/skillhub) for updates
- **Discord**: Join our community (coming soon)

## FAQ

**Q: What makes a good skill?**
A: A good skill is complete, well-documented, tested, and solves a real problem. It should be reproducible across different environments.

**Q: Can I use skills from other AI agents?**
A: Yes! Skills are platform-agnostic markdown files. They work with Claude Code, GitHub Copilot, ChatGPT, or human developers.

**Q: How do I update a skill?**
A: Submit a PR with the updated skill and increment the version number in the metadata.

**Q: Can skills have dependencies on other skills?**
A: Not yet, but this is planned for Phase 2. For now, link to related skills in the "Related Skills" section.

**Q: Is this only for Python?**
A: No! We have skills for JavaScript, Python, shell scripting, and more. Any reproducible workflow can be a skill.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by [Homebrew](https://brew.sh/) package manager
- Built for AI agent workflows like [Claude Code](https://github.com/anthropics/claude-code)
- Community-driven and open source

## Star History

If you find SkillHub useful, please star this repository!

---

**Made with ❤️ by the SkillHub community**

[Contribute a Skill](CONTRIBUTING.md) | [Report an Issue](https://github.com/v1k22/skillhub-registry/issues) | [CLI Documentation](https://github.com/v1k22/skillhub-cli)
