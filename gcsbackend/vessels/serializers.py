from rest_framework.serializers import ModelSerializer
from . import models

class VesselSerializer(ModelSerializer):
    class Meta:
        model = models.Vessel
        fields = "__all__"