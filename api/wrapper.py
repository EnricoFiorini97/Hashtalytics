import env
import json
import tweepy
from . import queries
from http import HTTPStatus
from api.errors import ApiError, TweepyError
from json import JSONDecodeError


class TWrapper:
    def __init__(self):
        self.__auth = tweepy.OAuthHandler(env.API_KEY, env.API_SECRETKEY)
        self.__auth.set_access_token(env.ACCESS_TOKEN, env.ACCESS_TOKEN_SECRET)
        self.__api = tweepy.API(self.__auth, parser=tweepy.parsers.JSONParser())
        
    @staticmethod
    def __get_response(body=None, db_response=None, status=HTTPStatus.OK):
        print("db_response", db_response)
        tweets = []
        if isinstance(body, dict) and \
           isinstance(body.get("statuses"), list):
            tweets = body.get("statuses")
        if isinstance(body, list):
            tweets = body

        if len(tweets) > 0 and \
           isinstance(db_response, list) and \
           len(db_response) > 0:
            for r in db_response:
                tweet = TWrapper.__db_object_to_tweet(r)
                add = True
                for t in tweets:
                    if t.get("id") == tweet.get("id"):
                        add = False
                        break
                if add:
                    tweets.append(tweet)
        return {
            "status": status,
            "body": json.dumps(body)
            }

    @staticmethod
    def __handle_error(error, context="") -> str:
        if error == TweepyError.PROTECTED_USER.value:
            return TWrapper.__get_response({"error": ApiError.PROTECTED_USER.value}, status=HTTPStatus.FORBIDDEN)
        if error.get("code") == TweepyError.INVALID_HASHTAG.value:
            if context == "hashtag":
                return TWrapper.__get_response({"error": ApiError.INVALID_HASHTAG.value}, status=HTTPStatus.BAD_REQUEST)
            if context == "text":
                return TWrapper.__get_response({"error": ApiError.INVALID_TEXT.value}, status=HTTPStatus.BAD_REQUEST)
            return TWrapper.__get_response({"error": ApiError.INVALID_INPUT.value}, status=HTTPStatus.BAD_REQUEST)
        if error.get("code") == TweepyError.INVALID_USER.value:
            return TWrapper.__get_response({"error": ApiError.USER_NOT_FOUND.value}, status=HTTPStatus.NOT_FOUND)
        else:
            return TWrapper.__get_response({"error": f"ERROR {error.get('code')}: {error.get('message')}"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    def fetch_trends(self, country_id="23424853") -> str:
        try:  
            return TWrapper.__get_response(self.__api.trends_place(country_id))
        except tweepy.error.TweepError as e:
            return TWrapper.__handle_error(e.args[0][0])

    def fetch_user(self, user="@twitter") -> str:
        ''' Returns user data '''
        try:
            return TWrapper.__get_response(self.__api.get_user(user))
        except tweepy.error.TweepError as e:
            return TWrapper.__handle_error(e.args[0][0])

    def fetch_tweets(self, user="@twitter") -> str:
        ''' Returns tweets data '''
        try:
            return TWrapper.__get_response(self.__api.user_timeline(user,count=100), queries.custom_query(queries.tweet_search_by_user(user)))
        except tweepy.error.TweepError as e:
            return TWrapper.__handle_error(e.args[0][0])
            
    def fetch_location(self, lat=45, lon=90, radius=5) -> str:
        ''' Returns location data '''
        try:
            return TWrapper.__get_response(self.__api.search(geocode=f"{lat},{lon},{radius}km"))
        except tweepy.error.TweepError as e:
            return TWrapper.__handle_error(e.args[0][0])

    def fetch_hashtag(self, hashtag="twitter") -> str:
        ''' Returns hashtag data '''
        try:
            return TWrapper.__get_response(self.__api.search(f"#{hashtag} -RT"), queries.custom_query(queries.tweet_search_by_hashtag(hashtag)))
        except tweepy.error.TweepError as e:
            return TWrapper.__handle_error(e.args[0][0], "hashtag")

    def fetch_text(self, text="twitter") -> str:
        ''' Returns text data '''
        try:
            return TWrapper.__get_response(self.__api.search(text), queries.custom_query(queries.tweet_search_by_text(text)))
        except tweepy.error.TweepError as e:
            return TWrapper.__handle_error(e.args[0][0], "text")
            
    def fetch_timeline(self, user="@twitter") -> str:
        req = self.fetch_tweets(user)
        if req.get("status") != HTTPStatus.OK or not req.get("body"):
            TWrapper.__handle_error(req)
        tmp = json.loads(req['body'])
        res = []
        for i in range(len(tmp)):
            try:
                if tmp[i]['place']['bounding_box']['coordinates']:
                    res.append(tmp[i])
            except (TypeError, KeyError):   pass
        if not len(res):
            return TWrapper.__get_response({"error": ApiError.USER_NOT_FOUND.value }, status=404)
        return TWrapper.__get_response(res)

    @staticmethod
    def __db_object_to_tweet(o):
        media = None
        try:
            media = json.loads(o.get("ent_media"))
        except JSONDecodeError:
            pass
        tweet = {
            "id": int(o.get("id_hash")) ,
            "created_at": o.get("created_at"),
            "text": o.get("text"),
            "id_str": o.get("id_str"),
            "truncated": o.get("truncated"),
            "ent_hashtags": o.get("ent_hashtags"),
            "ent_symbols": o.get("ent_symbols"),
            "ent_urls": o.get("ent_urls"),
            "metadata_iso_language_code": o.get("metadata_iso_language_code"),
            "metadata_result_type": o.get("metadata_result_type"),
            "source": o.get("source"),
            "in_reply_to_status_id": o.get("in_reply_to_status_id"),
            "in_reply_to_status_id_str": o.get("in_reply_to_status_id_str"),
            "in_reply_to_user_id": o.get("in_reply_to_user_id"),
            "in_reply_to_user_id_str": o.get("in_reply_to_user_id_str"),
            "in_reply_to_screen_name": o.get("in_reply_to_screen_name"),
            "user": {
                "id": o.get("user_id"),
                "id_str": o.get("user_id_str"),
                "name": o.get("user_name"),
                "screen_name": o.get("user_screen_name"),
                "location": o.get("user_location"),
                "description": o.get("user_description"),
                "url": o.get("user_url"),
                "protected": o.get("user_protected"),
                "followers_count": o.get("user_followers_count"),
                "friends_count": o.get("user_friends_count"),
                "listed_count": o.get("user_listed_count"),
                "created_at": o.get("user_created_at"),
                "favourites_count": o.get("user_favourites_count"),
                "utc_offset": o.get("user_utc_offset"),
                "time_zone": o.get("user_time_zone"),
                "geo_enabled": o.get("user_geo_enabled"),
                "verified": o.get("user_verified"),
                "statuses_count": o.get("user_statuses_count"),
                "lang": o.get("user_lang"),
                "contributors_enabled": o.get("user_contributors_enabled"),
                "is_translator": o.get("user_is_translator"),
                "is_translation_enabled": o.get("user_is_translation_enabled"),
                "profile_background_color": o.get("user_profile_background_color"),
                "profile_background_image_url": o.get("user_profile_background_image_url"),
                "profile_background_image_url_https": o.get("user_profile_background_image_url_https"),
                "profile_background_tile": o.get("user_profile_background_tile"),
                "profile_image_url": o.get("user_profile_image_url"),
                "profile_image_url_https": o.get("user_profile_image_url_https"),
                "profile_link_color": o.get("user_profile_link_color"),
                "profile_sidebar_border_color": o.get("user_profile_sidebar_border_color"),
                "profile_sidebar_fill_color": o.get("user_profile_sidebar_fill_color"),
                "profile_text_color": o.get("user_profile_text_color"),
                "profile_use_background_image": o.get("user_profile_use_background_image"),
                "has_extended_profile": o.get("user_has_extended_profile"),
                "default_profile": o.get("user_default_profile"),
                "default_profile_image": o.get("user_default_profile_image"),
                "following": o.get("user_following"),
                "follow_request_sent": o.get("user_follow_request_sent"),
                "notifications": o.get("user_notifications"),
                "translator_type": o.get("user_translator_type"),
                "withheld_in_countries": o.get("user_withheld_in_countries"),
            },
            "entities": {
                "media": media
            },
            "geo": o.get("geo"),
            "coordinates": o.get("coordinates"),
            "place": o.get("place"),
            "is_quote_status": o.get("is_quote_status"),
            "retweet_count": o.get("retweet_count"),
            "favorite_count": o.get("favorite_count"),
            "favorited": o.get("favorited"),
            "retweeted": o.get("retweeted"),
            "lang": o.get("lang"),
            "this_is_form_db": True
        }
        return tweet
