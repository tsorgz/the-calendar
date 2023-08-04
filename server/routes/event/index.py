from flask import request
from authorization.wrapper import requires_auth
from db.queries.event import create_event
import traceback
@requires_auth
def event(user_id: str):
    if request.method == "POST":


        ip = request.remote_addr

        payload = request.get_json()

        if not "start_time" in payload:
            return {"message": "start_time missing from request"}, 400

        if not "end_time" in payload:
            return {"message": "end_time missing from request"}, 400

        if not "title" in payload:
            return {"message": "title missing from request"}, 400

        start_time = payload["start_time"]
        end_time = payload["end_time"]
        title = payload["title"]

        description = payload.get("description", None)
        location = payload.get("location", None)
        tz = payload.get("timezone", None)

        try:
            event_id = create_event(
                user_id=user_id,
                start_time=start_time,
                end_time=end_time,
                title=title,
                location=location,
                description=description,
                ip=ip,
                tz=tz
            )

            return {
                "event_id": event_id
            }, 201
        except Exception as e:
            return traceback.print_exc(), 500