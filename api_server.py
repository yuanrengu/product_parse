from fastapi import FastAPI
from pydantic import BaseModel

from parser_core import parse_model, parse_models

app = FastAPI(
    title="型号解析服务",
    description="支持单条和批量型号解析，返回 JSON",
    version="1.0.0",
)


class SingleRequest(BaseModel):
    model: str


class BatchRequest(BaseModel):
    models: list[str]


@app.post("/parse/single")
async def parse_single(req: SingleRequest):
    return parse_model(req.model)


@app.post("/parse/batch")
async def parse_batch(req: BatchRequest):
    return parse_models(req.models)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
