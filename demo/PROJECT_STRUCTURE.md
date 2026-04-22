# Nature AI Demo - 项目结构与参考手册

## 📁 完整项目结构

```
Nature-AI/
│
├── README.md                          # 主项目文档
├── DEMO_QUICKSTART.md                 # ← demo 快速启动指南（从这里开始）
│
└── demo/                              # ← vLLM + FastAPI + Langchain 原型
    ├── README.md                      # demo 完整文档
    ├── TECHNICAL_DESIGN.md            # 技术设计文档
    ├── PROJECT_STRUCTURE.md           # 本文件
    │
    ├── pyproject.toml                 # 项目配置 (Python 3.11+)
    ├── requirements.txt               # 简单依赖列表
    │
    ├── config/
    │   └── .env.example               # 环境变量模板
    │
    ├── Dockerfile                     # FastAPI 容器定义
    ├── docker-compose.yml             # 完整编排配置
    │
    ├── src/                           # 核心源代码
    │   ├── __init__.py
    │   ├── config.py                  # 配置管理
    │   │
    │   ├── models/                    # LLM 模型层
    │   │   ├── __init__.py
    │   │   └── llm.py                 # vLLM 适配器 ⭐
    │   │
    │   ├── workflows/                 # AI 工作流层
    │   │   ├── __init__.py
    │   │   └── outline.py             # 大纲生成工作流 ⭐
    │   │
    │   └── api/                       # FastAPI 应用层
    │       ├── __init__.py
    │       ├── main.py                # 应用初始化 ⭐
    │       ├── routes.py              # API 路由定义 ⭐
    │       └── schemas.py             # 数据模型
    │
    ├── quickstart.sh                  # 快速启动脚本
    ├── test_demo.py                   # 单元测试脚本
    ├── test_client.py                 # API 客户端测试脚本
    │
    └── .gitignore                     # Git 忽略规则
```

## 🎯 快速导航

### 对于新用户

1. **首先阅读** → [DEMO_QUICKSTART.md](../../DEMO_QUICKSTART.md)（5 分钟）
2. **启动应用** → `docker-compose up` 或 `bash quickstart.sh`
3. **测试 API** → `curl http://localhost:8001/health`
4. **查看文档** → http://localhost:8001/docs (Swagger UI)

### 对于开发者

1. **理解架构** → 阅读 [TECHNICAL_DESIGN.md](TECHNICAL_DESIGN.md)
2. **查看核心代码**：
   - LLM 集成：[src/models/llm.py](src/models/llm.py)
   - 工作流：[src/workflows/outline.py](src/workflows/outline.py)
   - API 定义：[src/api/routes.py](src/api/routes.py)
3. **本地开发** → 编辑源代码，FastAPI 支持热重载

### 对于 DevOps

1. **Docker 部署** → [docker-compose.yml](docker-compose.yml)
2. **环境配置** → [config/.env.example](config/.env.example)
3. **监控** → `docker-compose logs -f`

---

## 📚 文件详解

### 配置与入口文件

| 文件 | 行数 | 说明 |
|------|------|------|
| `pyproject.toml` | ~30 | Poetry/PEP 517 项目配置 |
| `requirements.txt` | ~10 | pip 依赖列表 |
| `config/.env.example` | ~6 | 环境变量模板 |

### 源代码（核心）

| 文件 | 行数 | 功能 | 复杂度 |
|------|------|------|--------|
| `src/config.py` | ~25 | 配置加载与管理 | ⭐ |
| `src/models/llm.py` | ~70 | vLLM 适配器 | ⭐⭐⭐ |
| `src/workflows/outline.py` | ~90 | Langchain 多链工作流 | ⭐⭐⭐ |
| `src/api/main.py` | ~45 | FastAPI 应用初始化 | ⭐⭐ |
| `src/api/routes.py` | ~60 | API 路由与业务逻辑 | ⭐⭐ |
| `src/api/schemas.py` | ~30 | Pydantic 数据模型 | ⭐ |

