from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.models.llm_adapters import ModelRouter
from src.models.novel_repository import NovelRepository
from src.models.provider_manager import ProviderManager
import os

app = FastAPI(title="Nature AI Demo", version="0.1.0")

provider_manager = ProviderManager("/workspaces/Nature-AI/config/providers.json")
router = ModelRouter("/workspaces/Nature-AI/config/models.yaml", provider_manager=provider_manager)
novel_repo = NovelRepository()

class ChatRequest(BaseModel):
    message: str
    model: str = "auto"
    provider_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str

class ProviderInput(BaseModel):
    name: str
    provider: str
    apiKey: str
    model: str
    baseUrl: Optional[str] = None
    notes: Optional[str] = None

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    adapter = router.get_adapter(provider_id=request.provider_id)
    if not adapter:
        raise HTTPException(status_code=500, detail="No model available")
    try:
        response = await adapter.generate(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/providers")
async def list_providers():
    return provider_manager.list_providers()

@app.post("/api/providers")
async def create_provider(provider: ProviderInput):
    created = provider_manager.add_provider(provider.dict())
    return created

@app.put("/api/providers/{provider_id}")
async def update_provider(provider_id: str, provider: ProviderInput):
    updated = provider_manager.update_provider(provider_id, provider.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Provider not found")
    return updated

@app.delete("/api/providers/{provider_id}")
async def delete_provider(provider_id: str):
    success = provider_manager.delete_provider(provider_id)
    if not success:
        raise HTTPException(status_code=404, detail="Provider not found")
    return {"success": True}

@app.post("/api/providers/{provider_id}/activate")
async def activate_provider(provider_id: str):
    active = provider_manager.set_active_provider(provider_id)
    if not active:
        raise HTTPException(status_code=404, detail="Provider not found")
    return active

@app.get("/api/novels")
async def list_novels():
    return novel_repo.list_novels()

@app.get("/api/novels/{novel_id}")
async def get_novel(novel_id: str):
    novel = novel_repo.get_novel(novel_id)
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")
    return novel

@app.get("/health")
async def health():
    return {"status": "ok"}