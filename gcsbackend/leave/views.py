from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import DatabaseError
from . import models, serializers

class LeaveRequestViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = models.LeaveRequest.objects.all()
    serializer_class = serializers.LeaveRequestSerializer
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
        """Custom delete message instead of empty 204"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success": "Leave request deleted"}, status=status.HTTP_204_NO_CONTENT)
