from django.test import TestCase
from api.builder import APIUrlsBuilder
from api.wrapper import TWrapper
import json


class TestTWrapper(TestCase):   
    def test__can_fetch_tweets(self):
        url = "/twapi/user/twitter/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test__can_fetch_hashtag(self):
        url = "/twapi/hashtag/twitter/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test__can_fetch_trends(self):
        url = "/twapi/trends/id=23424853"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test__can_fetch_location(self):
        url = "/twapi/location/lat=44.50&lon=11.35&rad=5"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class TestAPIUrlsBuilder(TestCase):
    def test__can_build_user_url(self):
        target_url = "https://api.twitter.com/2/users/by?usernames=twitter"
        response_url = APIUrlsBuilder().build_user_url()
        self.assertEqual(target_url, response_url)

    def test__can_build_tweets_url(self):
        target_url = "https://api.twitter.com/2/tweets/search/recent?query=from:twitter&tweet.fields=author_id,created_at&max_results=10"
        response_url = APIUrlsBuilder().build_tweets_url()
        self.assertEqual(target_url, response_url)

    def test__can_build_hashtag_url(self):
        target_url = "https://api.twitter.com/2/tweets/search/recent?query=+%23twitter -RT&tweet.fields=created_at,id,text,author_id&expansions=author_id&max_results=15"
        response_url = APIUrlsBuilder().build_hashtag_url()
        self.assertEqual(target_url, response_url)

    def test__can_build_trends_url(self):
        target_url = "https://api.twitter.com/1.1/trends/place.json?id=23424853"
        response_url = APIUrlsBuilder().build_trends_url()
        self.assertEqual(target_url, response_url)    

    def test__can_build_location_url(self):
        target_url = "https://api.twitter.com/1.1/search/tweets.json?geocode=44.5,11.35,5mi&count=100"
        response_url = APIUrlsBuilder().build_location_url(44.50, 11.35, 5)
        self.assertEqual(target_url, response_url) 

class TestViews(TestCase):
    def test__can_send_json_user_tweets(self):
        try:
            json.loads(TWrapper().fetch_tweets())
            response_format = True
        except json.decoder.JSONDecodeError:
            response_format = False
        self.assertTrue(response_format)

    def test__can_send_json_hashtag(self):
        try:
            json.loads(TWrapper().fetch_hashtag())
            response_format = True
        except json.decoder.JSONDecodeError:
            response_format = False
        self.assertTrue(response_format)

    def test__can_send_json_location(self):
        try:
            json.loads(TWrapper().fetch_location())
            response_format = True
        except json.decoder.JSONDecodeError:
            response_format = False
        self.assertTrue(response_format)

    def test__can_send_json_trends(self):
        try:
            json.loads(TWrapper().fetch_trends())
            response_format = True
        except json.decoder.JSONDecodeError:
            response_format = False
        self.assertTrue(response_format)

    

       
