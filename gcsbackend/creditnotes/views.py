from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import DatabaseError
from .models import CreditNote
from .serializers import CreditNoteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter, OpenApiTypes


@extend_schema_view(
    list=extend_schema(summary="List objects"),
    retrieve=extend_schema(summary="Retrieve object"),
    create=extend_schema(summary="Create object", request=None, responses={201: OpenApiResponse(description="Created")}),
    update=extend_schema(summary="Update object"),
    destroy=extend_schema(summary="Destroy object"),
)
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
 