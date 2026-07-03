# TRAE 团队全局技能库（Team Global Skills）

本仓库用于**团队统一管理 TRAE 全局技能（Skill）**。所有成员将此仓库克隆到 TRAE 全局技能目录，即可共享同一套技能，实现"一处维护、全员同步"。

> 全局技能目录：
> - macOS / Linux：`~/.trae-cn/skills`
> - Windows：`%userprofile%/.trae-cn/skills`

---

## 一、首次使用（团队成员）

> ⚠️ 如果你的 `~/.trae-cn/skills` 目录里已有技能，请先备份再操作，避免覆盖。

### macOS / Linux

```bash
# 1. 备份现有技能目录（如果有）
mv ~/.trae-cn/skills ~/.trae-cn/skills_backup_$(date +%Y%m%d)

# 2. 克隆团队技能仓库到全局技能目录
git clone <团队仓库地址> ~/.trae-cn/skills

# 3. 重启 TRAE 客户端，即可在「设置 → 技能与命令 → 全局」看到统一技能
```

### Windows（PowerShell）

```powershell
# 1. 备份现有技能目录（如果有）
Rename-Item "$env:USERPROFILE\.trae-cn\skills" "skills_backup"

# 2. 克隆团队技能仓库
git clone <团队仓库地址> "$env:USERPROFILE\.trae-cn\skills"

# 3. 重启 TRAE 客户端
```

---

## 二、日常同步（拉取最新技能）

当管理员更新了技能后，成员执行：

```bash
cd ~/.trae-cn/skills
git pull
```

拉取后**重启 TRAE 客户端**使技能生效。

---

## 三、更新 / 新增技能（管理员或贡献者）

1. 在 `~/.trae-cn/skills/` 下新增或修改技能目录（每个技能一个文件夹，内含 `SKILL.md`）。
2. 提交并推送：

```bash
cd ~/.trae-cn/skills
git add .
git commit -m "feat: 新增/更新 XXX 技能"
git push
```

3. 通知团队成员执行 `git pull` 同步。

---

## 四、技能目录结构规范

每个技能是一个独立文件夹，必须包含 `SKILL.md`：

```
skill-name/
├── SKILL.md          # （必须）技能核心指令，含 YAML 头部 name/description
├── scripts/          # （可选）可执行脚本
├── references/       # （可选）参考文档
└── templates/        # （可选）可复用模板
```

`SKILL.md` 头部格式：

```markdown
---
name: 技能名称
description: 简要描述这个技能的功能和使用场景（决定 AI 是否自动触发）
---

# 技能名称
## 描述 / 使用场景 / 指令 / 示例
```

---

## 五、注意事项

- **不入库的内容**：`.DS_Store`、`__pycache__`、`node_modules`、`*.pyc`、`skill-config.json`（各成员本地技能开关状态）等，已在 `.gitignore` 中忽略。
- **技能开关是本地状态**：启用/禁用某个技能是各成员本地行为，不随仓库同步。
- **命名唯一**：技能文件夹名（即技能名）需保持唯一，避免冲突。
- **本地 vs 云端**：全局技能对本地任务生效；云端任务的技能生效范围请参考 TRAE 官方文档。

---

## 六、参考

- TRAE 技能官方文档：https://docs.trae.cn/ide/skills
- 写好 Skill 的最佳实践：https://docs.trae.cn/ide/best-practice-for-how-to-write-a-good-skill
