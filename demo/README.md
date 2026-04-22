# Nature AI Demo

一个生产级别的 **vLLM + FastAPI + Langchain** 集成示例，展示如何构建本地 AI 应用。

## 📋 项目结构

```
demo/
├── src/
│   ├── api/              # FastAPI 应用
│   │   ├── main.py       # 应用入口
│   │   ├── routes.py     # API 路由
│   │   └── schemas.py    # 数据模型
│   ├── models/           # LLM 模型
│   │   └── llm.py        # vLLM 适配器
│   ├── workflows/        # AI 工作流
│   │   └── outline.py    # 大纲生成工作流
│   └── config.py         # 配置管理
├── config/
│   └── .env.example      # 环境变量示例
├── docker-compose.yml    # Docker 编排
├── requirements.txt      # Python 依赖
├── pyproject.toml        # 项目配置
└── README.md
```

## 🚀 关键技术

| 技术 | 用途 |
|------|------|
| **vLLM** | 高性能本地 LLM 推理服务 |
| **FastAPI** | 异步 Web 框架 |
| **Langchain** | LLM 工具链与工作流编排 |
| **Pydantic** | 数据验证与序列化 |

## 📦 快速开始

### 前置要求

- Docker & Docker Compose
- 或 Python 3.10+、pip
- GPU 推荐（CPU 模式会很慢）

### 方案 1: Docker Compose（推荐）

```bash
# 复制环境配置
cp config/.env.example config/.env

# 启动服务
docker-compose up

# 等待初始化（首次下载模型需要 5-10 分钟）
```

服务启动后：
- **API 文档**: http://localhost:8001/docs
- **健康检查**: http://localhost:8001/health
- **vLLM API**: http://localhost:8000/v1

### 方案 2: 本地开发

```bash
# 运行快速启动脚本
bash quickstart.sh

# 激活虚拟环境
source venv/bin/activate

# 方法 A: 使用 Docker 启动 vLLM（推荐）
docker run --gpus all -p 8000:8000 \
  -e MODEL_NAME=qwen/qwen2.5-7b-instruct \
  vllm/vllm-openai:latest

# 方法 B: 在另一个终端启动 FastAPI
python -m uvicorn src.api.main:app --reload --port 8001
```

## 🧪 测试 API

### 生成故事大纲

```bash
curl -X POST http://localhost:8001/outline \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "一个孤儿在仙侠世界中的成长故事",
    "detailed": false
  }'
```

**响应示例：**

```json
{
  "idea": "一个孤儿在仙侠世界中的成长故事",
  "concept": "张小凡失去双亲后进入青云寺修仙...",
  "outline": "第一幕 (起) - 引入设定与主角：\n山中小寺...",
  "status": "success",
  "word_count": 1245
}
```

### 健康检查

```bash
curl http://localhost:8001/health
```

## 🏗 核心组件详解

### 1. vLLM 服务 (`src/models/llm.py`)

基于 vLLM 的 LLM 适配器，用 Langchain 自定义 LLM 类：

```python
from src.models.llm import get_llm

llm = get_llm()  # 自动连接 vLLM
response = llm.invoke("讲一个故事...")
```

特点：
- ✅ 支持异步调用 (`_acall`)
- ✅ 自动重试与错误处理
- ✅ 可配置的温度、max_tokens 等参数

### 2. Langchain 工作流 (`src/workflows/outline.py`)

多链工作流，将"灵感"-->>"大纲"的过程分成两步：

```python
from src.workflows.outline import get_outline_generator

generator = get_outline_generator()

# 同步调用
result = generator.generate_sync(idea="...")

# 异步调用
result = await generator.generate(idea="...")
```

工作流流程：
```
输入灵感 
  → 链 1: 扩展概念 (200 字核心概念)
  → 链 2: 生成大纲 (五幕式完整大纲)
  → 输出结构化结果
```

### 3. FastAPI 应用 (`src/api/main.py`)

异步 REST API，提供两个核心端点：

```
GET  /health        ← 健康检查 + vLLM 连接状态
POST /outline       ← 生成大纲
GET  /              ← 元信息
```

## 🔧 环境配置

编辑 `config/.env`：

```env
# vLLM 设置
VLLM_HOST=http://localhost
VLLM_PORT=8000
VLLM_MODEL=qwen2.5-7b-instruct

# FastAPI 设置
API_HOST=0.0.0.0
API_PORT=8001
LOG_LEVEL=info
```

