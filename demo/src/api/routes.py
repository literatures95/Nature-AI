"""API 路由定义"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.api.schemas import OutlineRequest, OutlineResponse, HealthResponse
from src.workflows.outline import get_outline_generator
import httpx
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查端点"""
    from src.config import settings
    
    # 尝试连接 vLLM
    vllm_ok = False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.vllm_url}/models")
            vllm_ok = response.status_code == 200
    except Exception as e:
        logger.warning(f"vLLM connection check failed: {e}")
    
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        vllm_connected=vllm_ok
    )


@router.post("/outline", response_model=OutlineResponse)
async def generate_outline(request: OutlineRequest):
    """
    生成故事大纲端点
    
    请求示例：
    ```json
    {
        "idea": "一个孤儿在仙侠世界中的成长故事",
        "detailed": false
    }
    ```
    """
    try:
        generator = get_outline_generator()
        result = await generator.generate(
            idea=request.idea,
            detailed=request.detailed
        )
        return OutlineResponse(**result)
    except Exception as e:
        logger.error(f"Error generating outline: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def root():
    """根端点"""
    return {
        "name": "Nature AI Demo - vLLM + FastAPI + Langchain",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "generate_outline": "/outline",
            "docs": "/docs"
        }
    }
