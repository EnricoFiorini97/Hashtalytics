import json
import env
from django.test import TestCase
from api.wrapper import TWrapper


class TestTWrapper(TestCase):   
    def test__can_fetch_tweets(self):
        url = "/twapi/user/twitter/"
        response = self.client.get(url, **{'HTTP_AUTHORIZATION': f"Bearer {env.MY_BEARER_TOKEN}"})
        self.assertEqual(response.status_code, 200)

    def test__can_fetch_hashtag(self):
        url = "/twapi/hashtag/twitter/"
        response = self.client.get(url, **{'HTTP_AUTHORIZATION': f"Bearer {env.MY_BEARER_TOKEN}"})
        self.assertEqual(response.status_code, 200)

    def test__can_fetch_trends(self):
        url = "/twapi/trends/"
        response = self.client.get(url, **{'HTTP_AUTHORIZATION': f"Bearer {env.MY_BEARER_TOKEN}"})
        self.assertEqual(response.status_code, 200)

    def test__can_fetch_location(self):
        url = "/twapi/location/44.50/11.35/5/"
        response = self.client.get(url, **{'HTTP_AUTHORIZATION': f"Bearer {env.MY_BEARER_TOKEN}"})
        self.assertEqual(response.status_code, 200)

class TestViews(TestCase):
    def test__can_send_json_user_tweets(self):
        try:
            json.loads(TWrapper().fetch_tweets()['body'])
            response_format = True
        except json.decoder.JSONDecodeError:
            response_format = False
        self.assertTrue(response_format)

    def test__can_send_json_hashtag(self):
        try:
            json.loads(TWrapper().fetch_hashtag()['body'])
            response_format = True
        except json.decoder.JSONDecodeError:
            response_format = False
        self.assertTrue(response_format)

    def test__can_send_json_location(self):
        try:
            json.loads(TWrapper().fetch_location()['body'])
            response_format = True
        except json.decoder.JSONDecodeError:
            response_format = False
        self.assertTrue(response_format)

class TestSecureAccess(TestCase):       
    def test__inexistent_tweets(self):
        url = "/twapi/user/kjdbfkiasb/"
        response = self.client.get(url, **{'HTTP_AUTHORIZATION': f"Bearer {env.MY_BEARER_TOKEN}"})
        self.assertEqual(response.status_code, 404)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test__can_protect_hashtag(self):
        url = "/twapi/hashtag/twitter/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test__can_protect_trends(self):
        url = "/twapi/trends/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test__can_protect_location(self):
        url = "/twapi/location/44.50/11.35/5/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

class TestInexistentSearch(TestCase):   
    def test__inexistent_tweets(self):
        url = "/twapi/user/kjdbfkiasb/"
        response = self.client.get(url, **{'HTTP_AUTHORIZATION': f"Bearer {env.MY_BEARER_TOKEN}"})
        self.assertEqual(response.status_code, 404)

    #If hashtag does not exist, the endpoint still return 200 because hashtags can be add easily with tweets.
    def test__inexistent_hashtag(self):
        url = "/twapi/hashtag/kjdbfkiasb/"
        response = self.client.get(url, **{'HTTP_AUTHORIZATION': f"Bearer {env.MY_BEARER_TOKEN}"})
        self.assertEqual(response.status_code, 200)
        

