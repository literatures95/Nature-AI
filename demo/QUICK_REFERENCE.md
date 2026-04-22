# 🚀 Nature AI Demo - 快速参考卡片

## 5 秒速记

```
一个完整的 vLLM + FastAPI + Langchain 原型应用
├─ 本地 LLM 推理服务（Qwen 2.5）
├─ 异步 REST API（FastAPI）
├─ Langchain 多链工作流
├─ Docker 完整编排
└─ 5 份详细文档 + 测试脚本
```

---

## ⚡ 30 秒快速启动

```bash
cd demo
docker-compose up
```

完成！API 已在 http://localhost:8001 运行。

---

## 🎯 核心命令速查

| 命令 | 功能 |
|------|------|
| `docker-compose up` | 启动所有服务 |
| `docker-compose down` | 停止服务 |
| `docker-compose logs -f` | 查看日志 |
| `curl http://localhost:8001/health` | 健康检查 |
| `python test_client.py` | API 测试 |
| `bash quickstart.sh` | 本地开发设置 |

---

## 📚 文档速查

| 需求 | 阅读 |
|------|------|
| "我想快速启动" | [DEMO_QUICKSTART.md](../../DEMO_QUICKSTART.md) |
| "我想了解项目" | [demo/README.md](README.md) |
| "我想学习架构" | [demo/TECHNICAL_DESIGN.md](TECHNICAL_DESIGN.md) |
| "我想浏览代码" | [demo/PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) |
| "我想看总结" | [demo/COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md) |

---

## 🔗 API 端点速查

```bash
# 健康检查
GET /health

# 生成故事大纲
POST /outline
Body: {"idea": "...", "detailed": false}

# 根路由（元信息）
GET /

# Swagger 文档
GET /docs
```

---

## 📁 文件树速查

```
demo/
├── src/
│   ├── models/llm.py           ← vLLM 适配器
│   ├── workflows/outline.py    ← Langchain 工作流
│   ├── api/
│   │   ├── main.py             ← FastAPI 应用
│   │   ├── routes.py           ← API 定义
│   │   └── schemas.py          ← 数据模型
│   └── config.py               ← 配置管理
│
├── docker-compose.yml          ← Docker 编排
├── requirements.txt            ← 依赖列表
│
├── README.md                   ← 项目指南
├── TECHNICAL_DESIGN.md         ← 技术设计
├── PROJECT_STRUCTURE.md        ← 代码导航
└── test_client.py              ← API 测试
```

---

## 🧪 测试速查

```bash
# API 集成测试
python test_client.py

# 本地单元测试
python test_demo.py

# 手动测试
curl -X POST http://localhost:8001/outline \
  -H "Content-Type: application/json" \
  -d '{"idea": "一个仙侠故事"}'
```

---

## 💻 开发者快速入门

```bash
# 1. 进入项目
cd demo

# 2. 本地设置
bash quickstart.sh
source venv/bin/activate

# 3. 启动 vLLM (终端 1)
docker run --gpus all -p 8000:8000 \
  -e MODEL_NAME=qwen/qwen2.5-7b-instruct \
  vllm/vllm-openai:latest

# 4. 启动 FastAPI (终端 2)
python -m uvicorn src.api.main:app --reload

# 5. 查看文档
# 访问 http://localhost:8001/docs
```

---

## 🔧 环境变量速查

```env
# vLLM 配置
VLLM_HOST=http://localhost
VLLM_PORT=8000
VLLM_MODEL=qwen2.5-7b-instruct

# FastAPI 配置
API_HOST=0.0.0.0
API_PORT=8001
LOG_LEVEL=info
```

---

## 🐛 故障排除速查

| 问题 | 解决 |
|------|------|
| vLLM 连接失败 | `docker logs nature-ai-vllm` |
| API 超时 | 等待 vLLM 完成首次推理（30-60 秒） |
| 显存溢出 | 使用更小的模型或量化 |
| Python 导入错误 | `pip install -r requirements.txt` |
| Docker 错误 | `docker system prune` 清理 |

---

## 📊 关键数字

- **文件数**: 21 个
- **代码行数**: ~450 行
- **文档行数**: 1500+ 行
- **模块数**: 6 个
- **依赖数**: 10 个
- **API 端点**: 3 个
- **Langchain 链**: 2 个
- **Docker 服务**: 2 个

---

## 🎯 使用场景

✅ 学习 vLLM + Langchain 集成
✅ 快速原型开发
✅ 本地 AI 应用部署
✅ Nature AI 主项目的技术验证
✅ 团队培训与技术分享

---

## ✨ 主要特性

- ✅ 异步优先设计（100+ 并发）
- ✅ 类型安全（Pydantic）
- ✅ 自动文档生成（Swagger）
- ✅ 分层架构（易扩展）
- ✅ Docker 一键启动
- ✅ 完整的错误处理
- ✅ 生产级代码质量

---

## 🔄 进度追踪

```
✅ 项目创建完成
├─ ✅ 核心模块 (6 个 Python 文件)
├─ ✅ 配置与依赖 (4 个文件)
├─ ✅ Docker 编排 (2 个文件)
├─ ✅ 完整文档 (5 份文档)
├─ ✅ 测试脚本 (2 个脚本)
└─ ✅ 快速参考 (本文件)

下一步：
→ 启动应用: docker-compose up
→ 测试 API: curl http://localhost:8001/health
→ 查看文档: http://localhost:8001/docs
```

---

## 💡 小贴士

1. **首次启动会很慢** - vLLM 需要下载和加载模型（5-10 分钟）
2. **使用 GPU 更快** - CPU 推理会很慢
3. **检查显存** - 7B 模型需要 14-16GB VRAM
4. **查看日志** - `docker-compose logs -f` 实时跟踪
5. **离线使用** - 可以提前下载模型到本地

---

## 🎓 学习路径

```
0. 启动应用 (5 分钟)
   ↓
1. 了解架构 (20 分钟)
   ↓
2. 修改 Prompt (10 分钟)
   ↓
3. 添加新工作流 (30 分钟)
   ↓
4. 性能优化 (1 小时)
   ↓
5. 集成到主项目 (几小时)
```

---

## 📞 需要帮助?

1. 查看相关文档（见上面的文档速查表）
2. 运行测试脚本：`python test_client.py`
3. 检查 Docker 日志：`docker-compose logs`
4. 查看 Swagger API 文档：http://localhost:8001/docs

---

## 🏁 现在就开始!

```bash
cd demo && docker-compose up
```

然后访问: **http://localhost:8001/docs**

---

**Happy coding! 🚀**

---

| 快速链接 | URL |
|---------|-----|
| API 文档 | http://localhost:8001/docs |
| 健康检查 | http://localhost:8001/health |
| 项目仓库 | github.com/literatures95/Nature-AI |
| vLLM 官方 | https://docs.vllm.ai |
| FastAPI 官方 | https://fastapi.tiangolo.com |
