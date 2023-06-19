
# search for artist
# find artist
# get artist id, 
# get tracks associated

from dotenv import load_dotenv
# easily load env files and 
# makes working with env variables easier

import os
import base64 # built in yasss
import json
from requests import post, get
 # post requests

load_dotenv()
# auto load enviro var (ONLY LOADS IF FILE = .env)

client_id = os.getenv("CLIENT_ID")
# get value of env var (which is CLIENT_ID here)

client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    #concatenate client_id to client_secret
    #encode string w base64
    #send to retrive access_token
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    # base64.b64encode(auth_base64) returns:
    # base 64, then convert into string

    url = "https://accounts.spotify.com/api/token" 
    headers = {
        "Authorization": "Basic " + auth_base64, # send auth data
        # verify everything is right
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data) # body of req
    # this returns JSON data in .content from result obj above
    json_result = json.loads(result.content) # loads is load from string
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}
    # shortcut for the headers thing i think


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    #construct query (q)
    query = f"?q={artist_name}&type=artist&limit=5"
    # text value searching for after q=
    # after &type, if artist or track, &type = artist,track
    # limit = 1 means first result that pops up
    # meaning first artist

    query_url = url + query
    # could also put the ? in query before the query here
    # now use get method for this (?) endpoint
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    # parse json result again
    # the artists and items fields are always going to exist
    if len(json_result) == 0:
        print("No artist with this name exists :(")
        return None
    elif len(json_result) > 1:
        print(f"There are {len(json_result)} results: ")

    print(json_result[0])
    
    #print(artist_list)


    return(json_result[0])
    
    # if limit greater than 1 probably return a list and let users scroll through

# def get_artist_list(token, artist_name):


    
# artist_list = search_for_artist(token, result)
# for idx, artist in enumerate(artist_list):
#     print(f"{idx + 1}. {json_result['artists']}")



def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    print(f"{json_result[0]['artists']} this prints artist info in list format")
    # print(json_result[1])
    print(f"{json_result} this is json_result")
    return json_result


token = get_token()
# print(token)

artist_input = input("Which artist do you want to search for?\n >> ")

result = search_for_artist(token, artist_input)
# print(result["name"])

artist_id = result["id"]
# intro_sentence = f"{result['name']}\'s genre: {result['genres']}"


def get_genre(result):
    genre_bit = ''
    if len(result["genres"]) == 0:
        #genre_bit = "[N/A]"
        print(genre_bit)
        return "N/A"
    else:
        return ', '.join(result['genres'])
        

genre_bit = get_genre(result)


# print(intro_sentence)

def cleanWord(word):
    return word.replace(']', '').replace('[', '').replace('\'', '')

acc_intro_sentence = f"{result['name']}\'s genre: "
for chara in genre_bit:
    acc_intro_sentence += cleanWord(chara)

print(acc_intro_sentence)

songs = get_songs_by_artist(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")
    # to my understanding idx is like i when you're going like i++
    # it's like the counter that you increase by one each time when looping

#####################################################
##                  CLEAN UP CODE                  ##
#####################################################




# difficult part is getting auth token right
# knowing how to encode it using base 64
# and how to send the right headers


# {'artists': 
# artists is the whole json object/py dictionary
# 
# {'href': 'https://api.spotify.com/v1/search?query=dpr+ian&type=artist&offset=0&limit=1', 
# 
# 'items': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/2o8gT0fQmFxGNbowbdgeZe'}, 'followers': {'href': None, 'total': 791259}, 'genres': ['k-rap'], 'href': 'https://api.spotify.com/v1/artists/2o8gT0fQmFxGNbowbdgeZe', 'id': '2o8gT0fQmFxGNbowbdgeZe', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5eb4d6b4481b6e8bb1bf426cb3a', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab676161000051744d6b4481b6e8bb1bf426cb3a', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f1784d6b4481b6e8bb1bf426cb3a', 'width': 160}], 'name': 'DPR IAN', 'popularity': 64, 'type': 'artist', 'uri': 'spotify:artist:2o8gT0fQmFxGNbowbdgeZe'}], 
# items contains all the different results, and the above is 1
# if there is a result, the look for it, else say no artist with this name
# 
# 'limit': 1, 'next': 'https://api.spotify.com/v1/search?query=dpr+ian&type=artist&offset=1&limit=1', 'offset': 0, 'previous': None, 'total': 22}}  



# authorization and authentication differs
# we just query information here (artist, album, song, track)
# but there's another aspect
# control spotify player
# information about profile or playlist
# this part req you to authenticate user
# usually done through website or front-end-interface
# this is back-end, CLI
# (using client credentials workflow)
# in this case, we have one set (v user credentials workflow)
# anybody who runs this code will use the one set of credentials

# req access token through send client_id, client_secret,
# grant_type,
# to spotify account services, who returns it (expires in 1 hour)
# (spotify acc services is diff from main api service)

# send req to spotify web API through access_token
# returns info about artists, tracks, etc.

# if token expires, then req new or use refresh token

# data must be encoded in 'application/x-www-form-urlencoded',



