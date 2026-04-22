"""LLM 模型适配器 - 集成 vLLM"""
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from typing import Optional, List, Any
import httpx
import json
import asyncio
from src.config import settings


class VLLMAdapter(LLM):
    """vLLM 本地推理服务适配器"""
    
    model_name: str = settings.vllm_model
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float = 0.9
    
    @property
    def _llm_type(self) -> str:
        return "vllm"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """同步调用 vLLM API"""
        response = self._make_request(prompt)
        return response
    
    def _make_request(self, prompt: str) -> str:
        """发送请求到 vLLM 服务"""
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    f"{settings.vllm_url}/completions",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "temperature": self.temperature,
                        "max_tokens": self.max_tokens,
                        "top_p": self.top_p,
                        "stop": ["<|end|>", "[END]"],
                    }
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["text"].strip()
        except Exception as e:
            return f"Error calling vLLM: {str(e)}"
    
    async def _acall(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """异步调用 vLLM API"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._make_request, prompt)


def get_llm() -> VLLMAdapter:
    """工厂函数 - 获取 LLM 实例"""
    return VLLMAdapter(
        model_name=settings.vllm_model,
        temperature=0.7,
        max_tokens=1024,
    )
