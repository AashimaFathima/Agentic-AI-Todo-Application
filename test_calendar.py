from calendar_service import create_calendar_event

link = create_calendar_event(
    title="Client Meeting",
    description="Meeting with client",
    start_datetime="2026-07-20 20:00:00",
)

print(link)