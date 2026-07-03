# Mermaid 语法速查表

## 1. 流程图 (Flowchart)

### 方向声明
```
flowchart TD    # 从上到下 (Top to Down) —— 默认
flowchart TB    # 从上到下 (Top to Bottom)
flowchart BT    # 从下到上 (Bottom to Top)
flowchart LR    # 从左到右 (Left to Right)
flowchart RL    # 从右到左 (Right to Left)
```

### 节点形状
```mermaid
flowchart LR
    A[矩形/默认] --> B(圆角矩形)
    B --> C([体育场形])
    C --> D[[子程序形]]
    D --> E[(圆柱形/数据库)]
    E --> F((圆形))
    F --> G>不对称形]
    G --> H{菱形/判断}
    H --> I{{六边形}}
    I --> J[/平行四边形/]
    J --> K[\反向平行四边形\]
    K --> L[/梯形\]
```

### 连线样式
```mermaid
flowchart LR
    A --> B[实线箭头]
    A --- C[实线无箭头]
    A -- 文字 --> D[带文字实线]
    A -.-> E[虚线箭头]
    A -. 文字 .-> F[带文字虚线]
    A ==> G[粗线箭头]
    A == 文字 ==> H[带文字粗线]
    A --o I[圆形箭头]
    A --x J[叉形箭头]
```

### 子图
```mermaid
flowchart TD
    subgraph 子图标题
        A --> B
    end
    subgraph 另一个子图
        C --> D
    end
    B --> C
```

### 样式
```mermaid
flowchart LR
    A[红色节点] --> B[绿色节点]
    style A fill:#f99,stroke:#f00,stroke-width:2px
    style B fill:#9f9,stroke:#090,stroke-width:2px
    linkStyle 0 stroke:#00f,stroke-width:2px,color:blue
```

## 2. 序列图 (Sequence Diagram)

### 基本语法
```mermaid
sequenceDiagram
    participant 用户
    participant 前端
    participant 后端
    participant 数据库

    用户->>前端: 点击登录
    前端->>后端: POST /api/login
    后端->>数据库: 查询用户
    数据库-->>后端: 返回用户数据
    后端-->>前端: 返回Token
    前端-->>用户: 登录成功
```

### 消息类型
```
->>     实线箭头（常用，请求）
-->>    虚线箭头（响应/返回）
-)      异步箭头（无等待）
--x     错误/终止箭头
```

### 控制结构
```mermaid
sequenceDiagram
    participant A as 客户端
    participant B as 服务器

    %% 条件判断
    alt 登录成功
        A->>B: 请求数据
        B-->>A: 返回数据
    else 登录失败
        B-->>A: 401 Unauthorized
    end

    %% 可选
    opt 首次访问
        A->>B: 获取Token
    end

    %% 循环
    loop 每30秒
        A->>B: 心跳检测
    end
```

### 激活与注释
```mermaid
sequenceDiagram
    participant A
    participant B
    A->>B: 请求
    activate B
    B->>B: 处理中
    Note over B: 耗时操作
    B-->>A: 响应
    deactivate B
    Note right of A: 注释在右侧
    Note left of B: 注释在左侧
```

## 3. 类图 (Class Diagram)

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +eat() void
        +sleep() void
    }
    class Dog {
        +String breed
        +bark() void
    }
    class Cat {
        +String color
        +meow() void
    }
    Animal <|-- Dog
    Animal <|-- Cat
```

### 关系符号
| 符号 | 关系 | 含义 |
|------|------|------|
| `<\|--` | 继承 | 泛化(Generalization) |
| `*--` | 组合 | 强拥有(Composition) |
| `o--` | 聚合 | 弱拥有(Aggregation) |
| `-->` | 关联 | 引用(Association) |
| `..>` | 依赖 | 使用(Dependency) |
| `<\|..` | 实现 | 接口实现(Realization) |

### 可见性标记
```
+   Public
-   Private
#   Protected
~   Package/Internal
```

## 4. 状态图 (State Diagram)

```mermaid
stateDiagram-v2
    [*] --> 待支付
    待支付 --> 已支付: 支付成功
    待支付 --> 已取消: 用户取消
    已支付 --> 已发货: 商家发货
    已发货 --> 已签收: 快递送达
    已签收 --> [*]
    已支付 --> 退款中: 申请退款
    退款中 --> 已退款: 退款成功
    退款中 --> 已支付: 退款失败
