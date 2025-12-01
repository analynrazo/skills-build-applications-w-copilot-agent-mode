from django.test import TestCase
from .models import Team, User, Activity, Workout, Leaderboard
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class ModelTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Marvel', description='Marvel Superheroes')
        self.user = User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=self.team, is_superhero=True)
        self.workout = Workout.objects.create(name='Web Swing', description='Swinging through the city')
        self.workout.suggested_for.add(self.team)
        self.leaderboard = Leaderboard.objects.create(team=self.team, points=100)
        self.activity = Activity.objects.create(user=self.user, type='Swing', duration=30, date='2025-12-01')

    def test_team_str(self):
        self.assertEqual(str(self.team), 'Marvel')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'Spider-Man')

    def test_activity_str(self):
        self.assertIn('Spider-Man', str(self.activity))

    def test_workout_str(self):
        self.assertEqual(str(self.workout), 'Web Swing')

    def test_leaderboard_str(self):
        self.assertIn('Marvel', str(self.leaderboard))

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='DC', description='DC Superheroes')
        self.user = User.objects.create(name='Batman', email='batman@dc.com', team=self.team, is_superhero=True)

    def test_api_root(self):
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('teams', response.data)

    def test_team_list(self):
        response = self.client.get('/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(t['name'] == 'DC' for t in response.data))
