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
        self.twitterApi = tweepy.API(auth)

    def newGame(self, game):
        winner = self.twitterApi.media_upload(f"static/images/{game.winFaction[0].shortName}.png")
        loser = self.twitterApi.media_upload(f"static/images/{game.losFaction[0].shortName}.png")
        self.twitterClient.create_tweet(
            text=f"New Game! "
                 f"\nkillteamdata.com/game/{game.id}"
                 f"\n\n"
                 f"Mission: {game.mission[0].name}"
                 f"\n\n"
                 f"{game.winFaction[0].name} ({game.winTotal})"
                 f" vs "
                 f"{game.losFaction[0].name} ({game.losTotal})"
                 f"\n\n"
                 f"For more information, visit killteamdata.com",
            media_ids=[winner.media_id, loser.media_id]
        )

    def weeklyTweet(self, games, factions):
        mediaIds = [self.twitterApi.media_upload(f"static/images/ktd.png").media_id]
        try:
            topOpenKey = next(iter(factions['open']))
            topOpen = self.twitterApi.media_upload(f"static/images/{topOpenKey}.png")
            mediaIds.append(topOpen.media_id)
        except StopIteration:
            topOpenKey = None
        try:
            topMatchedKey = next(iter(factions['matched']))
            topMatched = self.twitterApi.media_upload(f"static/images/{topMatchedKey}.png")
            mediaIds.append(topMatched.media_id)
        except StopIteration:
            topMatchedKey = None
        try:
            topNarrativeKey = next(iter(factions['narrative']))
            topNarrative = self.twitterApi.media_upload(f"static/images/{topNarrativeKey}.png")
            mediaIds.append(topNarrative.media_id)
        except StopIteration:
            topNarrativeKey = None
        self.twitterClient.create_tweet(
            text=f"Last week activity on killteamdata.com "
                 f"\n\n"
                 f"Open: "
                 f"\n"
                 f"Games: {len(games['open'])}"
                 f"\n"
                 f"Top faction: {factions['open'][topOpenKey]['name'] if topOpenKey else '-'} ({factions['open'][topOpenKey]['winRate'] if topOpenKey else '-'}% Win rate)"
                 f"\n\n"
                 f"Matched: "
                 f"\n"
                 f"Games: {len(games['matched'])}"
                 f"\n"
                 f"Top faction: {factions['matched'][topMatchedKey]['name'] if topMatchedKey else '-'} ({factions['matched'][topMatchedKey]['winRate'] if topMatchedKey else '-'}% Win rate)"
                 f"\n\n"
                 f"Narrative: "
                 f"\n"
                 f"Games: {len(games['narrative'])}"
                 f"\n"
                 f"Top faction: {factions['narrative'][topNarrativeKey]['name'] if topNarrativeKey else '-'} ({factions['narrative'][topNarrativeKey]['winRate'] if topNarrativeKey else '-'}% Win rate)"
                 f"\n\n"
                 f"For more information, visit killteamdata.com",
            media_ids=mediaIds
        )

