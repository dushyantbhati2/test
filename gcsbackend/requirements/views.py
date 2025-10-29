from rest_framework import viewsets,status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from . import serializers,models
from django.db import DatabaseError
from rest_framework.response import Response
# Create your views here.

class RequirementView(viewsets.ModelViewSet):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=models.Requirement.objects.all()
    serializer_class=serializers.RequirementSerializer
    lookup_field='id'

    def handle_exception(self, exc):
        """Custom error handler for database errors"""
        if isinstance(exc, DatabaseError):
            return Response(
                {"error": f"Database error: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return super().handle_exception(exc)