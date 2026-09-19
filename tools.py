from agno.tools import tool

import models
from calendar_service import (
    create_calendar_event,
    update_calendar_event,
)

@tool
def create_task(
    title: str,
    description: str,
    due_date: str | None = None,
):
    """
    Create a new todo task.
    """

    calendar_event_id = None
    calendar_link = None

    if due_date:

        calendar = create_calendar_event(
            title=title,
            description=description,
            start_datetime=due_date,
        )

        print("Calendar returned:", calendar)

        calendar_event_id = calendar["event_id"]
        calendar_link = calendar["calendar_link"]

        print("Event ID:", calendar_event_id)

    print("Passing to models:", calendar_event_id)

    task = models.create_task(
        title,
        description,
        due_date,
        calendar_event_id,
    )

    task["calendar_link"] = calendar_link

    return task

@tool
def get_all_tasks():
    """
    Return all tasks.
    """

    return models.get_all_tasks()


@tool
def get_task(task_id: int):
    """
    Return a single task.
    """

    return models.get_task(task_id)


@tool
def update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    completed: bool | None = None,
    due_date: str | None = None,
):
    """
    Update an existing todo task.

    Use this tool when the user wants to change a task's
    title, description, completion status, or due date.

    task_id is the ID of the task to update.
    Only change the fields that the user explicitly requests.
    due_date should be an ISO datetime when provided.
    """

    # Get the existing task first
    task = models.get_task(task_id)

    if task is None:
        return {
            "error": f"Task {task_id} not found."
        }

    # Keep old values for fields that were not changed
    new_title = title if title is not None else task["title"]

    new_description = (
        description
        if description is not None
        else task["description"]
    )

    new_due_date = (
        due_date
        if due_date is not None
        else task["due_date"]
    )

    # Update Google Calendar if this task has a Calendar event
    if task["calendar_event_id"]:

        update_calendar_event(
            event_id=task["calendar_event_id"],
            title=new_title,
            description=new_description,
            start_datetime=new_due_date,
        )

    # Update MySQL
    return models.update_task(
        task_id=task_id,
        title=title,
        description=description,
        completed=completed,
        due_date=due_date,
    )

@tool
def delete_task(
    task_id: int | None = None,
    title: str | None = None,
):
    """
    Delete one todo task.

    Use task_id when the user provides a task ID.
    Use title when the user identifies the task by its title.
    """

    if task_id is not None:
        return models.delete_task(task_id)

    if title is not None:
        tasks = models.search_tasks(title)

        if len(tasks) == 0:
            return {
                "error": f"No task found with title '{title}'."
            }

        if len(tasks) > 1:
            return {
                "error": "Multiple tasks matched that title. Please provide the task ID."
            }

        return models.delete_task(tasks[0]["id"])

    return {
        "error": "Please provide either a task ID or task title."
    }

@tool
def delete_all_tasks():
    """
    Delete every task from the database.
    """

    return models.delete_all_tasks()

@tool
def count_pending_tasks():
    """Return the number of pending tasks."""

    return models.count_pending_tasks()

@tool
def search_tasks(keyword: str):
    """
    Search tasks by title or description.
    """

    return models.search_tasks(keyword)

@tool
def complete_overdue_tasks():
    """
    Mark all overdue tasks as completed.
    """

    return models.complete_overdue_tasks()


@tool
def get_todays_tasks(dummy: str = ""):
    """
    Return tasks due today.
    """

    return models.get_todays_tasks()

@tool
def get_tasks_by_date(date: str):
    """
    Return all tasks due on a specific date.

    date must be provided in YYYY-MM-DD format.
    """

    return models.get_tasks_by_date(date)
