from datetime import datetime, timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def create_calendar_event(
    title,
    description,
    start_datetime,
    end_datetime=None,
):
    service = get_calendar_service()

    # Accept both:
    # 2026-07-22T10:00:00
    # 2026-07-22 10:00:00
    start_dt = datetime.fromisoformat(start_datetime)
    print("CALENDAR RECEIVED:", start_datetime)
    print("CALENDAR PARSED:", start_dt)

    if end_datetime is None:
        end_dt = start_dt + timedelta(hours=1)
    else:
        end_dt = datetime.fromisoformat(end_datetime)

    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": start_dt.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_dt.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
    }

    created_event = (
        service.events()
        .insert(
            calendarId="primary",
            body=event,
        )
        .execute()
    )

    return {
        "event_id": created_event["id"],
        "calendar_link": created_event["htmlLink"],
    }

def delete_calendar_event(event_id):
    service = get_calendar_service()

    service.events().delete(
        calendarId="primary",
        eventId=event_id,
    ).execute()


def update_calendar_event(
    event_id,
    title,
    description,
    start_datetime,
    end_datetime=None,
):
    service = get_calendar_service()

    start_dt = datetime.fromisoformat(start_datetime)

    if end_datetime is None:
        end_dt = start_dt + timedelta(hours=1)
    else:
        end_dt = datetime.fromisoformat(end_datetime)

    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": start_dt.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_dt.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
    }

    service.events().update(
        calendarId="primary",
        eventId=event_id,
        body=event,
    ).execute()

def get_calendar_events(start_datetime, end_datetime):

    service = get_calendar_service()

    events_result = service.events().list(
        calendarId="primary",
        timeMin=start_datetime,
        timeMax=end_datetime,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = events_result.get("items", [])

    result = []

    for event in events:

        start = event.get("start", {}).get("dateTime")
        end = event.get("end", {}).get("dateTime")

        result.append({
            "id": event.get("id"),
            "title": event.get("summary", "Untitled event"),
            "start": start,
            "end": end,
        })

    return result
