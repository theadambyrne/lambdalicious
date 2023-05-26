# Lambdalicious 

OpenAPI3 specification for the Lambdalicious API: [lambdalicious-api-oas30.yaml](lambdalicious-api-oas30.yaml)
## Base URL

The base URL for the API is `https://2x3pds3pyf.execute-api.eu-west-1.amazonaws.com/api/`.

## Endpoints

### `GET /`

Retrieves the customer queue.

#### Request

- Method: GET
- URL: `/`

#### Response

- Status Code: 200 OK
- Body: List of customer queue items

### `DELETE /reset`

Resets the customer queue.

#### Request

- Method: DELETE
- URL: `/reset`
- Headers:
  - `x-api-key`: API key (required)

#### Response

- Status Code: 204 No Content

### `PUT /add/{name}`

Adds a customer to the queue.

#### Request

- Method: PUT
- URL: `/add/{name}`
  - Replace `{name}` with the customer name.
- Headers:
  - `x-api-key`: API key (required)

#### Response

- Status Code: 204 No Content

### `DELETE /remove/{name}`

Removes a customer from the queue.

#### Request

- Method: DELETE
- URL: `/remove/{name}`
  - Replace `{name}` with the customer name.
- Headers:
  - `x-api-key`: API key (required)

#### Response

- Status Code: 204 No Content

### `POST /notify`

Notifies the next customer in the queue.

#### Request

- Method: POST
- URL: `/notify`
- Headers:
  - `x-api-key`: API key (required)

#### Response

- Status Code: 200 OK or 204 No Content
- Body: The name of the next customer or "No one in queue" if the queue is empty.

### `DELETE /next`

Removes the next customer from the queue.

#### Request

- Method: DELETE
- URL: `/next`
- Headers:
  - `x-api-key`: API key (required)

#### Response

- Status Code: 200 OK or 204 No Content
- Body: The name of the next customer or "No one in queue" if the queue is empty.

### `GET /stats`

Retrieves the number of customers in the queue.

#### Request

- Method: GET
- URL: `/stats`

#### Response

- Status Code: 200 OK
- Body: The number of customers in the queue.

### `GET /position/{name}`

Retrieves the position of a customer in the queue.

#### Request

- Method: GET
- URL: `/position/{name}`
  - Replace `{name}` with the customer name.

#### Response

- Status Code: 200 OK
- Body: The position of the customer in the queue or "Client not in queue" if the customer is not in the queue.
