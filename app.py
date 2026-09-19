from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from agent import agent
from models import initialize_database
import models

from calendar_service import get_calendar_events

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

    response = agent.run(request.message) # The natural language instruction that you send that hands the instruction to the Agno agent

    return {
        "response": response.content
    }

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

