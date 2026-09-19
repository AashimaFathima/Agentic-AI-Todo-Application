from agno.agent import Agent
from agno.models.groq import Groq

import tools
import config

from datetime import date

today = date.today().isoformat()
print("APP TODAY:", today)

agent = Agent(
    model = Groq(
    id="openai/gpt-oss-20b",
    api_key=config.GROQ_API_KEY,
    temperature=0.4,
    ),

    tools=[
        tools.create_task,
        tools.get_all_tasks,
        tools.get_task,
        tools.update_task,
        tools.delete_task,
        tools.delete_all_tasks, 
        tools.search_tasks,
        tools.count_pending_tasks,
        tools.complete_overdue_tasks,
        tools.get_todays_tasks,
        tools.get_tasks_by_date,
    ],


   instructions=[
    "You are a helpful AI Todo assistant.",
    "Use the available tools whenever appropriate.",
    "Never make up task information. Retrieve information using tools whenever possible.",
    "If a requested task does not exist, politely inform the user.",

    f"Today's date is {today}.",
    "When the user specifies a relative date or time such as 'today', 'tomorrow', 'next Monday', or 'in 3 days', convert it into the appropriate ISO date/time format before calling tools.",
    "If the user does not specify a due date or time, leave the due_datetime field empty.",

    "When creating a task, ALWAYS generate a short, meaningful title.",
    "If the user does not provide a description, ALWAYS generate a natural, human-like description in one concise sentence. Avoid simply repeating the title.",
    "After successfully creating a task, confirm it by mentioning the task title and its scheduled date/time if available.",

    "Never call delete_all_tasks unless the user explicitly asks to delete all tasks.",

    "Respond directly to the user.",

    "Do NOT explain your thought process, planning, or the steps you took internally.",
    "After using tools, provide only the final, user-facing response in a natural, conversational tone.",
    ],

    markdown=True,
)