from django.contrib import admin

from inventory import models

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
  pass

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
  pass

@admin.register(models.PlanogramProductDiscount)
class PlanogramProductDiscountAdmin(admin.ModelAdmin):
  pass

@admin.register(models.PlanogramProduct)
class PlanogramProductAdmin(admin.ModelAdmin):
  pass

@admin.register(models.PicklistProduct)
class PicklistProductAdmin(admin.ModelAdmin):
  pass

@admin.register(models.Picklist)
class PicklistAdmin(admin.ModelAdmin):
  pass

@admin.register(models.Planogram)
class PlanogramAdmin(admin.ModelAdmin):
  pass

@admin.register(models.Purchase)
class PurchaseAdmin(admin.ModelAdmin):
  pass
