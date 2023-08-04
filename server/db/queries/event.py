from uuid import uuid4

from events.utils import apply_tz_to_datetime, parse_timestamp_info
from geolocation.ip import get_information_from_ip
from db import get_psql_info

def create_event(
    user_id: str, 
    start_time: str, 
    end_time: str, 
    title: str,
    location: str = None,
    description: str = None,
    ip: str = None, 
    tz: str = None
):
    set_tz = tz or get_information_from_ip(ip).get("timezone", None) or "UTC"

    start_dt, has_tz = parse_timestamp_info(start_time)
    if not has_tz:
        start_dt = apply_tz_to_datetime(start_dt, set_tz)

    end_dt, has_tz = parse_timestamp_info(end_time)
    if not has_tz:
        end_dt = apply_tz_to_datetime(end_dt, set_tz)

    event_id = str(uuid4())

    fields = ["id", "organizer", "title", "start_time", "end_time"]
    values = [event_id, user_id, title, start_dt, end_dt]

    if description:
        fields.append("description")
        values.append(description)

    if location:
        fields.append("location")
        values.append(location)


    sql = "INSERT INTO events ({}) VALUES ({})".format(",".join(fields), ", ".join(["%s" for _ in fields]))
    
    connection, cursor = get_psql_info()

    try:
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()
    except:
        import traceback
        return traceback.format_exc()
    
    return event_id