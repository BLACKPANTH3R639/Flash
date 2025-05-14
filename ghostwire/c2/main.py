
from fastapi import FastAPI
from c2.api import agent

app = FastAPI(title="GhostWire C2 API")
app.include_router(agent.router, prefix="/api")
