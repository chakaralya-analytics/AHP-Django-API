# ahp_api/serializers.py

from rest_framework import serializers
from .models import AHPProject

class AHPInputSerializer(serializers.Serializer):
    project_name = serializers.CharField()
    criteria = serializers.ListField(child=serializers.CharField())
    alternatives = serializers.ListField(child=serializers.CharField())
    pairwise_matrix = serializers.ListField(child=serializers.ListField(child=serializers.FloatField()))
    alternative_matrices = serializers.ListField(child=serializers.ListField(child=serializers.ListField(child=serializers.FloatField())))

class AHPProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHPProject
        fields = '__all__'