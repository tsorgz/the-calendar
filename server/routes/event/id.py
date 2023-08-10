from flask import request, jsonify
from flasgger import swag_from
from authorization.wrapper import requires_auth
from db.queries import get_event_by_id, update_event, delete_event

import traceback

@swag_from("/apidocs/event/id_get.yml", methods=["GET"])
@swag_from("/apidocs/event/id_patch.yml", methods=["PATCH"])
@swag_from("/apidocs/event/id_delete.yml", methods=["DELETE"])
@requires_auth
def event_id(user_id: str, id: str):
    """Endpoint function to update an event, delete an event, or retrieve a single event 
    associated with the user.

    This PATCH method endpoint function will collect the user id and event_id, and modify
    the event if it is associated with the user. All of the fields associated with the event
    are editable and passable as parameters. Timezone is also a valid bosy arg, but it acts as
    an override for timezone-naive timestamps passed through for start_time and end_time.

    This GET method endpoint function will retrieve a certain event and return that event 
    if it is associated with the requesting user.

    This DELETE method endpoint function will send a message to the database to delete 
    an event only if it is associated with the requesting user.

    Args:
        user_id (str): The user ID associated with the access token.
        id (str): The event_id passed into the endpoint path.

    Returns:
        A 2-length tuple containing response information.
            [0]: The body payload. Newly created event ID on success, message on failure.
            [1]: The HTTP response code assocaited with the request.

    """
    if request.method == "GET":
        try:
            event = get_event_by_id(user_id=user_id, event_id=id)
            if event:
                return jsonify(event), 200
            return {"message": "No events found with associated user"}, 204
        except Exception:
            return traceback.format_exc(), 500
    elif request.method == "PATCH":
        ip = request.remote_addr

        payload = request.get_json()
        
        start_time = payload.get("start_time", None)
        end_time = payload.get("end_time", None)
        title = payload.get("title", None)

        description = payload.get("description", None)
        location = payload.get("location", None)
        tz = payload.get("timezone", None)

        try:
            event_id = update_event(
                user_id=user_id,
                event_id=id,
                start_time=start_time,
                end_time=end_time,
                title=title,
                location=location,
                description=description,
                ip=ip,
                tz=tz,
            )

            return {"event_id": event_id}, 200
        # TODO: Handle less generically, user will receive a traceback on error
        except Exception:
            return traceback.format_exc(), 500
    elif request.method == "DELETE":
        try:
            delete_event(user_id=user_id, event_id=id)
            return {"message": "Event deletion sent successfully"}, 200
        except Exception:
            return traceback.format_exc(), 500
