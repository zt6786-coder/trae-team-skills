# 国际搜索引擎高级搜索指南

## Google 搜索高级语法

### 基础运算符
| 语法 | 说明 | 示例 |
|------|------|------|
| `"exact phrase"` | 精确短语匹配 | `"machine learning bias"` |
| `-word` | 排除词汇 | `python -snake` |
| `OR` | 或运算（必须大写） | `React OR Vue` |
| `*` | 通配符 | `"best * for developers"` |
| `()` | 分组 | `(React OR Vue) tutorial` |
| `..` | 数字范围 | `laptop $500..$1000` |

### 高级搜索运算符
| 语法 | 说明 | 示例 |
|------|------|------|
| `site:domain.com` | 限定网站 | `site:github.com issues` |
| `filetype:pdf` | 文件类型 | `filetype:pdf research paper` |
| `intitle:text` | 标题包含 | `intitle:"best practices" API` |
| `allintitle:a b c` | 标题包含所有词 | `allintitle:Python performance tips` |
| `inurl:text` | URL包含 | `inurl:blog remote work` |
| `allinurl:a b c` | URL包含所有词 | |
| `intext:text` | 正文包含 | `intext:"deprecated" API` |
| `related:domain.com` | 相关网站 | `related:github.com` |
| `cache:url` | 查看缓存版本 | `cache:example.com` |
| `define:word` | 词义定义 | `define:serendipity` |
| `weather:city` | 天气预报 | `weather:Beijing` |
| `stocks:symbol` | 股票查询 | `stocks:AAPL` |
| `map:location` | 地图搜索 | `map:Shanghai` |
| `movie:name` | 电影信息 | `movie:Inception` |

### Google 时间过滤（URL参数）
```
过去1小时:  &tbs=qdr:h
过去24小时: &tbs=qdr:d
过去一周:   &tbs=qdr:w
过去一月:   &tbs=qdr:m
过去一年:   &tbs=qdr:y
自定义范围: &tbs=cdr:1,cd_min:1/1/2024,cd_max:12/31/2024
```

### Google 搜索技巧
1. **学术搜索**：使用 `scholar.google.com` 搜索学术论文
2. **开发文档**：`site:developer.mozilla.org` 或 `site:stackoverflow.com`
3. **找开源项目**：`site:github.com` + 技术关键词
4. **排除低质量内容**：`-pinterest -quora -medium`（按需）
5. **找免费资源**：`"free" OR "open source" filetype:pdf`

## DuckDuckGo 高级语法

### 基础语法
DuckDuckGo支持大部分Google通用语法：`site:`、`filetype:`、`""`、`-`、`OR`。

### DuckDuckGo 特有功能
| 语法 | 说明 |
|------|------|
| `!bang` | 快速跳转到其他网站搜索（见下方） |
| `weather [location]` | 天气 |
| `define [word]` | 定义 |
| `stopwatch` | 秒表 |
| `timer [time]` | 计时器 |

### DuckDuckGo !Bang 快捷指令（常用）
| Bang | 功能 | 示例 |
|------|------|------|
| `!g` | Google搜索 | `!g python tutorial` |
| `!gh` | GitHub搜索 | `!gh react hooks` |
| `!so` | Stack Overflow | `!so javascript error` |
| `!wiki` | Wikipedia | `!wiki artificial intelligence` |
| `!npm` | NPM包搜索 | `!npm lodash` |
| `!mdn` | MDN文档 | `!mdn fetch API` |
| `!yt` | YouTube搜索 | `!yt piano tutorial` |
| `!a` | Amazon搜索 | `!a keyboard` |
| `!w` | WolframAlpha计算 | `!w integral of x^2` |
| `!zhihu` | 知乎搜索 | `!zhihu 大模型` |
| `!ba` | 百度搜索 | `!ba 旅游攻略` |

## Brave Search 语法

支持通用语法：`site:`、`filetype:`、`""`、`-`、`OR`。

Brave特色：
- 独立索引，不依赖Google/Bing
- 内置AI摘要（Search Summarizer）
- 支持"Discussions"标签，论坛/Reddit讨论内容突出
- 默认无广告（或可选广告）

## Startpage 语法

Startpage使用Google的搜索结果但不追踪用户，语法与Google基本相同。

特点：
- 获得Google质量的结果但保护隐私
- 支持"Anonymous View"匿名浏览网页
- 支持通用搜索语法

## Ecosia 语法

Ecosia是环保搜索引擎（搜索收入用于种树），使用Bing的搜索结果。
支持基础语法：`site:`、`filetype:`、`""`、`-`。

## Qwant 语法

Qwant是欧洲隐私搜索引擎，拥有自己的索引。
支持通用语法，特色：
- 严格的隐私保护（符合GDPR）
- 音乐/图片/视频搜索集成
- 分栏显示（网页/新闻/社交）

## WolframAlpha 使用指南

WolframAlpha是计算知识引擎，不是传统搜索引擎，它直接计算答案。

### 适用场景
| 场景 | 示例查询 |
|------|----------|
| 数学计算 | `integrate x^2 sin(x) dx` |
| 单位换算 | `100 km in miles` |
| 日期计算 | `days until 2025-01-01` |
| 统计数据 | `GDP of China 2023` |
| 化学 | `molecular weight of caffeine` |
| 物理 | `speed of light in m/s` |
| 营养信息 | `calories in 1 apple` |
| 天气数据 | `weather Beijing last week` |

### 不适用场景
- 一般网页搜索
- 新闻事件
- 主观内容

## 国际搜索引擎对比

| 需求场景 | 推荐引擎 | 原因 |
|----------|----------|------|
| 通用英文搜索 | Google | 结果最全面 |
| 隐私优先搜索 | DuckDuckGo / Brave | 不追踪用户 |
| 技术/编程搜索 | Google + Stack Overflow | 开发资源最全 |
| 学术/论文 | Google Scholar | 学术索引最全 |
| 数学/计算 | WolframAlpha | 计算引擎 |
| 欧洲隐私合规 | Qwant / Startpage | GDPR合规 |
| 环保搜索 | Ecosia | 搜索即种树 |
| 免Google依赖 | Brave / DuckDuckGo | 独立索引 |

## 搜索效率提升技巧

### 1. 使用引号精确匹配
搜索特定错误信息、代码片段、名言时，用引号包裹可大幅提高准确率。

### 2. 善用site:限定域名
- 技术问题：`site:stackoverflow.com` 或 `site:github.com`
- 官方文档：`site:*.gov` 或 `site:*.edu`
- 优质教程：`site:medium.com` 或 `site:dev.to`

### 3. 排除低质量结果
```
- pinterest.com -quora.com -expert.com -spam-site.com
```

### 4. 时间过滤获取最新信息
搜索技术文档、新闻事件时，务必使用时间过滤，避免过时信息。

### 5. 多引擎交叉验证
重要信息至少在两个引擎搜索验证，特别是：
- 医疗健康信息
- 法律相关内容
- 投资决策依据
- 新闻事实核查
