# https://pypi.org/project/requests/
import requests
import json
from datetime import datetime
import os

api_key = input('Enter your api key: (you can get one at https://console.developers.google.com/)\n')
#api_key = 'hard_coded_api_key'
playlist_id = input('Enter your playlist id:\n')
#playlist_id = 'hard_coded_playlist_id'

payload = {'part': 'snippet', 'playlistId': playlist_id,
           'maxResults': 50, 'pageToken': None, 'key': api_key}

response = requests.get('https://youtube.googleapis.com/youtube/v3/playlistItems', params=payload)
response_json = response.json()

videos_in_playlist = []
videos_processed = 0
while True:
    video_ids = []
    for item in response_json['items']:
        video_ids.append(item['snippet']['resourceId']['videoId'])

    # make HTTP GET request
    video_payload = {'part': 'snippet', 'maxResults': 50, 'id': ','.join(video_ids), 'key': api_key}
    video_response = requests.get('https://youtube.googleapis.com/youtube/v3/videos', params=video_payload)
    video_response.raise_for_status()
    
    video_json = video_response.json()
    for video_resource in video_json['items']:
        video_snippet = video_resource['snippet']
        videos_in_playlist.append({'title': video_snippet['title'], 'channelTitle': video_snippet['channelTitle']})

    if not 'previousPageToken' in response_json and not 'nextPageToken' in response_json:
        break

    payload['pageToken'] = response_json['nextPageToken']
    response = requests.get('https://youtube.googleapis.com/youtube/v3/playlistItems', params=payload)
    response.raise_for_status()
    response_json = response.json()


    videos_processed += response_json['pageInfo']['resultsPerPage']
    print(str(videos_processed) + ' of ' + str(response_json['pageInfo']['totalResults']) + ' videos processed.', end='\r', flush=True)

# get playlist name
playlist_payload = {'part': 'snippet', 'id': playlist_id, 'key': api_key}
playlist_response = requests.get("https://youtube.googleapis.com/youtube/v3/playlists", playlist_payload)
playlist_response.raise_for_status()
playlist_json = playlist_response.json()

playlist_name = playlist_json['items'][0]['snippet']['title']
playlist_snapshot_count = len([f for f in os.listdir('.') if os.path.isfile(f) and f.startswith(playlist_name)])
snapshot_file_name = f"{playlist_name} Snapshot #{playlist_snapshot_count + 1}.json"

with open(snapshot_file_name, 'w') as file:
    file.write(json.dumps({'timeTaken': datetime.now().isoformat(), 'playlistId': playlist_id, 'videos': videos_in_playlist}))

print('Finished taking snapshot sucessfully.')