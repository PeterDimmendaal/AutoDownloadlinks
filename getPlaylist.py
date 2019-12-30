import requests
import json

#change this to the file location of your downloadlinks.txt
path = "C:\\Users\\Peter\\Music download"
playlistid = input("Paste the playlistID")

url = 'http://api.deezer.com/playlist/'+playlistid +'/tracks'



resp = requests.get(url=url) 
tracksJson = resp.json()
Tracks = tracksJson["data"]
#TODO add error handeling

downloadlinksFile = open(path+ "/downloadLinks.txt","w" )

for track in Tracks:
    downloadlinksFile.write(track['link']+ "\n")
