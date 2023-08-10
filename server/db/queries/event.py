from uuid import uuid4
from datetime import datetime, timezone
from logger import logger
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

    # TODO: Logic to make sure start_dt < end_dt

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

def update_event(
    user_id: str,
    event_id: str,
    start_time: str = None,
    end_time: str = None,
    title: str = None,
    location: str = None,
    description: str = None,
    ip: str = None,
    tz: str = None,
):
    """Updates an event with an associated user.

    The function updates an event associated with a user. All fields are editable, except the
    organizer and the ID associated with the event.

    If the times sent over do not have a timezone assocaited with the user, or if the user
    doesn't specify a fallback timezone, a timezone will be parsed from the incoming IP address,
    or it will default to UTC (+00:00).

    Args:
        user_id (str): The user ID associated with the event.
        event_id (str): The event ID associated with the event being updated.
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
    updating_fields = []

    if start_time:
        start_dt, has_tz = parse_timestamp_info(start_time)
        if not has_tz:
            start_dt = apply_tz_to_datetime(start_dt, set_tz)
        updating_fields.append(("start_time", start_dt))

    if end_time:
        end_dt, has_tz = parse_timestamp_info(end_time)
        if not has_tz:
            end_dt = apply_tz_to_datetime(end_dt, set_tz)
        updating_fields.append(("end_time", end_dt))

    # TODO: Logic to make sure start_dt < end_dt
    if title:
        updating_fields.append(("title", title))

    if description:
        updating_fields.append(("description", description))

    if location:
        updating_fields.append(("location", location))

    updating_fields.append(("updated_at", datetime.now(tz=timezone.utc)))

    fields, values = list(zip(*updating_fields))

    sql = "UPDATE events SET {} WHERE id = '{}' and organizer = '{}'".format(
        ",".join([f + ' = %s' for f in fields]), event_id, user_id
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


def get_event(user_id: str, page: int = 0, size: int = 20):
    """Retrieves events with an associated user.

    This function retrieves a certain number of events (up to 100) from the database, and
    formats it for proper response formatting.

    Args:
        user_id (str): The user ID associated with the event.
        page (int): The offset, determined with size parameter, of the elements returned from the database.
        size (int): The number of entries returned from the database.

    Returns:
        A list of events based on the size and offset requested, which can be empty.
    """

    logger.info(f"Getting events for {user_id=}, {page=}, {size=}")
    results = []
    fields = [
        "id",
        "title",
        "start_time",
        "end_time",
        "description",
        "location",
        "created_at",
        "updated_at",
    ]

    connection, cursor = get_psql_info()
    sql = "SELECT {} from events WHERE organizer = %s ORDER BY start_time DESC, end_time DESC LIMIT %s OFFSET %s".format(
        ",".join(fields)
    )

    cursor.execute(sql, (user_id, size, page * size))
    response = cursor.fetchall()

    for row in response:

        entry = {}
        for idx, key in enumerate(fields):
            if row[idx] == None:
                continue
            # TODO: serializer in utils, this will be reuired on every datetime object
            if isinstance(row[idx], datetime):
                entry[key] = row[idx].isoformat()
            else:
                entry[key] = row[idx]
        results.append(entry)

    cursor.close()
    connection.close()

    logger.info(f"Returning {len(results)} events for {user_id=}")

    return results

def get_event_by_id(user_id: str, event_id: str):
    """Retrieves a single event associated with an associated user.

    This function retrieves an event with a matching ID from the database if it is
    associated with the user, and formats it for proper response formatting.

    Args:
        user_id (str): The user ID associated with the event.
        event_id (str): The requested event ID.

    Returns:
        An event if one is found, otherwise, an empty dict.
    """

    entry = {}
    logger.info(f"Getting event for {user_id=}, {event_id=}")
    fields = [
        "id",
        "title",
        "start_time",
        "end_time",
        "description",
        "location",
        "created_at",
        "updated_at",
    ]

    connection, cursor = get_psql_info()
    sql = "SELECT {} from events WHERE organizer = %s AND id = %s".format(
        ",".join(fields)
    )

    cursor.execute(sql, (user_id, event_id))
    response = cursor.fetchone()

    if not response:
        return entry
    
    for idx, key in enumerate(fields):
        if response[idx] == None:
            continue
        # TODO: serializer in utils, this will be reuired on every datetime object
        if isinstance(response[idx], datetime):
            entry[key] = response[idx].isoformat()
        else:
            entry[key] = response[idx]

    cursor.close()
    connection.close()

    logger.info(f"Returning event {event_id=} for {user_id=}")

    return entry

def delete_event(user_id: str, event_id: str):
    """Deletes an event with an associated user.

    This function deletes the requested event from the database, if associated 
    with the user.

    Args:
        user_id (str): The user ID associated with the event.
        event_id (str): The requested event ID to be deleted.

    """

    connection, cursor = get_psql_info()
    sql = "DELETE FROM events WHERE organizer = %s AND id = %s"

    cursor.execute(sql, (user_id, event_id))
    connection.commit()

    cursor.close()
    connection.close()
