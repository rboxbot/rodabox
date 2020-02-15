from inventory import models
from inventory import serializers

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.utils import timezone

class CustomerViewSet(viewsets.ModelViewSet):
  queryset = models.Customer.objects.all()
  serializer_class = serializers.CustomerSerializer

class ProductViewSet(viewsets.ModelViewSet):
  queryset = models.Product.objects.all()
  serializer_class = serializers.ProductSerializer

class PlanogramProductDiscountViewSet(viewsets.ModelViewSet):
  queryset = models.PlanogramProductDiscount.objects.all()
  serializer_class = serializers.PlanogramProductDiscountSerializer

class PlanogramProductViewSet(viewsets.ModelViewSet):
  queryset = models.PlanogramProduct.objects.all()
  serializer_class = serializers.PlanogramProductSerializer

  @action(detail=False, methods=['get'], url_path="fast/resume/search")
  def _fast_resume_search(self, request):
    queryset = models.PlanogramProduct.objects.values_list(
      'id', 'product__description', 'price', 'product__barcode'
    ).order_by("product__description")
    response = list()
    for product in queryset:
      response.append(
        dict(
          id=product[0],
          description=product[1],
          price=product[2],
          barcode=product[3]
        )
      )
    return Response(response)

  @action(detail=False, methods=['get'], url_path="fast/barcode/search")
  def _fast_barcode_search(self, request):
    barcode = request.query_params.get('barcode')
    queryset = models.PlanogramProduct.objects.get(product__barcode=barcode)

    is_discount_active = False
    if queryset.discount.begin < timezone.now() < queryset.discount.end:
      is_discount_active = True
    discount_product = "%.2f" % (queryset.price - queryset.discount.percent*queryset.price/100)

    response = dict(
      id=queryset.pk,
      description=queryset.product.description,
      price=queryset.price,
      price_with_last_discount=discount_product,
      last_percent_discount=queryset.discount.percent,
      is_discount_active=is_discount_active,
      image=queryset.product.image
    )
    return Response(response)

class PicklistProductViewSet(viewsets.ModelViewSet):
  queryset = models.PicklistProduct.objects.all()
  serializer_class = serializers.PicklistProductSerializer

class PicklistViewSet(viewsets.ModelViewSet):
  queryset = models.Picklist.objects.all()
  serializer_class = serializers.PicklistSerializer

class PlanogramViewSet(viewsets.ModelViewSet):
  queryset = models.Planogram.objects.all()
  serializer_class = serializers.PlanogramSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
  queryset = models.Purchase.objects.all()
  serializer_class = serializers.PurchaseSerializer

  @action(detail=False, methods=['get'], url_path="start/transaction")
  def _start_transaction(self, request):
    return Response({})
