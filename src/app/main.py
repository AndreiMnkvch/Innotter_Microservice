from fastapi import FastAPI
from .consumer import consume
import asyncio
from .router import router

app = FastAPI()
app.include_router(router)

@app.get("/")
async def root():
    return {"works": "well"}

@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(consume(loop))
    await task
