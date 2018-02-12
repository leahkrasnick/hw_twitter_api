from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data1 # file that contains OAuth credentials
# import nltk # uncomment line after you install nltk

## SI 206 - HW
## COMMENT WITH:
#SECTION: Tuesdays 5:30 - 7
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends


#Write your code below:
#Code for Part 3:Caching

# on startup, try to load the cache from file
CACHE_FNAME = 'twitter_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()


except:
    CACHE_DICTION = {}


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

def make_request_using_cache(baseurl, params, auth):
    unique_ident = params_unique_combination(baseurl,params)



    if unique_ident in CACHE_DICTION:
        print("Fetching cached data...")
        return CACHE_DICTION[unique_ident]


    else:
        print("Making a request for new data...")

        resp = requests.get(baseurl, params, auth=auth)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


def get_twitter_data_caching(username, num_tweets):
    params_diction = {'screen_name': username, 'count' : num_tweets}
    return make_request_using_cache(baseurl, params_diction)


baseurl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
response = make_request_using_cache(baseurl, params={'screen_name': username, 'count': num_tweets}, auth=auth)






#Finish parts 1 and 2 and then come back to this

#Code for Part 1:Get Tweets

baseurl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
params = {'screen_name':username,'count': num_tweets}
r = requests.get(baseurl, params=params, auth=auth)
obj = json.loads(r.text)
#return obj

#Code for Part 2:Analyze Tweets
import nltk

list_of_text = []
for x in obj:
    list_of_text.append(x['text'])

big_string = " ".join(list_of_text)

#Creates list of tokens

tokens = nltk.word_tokenize(big_string)

#Creates frequency distribution from list

bad_word =["www.", 'http', 'https', 'RT']
freqDist = nltk.FreqDist(token for token in tokens if token.isalpha() and 'http' not in token and 'RT' not in token)

#Loop through and print the words and frequencies for the most common 5 words

for word, frequency in freqDist.most_common(5):
    print(word + " " + str(frequency))



if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
