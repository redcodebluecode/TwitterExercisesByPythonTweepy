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

def profile2(idlist):
    for id in idlist:
        p=api.get_user(user_id=id)
        print p.screen_name
        print p.id
profile2(ids)

# Collect the first 20 followers of a specified user.
def followers(idlist):
    for id in idlist:
        i = 1
        for follower in tweepy.Cursor(api.followers, user_id=id).items(20):
            print 'follower no.' + str(i) + ' of ' + str(id) + ': ' + follower.screen_name
            i += 1
followers(ids)

# Collect the first 20 friends of a specified user.
def friends(idlist):
    for id in idlist:
        i = 1
        for friendid in tweepy.Cursor(api.friends_ids, user_id=id).items(20):
            p = api.get_user(user_id=friendid)
            print 'friend no.' + str(i) + ' of ' + str(id) + ': ' + p.screen_name + ' ' + str(p.id)
            i += 1
friends(ids)

# Assign key words to the keyword_list
kws = ('Indiana', 'weather') 

# Collect 50 tweets that contain a specified keyword.
def tweets_with_kw(kwlist):
    for kw in kwlist:
        for tweet in tweepy.Cursor(api.search, q=kw).items(50):
            try:
	            print "tweet with keyword '" + kw + "' : " + tweet.text.encode('utf-8')
            except tweepy.TweepError as e:
	            print(e.reason)
tweets_with_kw(kws)

# Collect 50 tweets that originate from a specified geographic region
# Import Tweepy, sys, sleep, credentials.py
try:
    import json
except ImportError:
    import simplejson as json
import tweepy, sys
from time import sleep
from credentials import *

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Assign coordinates to the variable
box = [-74.0,40.73,-73.0,41.73]

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__()
        self.counter = 0
        
    def on_status(self, status):
        record = {'Text': status.text, 'Coordinates': status.coordinates, 'Place': status.place, 'Created At': status.created_at}
        self.counter += 1
        if self.counter <= 50:
            print record
            return True
        else:
            return False
            
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(api.auth, listener=myStreamListener)
myStream.filter(locations=box, async=True)

