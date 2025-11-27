from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing data...')
        
        # Delete all existing data using Django ORM
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('✓ Existing data deleted'))
        
        # Create Marvel superhero users
        self.stdout.write('Creating Marvel superheroes...')
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'tony.stark@marvel.com', 'fitness_level': 'advanced', 
             'avatar': 'https://example.com/ironman.jpg'},
            {'name': 'Captain America', 'email': 'steve.rogers@marvel.com', 'fitness_level': 'advanced',
             'avatar': 'https://example.com/cap.jpg'},
            {'name': 'Thor', 'email': 'thor.odinson@marvel.com', 'fitness_level': 'advanced',
             'avatar': 'https://example.com/thor.jpg'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@marvel.com', 'fitness_level': 'advanced',
             'avatar': 'https://example.com/blackwidow.jpg'},
            {'name': 'Hulk', 'email': 'bruce.banner@marvel.com', 'fitness_level': 'intermediate',
             'avatar': 'https://example.com/hulk.jpg'},
            {'name': 'Spider-Man', 'email': 'peter.parker@marvel.com', 'fitness_level': 'intermediate',
             'avatar': 'https://example.com/spiderman.jpg'},
        ]
        
        marvel_users = []
        for hero in marvel_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                fitness_level=hero['fitness_level'],
                avatar=hero['avatar']
            )
            user.set_password('marvel123')
            user.save()
            marvel_users.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(marvel_users)} Marvel heroes'))
        
        # Create DC superhero users
        self.stdout.write('Creating DC superheroes...')
        dc_heroes = [
            {'name': 'Batman', 'email': 'bruce.wayne@dc.com', 'fitness_level': 'advanced',
             'avatar': 'https://example.com/batman.jpg'},
            {'name': 'Superman', 'email': 'clark.kent@dc.com', 'fitness_level': 'advanced',
             'avatar': 'https://example.com/superman.jpg'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@dc.com', 'fitness_level': 'advanced',
             'avatar': 'https://example.com/wonderwoman.jpg'},
            {'name': 'Flash', 'email': 'barry.allen@dc.com', 'fitness_level': 'advanced',
             'avatar': 'https://example.com/flash.jpg'},
            {'name': 'Aquaman', 'email': 'arthur.curry@dc.com', 'fitness_level': 'intermediate',
             'avatar': 'https://example.com/aquaman.jpg'},
            {'name': 'Green Lantern', 'email': 'hal.jordan@dc.com', 'fitness_level': 'intermediate',
             'avatar': 'https://example.com/greenlantern.jpg'},
        ]
        
        dc_users = []
        for hero in dc_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                fitness_level=hero['fitness_level'],
                avatar=hero['avatar']
            )
            user.set_password('dc123')
            user.save()
            dc_users.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(dc_users)} DC heroes'))
        
        # Create Team Marvel
        self.stdout.write('Creating Team Marvel...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes united in fitness',
            captain=marvel_users[0].name,
            members=[user.name for user in marvel_users]
        )
        self.stdout.write(self.style.SUCCESS('✓ Team Marvel created'))
        
        # Create Team DC
        self.stdout.write('Creating Team DC...')
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League - Fighting for fitness and justice',
            captain=dc_users[0].name,
            members=[user.name for user in dc_users]
        )
        self.stdout.write(self.style.SUCCESS('✓ Team DC created'))
        
        # Create activities for all users
        self.stdout.write('Creating activities...')
        activity_types = ['running', 'cycling', 'swimming', 'gym', 'yoga', 'walking']
        activity_count = 0
        
        all_users = marvel_users + dc_users
        for user in all_users:
            # Create 5-10 activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                distance = round(random.uniform(2, 25), 2) if activity_type in ['running', 'cycling', 'swimming'] else None
                calories = duration * random.randint(5, 12)
                
                Activity.objects.create(
                    user=user.name,
                    activity_type=activity_type,
                    duration=duration,
                    distance=distance,
                    calories_burned=calories,
                    date=datetime.now() - timedelta(days=random.randint(0, 30)),
                    notes=f'{user.name} completed {activity_type} session'
                )
                activity_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {activity_count} activities'))
        
        # Create leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        leaderboard_entries = []
        
        # Calculate points for Marvel team
        for user in marvel_users:
            user_activities = Activity.objects.filter(user=user.name)
            total_points = sum(activity.calories_burned for activity in user_activities)
            leaderboard_entries.append({
                'user': user.name,
                'team': team_marvel.name,
                'total_points': total_points
            })
        
        # Calculate points for DC team
        for user in dc_users:
            user_activities = Activity.objects.filter(user=user.name)
            total_points = sum(activity.calories_burned for activity in user_activities)
            leaderboard_entries.append({
                'user': user.name,
                'team': team_dc.name,
                'total_points': total_points
            })
        
        # Sort by points and assign ranks
        leaderboard_entries.sort(key=lambda x: x['total_points'], reverse=True)
        for rank, entry in enumerate(leaderboard_entries, 1):
            Leaderboard.objects.create(
                user=entry['user'],
                team=entry['team'],
                total_points=entry['total_points'],
                rank=rank
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(leaderboard_entries)} leaderboard entries'))
        
        # Create workout suggestions
        self.stdout.write('Creating workout suggestions...')
        workouts = [
            {
                'title': 'Super Soldier Morning Run',
                'description': 'Start your day like Captain America with an intense morning run',
                'difficulty_level': 'advanced',
                'duration': 45,
                'activity_type': 'running',
                'target_fitness_level': 'advanced',
                'instructions': '1. Warm up for 5 minutes\n2. Run at moderate pace for 20 minutes\n3. Sprint intervals: 30 sec sprint, 90 sec jog (repeat 5 times)\n4. Cool down for 5 minutes'
            },
            {
                'title': 'Hulk Strength Training',
                'description': 'Build incredible strength with this power workout',
                'difficulty_level': 'intermediate',
                'duration': 60,
                'activity_type': 'gym',
                'target_fitness_level': 'intermediate',
                'instructions': '1. Deadlifts: 3 sets of 8 reps\n2. Bench Press: 3 sets of 10 reps\n3. Squats: 3 sets of 12 reps\n4. Shoulder Press: 3 sets of 10 reps\n5. Pull-ups: 3 sets to failure'
            },
            {
                'title': 'Spider-Man Agility Training',
                'description': 'Improve your flexibility and agility with web-slinging moves',
                'difficulty_level': 'intermediate',
                'duration': 30,
                'activity_type': 'yoga',
                'target_fitness_level': 'beginner',
                'instructions': '1. Dynamic stretching: 5 minutes\n2. Sun salutations: 5 rounds\n3. Balance poses: Tree, Warrior III\n4. Core work: Plank variations\n5. Cool down stretches'
            },
            {
                'title': 'Flash Speed Cycling',
                'description': 'High-speed cycling workout for explosive power',
                'difficulty_level': 'advanced',
                'duration': 50,
                'activity_type': 'cycling',
                'target_fitness_level': 'advanced',
                'instructions': '1. Easy pace warm up: 10 minutes\n2. Tempo intervals: 5 min hard, 2 min easy (repeat 4 times)\n3. Cool down: 10 minutes easy pace'
            },
            {
                'title': 'Aquaman Swimming Session',
                'description': 'Master the waters with this comprehensive swim workout',
                'difficulty_level': 'intermediate',
                'duration': 45,
                'activity_type': 'swimming',
                'target_fitness_level': 'intermediate',
                'instructions': '1. Warm up: 200m easy freestyle\n2. Main set: 8x50m freestyle (30 sec rest)\n3. Technique work: 4x100m mixed strokes\n4. Cool down: 200m easy'
            },
            {
                'title': 'Wonder Woman Warrior Workout',
                'description': 'Complete warrior training for total body fitness',
                'difficulty_level': 'advanced',
                'duration': 55,
                'activity_type': 'gym',
                'target_fitness_level': 'advanced',
                'instructions': '1. Battle ropes: 3 sets of 30 seconds\n2. Box jumps: 3 sets of 15\n3. Kettlebell swings: 3 sets of 20\n4. Burpees: 3 sets of 15\n5. Medicine ball slams: 3 sets of 20'
            },
            {
                'title': 'Beginner Hero Walk',
                'description': 'Start your hero journey with a gentle walking routine',
                'difficulty_level': 'beginner',
                'duration': 30,
                'activity_type': 'walking',
                'target_fitness_level': 'beginner',
                'instructions': '1. Start with 5 min slow pace\n2. Increase to moderate pace for 20 minutes\n3. Cool down with 5 min slow pace\n4. Focus on good posture and breathing'
            }
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(workouts)} workout suggestions'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Teams: {Team.objects.count()}')
        self.stdout.write(f'Activities: {Activity.objects.count()}')
        self.stdout.write(f'Leaderboard entries: {Leaderboard.objects.count()}')
        self.stdout.write(f'Workouts: {Workout.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\nDatabase ready for testing! 🦸‍♂️🦸‍♀️'))
