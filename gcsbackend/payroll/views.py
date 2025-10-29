from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import DatabaseError
from .models import Payroll
from .serializers import PayrollSerializer
from utils.pdf_generation import generate_payslip_pdf
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from django.http import FileResponse
import io

class PayrollViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    lookup_field = "id"

    def handle_exception(self, exc):
        """Custom error handler for DB errors"""
        if isinstance(exc, DatabaseError):
            return Response(
                {"error": f"Database error: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return super().handle_exception(exc)

    def perform_create(self, serializer):
        """Generate PDF after payroll creation"""
        return serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Custom delete response instead of empty 204"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success": "Payroll deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=["get"], url_path="generate-pdf")
    def generate_pdf(self, request, id=None):
        """Generate payslip PDF on-demand and send as file response"""
        payroll = self.get_object()
        try:
            pdf_file = generate_payslip_pdf(payroll)  # your ContentFile object

            # Serve the file directly from memory without saving to disk
            response = FileResponse(
                io.BytesIO(pdf_file.read()),
                as_attachment=False,
                filename=pdf_file.name,
                content_type="application/pdf",
            )
            return response

        except Exception as e:
            return Response(
                {"error": f"PDF generation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
