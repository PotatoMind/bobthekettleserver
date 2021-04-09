## BobTheKettleServer
This example defines a basic setup for BobTheKettleServer. BobTheKettleServer is used to be the backend hosted application for a water heater or kettle.

## API Functions

### /temperature/{mode}
* GET: Get the temperature from the water in the container. Returns temperature values as `{'c':float, 'f':float, 'k':float}`
* POST: Set the temperature mode of the container. Modes choices are boil at 90C, hot at 60C, and warm at 30C.
### /heat/<mode>/{duration}
* POST: Set a temperature mode for a duration. Modes choices are boil at 90C, hot at 60C, and warm at 30C. Duration is in seconds.
### /stats
* GET: Get all info saved to DB for the container. Rows include datetime, command, device, and response.
### /switch/{value}
* GET: Turns the device off if value is "off" and turns it on if value is "on".
### /power
* GET: Turns device off if it is on and turns it on if it is off.
### /cancel
* GET: Cancel the current running command.

## Initial Setup
This project requires to have a sqlite3 database to be created by running the following command:
```
$ python db.py
```

## Deploy with server.sh

```
$ ./server.sh
```

## Stop server

```
Ctrl+C
```
