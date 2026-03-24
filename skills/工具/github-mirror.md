---
metadata:
  name: "github-mirror"
  version: "1.0.0"
  description: "GitHub 镜像加速下载工具，自动将 GitHub URL 转换为加速链接，支持多种镜像站"
  category: "工具"
  tags: ["github", "镜像", "加速", "代理", "下载", "git"]
  author: "GiaoHYH"
---

# github-mirror GitHub 镜像加速

当需要从 GitHub 下载文件、克隆仓库时，自动使用镜像加速，解决国内访问 GitHub 慢或失败的问题。

## Overview

本技能提供 GitHub 镜像加速功能，自动将 GitHub URL 转换为加速链接下载。

## 支持的镜像站

| 镜像站 | 地址 | 特点 |
|--------|------|------|
| ghproxy | `https://ghproxy.com/` | 稳定，推荐 |
| mirror.ghproxy | `https://mirror.ghproxy.com/` | 备选 |
| gh.api | `https://gh.api.99988866.xyz/` | 备选 |

## Steps

### 1. 自动转换

当我帮你下载 GitHub 文件时，会自动使用镜像加速：

```
# 原地址
https://github.com/user/repo/archive/refs/heads/main.tar.gz

# 自动转换为
https://ghproxy.com/https://github.com/user/repo/archive/refs/heads/main.tar.gz
```

### 2. 手动使用

```bash
# 使用 ghproxy 加速下载
curl -L https://ghproxy.com/https://github.com/user/repo/archive/main.tar.gz -o repo.tar.gz

# 加速克隆仓库
git clone https://ghproxy.com/https://github.com/user/repo.git
```

## 加速规则

### 自动识别

- `github.com` → 添加 `ghproxy.com/` 前缀
- `raw.githubusercontent.com` → 添加镜像前缀
- `gist.githubusercontent.com` → 添加镜像前缀

### Fallback 机制

如果第一个镜像失败，自动尝试下一个镜像

## Expected Output

- 返回加速后的下载链接
- 优先使用稳定快速的镜像站

## Example

**下载 Release 文件**：
```
原: https://github.com/vercel/next.js/releases/download/v14.0.0/next.js.tar.gz
加: https://ghproxy.com/https://github.com/vercel/next.js/releases/download/v14.0.0/next.js.tar.gz
```

**克隆仓库**：
```
原: https://github.com/openclaw/openclaw.git
加: https://ghproxy.com/https://github.com/openclaw/openclaw.git
```

## 备选方案

如果镜像不可用，可使用：
- **JSDelivr CDN**: `https://cdn.jsdelivr.net/gh/user/repo@tag/file`
- **Statically**: `https://cdn.statically.io/gh/user/repo/tag/file`
- **GitClone**: `https://gitclone.com/github.com/user/repo`

## Troubleshooting

### 镜像站不可用
会自动切换到备选镜像站

### 大文件下载
建议直接使用代理服务

### 私有仓库
私有仓库无法通过镜像加速

## Related Skills
- `github` - GitHub CLI 操作
- `proxy-auto` - 代理自动配置
