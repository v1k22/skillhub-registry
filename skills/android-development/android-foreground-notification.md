---
metadata:
  name: "android-foreground-notification"
  version: "1.0.0"
  description: "Android foreground service persistent notification with anti-swipe recovery — battle-tested on MIUI/HyperOS and Chinese ROMs. Based on FLClash source analysis (41K+ stars)."
  category: "android-development"
  tags: ["android", "kotlin", "foreground-service", "notification", "miui", "anti-swipe", "proxy", "vpn"]
  author: "Markjinli"
  created: "2026-06-05"
  updated: "2026-06-05"

requirements:
  os: ["windows", "linux", "macos"]
  tools:
    - Android Studio
  languages:
    - kotlin

estimated_time: "5 minutes"
difficulty: "beginner"
---

# Android Foreground Notification — Persistent Status Bar Service

## Overview
This skill provides production-ready Android `Service` implementations for persistent status bar notifications that survive swipe-to-dismiss on MIUI and other Chinese ROMs. Based on reverse-engineering FLClash (41K+ stars on GitHub).

## Core Mechanism

`Service.startForeground(id, notification)` can be called repeatedly. On Android, re-calling it on an already-foreground service **re-posts** the notification. Simply re-call every 1-2 seconds — no need to detect dismissal.

## Files Provided

| File | Description |
|------|-------------|
| `templates/MinimalService.kt` | Minimal 40-line template (static notification) |
| `templates/TrafficService.kt` | FLClash-style template with real-time traffic display |
| `templates/AndroidManifest.xml` | Required manifest declarations |

## Quick Start

1. Copy `MinimalService.kt` to your project
2. Add the `<service>` declaration from `AndroidManifest.xml`
3. Start with: `startService(Intent(context, PersistentNotificationService::class.java))`

## Source Repository
https://github.com/Markjinli/android-foreground-notification-skill

## Trigger Words
"foreground service notification", "persistent notification android", "startForeground anti-swipe", "MIUI notification recovery", "android status bar notification", "notification won't dismiss android"
