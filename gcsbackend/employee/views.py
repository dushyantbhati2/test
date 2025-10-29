from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import DatabaseError
from . import serializers, models
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication   

class EmployeeViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    lookup_field = "id"

    def handle_exception(self, exc):
        """Custom error handler for database errors"""
        if isinstance(exc, DatabaseError):
            return Response(
                {"error": f"Database error: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return super().handle_exception(exc)

    def destroy(self, request, *args, **kwargs):
        """Custom delete message instead of empty 204 response"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success": "Employee deleted"},status=status.HTTP_204_NO_CONTENT)
