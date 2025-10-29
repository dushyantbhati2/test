from rest_framework import serializers
from .models import Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ["id", "description", "quantity", "unit_price", "amount"]
        read_only_fields = ["id", "amount"]

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            "id", "invoice_no", "customer", "project", "vessel",
            "invoice_date", "due_date", "total_amount",
            "status", "place_of_supply", "items", "cgst","sgst","igst","po_no","our_ref"
        ]
        read_only_fields = ["invoice_no", "total_amount"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        invoice = Invoice.objects.create(**validated_data)
        total = 0
        for item in items_data:
            item_obj = InvoiceItem.objects.create(invoice=invoice, **item)
            total += item_obj.amount
        invoice.total_amount = total
        invoice.save()
        return invoice


    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.items.all().delete()
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=instance, **item_data)
        instance.total_amount = sum(item.amount for item in instance.items.all())
        instance.save()
        return instance
    
