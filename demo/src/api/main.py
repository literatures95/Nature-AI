"""FastAPI 应用入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from src.api.routes import router
from src.config import settings

# 配置日志
logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="Nature AI Demo",
    description="vLLM + FastAPI + Langchain 集成示例",
    version="0.1.0",
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info(f"启动应用，连接到 vLLM: {settings.vllm_url}")
    logger.info(f"API 运行在 http://{settings.api_host}:{settings.api_port}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("应用关闭")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
    )
