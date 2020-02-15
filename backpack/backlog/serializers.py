from rest_framework import serializers
from backlog import models

class PeripheralsSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Peripherals
    fields = '__all__'
