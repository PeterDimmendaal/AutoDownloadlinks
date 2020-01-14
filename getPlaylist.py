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
        print("Something went wrong with acquiring track ids from Deezer.")
        print("Check if the playlist id is correct and you have a working connection.")        
    # Check if url contains more tracks
    try: 
        url_next = tracks_json["next"]
        next_tracks = get_track_ids_from_url(url_next)
        track_ids.extend(next_tracks)
    except:
        pass # 'next' is not always present    
    return track_ids

def remove_already_downloaded(ids, path):    
    # Idea: Optimized by running over file once and over the ids multiple times because ids list is probably shorter.
    track_ids = []
    remove_cnt = 0
    try: 
        with open(str(path)+"/downloadedSuccessfully.txt","r") as downloadedSuccesFile:
            for id_ in ids:
                downloadedSuccesFile.seek(0)
                if ('/'+str(id_)+'\n') in downloadedSuccesFile.read():
                    remove_cnt += 1
                else:
                    track_ids.append(id_)
        print('Removed '+str(remove_cnt)+' alrady downloaded track(s)')
        downloadedSuccesFile.close()
    except:
        print("Something went wrong during removing already downloaded files.")
        print("Check if path to files is correct and downloadedSuccessfully.txt exists.")
    return track_ids

def save_ids_to_file(ids, path):
    try:            
        downloadlinksFile = open(str(path)+"/downloadLinks.txt","w" )
        for id_ in ids:
            downloadlinksFile.write("https://www.deezer.com/track/"+str(id_)+"\n")
        print("Succesfully added "+str(len(ids))+" track(s).")
    except:
        print("Something went wrong during saving track ids.")
        print("Check if path to files is correct and downloadLinks.txt exists.")
    downloadlinksFile.close()

# Read data from config
config = ConfigParser()
config.read('CONFIG.ini')
path = config['main']['path_downloadlinks']
playlist_id = config['main']['playlistid']
exclude_ids = config['main']['exclude_already_donloaded']

url = 'http://api.deezer.com/playlist/'+str(playlist_id)+'/tracks'
track_ids = get_track_ids_from_url(url)
print("Found "+str(len(track_ids))+" track(s).")
if(int(exclude_ids)):
    track_ids = remove_already_downloaded(track_ids, path)
if (track_ids):
    save_ids_to_file(track_ids, path)

