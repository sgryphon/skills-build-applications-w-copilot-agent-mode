from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime
from .models import User, Team, Activity, Leaderboard, Workout


class UserAPITestCase(TestCase):
    """Test cases for User API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            fitness_level='beginner',
            avatar='https://example.com/avatar.jpg'
        )
        self.user.set_password('testpass123')
        self.user.save()
    
    def test_list_users(self):
        """Test listing all users."""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_user(self):
        """Test creating a new user."""
        data = {
            'name': 'New User',
            'email': 'new@example.com',
            'password': 'newpass123',
            'fitness_level': 'intermediate'
        }
        response = self.client.post('/api/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
    
    def test_get_user_by_email(self):
        """Test getting user by email."""
        response = self.client.get('/api/users/by_email/?email=test@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
    
    def test_get_users_by_fitness_level(self):
        """Test filtering users by fitness level."""
        response = self.client.get('/api/users/by_fitness_level/?level=beginner')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TeamAPITestCase(TestCase):
    """Test cases for Team API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            captain='Test Captain',
            members=['Member1', 'Member2']
        )
    
    def test_list_teams(self):
        """Test listing all teams."""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_team(self):
        """Test creating a new team."""
        data = {
            'name': 'New Team',
            'description': 'A new test team',
            'captain': 'New Captain',
            'members': ['Member3', 'Member4']
        }
        response = self.client.post('/api/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)
    
    def test_add_team_member(self):
        """Test adding a member to a team."""
        team_id = str(self.team._id)
        data = {'member_name': 'Member3'}
        response = self.client.post(f'/api/teams/{team_id}/add_member/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.team.refresh_from_db()
        self.assertIn('Member3', self.team.members)
    
    def test_remove_team_member(self):
        """Test removing a member from a team."""
        team_id = str(self.team._id)
        data = {'member_name': 'Member1'}
        response = self.client.post(f'/api/teams/{team_id}/remove_member/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.team.refresh_from_db()
        self.assertNotIn('Member1', self.team.members)


class ActivityAPITestCase(TestCase):
    """Test cases for Activity API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.activity = Activity.objects.create(
            user='Test User',
            activity_type='running',
            duration=30,
            distance=5.0,
            calories_burned=300,
            date=datetime.now(),
            notes='Test run'
        )
    
    def test_list_activities(self):
        """Test listing all activities."""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_activity(self):
        """Test creating a new activity."""
        data = {
            'user': 'Test User',
            'activity_type': 'cycling',
            'duration': 45,
            'distance': 10.0,
            'calories_burned': 400,
            'date': datetime.now().isoformat(),
            'notes': 'Test cycle'
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 2)
    
    def test_get_activities_by_user(self):
        """Test filtering activities by user."""
        response = self.client.get('/api/activities/by_user/?user=Test User')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_activities_by_type(self):
        """Test filtering activities by type."""
        response = self.client.get('/api/activities/by_type/?type=running')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_recent_activities(self):
        """Test getting recent activities."""
        response = self.client.get('/api/activities/recent/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class LeaderboardAPITestCase(TestCase):
    """Test cases for Leaderboard API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.entry = Leaderboard.objects.create(
            user='Test User',
            team='Test Team',
            total_points=1000,
            rank=1
        )
    
    def test_list_leaderboard(self):
        """Test listing all leaderboard entries."""
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_leaderboard_entry(self):
        """Test creating a new leaderboard entry."""
        data = {
            'user': 'Another User',
            'team': 'Test Team',
            'total_points': 800,
            'rank': 2
        }
        response = self.client.post('/api/leaderboard/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Leaderboard.objects.count(), 2)
    
    def test_get_top_leaderboard(self):
        """Test getting top leaderboard entries."""
        response = self.client.get('/api/leaderboard/top/?limit=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_get_leaderboard_by_team(self):
        """Test filtering leaderboard by team."""
        response = self.client.get('/api/leaderboard/by_team/?team=Test Team')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class WorkoutAPITestCase(TestCase):
    """Test cases for Workout API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(
            title='Test Workout',
            description='A test workout',
            difficulty_level='beginner',
            duration=30,
            activity_type='running',
            target_fitness_level='beginner',
            instructions='1. Warm up\n2. Run\n3. Cool down'
        )
    
    def test_list_workouts(self):
        """Test listing all workouts."""
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_workout(self):
        """Test creating a new workout."""
        data = {
            'title': 'New Workout',
            'description': 'A new test workout',
            'difficulty_level': 'intermediate',
            'duration': 45,
            'activity_type': 'gym',
            'target_fitness_level': 'intermediate',
            'instructions': '1. Warm up\n2. Exercise\n3. Cool down'
        }
        response = self.client.post('/api/workouts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 2)
    
    def test_get_workouts_by_difficulty(self):
        """Test filtering workouts by difficulty."""
        response = self.client.get('/api/workouts/by_difficulty/?difficulty=beginner')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_workouts_by_fitness_level(self):
        """Test filtering workouts by fitness level."""
        response = self.client.get('/api/workouts/by_fitness_level/?level=beginner')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_workouts_by_activity_type(self):
        """Test filtering workouts by activity type."""
        response = self.client.get('/api/workouts/by_activity_type/?type=running')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class APIRootTestCase(TestCase):
    """Test cases for API root endpoint."""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_api_root(self):
        """Test API root endpoint at /api/."""
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('endpoints', response.data)
        self.assertIn('users', response.data['endpoints'])
        self.assertIn('teams', response.data['endpoints'])
        self.assertIn('activities', response.data['endpoints'])
        self.assertIn('leaderboard', response.data['endpoints'])
        self.assertIn('workouts', response.data['endpoints'])
    
    def test_root_redirect(self):
        """Test root endpoint / points to API."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
