from djongo import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=200)
    avatar = models.URLField(blank=True, null=True)
    fitness_level = models.CharField(
        max_length=50,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        default='beginner'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email'], name='user_email_idx'),
        ]

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name


class Team(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    captain = models.CharField(max_length=200)  # Store user ID or name
    members = models.JSONField(default=list)  # List of user IDs or names
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    user = models.CharField(max_length=200)  # Store user ID or name
    activity_type = models.CharField(
        max_length=100,
        choices=[
            ('running', 'Running'),
            ('cycling', 'Cycling'),
            ('swimming', 'Swimming'),
            ('gym', 'Gym'),
            ('yoga', 'Yoga'),
            ('walking', 'Walking'),
            ('other', 'Other')
        ]
    )
    duration = models.IntegerField(help_text='Duration in minutes')
    distance = models.FloatField(help_text='Distance in kilometers', null=True, blank=True)
    calories_burned = models.IntegerField(default=0)
    date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-date']

    def __str__(self):
        return f"{self.user} - {self.activity_type} on {self.date}"


class Leaderboard(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    user = models.CharField(max_length=200)  # Store user ID or name
    team = models.CharField(max_length=200, blank=True)  # Store team ID or name
    total_points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank', '-total_points']

    def __str__(self):
        return f"{self.user} - Rank {self.rank}"


class Workout(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty_level = models.CharField(
        max_length=50,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ]
    )
    duration = models.IntegerField(help_text='Duration in minutes')
    activity_type = models.CharField(max_length=100)
    target_fitness_level = models.CharField(
        max_length=50,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ]
    )
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.title
