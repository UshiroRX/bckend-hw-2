from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from auth.router import router as auth_router
from config import settings
from utils.redis import get_redis
from redis.asyncio import Redis 
from celery.result import AsyncResult
from tasks.task import add, fetch_data_daily

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  

app = FastAPI(lifespan=lifespan, title="Good API")

origins = settings.FRONTEND_URLS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(auth_router, tags=["Auth"], prefix="/api")


@app.get("/visit")
async def count_visit(redis: Redis = Depends(get_redis)):
    await redis.incr("visits")
    visits = await redis.get("visits")
    return {"visits": visits}


@app.get("/run-task")
async def run_task():
    task = add.delay(4, 5)
    return {"task_id": task.id}

@app.get("/run-get")
async def run_get():
    task = fetch_data_daily.delay()
    return {"task_id": task.id}


@app.get("/task-status/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id)
    return {
        "status": result.status,
        "result": result.result if result.ready() else None
    }