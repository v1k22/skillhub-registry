---
metadata:
  name: "hermes-tweet"
  version: "1.0.0"
  description: "Install and operate the Hermes Tweet plugin for safe X/Twitter automation inside Hermes Agent"
  category: "automation"
  tags: ["hermes-agent", "twitter", "x", "automation", "social-media"]
  author: "Xquik"
  created: "2026-06-07"
  updated: "2026-06-07"

requirements:
  os: ["linux", "macos", "windows"]
  python: ">=3.12"
  packages:
    - hermes-agent
    - hermes-tweet
  hardware:
    - ram: ">=512MB"
    - disk_space: ">=50MB"

estimated_time: "10-15 minutes"
difficulty: "beginner"
---

# Hermes Tweet for Hermes Agent

## Overview
Hermes Tweet installs X/Twitter automation into Hermes Agent as a native plugin. Use it when an agent needs public X search, tweet lookup, profile context, thread reading, trend discovery, or carefully gated write actions without collecting browser cookies in chat.

The plugin separates safe exploration, authenticated read tools, and opt-in action tools. Read tools require an Xquik API key. Action tools also require an explicit action flag so posting, replying, liking, reposting, and following remain disabled by default.

## Task Description
Configure a Hermes Agent workspace so agents can use Hermes Tweet for X/Twitter work:

1. Install the plugin through the Hermes plugin manager.
2. Add the required API key to the runtime environment.
3. Keep action tools disabled unless the workflow explicitly needs them.
4. Verify the agent can discover available tweet tools.
5. Use the read tools for search, tweet lookup, profiles, threads, and trends.
6. Enable action tools only after the account owner approves the workflow.

## Prerequisites
- Hermes Agent installed and available from the terminal
- Python 3.12 or newer
- Xquik API key available as `XQUIK_API_KEY`
- Permission from the X account owner before enabling any action tool

## Steps

### 1. Install the Plugin
```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

This installs Hermes Tweet from GitHub and enables it in the current Hermes Agent plugin configuration.

### 2. Configure Read Access
```bash
read -rsp "Xquik API key: " XQUIK_API_KEY
export XQUIK_API_KEY
```

Use a local shell, secret manager, or deployment environment. Do not paste API keys into prompts, issues, logs, or public files.

### 3. Keep Actions Disabled by Default
```bash
unset HERMES_TWEET_ENABLE_ACTIONS
```

This keeps write-capable tools unavailable while still allowing public read workflows. Enable actions only when the user explicitly wants the agent to perform account-changing operations.

### 4. Verify Tool Discovery
```bash
hermes plugins list
```

Confirm that `hermes-tweet` is enabled. In Hermes Agent, ask for available tweet tools and verify that read tools are present before running a real task.

### 5. Run Read-Only Workflows
Ask Hermes Agent to use Hermes Tweet for read tasks such as:

```text
Find recent posts about Hermes Agent plugins and summarize the top themes.
```

```text
Read this X thread and extract the concrete product feedback.
```

The plugin exposes ungated exploration helpers plus authenticated read tools. Prefer read-only workflows for research, monitoring, digest generation, and social listening.

### 6. Enable Actions Only When Needed
```bash
export HERMES_TWEET_ENABLE_ACTIONS="true"
```

After enabling actions, keep prompts explicit about the exact action, account, content, and approval boundary. Turn actions off again after the task finishes.

## Expected Output
- Hermes Agent lists `hermes-tweet` as an enabled plugin.
- Read workflows can search posts, inspect tweets, read threads, and gather profile or trend context.
- Action tools remain unavailable unless `HERMES_TWEET_ENABLE_ACTIONS=true` is set.
- Agent responses return structured X/Twitter context that can be used for monitoring, digests, outreach research, and support workflows.

## Success Criteria
- Plugin installation completes without manual file edits.
- `XQUIK_API_KEY` is provided only through a local environment or secret store.
- Read tools work before any action tool is enabled.
- Action tools are disabled by default in normal research and monitoring workflows.
- The user can reproduce the install and safety checks from this skill alone.

## Troubleshooting

### Plugin Is Not Listed
```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
hermes plugins list
```

Reinstall and verify the active Hermes Agent configuration.

### Read Tools Are Missing or Unavailable
```bash
echo "${XQUIK_API_KEY:+configured}"
```

If this prints nothing, configure `XQUIK_API_KEY` in the same runtime that starts Hermes Agent.

### Action Tools Are Still Disabled
```bash
export HERMES_TWEET_ENABLE_ACTIONS="true"
```

Restart the Hermes Agent process after changing the environment. Keep this flag unset for read-only work.

### Authentication Data Appears in a Prompt
Stop the task, rotate the exposed key, and move the replacement value into a local environment or approved secret store.

## Related Skills
- `web-scraper`
- `etl-pipeline`
- `react-app-setup`

## References
- [Hermes Tweet](https://github.com/Xquik-dev/hermes-tweet)
- [Hermes Agent plugin guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins/)
- [Build a Hermes Plugin](https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin/)
- [Xquik](https://xquik.com)