**复杂度说明：**
- ⭐ 初学者友好（逻辑简单，容易理解）
- ⭐⭐ 中等（涉及设计模式或异步概念）
- ⭐⭐⭐ 进阶（涉及系统集成、性能优化）

### Docker & 部署

| 文件 | 说明 |
|------|------|
| `Dockerfile` | FastAPI 容器定义 |
| `docker-compose.yml` | vLLM + FastAPI 完整编排 |
| `.gitignore` | Git 忽略规则 |

### 文档 & 示例

| 文件 | 说明 | 读者 |
|------|------|------|
| `README.md` | 项目完整指南 | 所有人 |
| `TECHNICAL_DESIGN.md` | 详细技术设计 | 开发者 |
| `PROJECT_STRUCTURE.md` | 本文件 | 开发者 |
| `test_demo.py` | 本地单元测试 | 开发者 |
| `test_client.py` | API 客户端测试 | QA / 集成测试 |

---

## 🔄 工作流图

### 启动流程

```
1. 环境准备
   ├─ docker-compose.yml 定义了什么要启动
   └─ config/.env.example 定义了配置项
        │
        ↓

2. Docker 启动
   ├─ vllm 容器
   │  ├─ 下载 Qwen 2.5 7B 模型 (首次)
   │  └─ 加载到 GPU，启动 OpenAI 兼容 API
   │
   └─ api 容器
      ├─ 安装 Python 依赖
      └─ 启动 FastAPI 应用
        │
        ↓

3. 应用初始化 (src/api/main.py)
   ├─ 创建 FastAPI 实例
   ├─ 添加 CORS 中间件
   └─ 注册路由 (routes.py)
        │
        ↓

4. 就绪
   └─ 接受客户端请求
```

### 请求处理流程

```
客户端请求
  │
  ├─ POST /outline
  │  ├─ Content-Type: application/json
  │  └─ Body: {"idea": "...", "detailed": false}
  │
  ↓
FastAPI 路由处理 (src/api/routes.py)
  │
  ├─ 验证请求数据 (Pydantic)
  ├─ 错误处理
  └─ 调用工作流
  │
  ↓
Langchain 工作流 (src/workflows/outline.py)
  │
  ├─ 获取 LLM 实例
  ├─ 链 1: 概念扩展
  │  └─ 调用 llm.arun(prompt)
  │
  └─ 链 2: 大纲生成
     └─ 调用 llm.arun(prompt)
  │
  ↓
vLLM 适配器 (src/models/llm.py)
  │
  ├─ 构造请求到 vLLM API
  ├─ 异步 HTTP 调用
  └─ 解析响应
  │
  ↓
vLLM 推理服务
  │
  ├─ 接收 OpenAI 兼容 API 请求
  ├─ 模型推理
  └─ 流式返回 Token
  │
  ↓
响应处理
  │
  ├─ 聚合工作流结果
  ├─ 序列化到 JSON
  └─ 返回 HTTP 200
  │
  ↓
客户端收到响应
```

---

## 🔑 关键代码片段

### 1. 配置管理

```python
# src/config.py
class Settings(BaseSettings):
    vllm_host: str = "http://localhost"
    vllm_port: int = 8000
    @property
    def vllm_url(self) -> str:
        return f"{self.vllm_host}:{self.vllm_port}/v1"

settings = Settings()  # 全局实例
```

### 2. LLM 初始化

```python
# src/models/llm.py
class VLLMAdapter(LLM):
    async def _acall(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.vllm_url}/completions",
                json={"model": self.model_name, "prompt": prompt}
            )
        return response.json()["choices"][0]["text"]

llm = VLLMAdapter()
```

### 3. Langchain 链定义

```python
# src/workflows/outline.py
self.concept_chain = LLMChain(
    llm=self.llm,
    prompt=PromptTemplate(
        input_variables=["idea"],
        template="扩展这个创意: {idea}"
    )
)

concept = await self.concept_chain.arun(idea="...")
```

### 4. FastAPI 路由

