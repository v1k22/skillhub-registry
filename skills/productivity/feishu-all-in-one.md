---
metadata:
  name: "feishu-all-in-one"
  version: "1.0.0"
  description: "飞书（Lark）全面技能整合包，涵盖日历、文档、多维表格、任务、消息等核心功能的完整使用指南"
  category: "productivity"
  tags: ["feishu", "lark", "calendar", "document", "bitable", "task", "im", "飞书"]
  author: "胡雨豪"
  created: "2026-03-24"
  updated: "2026-03-24"

requirements:
  os: ["linux", "macos", "windows"]
  packages:
    - openclaw >= 1.0.0
    - feishu-openclaw-plugin

estimated_time: "根据具体任务而定"
difficulty: "intermediate"
---

# 飞书 All-in-One 技能整合

本技能整合了飞书（Lark）的核心功能，包括日历日程、文档管理、多维表格、任务管理、消息读取等模块。

## 📋 技能索引

| 模块 | 功能 | 相关工具 |
|------|------|---------|
| 日历日程 | 创建会议、查忙闲、管理参会人 | feishu_calendar_event, feishu_calendar_freebusy |
| 文档管理 | 创建、获取、更新云文档 | feishu_create_doc, feishu_fetch_doc, feishu_update_doc |
| 多维表格 | 数据表、记录、字段管理 | feishu_bitable_app, feishu_bitable_app_table, feishu_bitable_app_table_record |
| 任务管理 | 创建待办、管理清单 | feishu_task_task, feishu_task_tasklist |
| 消息读取 | 历史消息、搜索、下载资源 | feishu_im_user_get_messages, feishu_im_user_search_messages |
| 组织架构 | 搜索用户、群组管理 | feishu_search_user, feishu_chat |
| 知识库 | 文档与 Wiki 搜索 | feishu_search_doc_wiki |

---

## 🚨 通用约束

### 1. 用户身份

所有工具均以**用户身份**调用，需要用户授权 OAuth。工具会自动处理 token 刷新。

### 2. ID 格式约定

| 类型 | 格式 | 示例 |
|------|------|------|
| 用户 | ou_xxx | ou_d7a85d0e0a04cdccf6d91f61f855f3b8 |
| 群组 | oc_xxx | oc_abc123 |
| 文档 | doxcnxxx | doxcnXXXXXXXX |
| 多维表格 | Sxxx | S404bXXXX |
| 会议室 | omm_xxx | omm_xxx |

### 3. 时间格式

**ISO 8601 / RFC 3339（带时区）**：
```
2026-03-24T14:00:00+08:00
```

---

## 📅 日历日程模块

### 快速索引

| 用户意图 | 工具 | action | 必填参数 |
|---------|------|--------|---------|
| 创建会议 | feishu_calendar_event | create | summary, start_time, end_time |
| 查日程 | feishu_calendar_event | list | start_time, end_time |
| 改日程 | feishu_calendar_event | patch | event_id |
| 搜日程 | feishu_calendar_event | search | query |
| 查忙闲 | feishu_calendar_freebusy | list | time_min, time_max, user_ids[] |
| 邀请参会人 | feishu_calendar_event_attendee | create | calendar_id, event_id, attendees[] |

### 核心约束

- **user_open_id 强烈建议**：从 SenderId 获取（ou_xxx），确保用户能看到日程
- **时间格式**：必须使用 ISO 8601 带时区，如 `2026-03-24T14:00:00+08:00`
- **参会人权限**：默认 can_modify_event，参会人可以编辑日程
- **会议室预约是异步**：添加后状态为 needs_action，需等待后台处理

### 示例：创建会议

```json
{
  "action": "create",
  "summary": "项目复盘会议",
  "description": "讨论 Q1 项目进展",
  "start_time": "2026-03-25T14:00:00+08:00",
  "end_time": "2026-03-25T15:30:00+08:00",
  "user_open_id": "ou_xxx",
  "attendees": [
    {"type": "user", "id": "ou_aaa"},
    {"type": "user", "id": "ou_bbb"}
  ]
}
```

---

## 📄 文档管理模块

### 快速索引

| 用户意图 | 工具 | 必填参数 |
|---------|------|---------|
| 创建文档 | feishu_create_doc | markdown, title |
| 获取文档 | feishu_fetch_doc | doc_id |
| 更新文档 | feishu_update_doc | doc_id, mode |

### 文档模式（7种）

| 模式 | 说明 |
|------|------|
| overwrite | 覆盖整个文档 |
| append | 追加到文档末尾 |
| replace_range | 定位替换 |
| replace_all | 全文替换 |
| insert_before | 插入到指定内容之前 |
| insert_after | 插入到指定内容之后 |
| delete_range | 删除指定范围 |

### 定位方式

**selection_with_ellipsis**：`开头内容...结尾内容` 匹配范围

