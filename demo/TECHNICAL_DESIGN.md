# vLLM + FastAPI + Langchain Demo - 技术设计文档

## 📖 概述

这是一个**生产级别的微型 AI 应用框架**，展示如何将本地大模型（vLLM）与现代 Web 框架（FastAPI）和 LLM 工具链（Langchain）整合，实现一个可扩展的 AI 服务。

### 适用场景

✅ 学习 vLLM + Langchain 集成
✅ 本地 AI 应用快速原型 
✅ 离线 AI 服务部署
✅ Nature AI 主项目的阶段性验证

---

## 🏗 架构设计

### 整体架构图

```
┌──────────────────────────────────────────────────────┐
│                   客户端应用                          │
│              (Web / Mobile / Desktop)                 │
└─────────────────────────┬──────────────────────────┘
                          │
                    HTTP/REST
                          │
                          ↓
        ┌──────────────────────────────────┐
        │       FastAPI 应用服务           │
        │  (src/api/main.py + routes.py)   │
        │                                  │
        │  • 请求处理与验证               │
        │  • 响应序列化                   │
        │  • 错误处理与日志               │
        └────────────┬─────────────────────┘
                     │
              依赖注入（DI）
                     │
                     ↓
        ┌──────────────────────────────────┐
        │     工作流层（Langchain）        │
        │ (src/workflows/outline.py)       │
        │                                  │
        │  • OutlineGenerator              │
        │    - 链 1: 概念扩展              │
        │    - 链 2: 大纲生成              │
        │  • (可扩展为更多工作流)          │
        └────────────┬─────────────────────┘
                     │
            Langchain 链调用
                     │
                     ↓
        ┌──────────────────────────────────┐
        │   LLM 适配层（vLLM Wrapper）     │
        │   (src/models/llm.py)            │
        │                                  │
        │  • VLLMAdapter 类                │
        │  • 异步/同步双支持               │
        │  • 错误恢复与重试                │
        └────────────┬─────────────────────┘
                     │
                OpenAI 兼容 API
                     │
                     ↓
        ┌──────────────────────────────────┐
        │     vLLM 推理服务                │
        │     (Docker 容器或本地)          │
        │                                  │
        │  • 模型加载与管理                │
        │  • Token 生成                    │
        │  • GPU 显存管理                  │
        └────────────┬─────────────────────┘
                     │
                     ↓
        ┌──────────────────────────────────┐
        │     大语言模型                   │
        │  (Qwen 2.5 7B Instruct)          │
        │                                  │
        │  • 推理计算                      │
        │  • 文本生成                      │
        │  • 上下文理解                    │
        └──────────────────────────────────┘
```

### 数据流示例：生成故事大纲

```
1. 用户请求 (HTTP POST)
   {
     "idea": "一个孤儿在仙侠世界的成长"
   }
        │
        ↓

2. FastAPI 路由处理
   routes.generate_outline(request)
        │
        ↓

3. 工作流调用
   generator.generate(idea)
        │
        ├─ 链 1: 扩展概念
        │  prompt = "将这个创意扩展为 200 字核心概念"
        │  response = llm.invoke(prompt)
        │
        └─ 链 2: 生成大纲
           prompt = f"基于概念生成五幕式大纲\n\n概念: {concept}"
           response = llm.invoke(prompt)
        │
        ↓

4. vLLM 调用
   POST http://vllm:8000/v1/completions
   {
     "model": "qwen2.5-7b-instruct",
     "prompt": "...",
     "temperature": 0.7,
     "max_tokens": 1024
   }
        │
        ↓

5. 模型推理
   输入: 完整 Prompt (含系统角色、历史、当前任务)
   输出: Token 序列 (streaming 或 batch)
        │
        ↓

6. 响应返回
   {
     "idea": "一个孤儿在仙侠世界的成长",
     "concept": "张小凡失去双亲...",
     "outline": "第一幕...",
     "status": "success",
     "word_count": 1245
   }
```

---

## 🔧 核心模块详解

### 1. LLM 适配器 (`src/models/llm.py`)

#### 设计模式：适配器模式 + 工厂模式

