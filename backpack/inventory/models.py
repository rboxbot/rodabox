from django.db import models

class Customer(models.Model):
  name = models.CharField('Nome do cliente', max_length=80)

  # Meta Fields
  created = models.DateTimeField("Criado em", auto_now_add=True)
  updated = models.DateTimeField("Atualizado em", auto_now=True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = 'Cliente'
    verbose_name_plural = 'Clientes'

class Product(models.Model):
  description = models.CharField("Descrição do produto", max_length=255)
  image = models.TextField("Imagem em base64", blank=True, null=True)
  barcode = models.CharField("Código de barras", max_length=32)
  quantity = models.IntegerField("Quantidade em estoque", default=0)
  isActive = models.BooleanField('Produto ativo', null=True, blank=True, default=True)

  # Meta Fields
  created = models.DateTimeField("Criado em", auto_now_add=True)
  updated = models.DateTimeField("Atualizado em", auto_now=True)

  def __str__(self):
    return self.description

  class Meta:
    verbose_name = 'Produto'
    verbose_name_plural = 'Produtos'

class PlanogramProductDiscount(models.Model):
  percent = models.FloatField("Desconto em (%)")
  begin = models.DateTimeField("Data e hora inicial")
  end = models.DateTimeField("Data e hora final")

  # Meta Fields
  created = models.DateTimeField("Criado em", auto_now_add=True)
  updated = models.DateTimeField("Atualizado em", auto_now=True)

  def __str__(self):
    if self.percent == 100:
      return "Bonificado"
    elif self.percent == 0:
      return "Sem desconto"
    else:
      return "%f" % self.percent

class PlanogramProduct(models.Model):
  product = models.ForeignKey(Product, verbose_name="Produto da Nota Fiscal", on_delete=models.SET_NULL, null=True)
  price = models.FloatField("Preço do produto")
  discount = models.ForeignKey(PlanogramProductDiscount, verbose_name="Desconto no item do planograma", on_delete=models.SET_NULL, null=True)
  pair = models.IntegerField("Número de par")

  # Meta Fields
  created = models.DateTimeField("Criado em", auto_now_add=True)
  updated = models.DateTimeField("Atualizado em", auto_now=True)

  def __str__(self):
    return self.product.description

class PicklistProduct(models.Model):
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
  quantity = models.IntegerField("Quantidade")

  # Meta Fields
  created = models.DateTimeField("Criado em", auto_now_add=True)
  updated = models.DateTimeField("Atualizado em", auto_now=True)

  def __str__(self):
    return self.product.description

  class Meta:
    verbose_name = 'Produto de Picklist'
    verbose_name_plural = 'Produtos de Picklist'

class Picklist(models.Model):
  version = models.CharField('Versão da Picklist', max_length=32, blank=True, null=True)
  products = models.ManyToManyField(PicklistProduct)

  # Meta Fields
  created = models.DateTimeField("Criado em", auto_now_add=True)
  updated = models.DateTimeField("Atualizado em", auto_now=True)

  def __str__(self):
    if self.version:
      return self.version
    else:
      return "Versão da picklist não especificada"

  class Meta:
    verbose_name = 'Picklist'
    verbose_name_plural = 'Picklists'

class Planogram(models.Model):
  version = models.CharField("Versão do Planograma", max_length=8)
  products = models.ManyToManyField(PlanogramProduct, verbose_name="Produtos do Planograma")

  # Meta Fields
  created = models.DateTimeField("Criado em", auto_now_add=True)
  updated = models.DateTimeField("Atualizado em", auto_now=True)

  def __str__(self):
    return self.version

  class Meta:
    verbose_name = 'Planograma'
    verbose_name_plural = 'Planogramas'

class Purchase(models.Model):
  customer = models.ForeignKey(Customer, verbose_name="Nome do cliente", on_delete=models.PROTECT)
  token = models.CharField("Token da venda", max_length=255)
  products = models.ManyToManyField(PlanogramProduct, verbose_name="Produtos vendidos")

  # Meta Fields
  created = models.DateTimeField("Criado em", auto_now_add=True)
  updated = models.DateTimeField("Atualizado em", auto_now=True)

  def __str__(self):
    return self.token

  class Meta:
    verbose_name = 'Venda'
    verbose_name_plural = 'Vendas'
