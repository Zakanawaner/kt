import tweepy
import json


class TwitterClient:
    def __init__(self):
        data = json.load(open('secret/config.json'))
        auth = tweepy.OAuth1UserHandler(consumer_key=data['twitter-consumer-key'],
                                        consumer_secret=data['twitter-consumer-secret'])
        auth.set_access_token(data['twitter-access-token'],
                              data['twitter-access-token-secret'])
        # Create API object
        self.twitterClient = tweepy.Client(consumer_key=data['twitter-consumer-key'],
                                           consumer_secret=data['twitter-consumer-secret'],
                                           access_token=data['twitter-access-token'],
                                           access_token_secret=data['twitter-access-token-secret'])
        self.twitterClient.session.auth = auth
        self.globalFollow()

    def newGame(self, game):
        self.twitterClient.create_tweet(text="New Game!\n\n{} ({})\nVS\n{} ({})\n\nVisit killteamdata.com".format(game.winFaction[0].name,
                                                                                                                  game.winTotal,
                                                                                                                  game.losFaction[0].name,
                                                                                                                  game.losTotal))

    def globalFollow(self):
        pass
