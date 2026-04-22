# Nature AI

## 📖 项目介绍

**Nature AI** 不仅仅是一个对话式 AI，它是一个深耕小说领域的 **专家型智能体 (AI Agent)**。它模仿了法律 AI 标杆 Harvey AI 的严谨逻辑，将创作过程拆解为“知识检索、结构搭建、内容撰写、逻辑审计”四个标准流水线阶段。

### 为什么选择 Nature AI？
- **告别逻辑崩坏**：通过图数据库（Neo4j）强制约束世界观一致性。
- **保护创作 IP**：私有化 RAG 库，AI 学习的是你的笔触，而非通用模板。
- **工业化效率**：将繁琐的“查资料”与“对稿件”自动化，让作者专注于核心创意。

---

## 🛠 技术栈 (Tech Stack)

| 模块 | 技术选型 | 详细用途 | 推荐度 |
| :--- | :--- | :--- | :--- |
| **核心大脑** | Claude 3.5 Sonnet / GPT-4o | 负责高质量文本生成与复杂逻辑推理 | ⭐⭐⭐⭐⭐ |
| **Agent 编排引擎** | **CrewAI** | 协同四个 Agent(Architect/Scribe/Archive/Auditor)的任务流 | ⭐⭐⭐⭐⭐ |
| **推理与验证** | **ReAct (Reasoning + Acting)** | 多步推理验证逻辑一致性，驱动知识图谱查询 | ⭐⭐⭐⭐⭐ |
| **短期记忆检索** | **LlamaIndex + (Pinecone / Milvus)** | L2 向量RAG，存储前文剧情碎片和语义检索 | ⭐⭐⭐⭐ |
| **长期记忆图谱** | **Neo4j (Graph Database)** | L3 知识图谱，强制约束人物、地点、功法、时间线一致性 | ⭐⭐⭐⭐⭐ |
| **文风微调** | Llama 3.1 / Qwen-2.5 (LoRA) | 针对特定流派（如悬疑、仙侠）进行私有化文风训练 | ⭐⭐⭐⭐ |
| **交互界面** | Next.js + Tiptap Editor | 支持 Markdown 语法的沉浸式智能写作环境 | ⭐⭐⭐⭐ |
| **Markdown 处理引擎** | **MDL (Markdown Operation Language)** | 负责文档解析、优化、转换与分析，支持 25+ 格式，与 LLM 深度融合 | ⭐⭐⭐⭐⭐ |

---

## ✨ 核心功能列表

### 1. 世界观百科 (The Archive - Graph RAG)
- **实体关联**：自动提取人物、地点、功法、物品，构建结构化知识库。
- **一致性检查**：当剧情与设定冲突时（如：角色瞬间移动、战力溢出），系统自动预警。

### 2. 情节架构师 (The Architect)
- **多级大纲规划**：从 50 字核心创意扩展至百万字分章大纲。
- **钩子分析**：基于叙事学理论自动检查每一章的悬念设置与节奏起伏。

### 3. 协同笔耕 (The Scribe)
- **三层记忆写作**：同时调用当前窗口（L1 瞬时）、前文片段（L2 向量RAG）与设定集（L3 知识图谱）。
- **实时上下文检索**：使用 LlamaIndex 自动检索前 20 章的相关情节片段，确保连贯性。
- **风格迁移**：支持在不改变原意的情况下，将文本一键转化为特定作者或流派的笔风。
- **MDL 格式优化**：每次生成完毕，使用 MDL 智能引擎自动规范化 Markdown 格式、修复链接、插入元数据。

### 4. 逻辑审计员 (The Auditor)
- **ReAct 推理验证**：使用多步推理与行动循环，与 Neo4j 交互检查冲突。包括：
  - 战力体系一致性（境界突破、功法等级约束）
  - 时间线闭环（事件顺序、人物位置逻辑）
  - 人物性格一致性（言行矛盾检测）
- **MDL 实体提取**：审计前自动使用 MDL 提取人物、地点、事件等结构化实体，为知识图谱查询提供精准输入。
- **合规性扫描**：内置出版级敏感词库与平台风控模型检查。

---

## 🏗 系统架构设计

Nature AI 采用"大脑-记忆-四肢"模型，以及推荐的**CrewAI + LlamaIndex + ReAct + Neo4j** 混合技术栈：

