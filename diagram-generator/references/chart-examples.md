# 各类型图表示例

## 示例1：用户注册登录流程（流程图）

**适用场景**：描述业务流程、用户操作路径

```mermaid
flowchart TD
    Start([开始]) --> Input[用户输入手机号]
    Input --> Valid{格式校验}
    Valid -->|无效| Error[提示错误]
    Error --> Input
    Valid -->|有效| SendCode[发送验证码]
    SendCode --> InputCode[用户输入验证码]
    InputCode --> CheckCode{验证验证码}
    CheckCode -->|错误| Retry{重试次数>3?}
    Retry -->|是| Lock[账号锁定1小时]
    Retry -->|否| InputCode
    CheckCode -->|正确| CheckExist{是否已注册?}
    CheckExist -->|否| Register[注册新账号]
    CheckExist -->|是| Login[登录成功]
    Register --> SetInfo[设置个人信息]
    SetInfo --> Login
    Login --> End([进入首页])
    Lock --> End2([结束])
```

## 示例2：OAuth2.0授权码模式（序列图）

**适用场景**：API调用流程、系统间交互

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端应用
    participant BE as 后端服务
    participant Auth as 授权服务器
    participant RS as 资源服务器

    U->>FE: 点击"使用第三方登录"
    FE->>Auth: 重定向到授权页面
    Note right of FE: client_id, redirect_uri, scope
    Auth-->>U: 显示授权页面
    U->>Auth: 同意授权
    Auth-->>FE: 302重定向,携带code
    FE->>BE: 发送code
    BE->>Auth: code换Token
    Note right of BE: code + client_secret
    Auth-->>BE: access_token + refresh_token
    BE->>RS: 请求用户信息(带Token)
    RS-->>BE: 用户信息
    BE-->>FE: 登录成功,JWT
    FE-->>U: 进入系统
```

## 示例3：电商系统微服务架构（架构图/流程图）

**适用场景**：系统架构、模块关系、部署拓扑

```mermaid
flowchart LR
    subgraph 客户端
        Web[Web端]
        App[移动端]
        Mini[小程序]
    end

    subgraph 网关层
        CDN[CDN]
        Nginx[Nginx/API网关]
    end

    subgraph 服务层
        UserSvc[用户服务]
        OrderSvc[订单服务]
        ProductSvc[商品服务]
        PaySvc[支付服务]
        NotifySvc[通知服务]
    end

    subgraph 数据层
        MySQL[(MySQL)]
        Redis[(Redis)]
        MQ[[消息队列]]
        ES[(Elasticsearch)]
    end

    subgraph 第三方
        WXPay[微信支付]
        AliPay[支付宝]
        SMS[短信服务]
    end

    Web --> CDN
    App --> CDN
    Mini --> CDN
    CDN --> Nginx
    Nginx --> UserSvc
    Nginx --> OrderSvc
    Nginx --> ProductSvc
    OrderSvc --> PaySvc
    OrderSvc --> NotifySvc
    UserSvc --> MySQL
    UserSvc --> Redis
    OrderSvc --> MySQL
    OrderSvc --> MQ
    ProductSvc --> ES
    PaySvc --> WXPay
    PaySvc --> AliPay
    NotifySvc --> SMS
```

## 示例4：任务状态流转（状态图）

**适用场景**：状态机、订单状态、工单流转

```mermaid
stateDiagram-v2
    [*] --> 待处理
    待处理 --> 处理中: 开始处理
    待处理 --> 已取消: 用户取消
    处理中 --> 待审核: 提交审核
    处理中 --> 处理失败: 处理异常
    待审核 --> 已通过: 审核通过
    待审核 --> 已驳回: 审核不通过
    已驳回 --> 处理中: 重新处理
    已通过 --> 已完成: 确认完成
    处理失败 --> 处理中: 重试
    处理失败 --> 已关闭: 多次失败
    已完成 --> [*]
    已取消 --> [*]
    已关闭 --> [*]
```

## 示例5：项目排期（甘特图）

**适用场景**：项目管理、版本计划、里程碑

```mermaid
gantt
    title APP v2.0 开发计划
    dateFormat  YYYY-MM-DD
    section 产品设计
    需求文档       :done,    des1, 2024-03-01, 5d
    UI设计         :done,    des2, after des1, 7d
    设计评审       :milestone, done, m1, after des2, 1d
    section 开发
    前端开发       :active,  dev1, after m1, 14d
    后端开发       :         dev2, after m1, 21d
    接口联调       :         dev3, after dev1, 7d
    section 测试
    功能测试       :         test1, after dev3, 7d
    性能测试       :         test2, after test1, 3d
    Bug修复        :         test3, after test2, 5d
    section 上线
    UAT验收        :         uat, after test3, 3d
    正式上线       :milestone, m2, after uat, 1d
