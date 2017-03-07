# Import Tweepy, sys, sleep, credentials.py
import tweepy, sys
from time import sleep
from credentials import *

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Assign id values to the id_list
ids = (34373370, 26257166, 12579252)

# Collect the users' profile information.
def profile(idlist):
    for id in idlist:
	    print api.get_user(user_id=id)

profile(ids)

# Collect the first 20 followers of a specified user.
def followers(idlist):
    for id in idlist:
	    print 'follower: ' + api.followers(user_id=id).screen_name.items(20) 
		# for follower in tweepy.Cursor(api.followers, user_id=id).items(20):
		    # print 'follower: ' + follower.screen_name

followers(ids)

# Collect the first 20 friends of a specified user.
def friends(idlist):
    for id in idlist:
	    print 'friend: ' + api.friends_ids(user_id=id).screen_name.items(20)
		# for friend in tweepy.Cursor(api.friends_ids, user_id=id).items(20):
		    # print 'friend: ' + friend.screen_name
		
friends(ids)

# Assign key words to the keyword_list
kws = ('Indiana', 'weather') 

# Collect 50 tweets that contain a specified keyword.
def tweets_with_kw(kwlist):
    for kw in kwlist:
        for tweet in tweepy.Cursor(api.search, q=kw).items(50):
	        print "tweet with keyword '" + kw + "' : " + tweet.text

tweets_with_kw(kws)

# Assign coordinates to the variable
box = [-86.33,41.63,-86.20,41.74]

# Stream Data Function
class CustomStreamListener(tweepy.StreamListener):
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream
    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

stream = tweepy.streaming.Stream(auth, CustomStreamListener()).filter(locations=box).items(50)
stream