```
                              CrewAI 编排层
┌─────────────────────────────────────────────────────┐
│  Architect Agent    →    Scribe Agent               │
│  (大纲规划)              (内容撰写)                 │
│         ↓                    ↓                       │
│   (MDL 优化)         (MDL 格式规范)               │
│         ↓                    ↓                       │
│                    LlamaIndex 检索                  │
│                    (L2 向量RAG)                     │
├─────────────────────────────────────────────────────┤
│  Auditor Agent ←→ ReAct 推理 ↔ Neo4j 知识图谱     │
│  (逻辑审计)       (多步推理)    (L3 约束)          │
│       ↓(MDL 实体提取)                              │
│                                                     │
│  MDL Markdown 处理引擎 (贯穿全流程)               │
│  • 格式优化  • 实体提取  • 格式转换  • 文档清理     │
└─────────────────────────────────────────────────────┘
```

### 关键层次结构

1. **大脑 (Brain)**：Claude 3.5 Sonnet + GPT-4o
   - 多模型路由：根据任务类型自动切换（写作 vs 推理 vs 规划）
   - 任务类型：创意写作 → Claude、逻辑审计 → GPT-4o、初稿生成 → Qwen-2.5

2. **编排层 (Orchestration)**：CrewAI
   - 管理四个 Agent 的任务依赖与执行流
   - 支持串行、并行、层级化执行
   - 规范化 Agent 角色与工具集

3. **记忆系统 (Memory)**：
   - **L1 (Context Window)**：当前章节的 8k-16k Token（最新上下文）
   - **L2 (Vector RAG)**：前 20 章的情节碎片（LlamaIndex + Milvus），实现语义检索
   - **L3 (Knowledge Graph)**：全书知识图谱（Neo4j），约束人物、地点、时间线、功法体系

4. **推理层 (Reasoning)**：ReAct
   - **Auditor Agent** 运行 ReAct 循环，每一步都与 Neo4j 交互
   - Thought → Action (查询图谱) → Observation (结果) → 重新思考
   - 自动检测冲突并生成修改建议

5. **四肢 (Tools)**：标准化工具接口
   - Neo4j 查询工具
   - LlamaIndex 向量检索工具
   - **MDL 操作工具**：Markdown 解析、格式优化、实体提取、格式转换（支持 25+ 格式：HTML/PDF/JSON/LaTeX 等）
   - 外部搜索（历史资料查证）、版本 Git 协作
   - 敏感词库与合规检查工具

---

---

## 🔤 MDL: Markdown Operation Language（核心创新）

**MDL** 是 Nature AI 的"Markdown 大脑"，一门专为小说编辑设计的领域特定语言（DSL）。它负责：

| 能力 | 说明 | 应用场景 |
|------|------|--------|
| **格式标准化** | 自动调整标题层级、修复链接、规范化缩进 | 每次 LLM 生成完毕自动优化 |
| **实体提取** | 智能提取人物、地点、时间、事件、魔法等结构化信息 | 为 Neo4j 知识图谱和 Auditor Agent 供料 |
| **多格式转换** | 支持 25+ 格式（HTML、PDF、JSON、LaTeX、Word 等） | 导出排版版本、发布版本、提交版本 |
| **文档亮点标注** | 自动标记伏笔、回收、冲突、待验证的句子 | 帮助作者和审稿人聚焦逻辑问题 |
| **版本管理** | 跟踪多个草稿版本的变化，支持 Diff 与 Merge | 协作编辑与版本控制 |
| **智能分块** | 基于语义、节奏、视角点的智能段落分割 | 优化 LlamaIndex 的向量存储与检索 |

### MDL 工作流示例

```
用户写作流程                    MDL 处理管道
────────────────────────────────────────────
灵感输入
    ↓
大纲生成 (Architect)
    ↓                 MDL 优化: 调整标题层级、插入元数据
初稿撰写 (Scribe)
    ↓                 MDL 处理: 规范格式、提取实体、智能分块
                      ↓ 输入到 Neo4j
逻辑审计 (Auditor)
    ↓                 MDL 提取: 人物关系、时间线、地点、法术等
                      ↓ 与知识图谱校验
修改建议
    ↓
格式转换 (Export)
    ├─ HTML (排版预览)
    ├─ PDF (电子版)
    ├─ JSON (API 数据)
    └─ Word (投稿版本)
                      MDL 转换: 处理样式、分页、元信息
```

---

## ⚅ 可实现性评估

| 维度 | 评分 | 分析 |
|------|------|------|
| **商业价值** | ⭐⭐⭐⭐⭐ | 小说创作市场巨大，工业化编辑需求刚需化 |
| **技术复杂度** | ⭐⭐⭐⭐ | 需要多个系统协同，但各模块独立可行（MDL 独立开发） |
| **实现难度** | ⭐⭐⭐ | 可分阶段递增，初期MVP相对简单（MDL 可逐步集成） |
| **成本投入** | ⭐⭐⭐ | API费用 + 基础设施，可控范围内 |

