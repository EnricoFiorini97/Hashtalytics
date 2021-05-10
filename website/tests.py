from django.test import TestCase
from django.test import Client

class clientTest(TestCase):
    def setUp(self):
        self.c = Client()


    def test_home(self):
        res = self.c.get('/')
        self.assertEqual(res.status_code, 200)

    def test_details(self):
        res = self.c.get('/details/')
        self.assertEqual(res.status_code, 302)
        res = self.c.post('/details/')
        self.assertEqual(res.status_code, 400)
        res = self.c.post('/details/', {'hasher': "@mario"})
        self.assertEqual(res.status_code, 200)
        res = self.c.post('/details/', {'hasher': "#mario"})
        self.assertEqual(res.status_code, 200)