import json
import os
import uuid
from typing import Any, Dict, List, Optional

DEFAULT_CONFIG = {
    "activeProvider": None,
    "providers": []
}

class ProviderManager:
    def __init__(self, config_path: str = "/workspaces/Nature-AI/config/providers.json"):
        self.config_path = config_path
        self._ensure_config_file()

    def _ensure_config_file(self):
        dir_path = os.path.dirname(self.config_path)
        os.makedirs(dir_path, exist_ok=True)
        if not os.path.exists(self.config_path):
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)

    def _load(self) -> Dict[str, Any]:
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: Dict[str, Any]) -> None:
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def list_providers(self) -> List[Dict[str, Any]]:
        data = self._load()
        active_id = data.get("activeProvider")
        providers = data.get("providers", [])
        for provider in providers:
            provider["active"] = provider.get("id") == active_id
        return providers

    def get_provider(self, provider_id: str) -> Optional[Dict[str, Any]]:
        providers = self._load().get("providers", [])
        for provider in providers:
            if provider.get("id") == provider_id:
                return provider
        return None

    def add_provider(self, provider_data: Dict[str, Any]) -> Dict[str, Any]:
        data = self._load()
        providers = data.get("providers", [])
        provider_id = provider_data.get("id") or str(uuid.uuid4())
        provider = {
            "id": provider_id,
            "name": provider_data.get("name", "Unnamed Provider"),
            "provider": provider_data.get("provider"),
            "apiKey": provider_data.get("apiKey"),
            "model": provider_data.get("model"),
            "baseUrl": provider_data.get("baseUrl"),
            "notes": provider_data.get("notes", "")
        }
        providers.append(provider)
        data["providers"] = providers
        self._save(data)
        return provider

    def update_provider(self, provider_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        data = self._load()
        updated = None
        for idx, provider in enumerate(data.get("providers", [])):
            if provider.get("id") == provider_id:
                provider.update({
                    "name": updates.get("name", provider.get("name")),
                    "provider": updates.get("provider", provider.get("provider")),
                    "apiKey": updates.get("apiKey", provider.get("apiKey")),
                    "model": updates.get("model", provider.get("model")),
                    "baseUrl": updates.get("baseUrl", provider.get("baseUrl")),
                    "notes": updates.get("notes", provider.get("notes", ""))
                })
                data["providers"][idx] = provider
                updated = provider
                break
        if updated:
            self._save(data)
        return updated

    def delete_provider(self, provider_id: str) -> bool:
        data = self._load()
        providers = data.get("providers", [])
        next_providers = [p for p in providers if p.get("id") != provider_id]
        if len(next_providers) == len(providers):
            return False
        data["providers"] = next_providers
        if data.get("activeProvider") == provider_id:
            data["activeProvider"] = None
        self._save(data)
        return True

    def set_active_provider(self, provider_id: Optional[str]) -> Optional[Dict[str, Any]]:
        data = self._load()
        if provider_id is None:
            data["activeProvider"] = None
            self._save(data)
            return None
        if not any(p.get("id") == provider_id for p in data.get("providers", [])):
            return None
        data["activeProvider"] = provider_id
        self._save(data)
        return self.get_provider(provider_id)

    def get_active_provider(self) -> Optional[Dict[str, Any]]:
        data = self._load()
        active_id = data.get("activeProvider")
        if not active_id:
            return None
        return self.get_provider(active_id)
