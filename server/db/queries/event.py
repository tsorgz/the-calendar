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
    tz: str = None,
):
    """Creates an event with an associated user.

    The function creates an event associated with a user. At the minimum, the event will
    have a start and end time, and a title associated with it. The user can optionally set a
    location and description with the event.

    If the times sent over do not have a timezone assocaited with the user, or if the user
    doesn't specify a fallback timezone, a timezone will be parsed from the incoming IP address,
    or it will default to UTC (+00:00).

    Args:
        user_id (str): The user ID associated with the event.
        start_time (str): The start date timestamp following ISO 8601 standard.
        end_time (str): The end date timestamp following ISO 8601 standard.
        title (str): The human readable title of the event.
        location (str): The human readable location of the event.
        description (str): The human readable description of the event.
        ip (str): The incoming IP of the user.
        tz (str): The timezone override of timezone-naive timestamps.
    """

    # Timezone Priority: Timezone override, IP information, UTC (default)
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

    sql = "INSERT INTO events ({}) VALUES ({})".format(
        ",".join(fields), ", ".join(["%s" for _ in fields])
    )

    connection, cursor = get_psql_info()

    # TODO: Clean up return logic here, errors send full traceback in HTTP 201 Response body

    try:
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()
    except:
        import traceback

        return traceback.format_exc()

    return event_id
