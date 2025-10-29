from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import DatabaseError
from . import serializers, models
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomerViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerNestedSerializer
    lookup_field = "id" 

    def handle_exception(self, exc):
        if isinstance(exc, DatabaseError):
            return Response(
                {"error": f"Database error: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return super().handle_exception(exc)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"success": "Customer deleted"},
            status=status.HTTP_200_OK
        )

class AddressViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset=models.Address.objects.all()
    serializer_class=serializers.AddressSerializer
    lookup_field='id'

    def handle_exception(self, exc):
        if isinstance(exc, DatabaseError):
            return Response(
                {"error": f"Database error: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return super().handle_exception(exc)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"success": "Address deleted"},
            status=status.HTTP_200_OK
        )
    
class ContactViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset=models.Contact.objects.all()
    serializer_class=serializers.ContactSerializer
    lookup_field='id'

    def handle_exception(self, exc):
        if isinstance(exc, DatabaseError):
            return Response(
                {"error": f"Database error: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return super().handle_exception(exc)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"success": "Contact deleted"},
            status=status.HTTP_200_OK
        )