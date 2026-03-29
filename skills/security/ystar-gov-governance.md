---
metadata:
  name: "ystar-gov-governance"
  version: "1.0.0"
  description: "Set up Y*gov runtime governance for AI agents — enforce permissions, track obligations, write tamper-proof audit trails"
  category: "security"
  tags: ["ai-governance", "agent-security", "audit-trail", "compliance", "multi-agent", "permissions", "cieu", "runtime-governance"]
  author: "liuhaotian2024-prog"
  created: "2026-03-29"
  updated: "2026-03-29"

requirements:
  os: ["linux", "macos", "windows"]
  python: ">=3.11"
  packages:
    - ystar

estimated_time: "10-15 minutes"
difficulty: "beginner"
---

# Y*gov Runtime Governance for AI Agents

## Overview

Y*gov is a runtime governance framework for multi-agent AI systems. It enforces permission boundaries before tool execution, tracks agent obligations with automatic deadline enforcement, and writes every decision to a tamper-proof SHA-256 Merkle-chained audit database.

**Key properties:**
- Zero external dependencies (pure Python stdlib)
- No LLM in the enforcement path — governance cannot be prompt-injected
- 0.042ms enforcement latency per tool call
- Model-agnostic: governs Claude, GPT, MiniMax, or any other model

## Task Description

Set up Y*gov to govern your AI agent's tool calls. After completing this skill, every tool call your agent makes will be checked against your governance rules, and every decision will be recorded in an immutable audit chain.

## Prerequisites

- Python 3.11 or higher
- An AI agent project (Claude Code, OpenClaw, or any agent framework)
- Basic understanding of agent tool calls

## Steps

### 1. Install Y*gov

```bash
pip install git+https://github.com/liuhaotian2024-prog/Y-star-gov.git
```

### 2. Verify Installation

```bash
python -m ystar doctor
```

Expected: All checks pass. If any fail, the doctor output will tell you what to fix.

### 3. Create Your Governance Rules

Create an `AGENTS.md` file in your project root:

```markdown
# Governance Rules

## Prohibited Paths
- /etc
- /root
- ~/.ssh
- .env

## Prohibited Commands
- rm -rf
- sudo
- DROP TABLE

## Obligations
- Complete assigned tasks within 10 minutes
- Report findings after every search
```

### 4. Initialize Y*gov

```bash
python -m ystar setup --yes
```

This creates `.ystar_session.json` (session config) and `.ystar_retro_baseline.db` (baseline assessment).

### 5. Install the Governance Hook

```bash
python -m ystar hook-install
```

This registers Y*gov as a PreToolUse hook. Every tool call will now pass through `check()` before execution.

### 6. Verify Governance is Active

```bash
python -m ystar doctor
```

Expected: All 7 checks pass, including Hook Registration and Hook Self-Test.

### 7. Run Your Agent

Run your agent normally. Y*gov works transparently — it intercepts tool calls, checks them against your AGENTS.md rules, and records decisions.

### 8. View the Audit Trail

```bash
python -m ystar report
```

This shows all governance decisions: how many were allowed, how many denied, and which agents triggered them.

### 9. Verify Chain Integrity

```bash
python -m ystar verify
```

This verifies the SHA-256 Merkle chain has not been tampered with.

### 10. Seal a Session

```bash
python -m ystar seal
```

This cryptographically seals the current session, producing a Merkle root hash that proves no records were modified after sealing.

## Expected Output

After setup, `ystar doctor` should show:

```
[1] Session Config          ✅
[2] Hook Registration       ✅
[3] CIEU Database           ✅
[4] AGENTS.md               ✅
[4.5] Retroactive Baseline  ✅
[5] Hook Self-Test          ✅

✅ All 7 checks passed — Y*gov is healthy
```

After running your agent, `ystar report` should show governance decisions with allow/deny counts.

## Troubleshooting

### "No module named ystar"
- Ensure Python >= 3.11: `python --version`
- Reinstall: `pip install --force-reinstall git+https://github.com/liuhaotian2024-prog/Y-star-gov.git`

### Hook not triggering
- Run `ystar hook-install` again
- Check `.claude/settings.json` for hook registration
- Run `ystar doctor` to diagnose

### Windows: "python3 not found"
- Y*gov uses `python` (not `python3`) on Windows
- This is handled automatically in v0.41.1+

## Success Criteria

- [ ] `ystar doctor` shows all 7 checks passing
- [ ] Agent tool calls are being intercepted (check `ystar report`)
- [ ] Forbidden paths (e.g., /etc/passwd) are blocked
- [ ] CIEU database contains governance records
- [ ] `ystar verify` confirms chain integrity

## Related Skills

- AI agent development
- Security auditing
- Compliance reporting

## References

- [Y*gov Source Code](https://github.com/liuhaotian2024-prog/Y-star-gov)
- [Y* Bridge Labs](https://github.com/liuhaotian2024-prog/ystar-bridge-labs)
- [Quick Start Example](https://github.com/liuhaotian2024-prog/Y-star-gov/blob/main/examples/quickstart.py)
