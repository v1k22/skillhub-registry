---
metadata:
 name: "qcache"
 version: "1.0.0"
 description: "Q&A cache skill for OpenClaw that reduces token consumption by caching answers to objective, time-stable questions using semantic similarity matching"
 category: "automation"
 tags: ["openclaw", "cache", "token-saving", "qa", "python", "sqlite", "semantic-similarity"]
 author: "ben3132"
 created: "2026-04-24"
 updated: "2026-04-24"

requirements:
 os: ["linux", "macos", "windows"]
 python: ">=3.7"
---
## Overview

qcache is an OpenClaw skill that caches Q&A pairs to reduce token consumption on repeated or semantically similar questions. It uses keyword extraction and edit distance for similarity matching, automatically filters out time-sensitive and context-dependent questions, and stores data in a lightweight SQLite database.

**Key features:**
- Semantic similarity matching (keyword + edit distance)
- Auto-excludes time-sensitive and context-dependent questions
- Auto-trigger, no manual invocation needed
- SQLite storage, lightweight and efficient
- Zero external dependencies (Python standard library only)

## Task Description

Install and configure qcache to automatically intercept repeated questions, match them against cached answers using semantic similarity, and return cached responses instead of consuming fresh API tokens.

## Prerequisites

- OpenClaw installed and running
- Python 3.7+ (no external packages required, uses only standard library)
- qcache skill files placed in your OpenClaw skills directory

## Steps

### 1. Install the Skill

Clone or download qcache to your OpenClaw skills directory:


git clone https://github.com/ben3132/qcache.git ~/.openclaw/workspace/skills/qcache

Or manually copy the entire qcache/ folder (containing SKILL.md, meta.json, scripts/, config.json) into your skills directory.

2. Initialize the Database
Run the initialization script to create the SQLite cache database:

bash

复制
python scripts/init_db.py
This creates data/cache.db with the required tables.

3. Configure Thresholds (Optional)
Edit config.json to adjust settings:

json

复制
{
 "similarity_threshold": 0.4,
 "max_question_length": 100,
 "default_ttl_hours": 24,
 "max_cache_size": 1000
}
similarity_threshold: Similarity threshold (0.0-1.0), higher = stricter matching
default_ttl_hours: Cache expiration time in hours
max_question_length: Questions longer than this are not cached
max_cache_size: Maximum number of cached entries
4. Verify Installation
Test with a sample query:

bash

复制
python scripts/lookup.py "Python怎么安装"
Expected output: No cache hit (empty cache). Then store a test entry:

bash

复制
python scripts/store.py --question "Python怎么安装" --answer "访问 python.org 下载安装包..."
And verify lookup works:

bash

复制
python scripts/lookup.py "Python安装教程"
Expected output: Returns the cached answer with similarity score.

Expected Output
On cache hit: Returns the cached answer along with similarity score and timestamp
On cache miss: Returns empty/no result, allowing the question to proceed to the AI model
Token savings: Repeated similar questions consume zero additional tokens for the AI response
Example cache hit response:

json

复制
{"hit": true, "answer": "...", "similarity": 0.85}
Example cache miss response:

json

复制
{"hit": false}
Troubleshooting
Problem	Solution
ModuleNotFoundError	Ensure Python 3.7+ is in PATH; all scripts use only standard library
Database locked	Only one process can write at a time; ensure no concurrent store operations
GBK encoding error on Windows	Scripts include sys.stdout.reconfigure(encoding='utf-8'); if still failing, set PYTHONIOENCODING=utf-8 environment variable
Low hit rate	Lower similarity_threshold in config.json (try 0.3); check that questions are objective and not context-dependent
Cache growing too large	Run python scripts/manage.py clean to remove expired entries, or python scripts/manage.py clear to reset
Success Criteria
Database initializes without errors (python scripts/init_db.py completes successfully)
Store and lookup operations work end-to-end
Semantic similarity matches questions with meaningful overlap (e.g., “Python安装教程” matches “Python怎么安装”)
Time-sensitive questions (containing “今天”, “现在”, “最新”) are correctly excluded from caching
Context-dependent questions (containing “这个”, “刚才”, “那…”) are filtered out
Cache respects configured TTL and expires old entries automatically
Running python scripts/manage.py stats shows correct cache statistics
Related Skills
ima - IMA knowledge base integration for OpenClaw
online-search - Web search capability for OpenClaw
References
GitHub Repository: https://github.com/ben3132/qcache
OpenClaw Documentation: https://docs.openclaw.com
License: MIT