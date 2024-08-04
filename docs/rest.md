# REST Requests
Daytistics uses REST to communicate between frontend and backend. The different approaches can be found in the documentation of the respective modules. The goal of this file is to define general conventions for creating REST APIs.

## Files

## Return Values
The return values ​​of REST requests must be structured as in the examples shown here:

### General
```
{
  "status": "success" | "error",
  "data": { ... } | null,
  "message": "Optional message",
  "errors": [ ... ] | null
}

```

### Example 1
```
{
  "status": "success",
  "data": {
    "id": 123,
    "name": "John Doe"
  }
}
```

### Example 2
```
{
  "status": "error",
  "message": "Validation error",
  "errors": [
    {
      "field": "email",
      "message": "Invalid E-Mail-Format"
    }
  ]
}
```


## HTTP Codes
The most important codes for this project are:
- **200 OK**: The request was successful.
- **201 Created**: The request was successful, and a new resource was created.
- **204 No Content**: The request was successful, but there is no content to send in the response.
- **400 Bad Request**: The server cannot process the request due to a client error.
- **401 Unauthorized**: Authentication is required and has failed or has not yet been provided.
- **403 Forbidden**: The server understands the request but refuses to authorize it.
- **404 Not Found**: The requested resource could not be found.
- **500 Internal Server Error**: The server encountered an unexpected condition that prevented it from fulfilling the request.