from datetime import datetime, timezone

def parse_datetime(time_str):
    """
    Parses UTC time strings into timezone-aware local datetimes.
    """
    if not time_str:
        return datetime.now()
    try:
        if "T" in time_str:
            return datetime.fromisoformat(time_str).astimezone()
        if "." in time_str:
            time_str = time_str.split(".")[0]
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return dt.replace(tzinfo=timezone.utc).astimezone()
    except Exception:
        return datetime.now()

def format_timestamp(time_str):
    """
    Formats timestamp strings into a standard 12-hour AM/PM format.
    """
    dt = parse_datetime(time_str)
    return dt.strftime("%I:%M %p")

def get_date_label(dt):
    """
    Generates contextual date separators (e.g. Today, Yesterday, or specific dates).
    """
    from datetime import timedelta
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    msg_date = dt.date()
    if msg_date == today:
        return "Today"
    elif msg_date == yesterday:
        return "Yesterday"
    else:
        return msg_date.strftime("%B %d, %Y")