**结论**: 项目完全可行且高价值。建议采用**MVP → 完整 → 专业化**的渐进式路径，参考 Claude Workbench 的工程化做法。MDL 作为独立服务可同步开发，快速提升系统可用性。

---

## 🏛️ 前期工程化方案（项目结构）

```
Nature-AI/
├── .github/
│   └── workflows/              # CI/CD 自动化测试与部署
├── docs/
│   ├── architecture.md         # 详细架构设计文档
│   ├── api-spec.md             # API 规范
│   ├── data-schema.md          # 数据库Schema
│   └── examples/               # 工作流示例与最佳实践
├── src/
│   ├── core/
│   │   ├── models.py           # 多模型路由与适配
│   │   ├── graph_rag.py        # 知识图谱与RAG引擎
│   │   └── agents.py           # 多Agent编排
│   ├── models/
│   │   ├── llm_adapters.py     # Claude / GPT-4o / Qwen 适配器
│   │   ├── embedding.py        # 向量化模型接口
│   │   └── fine_tuning.py      # 微调管理器
│   ├── workflows/
│   │   ├── outline.py          # 灵感→大纲工作流
│   │   ├── writing.py          # 大纲→初稿工作流
│   │   ├── audit.py            # 逻辑审计工作流
│   │   └── flow_manager.py     # LangGraph 状态机
│   ├── storage/
│   │   ├── vector_db.py        # Pinecone / Milvus 接口
│   │   ├── graph_db.py         # Neo4j 接口
│   │   └── relational_db.py    # PostgreSQL 接口
│   ├── utils/
│   │   ├── markdown_parser.py  # Markdown 解析与YAML提取
│   │   ├── entity_extractor.py # 人物/地点/物品提取
│   │   └── validators.py       # 数据验证
│   └── api/
│       ├── main.py             # FastAPI 应用入口
│       ├── routes.py           # API 路由定义
│       └── schemas.py          # Pydantic 数据模型
├── tests/
│   ├── unit/                   # 单元测试
│   ├── integration/            # 集成测试
│   └── e2e/                    # 端到端工作流测试
├── frontend/
│   ├── pages/                  # Next.js 页面
│   ├── components/             # React 组件库
│   ├── hooks/                  # 自定义 Hook
│   └── styles/                 # 样式文件
├── docker/
│   ├── Dockerfile              # 应用容器
│   ├── docker-compose.yml      # 完整服务栈
│   └── .dockerignore
├── config/
│   ├── models.yaml             # 模型配置（成本/延迟/能力）
│   ├── workflows.yaml          # 工作流配置
│   └── defaults.yaml           # 默认参数与常量
├── pyproject.toml              # 依赖管理与项目配置
├── requirements.txt            # Python 依赖
└── README.md
```

---

## 🔌 模型接入架构（核心创新）

采用**适配器模式 + 策略路由**实现灵活的多模型架构：

### 模型配置体系

```yaml
# config/models.yaml
model_registry:
  llm:
    claude-3.5-sonnet:
      provider: "anthropic"
      context_window: 200000
      cost_per_1k_input: 0.003
      cost_per_1k_output: 0.015
      use_case: "creative_writing"      # 高质量创意写作
      latency: "medium"
      
    gpt-4o:
      provider: "openai"
      context_window: 128000
      cost_per_1k_input: 0.005
      cost_per_1k_output: 0.015
      use_case: "logic_audit"           # 逻辑审核与校验
      latency: "medium"
      
    qwen-2.5-72b:
      provider: "alibaba"
      context_window: 32000
      cost_per_1k_input: 0.0005
      cost_per_1k_output: 0.001
      use_case: "draft_generation"      # 初稿与大纲生成
      latency: "low"
      can_finetune: true
  
  embedding:
    text-embedding-3-large:
      provider: "openai"
      dimension: 3072
      cost_per_1m: 0.13
      use_case: "primary"
      
    bge-m3:
      provider: "open_source"
      dimension: 1024
      cost_per_1m: 0                    # 本地部署
      use_case: "fallback"

# 任务路由规则
route_strategy:
  creative_writing:
    primary: "claude-3.5-sonnet"
    fallback: "qwen-2.5-72b"
    temperature: 0.8
    max_tokens: 4000
    
  logic_audit:
    primary: "gpt-4o"
    fallback: "claude-3.5-sonnet"
    temperature: 0.2
    max_tokens: 2000
    
  outline_generation:
    primary: "qwen-2.5-72b"            # 成本优化
    fallback: "claude-3.5-sonnet"
    temperature: 0.7
    max_tokens: 3000
    
  consistency_check:
    primary: "qwen-2.5-72b"            # 图谱查询为主
    embedding: "text-embedding-3-large"
    temperature: 0.0
    max_tokens: 1000
```

