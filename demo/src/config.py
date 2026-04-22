"""配置管理模块"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置类"""
    
    # vLLM 设置
    vllm_host: str = "http://localhost"
    vllm_port: int = 8000
    vllm_model: str = "qwen2.5-7b-instruct"
    
    # FastAPI 设置
    api_host: str = "0.0.0.0"
    api_port: int = 8001
    log_level: str = "info"
    
    @property
    def vllm_url(self) -> str:
        """获取 vLLM API 完整 URL"""
        return f"{self.vllm_host}:{self.vllm_port}/v1"
    
    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 全局配置实例
settings = Settings()
