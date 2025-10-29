from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import DatabaseError
from .models import CreditNote
from .serializers import CreditNoteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class CreditNoteViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CreditNote.objects.all()
    serializer_class = CreditNoteSerializer
    lookup_field = "id"

    def handle_exception(self, exc):
        if isinstance(exc, DatabaseError):
            return Response(
                {"error": f"Database error: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return super().handle_exception(exc)
 