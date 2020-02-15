from rest_framework import serializers
from inventory import models

class CustomerSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Customer
    fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Product
    fields = '__all__'

class PlanogramProductDiscountSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.PlanogramProductDiscount
    fields = '__all__'

class PlanogramProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.PlanogramProduct
    fields = '__all__'

class PicklistProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.PicklistProduct
    fields = '__all__'

class PicklistSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Picklist
    fields = '__all__'

class PlanogramSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Planogram
    fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Purchase
    fields = '__all__'
