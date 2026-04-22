#!/bin/bash

# Nature AI Demo 快速启动脚本

set -e

echo "=========================================="
echo "Nature AI Demo - vLLM + FastAPI + Langchain"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查依赖
echo -e "${BLUE}[1/4]${NC} 检查依赖..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 未安装${NC}"
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo -e "${RED}✗ pip 未安装${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 和 pip 已检查${NC}"

# 创建虚拟环境
echo -e "${BLUE}[2/4]${NC} 设置虚拟环境..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ 虚拟环境已创建${NC}"
else
    echo -e "${GREEN}✓ 虚拟环境已存在${NC}"
fi

source venv/bin/activate

# 安装依赖
echo -e "${BLUE}[3/4]${NC} 安装 Python 依赖..."
pip install -q -r requirements.txt
echo -e "${GREEN}✓ 依赖已安装${NC}"

# 复制配置文件
echo -e "${BLUE}[4/4]${NC} 配置环境..."

if [ ! -f "config/.env" ]; then
    cp config/.env.example config/.env
    echo -e "${GREEN}✓ .env 文件已创建${NC}"
else
    echo -e "${GREEN}✓ .env 文件已存在${NC}"
fi

echo ""
echo -e "${GREEN}=========================================="
echo "启动完成！"
echo "==========================================${NC}"
echo ""
echo -e "${YELLOW}选项 1: 使用 Docker Compose（推荐）${NC}"
echo "  $ docker-compose up"
echo ""
echo -e "${YELLOW}选项 2: 本地启动（需手动启动 vLLM）${NC}"
echo "  # 终端 1: 启动 vLLM"
echo "  $ docker run --gpus all -p 8000:8000 \\"
echo "      -e MODEL_NAME=qwen/qwen2.5-7b-instruct \\"
echo "      vllm/vllm-openai:latest"
echo ""
echo "  # 终端 2: 启动 FastAPI"
echo "  $ source venv/bin/activate"
echo "  $ python -m uvicorn src.api.main:app --reload"
echo ""
echo -e "${YELLOW}原型已就绪！${NC}"
echo "API 文档: http://localhost:8001/docs"
echo "健康检查: curl http://localhost:8001/health"
echo ""
echo -e "${BLUE}快速测试:${NC}"
echo "curl -X POST http://localhost:8001/outline \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"idea\": \"一个孤儿在仙侠世界中的成长故事\"}'"
