from rest_framework import viewsets,status
from . import serializers,models
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.db import DatabaseError

class TaskView(viewsets.ModelViewSet):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=models.Task.objects.all()
    serializer_class=serializers.TaskSerializer
    lookup_field='id'

    def handle_exception(self, exc):
        """Custom error handler for database errors"""
        if isinstance(exc, DatabaseError):
            return Response(
                {"error": f"Database error: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return super().handle_exception(exc)
