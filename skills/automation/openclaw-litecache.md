[openclaw-litecache.md](https://github.com/user-attachments/files/27062122/openclaw-litecache.md)
---
metadata:
  name: "openclaw-litecache"
  version: "1.0.0"
  description: "Zero-dependency Q&A cache for OpenClaw - SQLite-based, no Redis/Embedding API needed. Reduce token consumption with keyword matching + edit distance."
  category: "automation"
  tags: ["openclaw", "openclaw-skill", "cache", "token-saving", "cost-reduction", "sqlite", "lightweight", "qa-cache", "python"]
  author: "ben3132"
  created: "2026-04-24"
  updated: "2026-04-25"

requirements:
  os: ["linux", "macos", "windows"]
  python: ">=3.7"
---
## Overview

**openclaw-litecache** is a zero-dependency Q&A cache skill for OpenClaw that reduces token consumption by caching answers to objective questions. Unlike other cache solutions, it requires no Redis, no Embedding API, and no vector database — just Python standard library and SQLite.

**Key differentiators:**
- ✅ **Zero external dependencies** (Python standard library only)
- ✅ **SQLite single-file storage** (backup is just one file)
- ✅ **No Embedding API calls** (saves an extra API round-trip)
- ✅ **Semantic similarity matching** (keyword + edit distance)
- ✅ **Auto-excludes time-sensitive and context-dependent questions**
- ✅ **Auto-trigger, no manual invocation needed**

## Who Should Use This

| Use Case | Recommendation |
|----------|---------------|
| Individual developers, small teams | ✅ **Perfect fit** — zero setup overhead |
| Offline / air-gapped environments | ✅ **Only option** — no external services needed |
| Budget-sensitive projects | ✅ **Cost-effective** — no extra API costs |
| Enterprise high-concurrency | ❌ Use GPTCache or similar |
| Need deep semantic matching | ❌ Use openclaw-semantic-cache with embeddings |

## Task Description

Install and configure openclaw-litecache to automatically intercept repeated questions, match them against cached answers using lightweight semantic similarity, and return cached responses instead of consuming fresh API tokens.

## Prerequisites

- OpenClaw installed and running
- Python 3.7+ (no external packages required)

## Steps

### 1. Install the Skill

Clone to your OpenClaw skills directory:

```bash
git clone https://github.com/ben3132/openclaw-litecache.git ~/.openclaw/workspace/skills/openclaw-litecache
```

### 2. Initialize the Database

```bash
python scripts/init_db.py
```

This creates `data/cache.db`.

### 3. Configure (Optional)

Edit `config.json`:

```json
{
  "similarity_threshold": 0.4,
  "max_question_length": 100,
  "default_ttl_hours": 24,
  "max_cache_size": 1000
}
```

### 4. Verify Installation

```bash
python scripts/lookup.py "Python怎么安装"
python scripts/store.py --question "Python怎么安装" --answer "访问 python.org..."
python scripts/lookup.py "Python安装教程"
```

## Expected Output

- **Cache hit**: Returns cached answer with similarity score
- **Cache miss**: Returns empty, proceeds to AI model
- **Token savings**: Repeated questions consume zero additional tokens

## Comparison with Alternatives

| Feature | openclaw-litecache | GPTCache | openclaw-semantic-cache |
|---------|-------------------|----------|------------------------|
| External dependencies | ❌ None | ✅ Redis/Milvus | ✅ Required |
| Embedding API | ❌ Not needed | ✅ Required | ✅ Required |
| Storage | SQLite file | Vector DB | Redis |
| Deployment | Copy & use | Infrastructure setup | Configuration needed |
| Best for | Individuals, small teams, offline | Enterprise, high-concurrency | Deep semantic matching |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Ensure Python 3.7+ is in PATH |
| Database locked | Only one process can write at a time |
| GBK encoding error | Set `PYTHONIOENCODING=utf-8` |
| Low hit rate | Lower `similarity_threshold` to 0.3 |

## Success Criteria

- Database initializes without errors
- Store and lookup operations work end-to-end
- Similar questions match (e.g., "Python安装教程" ↔ "Python怎么安装")
- Time-sensitive questions excluded from caching
- Cache respects TTL and expires old entries

## References

- GitHub: https://github.com/ben3132/openclaw-litecache
- License: MIT
