# Web App API

This API serves as the gateway to the backend for the desktop web UI.

## Build

See instructions under "Development" [here](../README.md).

## API requests

### Check service connections
Sent a GET request to `/api/status`. The response contains a JSON
object with the following boolean attributes indicating whether a
connection has been established with each of the upstream services.

| Attribute | Type      | Description      |
| --------- | --------- | ---------------- |
| home      | `boolean` | Homepage service |
| event     | `boolean` | Events service   |
| image     | `boolean` | Images service   |

### Read events

Send a GET request to `/api/events`. The `events` attribute in the
response's JSON corresponds to a list of event objects, each containing
the following attributes.

| Attribute | Type     | Description         |
| --------- | -------- | ------------------- |
| title     | `string` | Title               |
| start     | `string` | Start date and time |
| end       | `string` | End date and time   |

### Read group homepages

Send a GET request to `/api/group/:group_id:/home`. The API will return
a JSON object with the following attributes.

| Attribute | Type     | Description             |
| --------- | -------- | ----------------------- |
| id        | `number` | Group ID                |
| name      | `string` | Group name              |
| welcome   | `string` | Welcome message         |
| about     | `string` | About text              |
| icon      | `string` | URL to the group's icon |

### Edit group homepages

Send a PUT request to `/api/group/:group_id:/home` with the
`Content-Type: application/json` header and a JSON object in the body.
The JSON should contain any of the following attributes to edit the
corresponding field.

| Attribute | Type     | Description             |
| --------- | -------- | ----------------------- |
| name      | `string` | Group name              |
| welcome   | `string` | Welcome message         |
| about     | `string` | About text              |
