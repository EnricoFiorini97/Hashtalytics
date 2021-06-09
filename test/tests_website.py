from django.test import TestCase
from django.test import Client

class clientTest(TestCase):
    def setUp(self):
        self.c = Client()


    def test_home(self):
        res = self.c.get('/')
        self.assertEqual(res.status_code, 200)

    def test_hashtag_200(self):
        res = self.c.get('/details/',{"hasher": "#ciao"})
        self.assertEqual(res.status_code, 200)

    def test_user_200(self):
        res = self.c.get('/details/', {"hasher": "@fedez"})
        self.assertEqual(res.status_code, 200)

    def test_user_404(self):
        res = self.c.get('/details/',{"hasher": "@frsyhtdueteryhert"})
        self.assertEqual(res.status_code, 404)

    def test_place_200(self):
        res = self.c.get('/details/', {"hasher": "$milano"})
        self.assertEqual(res.status_code, 200)

    def test_details_400(self):
        res = self.c.get('/details/')
        self.assertEqual(res.status_code, 400)

    def test_timeline_200(self):
        res = self.c.get('/details/timeline/twitter')
        self.assertEqual(res.status_code, 200)