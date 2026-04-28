from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import openai
import anthropic
import httpx
import os

class LLMAdapter(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass

class OpenAIAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str = "gpt-4o", base_url: Optional[str] = None):
        init_args = {"api_key": api_key}
        if base_url:
            init_args["base_url"] = base_url
        self.client = openai.AsyncOpenAI(**init_args)
        self.model = model

    async def generate(self, prompt: str, **kwargs) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get("max_tokens", 1000),
            temperature=kwargs.get("temperature", 0.7),
        )
        return response.choices[0].message.content

class ClaudeAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", base_url: Optional[str] = None):
        init_args = {"api_key": api_key}
        if base_url:
            init_args["base_url"] = base_url
        self.client = anthropic.AsyncAnthropic(**init_args)
        self.model = model

    async def generate(self, prompt: str, **kwargs) -> str:
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 1000),
            temperature=kwargs.get("temperature", 0.7),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

class AlibabaAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str = "qwen2.5-72b-instruct", base_url: Optional[str] = None):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url or "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    async def generate(self, prompt: str, **kwargs) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "input": {
                "messages": [{"role": "user", "content": prompt}]
            },
            "parameters": {
                "max_tokens": kwargs.get("max_tokens", 1000),
                "temperature": kwargs.get("temperature", 0.7)
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result["output"]["text"]

class ModelRouter:
    def __init__(self, config_path: str, provider_manager: Optional[Any] = None):
        import yaml
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.adapters = self._init_adapters()
        self.provider_manager = provider_manager

    def _init_adapters(self):
        adapters = {}
        for model_name, model_config in self.config['model_registry']['llm'].items():
            provider = model_config['provider']
            if provider == 'openai':
                api_key = os.getenv('OPENAI_API_KEY')
                if api_key:
                    adapters[model_name] = OpenAIAdapter(api_key, model_name)
            elif provider == 'anthropic':
                api_key = os.getenv('ANTHROPIC_API_KEY')
                if api_key:
                    adapters[model_name] = ClaudeAdapter(api_key, model_name)
            elif provider == 'alibaba':
                api_key = os.getenv('ALIBABA_API_KEY')
                if api_key:
                    adapters[model_name] = AlibabaAdapter(api_key, model_name)
        return adapters

    def _create_adapter_for_provider(self, provider: Dict[str, Any]) -> Optional[LLMAdapter]:
        if not provider:
            return None
        provider_type = provider.get('provider')
        api_key = provider.get('apiKey') or provider.get('api_key')
        model = provider.get('model') or 'gpt-4o'
        base_url = provider.get('baseUrl') or provider.get('base_url')
        if not api_key or not provider_type:
            return None
        if provider_type == 'openai':
            return OpenAIAdapter(api_key, model, base_url)
        if provider_type == 'anthropic':
            return ClaudeAdapter(api_key, model, base_url)
        if provider_type == 'alibaba':
            return AlibabaAdapter(api_key, model, base_url)
        return None

    def get_adapter(self, task_type: str = "general", provider_id: Optional[str] = None) -> Optional[LLMAdapter]:
        provider = None
        if provider_id and self.provider_manager:
            provider = self.provider_manager.get_provider(provider_id)
        elif self.provider_manager:
            provider = self.provider_manager.get_active_provider()

        if provider:
            adapter = self._create_adapter_for_provider(provider)
            if adapter:
                return adapter

        route = self.config["route_strategy"].get(task_type, {})
        primary_model = route.get("primary")
        if primary_model in self.adapters:
            return self.adapters[primary_model]

        for adapter in self.adapters.values():
            return adapter
        return None