### 模型适配器示例

```python
# src/models/llm_adapters.py
from abc import ABC, abstractmethod
from typing import Optional
import anthropic
import openai

class LLMAdapter(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    async def stream_generate(self, prompt: str, **kwargs):
        pass

class ClaudeAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str = "claude-3.5-sonnet"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    async def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 4000),
            temperature=kwargs.get("temperature", 0.7),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

class ModelRouter:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.adapters = self._init_adapters()
    
    def get_adapter(self, task_type: str) -> LLMAdapter:
        """根据任务类型自动选择最优模型"""
        route = self.config["route_strategy"].get(task_type, {})
        primary_model = route.get("primary")
        return self.adapters.get(primary_model)
```

---

## 📚 小说结构拆分（雪花模型）

全新的分层次递进式结构，更符合编剧与编辑的思维方式：

### 多维度情节组织

```
Novel (全书)
│
├─ Story Arcs (故事弧线 - 全局宏观)
│  ├─ Act I: 起承 (0-25%)
│  ├─ Act II: 转折与冲突 (25-75%)
│  └─ Act III: 高潮与收笔 (75-100%)
│
├─ Plot Lines (5 条独立叙事线)
│  ├─ Main Line: 主角成长与目标
│  ├─ Relationship Arc: 感情与人物关系演变
│  ├─ Antagonist Arc: 反派与阴谋布局
│  ├─ World Arc: 世界观揭示与规则发现
│  └─ Thematic Arc: 主题升华与思想表达
│
├─ Book / Volume (分册)
│  │
│  └─ Chapter (章节)
│     ├─ Scene (场景 - 最小叙事单位)
│     │  ├─ pov: "张小凡"              # 视角人物
│     │  ├─ setting: "青云山万剑阁"    # 时地信息
│     │  ├─ conflict: "发现身世真相"   # 冲突发端
│     │  ├─ beats: [                 # 节奏点序列
│     │  │    "铜镜映照",
│     │  │    "灵力异变",
│     │  │    "昔日往事闪现",
│     │  │    "决然转身离去"
│     │  │  ]
│     │  └─ content: "张小凡握紧..."   # 正文内容
│     │
│     ├─ Chapter Metadata
│     │  ├─ chapter_id: 15
│     │  ├─ title: "幽谷奇缘"
│     │  ├─ word_count: 3500
│     │  ├─ characters: ["张小凡", "碧瑶", "陆雪琪"]
│     │  ├─ locations: ["空桑山", "蛮荒古林"]
│     │  ├─ timeline_event: "陆雪琪入队 Day 15"
│     │  ├─ plot_momentum: 0.72        # 0.0-1.0 情节推动度
│     │  ├─ emotional_peak: 0.85       # 情感强度
│     │  ├─ foreshadowing: [           # 埋伏笔
│     │  │    "id": "mystery_001",
│     │  │    "hint": "碧瑶眼中闪过异芒"
│     │  │  ]
│     │  └─ callbacks: [               # 回收记录
│     │       { "foreshadow_id": "mystery_001", "resolved": true }
│     │     ]
│     │
│     └─ Revision History
│        ├─ draft_v1: "2026-04-15"
│        ├─ draft_v2: "2026-04-17"
│        └─ published: "2026-04-19"
│
└─ Knowledge Graph (世界设定)
   ├─ Characters (人物库)
   │  └─ 张小凡
   │     ├─ aliases: ["凡哥", "小凡"]
   │     ├─ background: "诛仙第一部主角"
   │     ├─ abilities: ["青云诀", "噬血珠"]
   │     ├─ relationships: {
   │     │    "碧瑶": "love_interest",
   │     │    "陆雪琪": "ally",
   │     │    "鬼厉": "enemy"
   │     │  }
   │     └─ appearance: "黑发剑眉，眼神深邃"
   │
   ├─ Locations (地点库)
   │  └─ 青云山
   │     ├─ geography: "中原南方"
   │     ├─ rules: "禁飞/禁魔法"
   │     ├─ connected_to: ["空桑山", "幽冥界"]
   │     └─ first_appearance: "Chapter 1"
   │
   ├─ Magic System (魔法/功法体系)
   │  └─ 青云诀
   │     ├─ type: "sword_art"
   │     ├─ power_level: "S-tier"
   │     ├─ cost: "high_spiritual_energy"
   │     ├─ side_effects: "心火灼烧"
   │     └─ creator: "青云门祖师"
   │
   ├─ Timeline (事件轴)
   │  ├─ Era 1: "仙魔大战"
   │  ├─ Era 2: "诛仙故事"
   │  │   ├─ Day 0: "张小凡入门"
   │  │   ├─ Day 15: "陆雪琪加入"
   │  │   └─ Day 360: "十大弟子大比"
   │  └─ Era 3: "逆仙时代"
   │
   └─ Constraints (世界观约束规则)
      ├─ rule_1: "仙人不可干涉凡人历史"
      ├─ rule_2: "魔法总是有代价的"
      ├─ rule_3: "死人不可复活（绝对禁忌）"
      ├─ rule_4: "双修伤害境界突破"
      └─ inconsistency_log: []  # 冲突记录
```

