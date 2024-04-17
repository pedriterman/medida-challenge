from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Host machine's IP address in order to dockerize this challenge
HOST = os.environ.get('HOST_IP', 'localhost')


# Function to fetch events data from the third-party API
def fetch_events_from_third_party_api(league, start_date=None, end_date=None):
    # URL of the third-party API
    api_url = f'http://{HOST}:9000/{league}/scoreboard'

    # Parameters for the API request
    params = {'since': start_date, 'until': end_date}

    # Example: Make a GET request to the third-party API to retrieve events data
    response = requests.get(api_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return the JSON data from the response
        return response.json()
    else:
        # If the request was not successful, raise an exception or handle the error
        raise Exception('Failed to fetch events data from the third-party API')


# Function to fetch team rankings from the third-party API
def fetch_team_rankings_from_third_party_api(league):
    # URL of the team rankings endpoint
    api_url = f'http://{HOST}:9000/{league}/team-rankings'

    # Make a GET request to the third-party API to retrieve team rankings data
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return the JSON data from the response
        return response.json()
    else:
        # If the request was not successful, raise an exception or handle the error
        raise Exception('Failed to fetch team rankings data from the third-party API')


@app.route('/events', methods=['POST'])
def polling_events():
    # Parse request body
    data = request.json

    league = data.get('league')
    start_date = data.get('startDate')
    end_date = data.get('endDate')

    # Check if start date is greater than end date
    if start_date > end_date:
        return jsonify({'error': 'Start date cannot be greater than end date.'}), 400

    try:
        # Retrieve events data from the third-party API
        events_data = fetch_events_from_third_party_api(league, start_date, end_date)

        # Retrieve team rankings data from the third-party API
        team_rankings = fetch_team_rankings_from_third_party_api(league)

        # Transform the data to match the EventsResponse schema and filter by date
        transformed_data = []
        for event in events_data:
            event_date = event['timestamp'][:10]  # Extract date part from timestamp
            if start_date <= event_date <= end_date:  # Check if the event date is within the specified range
                home_team_rank = next((team['rank'] for team in team_rankings if team['teamId'] == event['home']['id']), 0)
                away_team_rank = next((team['rank'] for team in team_rankings if team['teamId'] == event['away']['id']), 0)
                home_team_rank_points = next((team['rankPoints'] for team in team_rankings if team['teamId'] == event['home']['id']), 0.0)
                away_team_rank_points = next((team['rankPoints'] for team in team_rankings if team['teamId'] == event['away']['id']), 0.0)
                transformed_event = {
                    'eventId': event['id'],
                    'eventDate': event_date,
                    'eventTime': event['timestamp'][11:-1],  # Extract time part from timestamp
                    'homeTeamId': event['home']['id'],
                    'homeTeamNickName': event['home']['nickName'],
                    'homeTeamCity': event['home']['city'],
                    'homeTeamRank': home_team_rank,
                    'homeTeamRankPoints': home_team_rank_points,
                    'awayTeamId': event['away']['id'],
                    'awayTeamNickName': event['away']['nickName'],
                    'awayTeamCity': event['away']['city'],
                    'awayTeamRank': away_team_rank,
                    'awayTeamRankPoints': away_team_rank_points
                }
                transformed_data.append(transformed_event)

        # Return transformed response matching the EventsResponse schema
        return jsonify(transformed_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
