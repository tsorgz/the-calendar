# the-calendar

`the-calendar` is a project maintained by me, [TJ Soregaroli](https://linkedin.com/in/tj-soregaroli), as a light showcase of the individual skills I have picked up through my software engineering experience. I will be continuing to expand features and improve functionality as my time permits, although I have no plans on creating a live deployment.

## Installation

As a demonstration of my containerization and database management skills, I have prepared the entire environmen in a `docker-compose.yml` file, having no need to have anything else other than [docker and docker-compose](https://docs.docker.com/get-docker/) installed.

Following that, run the following commands to clone and run the container:
```bash
git clone https://github.com/tsorgz/the-calendar.git
docker-compose up -d
```

To stop all services, you can use the following commands to stop the containers and delete the images:
```bash
docker-compose down
docker rmi $(docker images -q)
```

## Usage

Currently (as of 08/06/2023), the only functionality supported by the app is to create an account, login, and create events. To sign up, use the following:
```bash
curl -XPOST -H "Content-type: application/json" -d '{"email":"<email>","password":"<password>","first_name":"<first_name>","last_name":"<last_name>"}' 'http://localhost:8000/auth/signup'
```
Alternatively, you can log in subsequently with the following:
```bash
curl -XPOST -H "Content-type: application/json" -d '{"email":"<email>","password":"<password>"}' 'http://localhost:8000/auth/login'
```

Both commands will return access and refresh JWT tokens, the former used to identify the calling user on application events, and the other to retrieve a new access token when the former expires. This can be done by the following command:
```bash
curl -XPOST -H 'Authorization: Bearer <REFRESH_TOKEN>' -H "Content-type: application/json" 'http://localhost:8000/auth/token'
```

To create an event, you can use the following cURL command:
```bash
curl -XPOST -H 'Authorization: Bearer <REFRESH_TOKEN>' -H "Content-type: application/json" -d '{"title":"<title>","start_time":"<start_time>","end_time":"<end_time>","last_name":"<last_name>"}' 'http://localhost:8000/event'
```

For the above command, the body requires `title`, the name of the event, `start_time` and `end_time`, both [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) compliant timestamps representing the time the event starts and ends, respectively. Additionally, `description`, a human readable explanation of the event, `location`, a human readable location where the event takes place, and `timezone`, an override from the [tz database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) for timezone-naive timestamps, can be passed in the body.

## Known Issues

- Start time can actually be later than end time, logic must be implemented for it
- Many endpoints currently will send the full traceback as the response payload
- On `/auth/token`, missing Authorization header will throw a generic 500 message. We need to handle with messaging and 400 level response code
- Caught by tests, ISO 8601 compliant datetimes in the form `%Y-%m-%d%z`/`YYYY-MM-DD+ZZ:ZZ` actually get parsed as `%Y-%m-%dT%H%M`/`YYYY-MM-DD hh:mm`, ignoring potential timezone options.
- Authorization and Refresh tokens are implemented to be useable until their expiry, and many can be issued for the same user simutaneously. Adding a Redis caching layer to keep track of valid refresh tokens based off the uid and exp would help expire the session of a malicious user on a new login.


## Considerations
- We can add events, but there is currently no way to view them via API. Of course, we can query events through `psql`, but this is less than ideal.
- There are many fields that pertain to [iCalendar standards](https://www.ietf.org/rfc/rfc2445.txt) that we can further model our database to include.
    - By using the iCalendar standard, we can export events from our service into many common calendars, such as Google, Apple, and Outlook
- Being able to search locations using the [Google Maps Places](https://developers.google.com/maps) API suite would be able to create a great user experience boost.
- Inviting guests should be a functionality, and implementing a connections list would be useful for user experience.
    - Not only that, but having a service to send notifications to a user who is invited by another user to an event would be a great addition.
    - Along with that, there could also be a way to notify an event organizer on potential conflicts with invitees.
    - Expanding further, being able to view the calendars of porential invitees, as well as for them to set the privacy settings of events would be hugely important.