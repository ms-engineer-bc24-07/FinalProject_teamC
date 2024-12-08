# api/serializers/participation_serializer.py

from rest_framework import serializers
from api.models.participation_model import Participation

class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'
