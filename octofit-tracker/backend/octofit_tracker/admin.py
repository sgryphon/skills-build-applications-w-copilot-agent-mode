from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model."""
    list_display = ('name', 'email', 'fitness_level', 'created_at')
    list_filter = ('fitness_level', 'created_at')
    search_fields = ('name', 'email')
    ordering = ('-created_at',)
    readonly_fields = ('_id', 'created_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('_id', 'name', 'email', 'avatar')
        }),
        ('Fitness Details', {
            'fields': ('fitness_level',)
        }),
        ('Authentication', {
            'fields': ('password',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model."""
    list_display = ('name', 'captain', 'member_count', 'created_at')
    search_fields = ('name', 'captain', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('_id', 'created_at')
    
    fieldsets = (
        ('Team Information', {
            'fields': ('_id', 'name', 'description', 'captain')
        }),
        ('Members', {
            'fields': ('members',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    
    def member_count(self, obj):
        """Display the number of members in the team."""
        return len(obj.members) if obj.members else 0
    member_count.short_description = 'Members'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model."""
    list_display = ('user', 'activity_type', 'duration', 'distance', 'calories_burned', 'date')
    list_filter = ('activity_type', 'date', 'created_at')
    search_fields = ('user', 'notes')
    ordering = ('-date',)
    readonly_fields = ('_id', 'created_at')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Activity Information', {
            'fields': ('_id', 'user', 'activity_type', 'date')
        }),
        ('Activity Details', {
            'fields': ('duration', 'distance', 'calories_burned', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model."""
    list_display = ('rank', 'user', 'team', 'total_points', 'last_updated')
    list_filter = ('team', 'last_updated')
    search_fields = ('user', 'team')
    ordering = ('rank',)
    readonly_fields = ('_id', 'last_updated')
    
    fieldsets = (
        ('Ranking Information', {
            'fields': ('_id', 'rank', 'user', 'team')
        }),
        ('Points', {
            'fields': ('total_points',)
        }),
        ('Timestamps', {
            'fields': ('last_updated',)
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model."""
    list_display = ('title', 'difficulty_level', 'duration', 'activity_type', 'target_fitness_level')
    list_filter = ('difficulty_level', 'target_fitness_level', 'activity_type', 'created_at')
    search_fields = ('title', 'description', 'instructions')
    ordering = ('-created_at',)
    readonly_fields = ('_id', 'created_at')
    
    fieldsets = (
        ('Workout Information', {
            'fields': ('_id', 'title', 'description')
        }),
        ('Workout Details', {
            'fields': ('difficulty_level', 'duration', 'activity_type', 'target_fitness_level')
        }),
        ('Instructions', {
            'fields': ('instructions',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
