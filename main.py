import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from models.base import init_db
from services.auth_service import create_admin_user
from services.data_service import start_data_generation

# Routers
from routes.auth import router as auth_router
from routes.dashboard import router as dashboard_router
from routes.traffic import router as traffic_router
from routes.reports import router as reports_router
from routes.analysis import router as analysis_router
from routes.traffic_live import router as traffic_live_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    create_admin_user()

    try:
        app.state.task = asyncio.create_task(start_data_generation())
    except Exception as e:
        print("Data error:", e)

    yield

    task = getattr(app.state, "task", None)
    if task:
        task.cancel()
        try:
            await task
        except:
            pass


app = FastAPI(lifespan=lifespan)

# static
app.mount("/static", StaticFiles(directory="static"), name="static")

# routers
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(traffic_router)
app.include_router(reports_router)
app.include_router(analysis_router)
app.include_router(traffic_live_router)