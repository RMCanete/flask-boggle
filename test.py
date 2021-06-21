from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """ To do before each test """
        app.config['TESTING'] = True

    def test_homepage(self):
        """ Test the session """

        with app.test_client() as client:
           resp = client.get("/")
           self.assertIn('board', session)
           self.assertIsNone(session.get('highscore'))
           self.assertIsNone(session.get('num_plays'))

           
    def test_valid_word(self):
        """ Test if word is valid """

        with app.test_client() as client:
            client.get('/')
            session['board'] = [['a', 'n', 'd', 'a', 'a'],
                                ['n', 'a', 'a', 'a', 'a'],
                                ['d', 'a', 'a', 'a', 'a'],
                                ['a', 'a', 'a', 'a', 'a'],
                                ['a', 'a', 'a', 'a', 'a']]
            resp = client.get('/check-word?word=and')
            self.assertIn(resp.json['result'], 'ok')
    
    def test_not_on_board(self):
        """ Test if word is not on board """

        with app.test_client() as client:
            client.get('/')
            resp = client.get('/check-word?word=chicken')
            self.assertEqual(resp.json['result'], 'not-on-board')

    def test_not_a_word(self):
        """ Test if word is not a word """

        with app.test_client() as client:
            client.get('/')
            resp = client.get('/check-word?word=abcdefg')
            self.assertEqual(resp.json['result'], 'not-word')