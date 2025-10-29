from rest_framework import serializers
from .models import Customer, Contact, Address
from django.db import transaction


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
        extra_kwargs = {
            "customer": {"write_only": True},
        }


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["customer"]


class CustomerNestedSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True,read_only=True)
    addresses = AddressSerializer(many=True,read_only=True)

    class Meta:
        model = Customer
        fields = "__all__"

    def create(self, validated_data):
        contacts_data = self.initial_data.get("contacts", [])
        addresses_data = self.initial_data.get("addresses", [])

        with transaction.atomic():
            customer = Customer.objects.create(**validated_data)

            for contact in contacts_data:
                Contact.objects.create(customer=customer, **contact)

            for address in addresses_data:
                Address.objects.create(customer=customer, **address)

        return customer