### 可视化写作仪表板

```
╔════════════════════════════════════════════════════════════╗
║              📊 Nature AI 写作进度仪表板                     ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║ 📈 全局进度                                                ║
║   写作: ███████████░░░░░░░░░░░░░░  40/100 章 (40%)      ║
║   审核: █████░░░░░░░░░░░░░░░░░░░░  13/100 章 (13%)      ║
║   发布: ██░░░░░░░░░░░░░░░░░░░░░░░   2/100 章 (2%)       ║
║   总字数: 320,000 / 1,000,000 字                         ║
║                                                            ║
║ 📋 最近任务队列                                            ║
║   □ 第 15 章 初稿撰写              优先级: 🔴 高        ║
║   □ 人物关系微调（碧瑶视角）       优先级: 🟡 中        ║
║   □ 时间线校验（第 10-15 章）      优先级: 🟢 低        ║
║                                                            ║
║ ⚠️  逻辑警告                                              ║
║   [第 12 章] ⚡ 战力溢出警告: 张小凡秒杀魔头            ║
║   [第 8 章]  ⚠️  人物矛盾: 碧瑶性格与出场不符           ║
║   [全书]     📆 时间线缺口: 第 20-25 章时间轴未定义     ║
║                                                            ║
║ 💡 AI 建议                                                ║
║   强化第 15 章的感情描写，参考第 8 章铺垫              ║
║   建议补充碧瑶身世的伏笔回收机制                         ║
║   重新校验青云诀的魔力消耗规则                           ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

---

## 🚀 MVP 实现路径 (60天快速启动)

### 🎯 第 1 周：工程基础搭建 + 原型验证

**目标**: 可运行的 CrewAI + LlamaIndex + MDL 工程框架

- [ ] **Day 1-2**: 项目初始化
  - 创建 Python 项目结构（FastAPI + CrewAI + LlamaIndex）
  - 配置 Dockerfile 与 Docker Compose
  - 初始化 Milvus 向量数据库、PostgreSQL、Redis
  - **集成 MDL 服务** (可选：独立 Python 包或本地部署)
  
- [ ] **Day 3-4**: CrewAI 框架与多模型接入
  - 实现 Claude / GPT-4o / Qwen API 适配器
  - 集成模型路由配置管理
  - 定义四个基础 Agent 类（Architect, Scribe, Archive, Auditor）
  - **集成 MDL 工具**：Markdown 格式优化、实体提取
  - 编写单元测试
  
- [ ] **Day 5-7**: 第一个工作流（灵感 → 大纲 → 初稿）
  - 使用 CrewAI 编排 Architect → Scribe 工作流
  - **在 Scribe Agent 中集成 MDL** 格式规范化
  - 集成 LlamaIndex 简单向量检索（L2 存储）
  - 完成端到端测试（输入灵感，输出初稿）

**可交付物**:
```bash
curl -X POST http://localhost:8000/api/workflows/outline \
  -H "Content-Type: application/json" \
  -d '{"idea": "一个孤儿少年在仙侠世界的成长", "words": 50}'
  
