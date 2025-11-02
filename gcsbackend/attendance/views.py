from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import DatabaseError
from . import models, serializers
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter, OpenApiTypes


@extend_schema_view(
    list=extend_schema(summary="List objects"),
    retrieve=extend_schema(summary="Retrieve object"),
    create=extend_schema(summary="Create object", request=None, responses={201: OpenApiResponse(description="Created")}),
    update=extend_schema(summary="Update object"),
    destroy=extend_schema(summary="Destroy object"),
)
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = models.Attendance.objects.all()
    serializer_class = serializers.AttendanceSerializer
    lookup_field = "id"

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        """Custom error handler for DB errors"""
        if isinstance(exc, DatabaseError):
            return Response(
                {"error": f"Database error: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return super().handle_exception(exc)

    def destroy(self, request, *args, **kwargs):
        """Custom delete response"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"success": "Attendance record deleted"},
            status=status.HTTP_200_OK,
        )
