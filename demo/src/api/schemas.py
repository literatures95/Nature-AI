"""API 数据模型"""
from pydantic import BaseModel, Field
from typing import Optional


class OutlineRequest(BaseModel):
    """大纲生成请求"""
    idea: str = Field(..., description="创作灵感（50 字以内）", max_length=200)
    detailed: bool = Field(False, description="是否生成详细大纲")


class OutlineResponse(BaseModel):
    """大纲生成响应"""
    idea: str
    concept: str
    outline: str
    status: str
    word_count: int


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    version: str
    vllm_connected: bool
