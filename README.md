# MEDIDA CHALLENGE

## Overview
This repository contains the source code for a RESTful API that provides access to sports events data for a specified league. The API integrates with a third-party service to fetch events information and exposes endpoints for clients to retrieve data.

## Setup
To run the API locally, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the root directory of the cloned repository.
3. Run the following command to start the API using Docker Compose:
   ```bash
   docker-compose up -d

This command will build the necessary Docker containers and start the API service.

## Usage
Once the API is running, you can make HTTP POST requests to the following endpoint to retrieve sports events data:

## Endpoint
URL: POST http://localhost:5000/events

### Request Body
```json
{
    "league": "NFL",
    "startDate": "YYYY-MM-DD",
    "endDate": "YYYY-MM-DD"
}