```python
# src/api/routes.py
@router.post("/outline")
async def generate_outline(request: OutlineRequest):
    generator = get_outline_generator()
    result = await generator.generate(request.idea)
    return OutlineResponse(**result)
```

---

## 🧪 测试运行

### 单元测试 (本地)

```bash
python test_demo.py
```

输出示例：
```
==================================================
Nature AI Demo - 本地测试
==================================================

[测试 1] LLM 基础连接...
  LLM 类型: vllm
  模型: qwen2.5-7b-instruct
  ✓ LLM 已初始化

[测试 2] 大纲生成器...
  输入: 一个少年在魔法学院的冒险
  ✓ 大纲生成成功
  概念: 主角因机缘进入魔法学院...
  字数: 1245

==================================================
所有测试完成！
==================================================
```

### API 集成测试

```bash
python test_client.py
```

### 手动测试

```bash
# 健康检查
curl http://localhost:8001/health

# 生成大纲
curl -X POST http://localhost:8001/outline \
  -H "Content-Type: application/json" \
  -d '{"idea": "一个孤儿的仙侠之旅"}' | jq .
```

---

## 📈 代码复杂度分析

### 循环复杂度 (Cyclomatic Complexity)

```
src/models/llm.py:VLLMAdapter._make_request    - CC: 3  (低)
src/workflows/outline.py:OutlineGenerator      - CC: 2  (低)
src/api/routes.py:generate_outline             - CC: 3  (低)
```

**结论**: 代码设计简洁，不存在过度嵌套。

---

## 🚀 扩展建议

### 短期（1-2 周）

- [ ] 添加日志系统 (logging)
- [ ] 实现请求缓存
- [ ] 添加更多工作流 (人物、地点等)

### 中期（1 个月）

- [ ] 集成数据库存储结果
- [ ] 实现用户认证 (JWT)
- [ ] 添加速率限制

### 长期（3 个月+）

- [ ] 迁移到 CrewAI Agent 框架
- [ ] 集成 Neo4j 知识图谱
- [ ] 添加 LlamaIndex RAG 能力

---

## 💡 最佳实践

### 代码风格

```python
# ✅ 好的实践
class OutlineGenerator:
    def __init__(self):
        self.llm = get_llm()  # 依赖注入
    
    async def generate(self, idea: str) -> dict:  # 类型提示
        """生成故事大纲。"""  # 文档字符串
        return await self._run_chains(idea)

# ❌ 避免
def generate(idea):
    llm = VLLMAdapter()  # 直接创建，难以测试
    return llm.call(idea)
```

### 异步编程

```python
# ✅ 好的实践
async def generate(self, idea: str):
    return await self.llm.arun(prompt)  # 使用 async/await

# ❌ 避免
def generate(self, idea: str):
    return self.llm.invoke(prompt)  # 同步调用会阻塞
```

### 错误处理

```python
# ✅ 好的实践
try:
    response = await self.llm._acall(prompt)
except httpx.TimeoutException:
    return "推理超时，请重试"
except Exception as e:
    log.error(f"错误: {e}")
    raise

# ❌ 避免
response = self.llm._acall(prompt)  # 无错误处理
```

---

## 🔗 相关资源

### 内部文档

- [TECHNICAL_DESIGN.md](TECHNICAL_DESIGN.md) - 深度技术设计
- [README.md](README.md) - 项目完整指南
- [../../README.md](../../README.md) - Nature AI 主项目

### 外部资源

- [vLLM 官方文档](https://docs.vllm.ai)
- [FastAPI 教程](https://fastapi.tiangolo.com)
- [Langchain Python 文档](https://api.python.langchain.com)

---

## 📞 支持与反馈

如有问题，请：

1. 查看 [README.md](README.md) 的 FAQ 部分
2. 检查 Docker 日志：`docker-compose logs`
3. 运行测试脚本：`python test_client.py`
4. 提交 Issue 到 GitHub

---

**Happy coding! 🚀**

*Made with ❤️ for AI builders.*
