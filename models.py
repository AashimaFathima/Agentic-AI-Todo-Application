from database import get_connection
from calendar_service import delete_calendar_event
from datetime import date

def task_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "completed": bool(row["completed"]),
        "due_date": row["due_date"],
        "calendar_event_id": row["calendar_event_id"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }

def initialize_database():
    """Create the tasks table if it doesn't already exist."""

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        completed BOOLEAN DEFAULT FALSE,

        due_date DATETIME,
        calendar_event_id VARCHAR(255),

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def create_task(
    title: str,
    description: str = "",
    due_date=None,
    calendar_event_id=None
):
    print("Received calendar_event_id:", calendar_event_id)
    

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        INSERT INTO tasks(
            title,
            description,
            due_date,
            calendar_event_id
        )
        VALUES(%s, %s, %s, %s)
        """,
        (
            title,
            description,
            due_date,
            calendar_event_id
        )
    )

    conn.commit()

    task_id = cursor.lastrowid

    conn.close()

    return {
        "id": task_id,
        "title": title,
        "description": description,
        "completed": False,
        "due_date": due_date,
        "calendar_event_id": calendar_event_id
    }

def get_all_tasks():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    conn.close()

    return [task_to_dict(row) for row in rows]


def get_task(task_id: int):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE id = %s
        """,
        (task_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return task_to_dict(row)


def update_task(
    task_id: int,
    title: str = None,
    description: str = None,
    completed: bool = None,
    due_date=None,
):

    task = get_task(task_id)

    if task is None:
        raise ValueError(f"Task {task_id} not found")

    if title is None:
        title = task["title"]

    if description is None:
        description = task["description"]

    if completed is None:
        completed = task["completed"]

    if due_date is None:
        due_date = task["due_date"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        UPDATE tasks
        SET
            title = %s,
            description = %s,
            completed = %s,
            due_date = %s
        WHERE id = %s
        """,
        (
            title,
            description,
            completed,
            due_date,
            task_id
        )
    )

    conn.commit()
    conn.close()

    return {
        "id": task_id,
        "title": title,
        "description": description,
        "completed": completed,
        "due_date": due_date
    }

def delete_task(task_id: int):

    task = get_task(task_id)

    if task is None:
        raise ValueError(f"Task {task_id} not found")
    
    if task["calendar_event_id"]:
        delete_calendar_event(task["calendar_event_id"])

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = %s
        """,
        (task_id,)
    )

    conn.commit()
    conn.close()

    return task

def delete_all_tasks():

    tasks = get_all_tasks()

    print("\n===== DELETE ALL =====")
    print("Tasks fetched:", tasks)

    for task in tasks:
        print("Calendar Event ID:", task["calendar_event_id"])

        if task["calendar_event_id"]:
            print("Deleting Google Calendar event:", task["calendar_event_id"])
            delete_calendar_event(task["calendar_event_id"])

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT COUNT(*) AS total_tasks
        FROM tasks
        """
    )

    total = cursor.fetchone()["total_tasks"]

    cursor.execute(
        """
        TRUNCATE TABLE tasks
        """
    )

    conn.commit()
    conn.close()

    print("Database truncated.")
    print("======================\n")

    return {
        "deleted_tasks": total
    }


def count_pending_tasks():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT COUNT(*) AS pending_tasks
        FROM tasks
        WHERE completed = FALSE
        """
    )

    count = cursor.fetchone()

    conn.close()

    return {
        "pending_tasks": count["pending_tasks"]
    }


def search_tasks(keyword: str):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE title LIKE %s
           OR description LIKE %s
        """,
        (f"%{keyword}%", f"%{keyword}%")
    )

    rows = cursor.fetchall()

    conn.close()

    return [task_to_dict(row) for row in rows]


def complete_overdue_tasks():

    today = date.today()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        UPDATE tasks
        SET completed = TRUE
        WHERE due_date < %s
          AND completed = FALSE
        """,
        (today,)
    )

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return {
        "completed_tasks": updated
    }


def get_todays_tasks():

    today = date.today()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE due_date = %s
        """,
        (today,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [task_to_dict(row) for row in rows]

def get_tasks_by_date(target_date: str):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE due_date >= %s
          AND due_date < DATE_ADD(%s, INTERVAL 1 DAY)
        ORDER BY due_date
        """,
        (target_date, target_date)
    )

    rows = cursor.fetchall()

    conn.close()

    return [task_to_dict(row) for row in rows]