**selection_by_title**：`## 章节标题` 定位整个章节

### 示例：创建文档

```json
{
  "action": "create",
  "title": "项目文档",
  "markdown": "## 概述\n\n这是一个示例文档。",
  "folder_token": "fldcnxxx"
}
```

---

## 📊 多维表格模块

### 快速索引

| 用户意图 | 工具 | action | 必填参数 |
|---------|------|--------|---------|
| 创建多维表格 | feishu_bitable_app | create | name |
| 创建数据表 | feishu_bitable_app_table | create | app_token, name |
| 查记录 | feishu_bitable_app_table_record | list | app_token, table_id |
| 新增记录 | feishu_bitable_app_table_record | create | app_token, table_id, fields |
| 批量导入 | feishu_bitable_app_table_record | batch_create | app_token, table_id, records |

### 字段类型与值格式

| type | 字段类型 | 正确格式 | 常见错误 |
|------|---------|---------|---------|
| 1 | 文本 | "字符串" | - |
| 2 | 数字 | 123 | - |
| 3 | 单选 | "选项名" | 传数组 |
| 4 | 多选 | ["选项1", "选项2"] | 传字符串 |
| 5 | 日期 | 1674206443000（毫秒） | 传秒时间戳 |
| 7 | 复选框 | true/false | - |
| 11 | 人员 | [{id: "ou_xxx"}] | 传字符串 |
| 15 | 超链接 | {link: "...", text: "..."} | 只传 URL |
| 17 | 附件 | [{file_token: "..."}] | 传外部 URL |

### 核心约束

- **先查字段**：写入前先调用 list 获取字段 type
- **日期是毫秒**：必须用毫秒时间戳，不是秒
- **人员用 open_id**：格式 [{id: "ou_xxx"}]
- **批量上限**：单次 ≤ 500 条
- **空行坑**：新建表可能有空记录，插入前建议删除

---

## ✅ 任务管理模块

### 快速索引

| 用户意图 | 工具 | action | 必填参数 |
|---------|------|--------|---------|
| 新建待办 | feishu_task_task | create | summary |
| 查任务 | feishu_task_task | list | - |
| 完成任务 | feishu_task_task | patch | task_guid, completed_at |
| 创建清单 | feishu_task_tasklist | create | name |

### 核心约束

- **current_user_id**：强烈建议传 SenderId，确保创建者能编辑任务
- **时间格式**：ISO 8601 带时区
- **完成任务**：completed_at = "2026-03-24T15:00:00+08:00"
- **反完成**：completed_at = "0"

---

## 💬 消息读取模块

### 快速索引

| 用户意图 | 工具 | 必填参数 |
|---------|------|---------|
| 获取历史消息 | feishu_im_user_get_messages | chat_id 或 open_id |
| 获取话题回复 | feishu_im_user_get_thread_messages | thread_id |
| 搜索消息 | feishu_im_user_search_messages | 至少一个过滤条件 |
| 下载图片/文件 | feishu_im_user_fetch_resource | message_id, file_key, type |

### 核心约束

- **chat_id 与 open_id 互斥**：二选一
- **relative_time**：支持 today, yesterday, this_week 等
- **话题消息**：获取历史消息时如发现 thread_id，建议展开获取上下文
- **搜索**：支持按关键词、发送者、时间、消息类型过滤

---

## 🔍 组织架构模块

### 快速索引

| 用户意图 | 工具 | 必填参数 |
|---------|------|---------|
| 搜索用户 | feishu_search_user | query |
| 获取用户信息 | feishu_get_user | user_id |
| 搜索群组 | feishu_chat | query |
| 获取群成员 | feishu_chat_members | chat_id |

---

## 🔧 知识库模块

### 快速索引

| 用户意图 | 工具 | 必填参数 |
|---------|------|---------|
| 搜索文档/Wiki | feishu_search_doc_wiki | query |

### 核心约束

- **搜索范围**：支持同时搜索云空间文档和知识库 Wiki
- **过滤条件**：可按文档类型、创建者、时间筛选
- **返回格式**：标题和摘要带高亮标签

---

## 📚 附录

### 飞书 OAPI 常用限制

| 资源 | 限制 |
|------|------|
| 日程参会人 | 最多 3000 人 |
| 单次添加用户 | 最多 1000 人 |
| 单次添加会议室 | 最多 100 个 |
| 多维表格批量 | 单次 ≤ 500 条 |
| 消息分页 | 每页 ≤ 50 条 |

### 相关技能

如需更详细的使用说明，可参考各独立技能文档：
- feishu-calendar - 日历日程详解
- feishu-bitable - 多维表格深度指南
- feishu-task - 任务管理详解
- feishu-im-read - 消息读取指南
- feishu-create-doc / feishu-fetch-doc / feishu-update-doc - 文档管理系列