```python
class VLLMAdapter(LLM):  # 继承 Langchain 基类
    """
    将 vLLM OpenAI 兼容 API 适配成 Langchain LLM 接口
    """
    
    def _call(self, prompt: str) -> str:
        """同步方法 - 阻塞直到完成"""
        
    async def _acall(self, prompt: str) -> str:
        """异步方法 - 非阻塞，可与 FastAPI 的异步流程配合"""

def get_llm() -> VLLMAdapter:
    """工厂函数 - 单例模式（可扩展为连接池）"""
```

#### 关键特性

✅ **异步优先**：支持 `async/await`，避免阻塞事件循环
✅ **错误处理**：网络异常、超时自动恢复
✅ **可配置性**：温度、max_tokens 等参数灵活调整
✅ **扩展性**：轻易切换到其他模型服务（如 OpenAI API）

#### 参数详解

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `model_name` | qwen2.5-7b-instruct | 模型标识 |
| `temperature` | 0.7 | 创意程度 (0.0-1.0) |
| `max_tokens` | 1024 | 最大输出长度 |
| `top_p` | 0.9 | 核采样 nucleus sampling |

### 2. 工作流层 (`src/workflows/outline.py`)

#### 设计模式：链模式 + 组合模式

```python
class OutlineGenerator:
    """
    Langchain 多链工作流
    
    工作流分为两个阶段：
    1. 概念扩展阶段：50 字创意 → 200 字核心概念
    2. 大纲生成阶段：核心概念 → 500-1000 字五幕式大纲
    """
    
    def __init__(self):
        self.llm = get_llm()
        self.concept_chain = LLMChain(...)
        self.outline_chain = LLMChain(...)
    
    async def generate(self, idea: str) -> dict:
        """编排两个链的执行"""
        concept = await self.concept_chain.arun(idea=idea)
        outline = await self.outline_chain.arun(concept=concept)
        return {concept, outline}
```

#### Prompt 工程

**概念扩展 Prompt：**
```
你是一个专业的小说编剧。用户给了一个创意灵感，你需要将其扩展成 200 字的核心概念说明。

灵感: {idea}

请从以下几个维度阐述这个故事：
1. 核心冲突：故事的主要矛盾点是什么？
2. 主角背景：主角是谁？面临什么困境？
3. 世界观：故事发生在什么背景下？
4. 终局：这个故事的结局会是什么？

核心概念：
```

**大纲生成 Prompt：**
```
基于以下书籍概念，生成一个五幕式的故事大纲（每幕 50-100 字）：

概念：{concept}

请按照这个格式生成大纲：

第一幕 (起) - 引入设定与主角：[内容]
第二幕 (承) - 冲突升级：[内容]
...（以此类推）
```

#### 可扩展性

轻易添加更多链：

```python
class ScribeGenerator:  # 新的写作工作流
    def __init__(self):
        self.llm = get_llm()
        self.research_chain = ...      # 资料搜集
        self.outline_chain = ...        # 段落大纲
        self.writing_chain = ...        # 初稿撰写
        self.format_chain = ...         # 格式优化
    
    async def generate(self, outline: str) -> str:
        research = await self.research_chain(outline)
        detailed = await self.outline_chain(research)
        draft = await self.writing_chain(detailed)
        return await self.format_chain(draft)
```

### 3. FastAPI 应用层 (`src/api/`)

#### 项目结构

| 文件 | 职责 |
|------|------|
| `main.py` | FastAPI 应用初始化、CORS、中间件、生命周期钩子 |
| `routes.py` | API 端点定义与业务逻辑 |
| `schemas.py` | Pydantic 数据模型（请求/响应验证） |

#### 异步设计

```python
# routes.py
@router.post("/outline", response_model=OutlineResponse)
async def generate_outline(request: OutlineRequest):
    """
    异步端点 - 不阻塞事件循环
    支持并发处理多个请求
    """
    generator = get_outline_generator()
    result = await generator.generate(
        idea=request.idea,
        detailed=request.detailed
    )
    return OutlineResponse(**result)
```

**性能优势：**
- 单线程处理 100+ 并发请求
- 自动 I/O 复用（httpx 异步客户端）
- 响应时间 vs 吞吐量的最优平衡

#### 数据验证（Pydantic）

```python
class OutlineRequest(BaseModel):
    idea: str = Field(..., max_length=200)
    detailed: bool = Field(False)

# 自动做到：
# ✅ 类型检查 (str, bool)
# ✅ 长度验证 (max_length=200)
# ✅ 必填检查
# ✅ JSON 反序列化
# ✅ OpenAPI 文档生成
```

---

