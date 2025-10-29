from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.db import DatabaseError
from .models import Invoice
from .serializers import InvoiceSerializer
from utils.generate_invoice import generate_invoice_pdf
from rest_framework.decorators import action
from django.http import FileResponse
import io

class InvoiceViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Invoice.objects.all().prefetch_related("items")
    serializer_class = InvoiceSerializer
    lookup_field = "id"

    def handle_exception(self, exc):
        if isinstance(exc, DatabaseError):
            return Response(
                {"error": f"Database error: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return super().handle_exception(exc)
    
    @action(detail=True, methods=["get"], url_path="generate-pdf")
    def generate_pdf(self, request, id=None):
        """Generate invoice PDF on-demand and send as file response"""
        invoice = self.get_object()
        try:
            pdf_file = generate_invoice_pdf(invoice, save_to_model=False)

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
