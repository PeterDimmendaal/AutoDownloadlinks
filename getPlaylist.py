import requests
from configparser import ConfigParser

def get_track_ids_from_url(url):
    # Get JSON data from url    
    resp = requests.get(url=url) 
    tracks_json = resp.json()    
    # Save all track ID's from JSON data
    track_ids = []
    try: 
        tracks = tracks_json["data"]
        for track in tracks:
            track_ids.append(track['id'])
    except:
        print("Something went wrong, check if the playlist id is correct and you have a working connection.")        
    # Check if url contains more tracks
    try: 
        url_next = tracks_json["next"]
        next_tracks = get_track_ids_from_url(url_next)
        track_ids.extend(next_tracks)
    except:
        pass # 'next' is not always present    
    return track_ids

def save_ids_to_file(ids, path):
        try:            
            downloadlinksFile = open(str(path)+"/downloadLinks.txt","w" )
            for id_ in ids:
                downloadlinksFile.write("https://www.deezer.com/track/"+str(id_)+"\n")
            print("Succesfully downloaded "+str(len(ids))+" tracks.")
        except:
            print("Something went wrong, check if ... is correct.")

# Read data from config
config = ConfigParser()
config.read('CONFIG.ini')
path = config['main']['path_downloadlinks']
playlist_id = config['main']['playlistid']

url = 'http://api.deezer.com/playlist/'+str(playlist_id)+'/tracks'
track_ids = get_track_ids_from_url(url)
if (track_ids):
    save_ids_to_file(track_ids, path)

