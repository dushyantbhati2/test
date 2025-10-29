from rest_framework import serializers
from django.db import transaction
from .models import Quotation, QuotationItem

class QuotationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = "__all__"
        extra_kwargs = {"quotation": {"read_only": True}}


class QuotationSerializer(serializers.ModelSerializer):
    items = QuotationItemSerializer(many=True)

    class Meta:
        model = Quotation
        fields = "__all__"

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        with transaction.atomic():
            quotation = Quotation.objects.create(**validated_data)
            for item in items_data:
                QuotationItem.objects.create(quotation=quotation, **item)
        return quotation

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # replace old items with new ones
        instance.items.all().delete()
        for item in items_data:
            QuotationItem.objects.create(quotation=instance, **item)

        return instance