## 📊 模型选择

当前使用 **Qwen 2.5 7B Instruct**：

| 方面 | 评价 |
|------|------|
| **推理速度** | ⭐⭐⭐⭐ (1-2 秒/512 token) |
| **质量** | ⭐⭐⭐⭐ (适合创意写作) |
| **VRAM** | ⭐⭐⭐⭐ (14GB) |
| **成本** | ⭐⭐⭐⭐⭐ (免费本地部署) |

**其他推荐模型：**
- `mistral-7b-instruct` - 快速通用模型
- `llama2-13b-chat` - Meta 高质量模型
- `neural-chat-7b` - Intel 优化模型

## 🚦 监控与调试

### 查看日志

```bash
# Docker Compose
docker-compose logs -f api
docker-compose logs -f vllm

# 本地
# FastAPI 会自动打印日志到控制台
```

### vLLM GPU 监控

```bash
# 实时 GPU 使用情况
docker exec nature-ai-vllm nvidia-smi

# 或如果在本地运行
nvidia-smi -l 1  # 每秒更新一次
```

### API 文档

访问 http://localhost:8001/docs（Swagger UI）查看完整的 API 文档。

## 🔌 扩展示例

### 添加新的工作流

1. 在 `src/workflows/` 中创建新文件
2. 定义 Langchain 链
3. 在 `src/api/routes.py` 中添加新端点

```python
# src/workflows/character.py
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from src.models.llm import get_llm

class CharacterGenerator:
    def __init__(self):
        self.llm = get_llm()
        self.prompt = PromptTemplate(...)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    async def generate(self, name: str):
        return await self.chain.arun(name=name)
```

### 切换不同的 LLM

编辑 `config/.env`：

```env
# 使用 Mistral
VLLM_MODEL=mistral-7b-instruct

# 或使用 Llama 2
VLLM_MODEL=meta-llama/Llama-2-13b-chat-hf
```

重启 vLLM 服务即可。

## 📈 性能优化建议

| 优化项 | 方法 |
|--------|------|
| **推理速度** | 使用量化模型（GGUF）、减少 max_tokens |
| **吞吐量** | 启用 vLLM 的批处理 (`batch_size=4`) |
| **内存** | 使用 4-bit 或 8-bit 量化 |
| **延迟** | 启用 `tensor_parallel` 多 GPU 分布式 |

## ⚠️ 常见问题

**Q: 首次启动很慢？**
A: 正常。vLLM 需要从 Hugging Face 下载模型（7B 模型约 14GB）。首次下载需要 5-10 分钟。

**Q: 显存溢出？**
A: 使用更小的模型或启用量化。编辑 `docker-compose.yml`：
```yaml
environment:
  - DTYPE=float8  # 改为 float8 或 bfloat16
```

**Q: 离线使用？**
A: 预先下载模型到本地：
```bash
# 方法 1: 使用 Hugging Face 提供的脚本
huggingface-cli download qwen/qwen2.5-7b-instruct

# 方法 2: 编辑 docker-compose.yml，挂载本地模型目录
volumes:
  - /path/to/models:/root/.cache/huggingface
```

**Q: 如何使用多个 GPU？**
A: 编辑 `docker-compose.yml`：
```yaml
environment:
  - TENSOR_PARALLEL_SIZE=2  # 使用 2 个 GPU
  - PIPELINE_PARALLEL_SIZE=1
```

## 📚 推荐阅读

- [vLLM 官方文档](https://docs.vllm.ai)
- [FastAPI 官方文档](https://fastapi.tiangolo.com)
- [Langchain 官方文档](https://python.langchain.com)
- [Qwen 2.5 模型卡](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct)

## 📝 下一步开发

这个 demo 已为后续开发奠定基础。可继续扩展：

1. ✅ **当前**: 灵感 → 大纲工作流
2. 📝 **下一步**: 
   - 大纲 → 初稿写作工作流（使用长上下文窗口）
   - 逻辑审计工作流（基于 ReAct）
   - 知识图谱集成（Neo4j）
   - 向量 RAG（Milvus + LlamaIndex）

## 📄 许可证

MIT License

---

**Made with ❤️ for writers and AI builders.**
