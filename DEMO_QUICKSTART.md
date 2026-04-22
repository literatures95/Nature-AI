# Nature AI Demo - 快速开始指南

## 🎯 5 分钟入门

### 前置要求
- Docker & Docker Compose
- （可选）GPU（推荐）或至少 16GB RAM

### 启动

```bash
cd demo

# 方式 1: 一键启动（推荐）
docker-compose up

# 方式 2: 本地开发
bash quickstart.sh
source venv/bin/activate
python -m uvicorn src.api.main:app --reload
```

### 测试

```bash
# API 健康检查
curl http://localhost:8001/health

# 生成故事大纲
curl -X POST http://localhost:8001/outline \
  -H "Content-Type: application/json" \
  -d '{"idea": "一个孤儿在仙侠世界的成长"}'
```

## 📚 架构概览

```
用户输入
  ↓
FastAPI (Port 8001)
  ↓
Langchain 工作流
  ↓
vLLM API (Port 8000) ← 本地 LLM 推理
  ↓
Qwen 2.5 7B Model ← GPU/CPU 推理
  ↓
结构化输出 (JSON)
```

## 🔑 关键代码文件

| 文件 | 功能 |
|------|------|
| `src/api/main.py` | FastAPI 应用主文件 |
| `src/api/routes.py` | API 路由定义 |
| `src/models/llm.py` | vLLM 适配器 |
| `src/workflows/outline.py` | 大纲生成工作流 |
| `docker-compose.yml` | Docker 编排配置 |

## 🚀 下一步

1. 阅读 `demo/README.md` 了解详细内容
2. 修改 `src/workflows/outline.py` 自定义 Prompt
3. 在 `src/api/routes.py` 中添加新的 API 端点
4. 集成到主项目的 Nature AI 系统中

## 💬 API 文档

启动后访问: http://localhost:8001/docs (Swagger UI)

---

更多信息详见 [demo/README.md](demo/README.md)
