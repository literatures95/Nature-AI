FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
COPY pyproject.toml .
COPY src ./src
COPY config ./config

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8001

# 默认命令
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8001"]
