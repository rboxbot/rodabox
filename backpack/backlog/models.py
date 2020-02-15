from django.db import models

class Peripherals(models.Model):
  started_at = models.DateTimeField('Captura iniada em:')
  onbarcode = models.BooleanField('Código de barras', null=True, blank=True)
  hasBluetooth = models.BooleanField('Bluetooth', null=True, blank=True)
  hasEthernet = models.BooleanField('Ethernet', null=True, blank=True)
  hasGPRS = models.BooleanField('GPRS', null=True, blank=True)
  hasHDMI = models.BooleanField('HDMI', null=True, blank=True)
  hasTouch = models.BooleanField('Touch', null=True, blank=True)
  hasWifi = models.BooleanField('Wifi', null=True, blank=True)

  def __str__(self):
    return self.started_at

  class Meta:
    verbose_name = 'Periférico'
    verbose_name_plural = 'Periféricos'
