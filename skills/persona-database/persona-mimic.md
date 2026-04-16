# persona-mimic

> AI Character Persona Database — 1000 Famous Historical & Contemporary Figures

## Description

A comprehensive AI persona database featuring **1000 famous characters** from 8 domains.

Each character includes 10 fields:
- **thinking**: Cognitive style and thought patterns (思维方式)
- **speaking**: Communication style and expression (说话风格)
- **solving**: Problem-solving approach (解决问题方式)
- **recommended_skills**: AI tool skill tags (推荐技能标签)
- **quotes**: Famous quotes (经典语录)
- Plus: name, zhName, years, field, core

## Contents

| File | Domain | Count |
|------|--------|-------|
| 01_scientists.json | Scientists & Inventors | 160 |
| 02_artists.json | Artists & Musicians | 55 |
| 03_entrepreneurs.json | Entrepreneurs & Business Leaders | 133 |
| 04_athletes.json | Athletes | 246 |
| 05_writers.json | Writers & Thinkers | 90 |
| 06_actors.json | Actors & Directors | 124 |
| 07_historical.json | Historical Figures | 66 |
| 08_others.json | Other Famous People | 126 |
| **Total** | | **1000** |

## Skill Tags (45 types)

| Tag | Description | Count |
|-----|-------------|-------|
| athlete_basketball | Basketball players | 133 |
| musician_pop | Pop musicians | 125 |
| actor_classical | Actors | 106 |
| entrepreneur_tech | Tech entrepreneurs | 65 |
| scientist_ai | AI/Computer scientists | 94 |
| athlete_soccer | Soccer players | 49 |
| business_ceo | CEOs | 47 |
| writer | Writers | 38 |
| director | Directors | 37 |
| scientist_physics | Physicists | 30 |
| artist_painter | Painters | 30 |
| philosopher_western | Western philosophers | 17 |
| entrepreneur_chinese | Chinese entrepreneurs | 16 |
| athlete_chinese | Chinese athletes | 18 |
| military_commander | Military commanders | 10 |
| activist | Social activists | 4 |

## Example Character

```json
{
  "id": "albert_einstein",
  "name": "Albert Einstein",
  "zhName": "阿尔伯特·爱因斯坦",
  "years": "1879-1955",
  "field": "物理学",
  "core": "相对论创立者，现代物理学的奠基人",
  "thinking": "第一性原理思维与物理直觉",
  "speaking": "睿智、幽默、反权威",
  "solving": "思想实验与数学推导结合",
  "quotes": ["想象力比知识更重要", "上帝不掷骰子"],
  "recommended_skills": ["scientist_physics", "online-search"]
}
```

## Use Cases

- AI character roleplay conversations
- Few-shot prompting for LLMs
- Creative writing and storytelling
- Educational character simulation
- Game NPC personality design

## Installation

```bash
skillhub install persona-mimic
```

Or clone from GitHub:
```bash
git clone https://github.com/richard3153/persona-mimic.git
```

## License

MIT

## Author

richard3153
