from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from agent import agent
from models import initialize_database
import models

from calendar_service import get_calendar_events

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Agentic AI Todo API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel): # Structure of the data that the endpoint expects
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    logger.info("Received chat request")

    try:
        response = agent.run(request.message)
        logger.info("Chat request processed successfully")

        return {
            "response": response.content
        }

    except Exception:
        logger.exception("Failed to process chat request")
        raise

@app.get("/tasks")
async def get_tasks():
    return models.get_all_tasks()


@app.get("/calendar/events")
async def calendar_events(
    start_datetime: str,
    end_datetime: str
):
    return get_calendar_events(
        start_datetime,
        end_datetime
    )

