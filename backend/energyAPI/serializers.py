from rest_framework import serializers
from .models import DesempenhoPainelSolar

class DesempenhoPainelSolarSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesempenhoPainelSolar
        fields = ['hora', 'temperatura', 'radiacao', 'potencia']