# 返回: 经过 MDL 优化的 100-500字完整章节大纲
```

---

### 🎯 第 2-3 周：LlamaIndex RAG 深化 + Agent 协同强化 + MDL 优化

**目标**: 完整的 L2 向量检索系统 + 三个协同 Agent（架构师 + 笔手 + 管理员） + MDL 深度集成

- [ ] **Week 2**:
  - 优化 LlamaIndex 向量索引（Milvus 后端）
  - 构建高质量的 Markdown 解析与智能 Chunk 分割器
  - **使用 MDL 进行智能分块**：基于语义、节奏、视角点的分割
  - 实现混合检索（向量 + 关键词）以改进召回率
  - 集成自动 Embedding 更新管道
  
- [ ] **Week 3**:
  - 增强 Architect Agent（大纲审核与优化）
  - **增强 Scribe Agent**（使用 L2 检索写作，集成 MDL 格式优化）
  - 开发 Archive Agent（知识库初级管理，无需 Neo4j）
  - **MDL 与 Archive 的协同**：自动提取和存储实体元数据
  - 实现 CrewAI 任务依赖与反馈循环
  - 集成三个 Agent 的协作与评审流程

**可交付物**:
```python
# 工作流示例：从灵感到初稿（包含 MDL 处理）
workflow = WorkflowManager()
result = await workflow.run(
    template="inspiration_to_draft",
    input={
        "idea": "...",
        "style": "武侠悬疑",
        "target_words": 1000
    }
)
# 自动返回: 经过两个 Agent 审核 + MDL 优化的初稿
# 包含结构化元数据（人物、地点、魔法等）
```

---

### 🎯 第 4-5 周：Neo4j + ReAct 推理审计系统 + MDL 实体集成

**目标**: 知识图谱系统 + ReAct 逻辑审计能力 + MDL 实体提取

- [ ] **Week 4**:
  - 设计并部署 Neo4j 数据模型（Character, Location, Ability, Event, Timeline）
  - **使用 MDL 自动提取实体**：智能识别人物、地点、魔法、时间事件
  - 实现自动实体提取器（NER 模块，可结合 MDL 大幅简化）
  - 构建关系推断与约束规则引擎（战力体系、时间线约束）
  - 开发 Neo4j → LLM 的安全查询包装器
  
- [ ] **Week 5**:
  - 开发 **Auditor Agent + ReAct 推理引擎**
    - 实现 Thought → Action(查询 Neo4j) → Observation → 重新思考的循环
    - **MDL 支持**：Auditor 先用 MDL 提取实体，再进行逻辑校验
    - 支持多步推理：战力检查、时间线校验、人物矛盾检测
  - 实现冲突检测与修改建议生成
  - **MDL 标注冲突**：自动在源文档中标记发现的逻辑问题
  - 自动生成"全书逻辑体检报告"（含问题等级、影响范围、修改建议）

**可交付物**:
```python
audit_result = await auditor.check_consistency(
    chapter_content="...",
    knowledge_graph=kg_instance
)

# 返回示例（包含 MDL 标注）：
{
    "status": "warning",
    "mdl_annotations": [
        {
            "type": "entity_mismatch",
            "location": "paragraph_3, sentence_2",
            "entity": "张小凡",
            "issue": "战力溢出 50%"
        }
    ],
    "issues": [
        {
            "type": "power_escalation",
            "severity": "high",
            "description": "第 15 章中角色战力溢出 50%",
            "suggestion": "建议降低敌人实力或增加约束条件"
        }
    ]
}
```

---

### 🎯 第 6-7 周：前端 UI + 集成测试

**目标**: 可用的编辑器界面 + 完整工作流演示

- [ ] **Week 6**:
  - 构建 Next.js 编辑器框架
  - 集成 Tiptap 富文本编辑器
  - 设计 AI 建议侧边栏
  
- [ ] **Week 7**:
  - 实现 WebSocket 实时反馈
  - 完成端到端集成测试
  - 编写使用文档与最佳实践指南

**可交付物**: 一个可以完整体验"灵感→大纲→初稿→审核→修改"的演示系统

---

### 🎯 第 8 周：性能优化 + 边界测试

**目标**: 生产级可用性 + 性能基准达成

- [ ] 并发调用优化（同时调用多个 Agent）
- [ ] 缓存策略优化（Redis）
- [ ] 错误处理与降级方案
- [ ] 真实小说数据验证
- [ ] 负载测试与瓶颈分析

**KPI 目标**:
- 大纲生成延迟 < 30 秒（Architect Agent）
- 初稿生成延迟 < 2 分钟（Scribe + L2 检索）
- 逻辑审计延迟 < 90 秒（Auditor ReAct，3-5 步推理）
- 向量检索准确率 (Recall@10) > 85%
- 知识图谱查询成功率 > 99%
- 系统整体可用性 > 99%

---

### 📦 第二阶段：逻辑强化与图谱 (3-4个月)

- [ ] 完整的 Neo4j 知识图谱系统
- [ ] "生成-审计-重写"自动化循环
- [ ] 可视化编辑器插件（关系网、时间线可视化）
- [ ] 多工作流编排（同时支持多个作品）

---

### 🎓 第三阶段：生态与微调 (5个月+)

- [ ] 针对武侠、言情、悬疑等 5 个垂直流派的 LoRA 微调
- [ ] 多租户系统与工作室白标方案
- [ ] 全书"逻辑体检报告"生成
- [ ] 社区插件生态与扩展机制

---

## � 快速开始

### 前置要求
- Python 3.10+
- Docker & Docker Compose
- 模型 API 密钥：Claude、GPT-4o（可选）

### 本地开发

```bash
# 1. 克隆并进入项目
git clone https://github.com/literatures95/Nature-AI
cd Nature-AI

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env，填入 API 密钥和数据库配置

