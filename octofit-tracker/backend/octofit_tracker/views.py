from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User CRUD operations.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = '_id'
    
    @action(detail=False, methods=['get'])
    def by_email(self, request):
        """Get user by email query parameter."""
        email = request.query_params.get('email', None)
        if email:
            try:
                user = User.objects.get(email=email)
                serializer = self.get_serializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {'error': 'Email parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def by_fitness_level(self, request):
        """Filter users by fitness level."""
        fitness_level = request.query_params.get('level', None)
        if fitness_level:
            users = User.objects.filter(fitness_level=fitness_level)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Level parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Team CRUD operations.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = '_id'
    
    def get_object(self):
        """Override to handle ObjectId lookup."""
        from bson import ObjectId
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        
        # Convert string to ObjectId for MongoDB
        try:
            filter_kwargs = {self.lookup_field: ObjectId(lookup_value)}
        except:
            filter_kwargs = {self.lookup_field: lookup_value}
        
        obj = queryset.get(**filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, _id=None):
        """Add a member to the team."""
        team = self.get_object()
        member_name = request.data.get('member_name')
        
        if member_name:
            if member_name not in team.members:
                team.members.append(member_name)
                team.save()
                serializer = self.get_serializer(team)
                return Response(serializer.data)
            return Response(
                {'error': 'Member already exists in team'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'error': 'member_name is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def remove_member(self, request, _id=None):
        """Remove a member from the team."""
        team = self.get_object()
        member_name = request.data.get('member_name')
        
        if member_name:
            if member_name in team.members:
                team.members.remove(member_name)
                team.save()
                serializer = self.get_serializer(team)
                return Response(serializer.data)
            return Response(
                {'error': 'Member not found in team'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {'error': 'member_name is required'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Activity CRUD operations.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    lookup_field = '_id'
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get activities for a specific user."""
        user_name = request.query_params.get('user', None)
        if user_name:
            activities = Activity.objects.filter(user=user_name)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'User parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Filter activities by type."""
        activity_type = request.query_params.get('type', None)
        if activity_type:
            activities = Activity.objects.filter(activity_type=activity_type)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Type parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities (last 10)."""
        activities = Activity.objects.all()[:10]
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Leaderboard CRUD operations.
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    lookup_field = '_id'
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        """Get top N entries from leaderboard."""
        limit = int(request.query_params.get('limit', 10))
        entries = Leaderboard.objects.all()[:limit]
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get leaderboard entries for a specific team."""
        team_name = request.query_params.get('team', None)
        if team_name:
            entries = Leaderboard.objects.filter(team=team_name)
            serializer = self.get_serializer(entries, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Team parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Workout CRUD operations.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    lookup_field = '_id'
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Filter workouts by difficulty level."""
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            workouts = Workout.objects.filter(difficulty_level=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Difficulty parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def by_fitness_level(self, request):
        """Filter workouts by target fitness level."""
        fitness_level = request.query_params.get('level', None)
        if fitness_level:
            workouts = Workout.objects.filter(target_fitness_level=fitness_level)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Level parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def by_activity_type(self, request):
        """Filter workouts by activity type."""
        activity_type = request.query_params.get('type', None)
        if activity_type:
            workouts = Workout.objects.filter(activity_type=activity_type)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Type parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
