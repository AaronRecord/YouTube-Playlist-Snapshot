# YouTube Playlist Snapshot
 Create snapshots of your youtube playlists to easily recover deleted videos
 
 ## How to use:
To take a snapshot run `take_snapshot.py` and enter the id of your playlist and your api key  
(you can get one for free at https://console.developers.google.com/)  
  
To compare 2 snapshots, run `compare_snapshots.py` and enter the file names of your 2 snapshots  

Snapshots are .json files that save the names and the channel titles of all the videos in your playlist

## Example usage:  
Take a snapshot of one of your playlists. When one of the videos in said playlist gets deleted, take a new snapshot and compare it to the old one.
