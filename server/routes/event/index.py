from flask import request, jsonify
from flasgger import swag_from
from authorization.wrapper import requires_auth
from db.queries import create_event, get_event
import traceback


@swag_from("/server/apidocs/event/index_post.yml", methods=["POST"])
@swag_from("/server/apidocs/event/index_get.yml", methods=["GET"])
@requires_auth
def event(user_id: str):
    """Endpoint function to create an event or retrieve events associated with the user.

    This POST method endpoint function will collect the user id, start time, end time,
    and title for an event being created in the database. Optionally, a description
    and location for the event can be sent with the request, as well as a timezone
    override for timezone-naive timestamps passed through.

    This GET method endpoint function will get a certain amount of events (up to 100)
    and return those events associated with the user through pagination, using arguments
    page for the offset and size for the payload amount.

    Args:
        user_id (str): The user ID associated with the access token.

    Returns:
        A 2-length tuple containing response information.
            [0]: The body payload. Newly created event ID on success, message on failure.
            [1]: The HTTP response code assocaited with the request.

    """
    if request.method == "POST":
        ip = request.remote_addr

        payload = request.get_json()

        if not "start_time" in payload:
            return {"message": "start_time missing from request"}, 400

        if not "end_time" in payload:
            return {"message": "end_time missing from request"}, 400

        if not "title" in payload:
            return {"message": "title missing from request"}, 400

        # Mandatory fields
        start_time = payload["start_time"]
        end_time = payload["end_time"]
        title = payload["title"]

        # Optional fields
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
                tz=tz,
            )

            return {"event_id": event_id}, 201

        # TODO: Handle less generically, user will receive a traceback on error
        except Exception:
            return traceback.print_exc(), 500

    elif request.method == "GET":

        page = int(request.args.get("page", 0))
        size = max(min(int(request.args.get("size", 20)), 100), 0)

        try:
            events = get_event(user_id=user_id, page=page, size=size)

            if events:
                return jsonify(events), 200
            return {"message": "No events found with associated user"}, 204

        # TODO: Handle less generically, user will receive a traceback on error
        except Exception:
            return traceback.print_exc(), 500
