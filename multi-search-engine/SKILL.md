---
name: multi-search-engine
description: 多搜索引擎聚合搜索技能，集成16个国内外搜索引擎（百度、必应、Google、DuckDuckGo、搜狗、微信搜索等），零配置无需API Key，自动根据查询语言选择引擎，支持高级搜索语法。当用户需要搜索信息、查询资料、对比多个搜索结果、或需要使用特定搜索引擎时触发。
---

# Multi Search Engine - 多搜索引擎聚合

## 概述

本技能提供统一的多搜索引擎搜索接口，覆盖7个国内引擎和9个国际引擎，零配置、无需API Key。根据查询语言自动选择最合适的搜索引擎组合，并支持失败重试和高级搜索语法。

## 搜索引擎列表

### 国内引擎（7个）
| 引擎 | 基础URL | 特点 |
|------|---------|------|
| 百度 | `https://www.baidu.com/s?wd={query}` | 中文信息最全，适合中文日常搜索 |
| 必应中国 | `https://cn.bing.com/search?q={query}&ensearch=0` | 中英混合结果，质量较高 |
| 必应国际 | `https://cn.bing.com/search?q={query}&ensearch=1` | 国际结果，可访问 |
| 360搜索 | `https://www.so.com/s?q={query}` | 国内备用，安全相关结果好 |
| 搜狗 | `https://www.sogou.com/web?query={query}` | 微信公众号内容独家 |
| 微信搜索 | `https://weixin.sogou.com/weixin?type=2&query={query}` | 微信公众号文章 |
| 神马 | `https://yz.m.sm.cn/s?q={query}` | 移动端优化结果 |

### 国际引擎（9个）
| 引擎 | 基础URL | 特点 |
|------|---------|------|
| Google | `https://www.google.com/search?q={query}` | 全球最全面，需网络支持 |
| Google HK | `https://www.google.com.hk/search?q={query}` | 香港节点 |
| DuckDuckGo | `https://duckduckgo.com/?q={query}` | 隐私优先，无追踪 |
| Yahoo | `https://search.yahoo.com/search?p={query}` | 英文结果补充 |
| Startpage | `https://www.startpage.com/do/search?q={query}` | Google结果+隐私保护 |
| Brave | `https://search.brave.com/search?q={query}` | 新兴隐私引擎 |
| Ecosia | `https://www.ecosia.org/search?q={query}` | 环保搜索引擎 |
| Qwant | `https://www.qwant.com/?q={query}` | 欧洲隐私引擎 |
| WolframAlpha | `https://www.wolframalpha.com/input?i={query}` | 计算/科学/数据查询 |

## 自动语言检测规则

- 查询中包含中文字符比例 > 30% → 优先国内引擎（百度、必应CN、搜狗）
- 查询纯英文或中文比例 < 10% → 优先国际引擎（Google、DuckDuckGo、Brave）
- 查询包含数学/科学计算关键词 → 自动加入WolframAlpha
- 查询包含微信/公众号关键词 → 自动加入微信搜索
- 用户明确指定引擎时 → 使用指定引擎

## 工作流程

### 标准搜索流程
1. **分析查询**：检测语言、意图、是否需要特定引擎
2. **选择引擎**：根据规则选择2-4个最合适的引擎
3. **构造URL**：将查询编码为各引擎的搜索URL
4. **获取结果**：使用WebFetch或WebSearch依次请求，设置超时（每个引擎8秒）
5. **失败重试**：主引擎失败时自动切换到备用引擎
6. **整合呈现**：合并去重，标注来源引擎

### 引擎选择策略
```
中文日常查询 → 百度(主) + 必应CN(辅) + 搜狗(补)
中文技术查询 → 必应CN(主) + 百度(辅) + 微信搜索(补)
英文通用查询 → DuckDuckGo(主) + Brave(辅) + Startpage(补)
英文技术查询 → Google(主) + DuckDuckGo(辅) + Brave(补)
隐私敏感查询 → DuckDuckGo(主) + Startpage(辅) + Qwant(补)
学术/计算查询 → Google(主) + WolframAlpha(辅)
微信公众号 → 微信搜索(主) + 搜狗(辅)
```

## 高级搜索语法

本技能支持传递高级搜索语法到各引擎。详细用法见：
- [国内搜索语法指南](references/advanced-search.md)
- [国际搜索语法指南](references/international-search.md)

### 通用语法（所有引擎支持）
| 语法 | 功能 | 示例 |
|------|------|------|
| `site:域名` | 限定网站 | `site:github.com 大模型` |
| `filetype:类型` | 限定文件类型 | `filetype:pdf 年报` |
| `"精确短语"` | 精确匹配 | `"人工智能伦理"` |
| `-关键词` | 排除词 | `苹果 -手机 -水果` |
| `OR` | 或条件 | `Python OR Java` |
| `intitle:词` | 标题包含 | `intitle:教程 React` |
| `inurl:词` | URL包含 | `inurl:blog AI` |

### 时间过滤
| 语法 | 功能 |
|------|------|
| `tbs=qdr:d` | 过去24小时（Google） |
| `tbs=qdr:w` | 过去一周 |
| `tbs=qdr:m` | 过去一月 |
| `tbs=qdr:y` | 过去一年 |
| `filters=ex1:"ez5_XXXXX"` | 必应时间过滤 |

## 使用方式

### 基本搜索
当用户说"搜索XXX"、"查一下XXX"、"XXX是什么"时：
1. 自动检测语言和意图
2. 选择2-3个引擎搜索
3. 整合结果返回

### 指定引擎搜索
当用户说"用百度搜XXX"、"Google一下XXX"时：
1. 使用用户指定的引擎
2. 搭配1个备用引擎
3. 返回结果

### 高级搜索
当用户需要精确搜索时：
1. 引导用户使用高级语法
2. 构造精确查询
3. 多引擎交叉验证

## 搜索实现方式

本技能通过以下方式执行搜索：
1. 使用内置WebSearch工具进行搜索
2. 使用WebFetch工具获取具体搜索页面内容
3. 构造搜索引擎URL直接访问
4. 解析返回的HTML提取搜索结果

### User-Agent设置
```
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

## 失败重试机制

1. **第一次失败**：等待2秒后重试同一引擎
2. **第二次失败**：切换到同类型备用引擎
3. **全部失败**：告知用户当前引擎不可用，建议切换网络或换词

失败判定标准：
- HTTP状态码非200
- 响应时间超过8秒
- 返回内容为验证码页面
- 结果数为0且查询非冷门

## 结果呈现格式

搜索结果统一格式：
```
### [标题](链接)
**来源**：[引擎名] | **摘要**：内容摘要...
---
```

多引擎结果合并时：
- 去重（按URL）
- 按相关性和引擎权重排序（百度中文结果权重高，Google技术结果权重高）
- 标注信息矛盾的结果
- 区分官方结果和第三方结果

## 注意事项

1. 搜索结果仅供参考，关键信息需交叉验证
2. 部分国际引擎在特定网络环境下可能不可用，自动降级
3. 控制请求频率，避免触发反爬机制
4. 不搜索违法违规内容
