from rest_framework import serializers

from recomendation_app.models import PropertyDetails


class PropertySerilizers(serializers.ModelSerializer):
    class Meta:
        model = PropertyDetails
        fields = '__all__'

