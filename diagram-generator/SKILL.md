---
name: diagram-generator
description: 图表生成器技能，用自然语言描述生成流程图、架构图、思维导图、时序图、甘特图、ER图等。支持Mermaid（流程图/序列图/类图/状态图/甘特图/饼图/Git图/ER图）、Graphviz DOT、PlantUML三种格式，自动选择最合适的图表类型，生成可编辑源码并说明渲染方式。当用户需要画图、做流程图、画架构图、画思维导图、画时序图、可视化流程或关系时触发。
---

# Diagram Generator - 图表生成器

## 概述

本技能将自然语言描述转化为专业图表，支持Mermaid、Graphviz DOT、PlantUML三种主流图表描述语言。根据用户需求自动选择最合适的图表类型，生成高质量可编辑的图表源码，并提供渲染和编辑指导。

## 支持的图表类型

| 图表类型 | 推荐格式 | 适用场景 |
|----------|----------|----------|
| 流程图(Flowchart) | Mermaid | 业务流程、工作流、决策树 |
| 序列图(Sequence) | Mermaid/PlantUML | 接口调用、消息传递、交互流程 |
| 类图(Class) | Mermaid/PlantUML | 面向对象设计、数据模型 |
| 状态图(State) | Mermaid | 状态机、生命周期 |
| 甘特图(Gantt) | Mermaid | 项目排期、任务计划 |
| 饼图(Pie) | Mermaid | 占比统计、数据分布 |
| Git图(Git) | Mermaid | Git分支、提交历史 |
| ER图(ER) | Mermaid/PlantUML | 数据库设计、实体关系 |
| 思维导图(Mindmap) | Mermaid | 头脑风暴、知识整理 |
| 架构图 | Mermaid/Graphviz | 系统架构、部署拓扑 |
| 组织结构图 | Mermaid/Graphviz | 组织架构、汇报关系 |
| 网络图 | Graphviz | 网络拓扑、依赖关系 |
| 用户旅程图 | Mermaid | 用户体验、产品流程 |
| 需求图 | PlantUML | 需求追踪、系统建模 |

## 图表类型选择指南

### 如何选择图表类型？

1. **描述流程/步骤** → 流程图（Flowchart）
   - 关键词：流程、步骤、如果...那么...、分支、循环、审批流
   
2. **描述交互/消息传递** → 序列图（Sequence Diagram）
   - 关键词：调用、请求响应、消息、通知、API、前后端交互
   
3. **描述时间计划** → 甘特图（Gantt）
   - 关键词：排期、里程碑、工期、阶段、deadline
   
4. **描述数据/对象关系** → ER图（ER Diagram）
   - 关键词：表关系、一对多、外键、实体、数据库
   
5. **描述层次/分类** → 思维导图（Mindmap）
   - 关键词：分类、脑图、梳理、整理、知识点
   
6. **描述状态变化** → 状态图（State Diagram）
   - 关键词：状态、流转、从...到...、生命周期
   
7. **描述系统结构** → 架构图（用Mermaid flowchart或Graphviz）
   - 关键词：架构、组件、模块、部署、分层
   
8. **描述占比/比例** → 饼图（Pie Chart）
   - 关键词：占比、比例、百分比、分布
   
9. **描述类/对象设计** → 类图（Class Diagram）
   - 关键词：类、继承、接口、属性、方法
   
10. **复杂网络/依赖图** → Graphviz DOT
    - 关键词：复杂依赖、网络拓扑、自动布局

## 工作流程

### 标准流程
1. **理解需求**：分析用户描述，识别核心元素（节点/角色/步骤）和关系
2. **选择类型**：根据上述指南选择最合适的图表类型
3. **规划结构**：确定节点命名、关系方向、分组/子图
4. **生成代码**：编写Mermaid/Graphviz/PlantUML源码
5. **添加注释**：在代码中添加说明注释
6. **渲染指导**：告知用户如何渲染（在线工具/IDE插件/代码平台）
7. **提供说明**：解释图表结构，说明关键节点和关系

### 输出格式
生成图表时统一使用以下格式：

```
### 图表说明
（简要说明图表内容、关键节点）

### 图表源码
```mermaid
（图表代码）
```

### 渲染方式
- **在线渲染**：https://mermaid.live （粘贴Mermaid代码即可预览）
- **VS Code**：安装 "Markdown Preview Mermaid Support" 插件
- **GitHub/GitLab**：直接在Markdown中支持Mermaid渲染
- **PlantUML在线**：https://www.plantuml.com/plantuml/uml
- **Graphviz在线**：https://dreampuf.github.io/GraphvizOnline/
```

## Mermaid 语法速查

详见 [Mermaid速查表](references/mermaid-cheatsheet.md)。

## 图表示例库

详见 [各类型图表示例](references/chart-examples.md)。

## 最佳实践

### 节点命名规范
- 使用简短有意义的名称（2-6个字符或1-3个词最佳）
- 中文节点加引号：`A["用户登录"]`
- 避免节点名称过长，详细说明用注释
- 保持命名风格一致（全中文或全英文缩写）

### 流程图布局原则
- **方向选择**：
  - 从上到下（TD/TB）：适合流程、时间线
  - 从左到右（LR）：适合架构、层次
- **不要让线交叉**：通过调整节点顺序避免
- **使用子图（subgraph）**分组相关节点
- **决策节点**用菱形，起止节点用圆角矩形

### 序列图设计原则
- 参与者从左到右排列（调用者→被调用者）
- 标注关键消息的返回值或状态码
- 用`alt/opt/loop`表示条件和循环
- 激活框（activate/deactivate）表示处理时间

### 颜色和样式建议
- 默认样式即可，不要过度美化
- 关键节点可用样式强调：`style A fill:#f9f,stroke:#333,stroke-width:2px`
- 子图可以设背景色区分模块
- 配色不超过3-4种

### 复杂度控制
- 单张图节点不超过15-20个
- 超过则拆分多张图或使用子图分组
- 关系连线尽量清晰，避免密集交叉

## 渲染方式汇总

### Mermaid 渲染
| 平台 | 方式 |
|------|------|
| 在线编辑器 | https://mermaid.live |
| VS Code | Markdown Preview Mermaid Support 插件 |
| GitHub/GitLab | 原生支持 .md/.mmd 文件 |
| Notion | 支持 Mermaid 代码块 |
| Obsidian | 原生支持 Mermaid |
| 语雀 | 支持 Mermaid 画板 |
| 飞书文档 | 支持 UML 图（Mermaid/PlantUML） |
| 命令行 | `npm install -g @mermaid-js/mermaid-cli` → `mmdc -i input.mmd -o output.png` |

### PlantUML 渲染
| 平台 | 方式 |
|------|------|
| 在线编辑器 | https://www.plantuml.com/plantuml/uml |
| VS Code | PlantUML 插件 |
| 命令行 | 需要Java + plantuml.jar |

### Graphviz 渲染
| 平台 | 方式 |
|------|------|
| 在线编辑器 | https://dreampuf.github.io/GraphvizOnline/ |
| VS Code | Graphviz Preview 插件 |
| 命令行 | `brew install graphviz` → `dot -Tpng input.dot -o output.png` |

## 注意事项

1. 生成图表前先明确用户要表达什么关系（流程/交互/结构/时间）
2. 节点名称要简洁，长文字用换行`<br/>`或缩短
3. 方向选择要符合阅读习惯（中文从上到下、从左到右）
4. 代码要规范缩进，方便用户后续编辑
5. 复杂图表建议拆分成多个子图
6. 生成后检查语法是否正确（特别是括号和引号配对）