```

### 状态语法
```mermaid
stateDiagram-v2
    state "复合状态" as CS {
        [*] --> 子状态1
        子状态1 --> 子状态2
    }
    [*] --> CS
    CS --> [*]

    %% 分叉/汇合
    state 分叉状态 <<fork>>
    state 汇合状态 <<join>>
```

## 5. 甘特图 (Gantt)

```mermaid
gantt
    title 项目开发计划
    dateFormat  YYYY-MM-DD
    section 需求阶段
    需求分析       :a1, 2024-01-01, 7d
    需求评审       :after a1, 3d
    section 开发阶段
    前端开发       :2024-01-11, 14d
    后端开发       :2024-01-11, 21d
    联调测试       :2024-02-01, 7d
    section 上线
    部署上线       :milestone, 2024-02-08, 1d
```

### 甘特图语法
```
title 标题
dateFormat YYYY-MM-DD    # 日期格式
section 分组名
任务名    :[id,] [start,] duration|end
任务名    :crit, [id,] ...    # 关键任务（红色高亮）
任务名    :done, [id,] ...    # 已完成
任务名    :active, [id,] ...  # 进行中
任务名    :milestone, [id,] ...  # 里程碑
```

## 6. 饼图 (Pie Chart)

```mermaid
pie showData
    title 用户设备占比
    "iOS" : 45
    "Android" : 40
    "PC" : 12
    "其他" : 3
```

## 7. ER图 (Entity Relationship)

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER }|..|{ DELIVERY-ADDRESS : uses
    ORDER {
        int id PK
        int customer_id FK
        date order_date
        decimal total
    }
    CUSTOMER {
        int id PK
        string name
        string email
    }
```

### 关系符号
| 符号 | 含义 |
|------|------|
| `\|o` | 零或一个 |
| `\|\|` | 恰好一个 |
| `}o` | 零或多个 |
| `}\|` | 一个或多个 |

## 8. Git图 (Git Graph)

```mermaid
gitGraph
    commit
    branch develop
    checkout develop
    commit
    commit
    checkout main
    merge develop
    commit
    branch hotfix
    checkout hotfix
    commit
    checkout main
    merge hotfix
```

## 9. 思维导图 (Mindmap)

```mermaid
mindmap
  root((技能系统))
    内置技能
      WebSearch
      WebFetch
      Read/Write
    社区技能
      搜索技能
      写作技能
      图表技能
    自定义技能
      个人偏好
      工作流
```

## 10. 用户旅程图 (User Journey)

```mermaid
journey
    title 我的电商购物体验
    section 浏览商品
      打开APP: 5: 用户
      搜索商品: 4: 用户
      查看详情: 3: 用户
    section 下单
      加入购物车: 5: 用户
      填写地址: 2: 用户, APP
      支付: 4: 用户, 支付系统
    section 售后
      等待发货: 3: 用户
      收货: 5: 用户
      评价: 4: 用户
```

## 11. 常用样式技巧

### 节点内换行
```
A[第一行<br/>第二行]
```

### Markdown文字（加粗/斜体）
```
A["**加粗** 和 *斜体*"]
```

### 中文节点注意事项
- 中文节点名建议加双引号：`A["用户登录模块"]`
- 避免在节点名中使用特殊字符：`( ) [ ] { } "`

### 方向选择建议
- 流程图、时间线 → TD（从上到下）
- 架构图、层级结构 → LR（从左到右）
- 状态机 → TD
- 序列图 → 不需要指定方向
