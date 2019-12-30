import requests
import json

#change this to the file location of your downloadlinks.txt
path = "C:\\Users\\Peter\\Music download"
playlistid = input("Paste the playlistID")

url = 'http://api.deezer.com/playlist/'+playlistid +'/tracks'



resp = requests.get(url=url) 
tracksJson = resp.json()
try: 
    Tracks = tracksJson["data"]
    downloadlinksFile = open(path+ "/downloadLinks.txt","w" )
    for track in Tracks:
        downloadlinksFile.write(track['link']+ "\n")
    print("succes")
except:
    print("Something went wrong, check if the playlist id is correct and you have a working connection")

input()

    