# 5. 启动服务（使用 Docker Compose）
docker-compose up -d

# 6. 部署 MDL 服务（独立或已包含在上述 docker-compose 中）
docker-compose -f docker/docker-compose.mdl.yml up mdl-service
# 或本地运行
python src/api/mdl_service.py

# 7. 检查服务状态
curl http://localhost:8000/health
curl http://localhost:8001/health  # MDL 服务

# 8. 运行示例
python -m examples.quick_start
```

### Docker 一键启动

```bash
docker-compose -f docker/docker-compose.yml up -d

# 查看日志
docker-compose logs -f app

# 停止服务
docker-compose down
```

---

## � 技术方案详细论证

本项目精选了 **CrewAI + LlamaIndex + ReAct + Neo4j + MDL** 的混合技术栈：

- **CrewAI**：多 Agent 编排与协同（Architect、Scribe、Archive、Auditor）
- **LlamaIndex**：向量检索与 RAG（L2 短期记忆）
- **Neo4j**：知识图谱与逻辑约束（L3 长期记忆）
- **ReAct**：多步推理与验证（Auditor Agent 的核心）
- **MDL**：Markdown 操作语言（文档处理与实体提取的统一引擎）

详细的技术方案对比、优缺点分析、MDL 集成指南等请参考：

👉 **[技术方案分析文档](docs/技术方案分析.md)**

该文档包含：
- ✅ 四种技术方案的详细对标（CrewAI、LlamaIndex、Self-Ask、ReAct）
- ✅ 各方案在小说创作场景的适用性评分
- ✅ 混合架构的工作流设计图（含 MDL 处理引擎）
- ✅ 分阶段实现路线与 FAQ

---

## �💼 商业模式与定价

| 方案 | 目标用户 | 定价 | 主要功能 |
|------|--------|------|--------|
| **单稿服务** | 独立作者 | ￥99-199/万字 | 一次性初稿生成与审核 |
| **Premium 订阅** | 专职作者 | ￥1999/月 | 无限稿件、私有 RAG、高级审核 |
| **工作室套餐** | 文学工作室 | ￥19999/年 | 多用户、多IP隔离、白标方案 |
| **企业定制** | 出版社/平台 | 按需报价 | 私有部署、模型微调、集成支持 |

---

## 📖 文档导航

- [🏛️ 系统架构深度解读](docs/architecture.md)
- [🔌 模型集成指南](docs/model-integration.md)
- [📊 数据库 Schema 规范](docs/data-schema.md)
- [📝 MDL 快速参考](docs/MDL快速参考.md) — Markdown 处理引擎快速入门
- [🔗 MDL 集成方案](docs/MDL集成方案.md) — 详细的架构设计与功能集成
- [🛠 MDL 集成建设指南](docs/MDL集成建设指南.md) — 部署、配置与开发步骤
- [🔄 工作流开发指南](docs/workflow-development.md)
- [🧪 测试与质量保证](docs/testing.md)
- [🌐 部署与运维](docs/deployment.md)
- [💬 API 文档](docs/api-spec.md)

---

## 🤝 贡献指南

我们欢迎开发者贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解：
- 代码风格与提交规范
- Pull Request 流程
- 开发环境配置

---


## 📄 Markdown 存储与检索规范

为了确保 AI 能够像专家一样理解你的作品，推荐使用以下 MD 格式：

### 章节文件格式

```markdown
---
chapter_id: 15
chapter_title: 幽谷奇缘
book_id: 1
volume: 2
word_count: 3500
characters: [张小凡, 碧瑶, 陆雪琪]
locations: [空桑山, 蛮荒古林]
timeline_event: "陆雪琪入队 Day 15"
plot_beat: "遭遇蝙蝠群袭，感情升温"
tags: [对话, 战斗, 感情线]
foreshadowing: [mystery_001, mystery_002]
callbacks: [callback_005]
---

