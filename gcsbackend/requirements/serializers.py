from rest_framework.serializers import ModelSerializer
from . import models

class RequirementSerializer(ModelSerializer):
    class Meta:
        model=models.Requirement
        fields='__all__'