```

## 示例6：数据库ER图

**适用场景**：数据库设计、表关系

```mermaid
erDiagram
    USERS ||--o{ ORDERS : creates
    USERS {
        bigint id PK
        string username
        string email
        string password_hash
        datetime created_at
    }
    ORDERS ||--|{ ORDER_ITEMS : contains
    ORDERS {
        bigint id PK
        bigint user_id FK
        decimal total_amount
        string status
        datetime created_at
    }
    ORDER_ITEMS }o--|| PRODUCTS : references
    ORDER_ITEMS {
        bigint id PK
        bigint order_id FK
        bigint product_id FK
        int quantity
        decimal unit_price
    }
    PRODUCTS {
        bigint id PK
        string name
        decimal price
        int stock
        bigint category_id FK
    }
    CATEGORIES ||--o{ PRODUCTS : contains
    CATEGORIES {
        bigint id PK
        string name
        bigint parent_id FK
    }
```

## 示例7：知识体系（思维导图）

**适用场景**：脑图、知识整理、分类

```mermaid
mindmap
  root((前端开发))
    HTML/CSS
      HTML5语义化
      CSS3/Flex/Grid
      响应式设计
      CSS预处理器
        Sass
        Less
    JavaScript
      ES6+语法
      异步编程
      DOM操作
      框架
        React
        Vue
        Angular
    工程化
      Webpack/Vite
      Git版本控制
      CI/CD
      单元测试
    性能优化
      加载优化
      渲染优化
      缓存策略
```

## 示例8：用户旅程地图

**适用场景**：用户体验分析、产品流程优化

```mermaid
journey
    title 外卖点餐体验
    section 找餐厅
      打开外卖APP: 5: 用户
      浏览推荐: 3: 用户
      搜索想吃的: 4: 用户
      看评价: 3: 用户
    section 下单
      选择菜品: 4: 用户
      凑满减: 2: 用户
      填写地址: 3: 用户
      选择支付方式: 4: 用户
      付款: 5: 用户
    section 等待
      查看骑手位置: 4: 用户
      等待配送: 2: 用户
    section 用餐
      收到外卖: 5: 用户
      用餐: 5: 用户
      评价: 4: 用户
```

## 示例9：Git分支策略（Git Graph）

**适用场景**：Git工作流、版本管理

```mermaid
gitGraph
    commit id: "v1.0发布"
    branch develop
    checkout develop
    commit id: "功能A开发"
    commit id: "功能A测试"
    branch feature/payment
    checkout feature/payment
    commit id: "支付功能"
    commit id: "支付联调"
    checkout develop
    merge feature/payment
    commit id: "合并支付"
    checkout main
    merge develop tag: "v1.1"
    branch hotfix/pay-bug
    checkout hotfix/pay-bug
    commit id: "修复支付bug"
    checkout main
    merge hotfix/pay-bug tag: "v1.1.1"
    checkout develop
    merge hotfix/pay-bug
```

## 示例10：Graphviz DOT 复杂网络拓扑

**适用场景**：复杂依赖关系、自动布局需求

```dot
digraph Infrastructure {
    rankdir=TB;
    node [shape=box, style=filled, fillcolor=lightblue];

    subgraph cluster_prod {
        label="生产环境";
        style=filled;
        color=lightgrey;

        LB [label="负载均衡", shape=doubleoctagon, fillcolor=orange];

        subgraph cluster_app {
            label="应用集群";
            APP1 [label="App Server 1"];
            APP2 [label="App Server 2"];
            APP3 [label="App Server 3"];
        }

        subgraph cluster_db {
            label="数据库层";
            M [label="MySQL Master", shape=cylinder, fillcolor=lightgreen];
            S1 [label="MySQL Slave 1", shape=cylinder, fillcolor=lightgreen];
            S2 [label="MySQL Slave 2", shape=cylinder, fillcolor=lightgreen];
            R [label="Redis Cluster", shape=cylinder, fillcolor=pink];
        }
    }

    LB -> APP1;
    LB -> APP2;
    LB -> APP3;
    APP1 -> M;
    APP2 -> M;
    APP3 -> M;
    APP1 -> R;
    APP2 -> R;
    APP3 -> R;
    M -> S1;
    M -> S2;
}
```

## 示例11：PlantUML 组件图

**适用场景**：UML建模、详细组件关系

```plantuml
@startuml
!theme plain
skinparam componentStyle rectangle

package "表现层" {
    [Web前端] as Web
    [移动APP] as App
    [管理后台] as Admin
}

package "网关层" {
    [API网关] as Gateway
    [认证中心] as Auth
}

package "业务服务层" {
    [用户服务] as UserSvc
    [订单服务] as OrderSvc
    [商品服务] as ProductSvc
    [支付服务] as PaySvc
}

package "数据层" {
    database "MySQL" as MySQL
    database "Redis" as Redis
    database "MongoDB" as MongoDB
}

Web --> Gateway
App --> Gateway
Admin --> Gateway
Gateway --> Auth
Gateway --> UserSvc
Gateway --> OrderSvc
Gateway --> ProductSvc
Gateway --> PaySvc
UserSvc --> MySQL
OrderSvc --> MySQL
ProductSvc --> MongoDB
PaySvc --> MySQL
UserSvc --> Redis
OrderSvc --> Redis
@enduml
```

## 示例12：饼图数据可视化

**适用场景**：占比展示、分布统计

```mermaid
pie showData
    title 2024年Q1营收构成（万元）
    "产品销售" : 520
    "技术服务" : 280
    "订阅收入" : 180
    "广告收入" : 90
    "其他" : 30
```