## 🐳 Docker 编排设计

### docker-compose.yml 架构

```yaml
services:
  vllm:          # 推理服务
    image: vllm/vllm-openai:latest
    ports: [8000]
    healthcheck: 连接检查
    volumes: 模型缓存
  
  api:           # Web 服务
    build: ./Dockerfile
    ports: [8001]
    depends_on: [vllm]  # 等待 vllm 就绪
    healthcheck: API 检查
    environment: 配置传递
```

### 启动顺序

```
1. docker-compose up
   ↓
2. vllm 容器启动
   ├─ 拉取模型 (首次)
   ├─ 加载到 GPU
   └─ 启动 OpenAI API 服务器
   ↓
3. vllm healthcheck 通过
   ↓
4. api 容器启动（因为 depends_on）
   └─ 连接到 vllm:8000
   ↓
5. 所有服务就绪
   └─ 接受客户端请求
```

---

## 💾 配置管理

### 分层配置

```
环境变量 (.env)
    ↓
Pydantic Settings (src/config.py)
    ↓
全局 settings 实例
    ↓
各模块使用 (LLM, API 等)
```

### 配置覆盖优先级

```
1. 环境变量 (最高)
2. .env 文件
3. 代码默认值 (最低)
```

示例：

```bash
# 通过环境变量覆盖
export VLLM_MODEL="mistral-7b-instruct"
docker-compose up

# 或在 .env 中设置
VLLM_MODEL=meta-llama/Llama-2-13b-chat-hf
```

---

## 🧪 测试策略

### 层次化测试

```
┌─ 单元测试 (Unit)
│  └─ 测试各个组件的单独功能
│     • LLM 适配器的请求构造
│     • Prompt 模板的格式化
│     • 数据模型的验证
│
├─ 集成测试 (Integration)
│  └─ 测试模块间的协作
│     • 工作流链的串联
│     • API 端点的端到端流程
│
└─ 系统测试 (System)
   └─ 测试完整的应用
      • Docker Compose 启动 & 停止
      • 真实网络调用
      • 负载与并发测试
```

### 提供的测试脚本

| 脚本 | 用途 |
|------|------|
| `test_demo.py` | 本地单元测试（需要已启动的服务） |
| `test_client.py` | API 客户端集成测试 |

### 运行测试

```bash
# 本地测试 (需先启动服务)
python test_demo.py

# API 集成测试
python test_client.py

# 使用 pytest (高级)
pip install pytest pytest-asyncio
pytest tests/
```

---

## 🔄 工作流扩展指南

### 案例：添加"人物生成"工作流

**第 1 步：创建工作流类**

```python
# src/workflows/character.py
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from src.models.llm import get_llm

class CharacterGenerator:
    """人物档案生成器"""
    
    def __init__(self):
        self.llm = get_llm()
        self._setup_chains()
    
    def _setup_chains(self):
        # 链 1: 生成基础档案
        self.profile_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["name", "role"],
                template="""生成一个名叫 {name} 的 {role} 的人物档案。
                
包括：
- 基本信息（年龄、身份、背景）
- 性格特征（5 个关键词）
- 核心能力与缺陷
- 在故事中的作用

人物档案："""
            )
        )
        
        # 链 2: 外观描写
        self.appearance_chain = LLMChain(...)
    
    async def generate(self, name: str, role: str) -> dict:
        profile = await self.profile_chain.arun(name=name, role=role)
        appearance = await self.appearance_chain.arun(name=name, role=role)
        return {"profile": profile, "appearance": appearance}
```

**第 2 步：添加 API 端点**

```python
# src/api/routes.py
from src.workflows.character import CharacterGenerator

@router.post("/character")
async def generate_character(name: str, role: str):
    """生成人物档案"""
    generator = CharacterGenerator()
    result = await generator.generate(name, role)
    return {"name": name, "role": role, **result}
```

**第 3 步：更新数据模型**

```python
# src/api/schemas.py
class CharacterResponse(BaseModel):
    name: str
    role: str
    profile: str
    appearance: str
```

**第 4 步：测试**

```bash
curl -X POST "http://localhost:8001/character?name=张小凡&role=主角"
```

---

## 🚀 性能优化建议

### 1. Prompt 缓存

