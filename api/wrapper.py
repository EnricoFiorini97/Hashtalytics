import env
import json
import tweepy
from tweepy.parsers import JSONParser
from api.errors import ApiError, TweepyError
from http import HTTPStatus

# -- TWrapper version 1.5 --
#
# Welcome to TWrapper! A small, powerful Twitter APIs wrapper.
#
# Authors: Carmine la Luna, Enrico Fiorini, Blu Borghi
#
# Published under GPLv3 License


class TWrapper:
    def __init__(self):
        self.__auth = tweepy.OAuthHandler(env.API_KEY, env.API_SECRETKEY)
        self.__auth.set_access_token(env.ACCESS_TOKEN, env.ACCESS_TOKEN_SECRET)
        self.__api = tweepy.API(self.__auth, parser=tweepy.parsers.JSONParser())
        self.__version = 1.5
        
    @staticmethod
    def __get_response(body, status=HTTPStatus.OK):
        return {
            "status": status,
            "body": json.dumps(body)
            }

    @staticmethod
    def __handle_error(error, context=""):
        if error.get("code") == TweepyError.INVALID_HASHTAG.value:
            if context == "hashtag":
                return TWrapper.__get_response({"error": ApiError.INVALID_HASHTAG.value}, HTTPStatus.BAD_REQUEST)
            if context == "text":
                return TWrapper.__get_response({"error": ApiError.INVALID_TEXT.value}, HTTPStatus.BAD_REQUEST)
            return TWrapper.__get_response({"error": ApiError.INVALID_INPUT.value}, HTTPStatus.BAD_REQUEST)
        if error.get("code") == TweepyError.INVALID_USER.value:
            return TWrapper.__get_response({"error": ApiError.USER_NOT_FOUND.value}, HTTPStatus.NOT_FOUND)
        else:
            return TWrapper.__get_response({"error": f"ERROR {error.get('code')}: {error.get('message')}"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def get_version(self):
        ''' Returns current TWrapper version. '''
        return f"Version {self.__version}"

    def fetch_trends(self, country_id="23424853"):
        ''' Returns top trends in a country '''
        try:  
            return TWrapper.__get_response(self.__api.trends_place(country_id))
        except tweepy.error.TweepError as e:
            return TWrapper.__handle_error(e.args[0][0])

    def fetch_user(self, user="@twitter"):
        ''' Returns user data '''
        try:
            return TWrapper.__get_response(self.__api.get_user(user))
        except tweepy.error.TweepError as e:
            return TWrapper.__handle_error(e.args[0][0])

    def fetch_tweets(self, user="@twitter"):
        ''' Returns tweets data '''
        try:
            return TWrapper.__get_response(self.__api.user_timeline(user,count=100))
        except tweepy.error.TweepError as e:
            return TWrapper.__handle_error(e.args[0][0])

    def fetch_location(self, lat=45, lon=90, radius=5):
        ''' Returns location data '''
        try:
            return TWrapper.__get_response(self.__api.search(geocode=f"{lat},{lon},{radius}km"))
        except tweepy.error.TweepError as e:
            return TWrapper.__handle_error(e.args[0][0])

    def fetch_hashtag(self, hashtag="twitter"):
        ''' Returns hashtag data '''
        try:
            return TWrapper.__get_response(self.__api.search(f"#{hashtag} -RT"))
        except tweepy.error.TweepError as e:
            return TWrapper.__handle_error(e.args[0][0], "hashtag")

    def fetch_text(self, text="twitter"):
        ''' Returns text data '''
        try:
            return TWrapper.__get_response(self.__api.search(text))
        except tweepy.error.TweepError as e:
            return TWrapper.__handle_error(e.args[0][0], "text")
            
    def fetch_timeline(self, user="@twitter"):
        req = self.fetch_tweets(user)
        if req.get("status") != HTTPStatus.OK or not req.get("body"):
            TWrapper.__handle_error(req)
        tmp = json.loads(req['body'])
        res = ""
        for i in range(len(tmp)):
            try:
                if tmp[i]['place']['bounding_box']['coordinates']:
                    res += str(tmp[i])
            except (TypeError, KeyError):   pass
        #You're not supposed to understand this - DO NOT TOUCH (we know it's awful, but trust us..)
        if res == "":
            res = "{status:200, body: user not geolocalized or user not found}"
        return TWrapper.__get_response(res)
