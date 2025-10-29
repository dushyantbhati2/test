from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import DatabaseError
from .models import Quotation
from .serializers import QuotationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class QuotationViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
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
        """Custom delete response instead of empty 204"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"success": "Quotation deleted"},
            status=status.HTTP_204_NO_CONTENT
        )