```python
class CachedOutlineGenerator(OutlineGenerator):
    """带缓存的大纲生成器"""
    
    def __init__(self):
        super().__init__()
        self.cache = {}  # {idea_hash: result}
    
    async def generate(self, idea: str):
        key = hash(idea)
        if key in self.cache:
            return self.cache[key]
        result = await super().generate(idea)
        self.cache[key] = result
        return result
```

### 2. 批处理

```python
async def generate_batch_outlines(ideas: List[str]):
    """并发生成多个大纲"""
    generator = OutlineGenerator()
    results = await asyncio.gather(
        *[generator.generate(idea) for idea in ideas]
    )
    return results
```

### 3. 流式响应

```python
@router.post("/outline/stream")
async def stream_outline(request: OutlineRequest):
    """流式返回生成过程"""
    generator = OutlineGenerator()
    
    async def event_generator():
        concept = await generator.concept_chain.arun(idea=request.idea)
        yield f"data: {json.dumps({'stage': 'concept', 'text': concept})}\n\n"
        
        outline = await generator.outline_chain.arun(concept=concept)
        yield f"data: {json.dumps({'stage': 'outline', 'text': outline})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

---

## 🔌 与 Nature AI 主项目的集成

### 集成点

```
Nature AI 主项目
  ├─ demo/ ← 当前项目（原型验证）
  │  ├─ src/models/llm.py → 可复用的 vLLM 适配器
  │  ├─ src/workflows/ → 工作流编排模式
  │  └─ src/api/ → FastAPI 应用框架
  │
  └─ src/core/ ← 后续迁移位置
     ├─ llm_adapters.py ← 从 demo/ 迁移
     ├─ agents.py ← CrewAI Agent 定义
     └─ workflows/ ← 复杂工作流编排
```

### 迁移路径

```
阶段 1（当前）编写 demo
  ↓
  学习和验证：vLLM + FastAPI + Langchain 的最佳实践
  
阶段 2：集成 CrewAI
  ↓
  扩展 demo 中的工作流到 CrewAI Agent 框架
  示例：OutlineGenerator → Architect Agent
  
阶段 3：添加 Neo4j 与 ReAct
  ↓
  集成图数据库与逻辑推理能力
  
阶段 4：完整系统
  ↓
  Nature AI 完整应用（含 MDL、LlamaIndex 等）
```

---

## 📊 成本分析

### 推理成本（vLLM 本地部署）

| 成本类别 | 详情 | 月成本 |
|----------|------|--------|
| **模型费用** | 开源模型（无 API 费） | ￥0 |
| **GPU 租赁** | V100 32GB (按小时) | ￥50-100 |
| **存储** | 模型权重 (7B-13B) | ￥1-5 |
| **总计** | | ￥50-100 |

vs. 使用 API 的成本：

```
Claude API:
100 个 1000-token 请求 × ¥0.10/1K-token = ¥10/天 = ¥300/月

Nature AI 本地部署:
一次性 GPU 租赁 = ¥50-100/月 (或购买设备)
```

---

## 📚 学习资源推荐

| 主题 | 资源 |
|------|------|
| **vLLM** | [官方文档](https://docs.vllm.ai) + [GitHub](https://github.com/vllm-project/vllm) |
| **FastAPI** | [官方教程](https://fastapi.tiangolo.com) + 《FastAPI 学习手册》 |
| **Langchain** | [官方文档](https://api.python.langchain.com) + [Cookbook](https://github.com/langchain-ai/langchain) |
| **异步 Python** | [Real Python 教程](https://realpython.com/async-io-python/) |

---

## ⚡ 故障排除

### 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| vLLM 连接失败 | vLLM 服务未启动 | `docker logs nature-ai-vllm` |
| 显存溢出 | 模型太大 | 使用更小的模型或启用量化 |
| 响应超时 | 推理耗时 | 增加 `max_tokens`，或使用流式响应 |
| Python 导入错误 | 依赖未安装 | `pip install -r requirements.txt` |

---

## 📝 总结

这个 demo 提供了一个**生产就绪的微型 AI 应用框架**，具有：

✅ **清晰的架构分层**（模型、工作流、API）
✅ **异步优先设计**（高并发、低延迟）
✅ **易于扩展**（添加新工作流无需修改核心）
✅ **完整的 Docker 支持**（本地和云端部署一致）
✅ **详细的文档与示例**（快速上手与二次开发）

是学习现代 LLM 应用开发的**不二选择**。

---

**Made with ❤️ for AI builders.**
