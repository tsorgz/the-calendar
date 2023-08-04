from datetime import datetime, timezone
from pytz import timezone as get_timezone

def parse_timestamp_info(timestamp: str):
    dt = None

    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return
    
    if dt.tzinfo and dt.tzinfo != timezone.utc:
        dt = dt.astimezone(timezone.utc)
    
    return dt, dt.tzinfo != None

def apply_tz_to_datetime(dt: datetime, tz: str):
    tz_obj = get_timezone(tz)
    dt = tz_obj.localize(dt)
    if dt.tzinfo != timezone.utc:
        dt = dt.astimezone(timezone.utc)
    return dt