# 第十五章：幽谷奇缘

## 场景一：林中遭遇

[[张小凡]] 握紧了手中的武器。此时，[[碧瑶]] 侧过头，在火光的映照下，她的眼神如同宝石般闪烁...

> **AI 注释**：此处需调用 [设定库/法术/青云门雷法] 进行逻辑校验。

### 节奏点 (Beats)
- [x] "铜镜映照" - 发现异常信号
- [ ] "灵力异变" - 敌人现身
- [ ] "昔日往事闪现" - 情感催化
- [ ] "决然转身离去" - 行动抉择

---

## 场景二：雨夜对话

[[碧瑶]]："你相信命运吗？"

**情感强度**: 0.85 | **节奏**: 平缓推进 | **冲突度**: 0.3
```

---

## 🔬 系统集成实例

### 示例工作流：初稿生成

```
用户输入
  ↓
[灵感预处理]
  ├─ 解析 Markdown YAML Frontmatter
  ├─ 提取人物、地点、情节要点
  └─ 加载相关知识库片段
  ↓
[架构师 Agent (Claude)]
  ├─ 生成详细的场景大纲
  ├─ 设置冲突点与节奏
  └─ 输出结构化的情节框架
  ↓
[笔手 Agent (Qwen-2.5)]
  ├─ 基于框架生成初稿文本
  ├─ 应用风格微调
  └─ 输出完整章节
  ↓
[逻辑审计 Agent (GPT-4o)]
  ├─ 查询知识图谱
  ├─ 检查逻辑矛盾
  ├─ 验证时间线一致性
  └─ 生成提示与建议
  ↓
[用户审核与修改]
  ├─ 手动编辑与反馈
  ├─ AI 学习优化版
  └─ 保存到发布池
```

---

## 💡 FAQ

**Q: 为什么选择 CrewAI 而不是 LangGraph / Dify？**
A: 详见[技术方案分析](docs/技术方案分析.md)。CrewAI 提供了更好的 DSL 抽象（Agent 角色定义），适合小说创作的四个明确角色（Architect/Scribe/Archive/Auditor）。LangGraph 更灵活但配置复杂，Dify 是低代码平台，适合非工程师但灵活性较差。

**Q: ReAct 推理会不会新增太多 API 调用成本？**
A: ReAct 用于异步的逻辑审计流程，不会阻塞实时写作。且可通过：
1. 使用成本优化的 Qwen-2.5 模型进行图查询
2. 批量审计（作者完成一章后进行）
3. 离线预计算（规划阶段不检查）
来控制成本。详见[技术方案分析](docs/技术方案分析.md)的 FAQ 部分。

**Q: 可以使用开源 LLM 吗？**
A: 完全可以。我们的架构支持任何兼容 OpenAI API 的模型（如 Ollama、Vllm 部署的 Llama、Qwen）。成本会大幅下降。生成初稿可用 Qwen-2.5，审计可用 GPT-4o，写作用 Claude。

**Q: 数据隐私如何保证？**
A: 支持私有部署。使用本地部署的 Neo4j、Milvus，通过私有化 LLM（如 Ollama 本地部署）实现完全隔离。所有知识库与 RAG 数据都在本地。

**Q: 能否支持其他语言？**
A: 可以。只需提供相应语言的微调数据，架构完全支持多语言。Embedding 模型和 LLM 都支持多语言。

**Q: 相比 ChatGPT 有什么优势？**
A: 我们针对小说创作的工业化需求专门优化，全栈包括：
- 知识图谱约束（Neo4j）强制逻辑一致性
- 多 Agent 协同（CrewAI）分工明确
- ReAct 推理验证 (Auditor) 自动审计
- L2 向量 RAG (LlamaIndex) 确保连贯性

是一个完整的**创作生产系统**而不是通用对话工具。

---

## 📜 许可证

本项目采用 [MIT License](LICENSE)。

---

## 📧 联系与反馈

- 📬 Email: team@nature-ai.dev
- 💬 Discord: [加入我们的社区](https://discord.gg/nature-ai)
- 🐛 Bug Report: [GitHub Issues](https://github.com/literatures95/Nature-AI/issues)
- 💡 Feature Request: [GitHub Discussions](https://github.com/literatures95/Nature-AI/discussions)

---

**Made with ❤️ for writers and screenwriters worldwide.**
