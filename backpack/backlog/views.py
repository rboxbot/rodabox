from backlog import models
from backlog import serializers
from backpack.settings import ENVIRON_ADDRESS, BYTE_LIMIT

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import json
import socket

class PeripheralsViewSet(viewsets.ModelViewSet):
  queryset = models.Peripherals.objects.all()
  serializer_class = serializers.PeripheralsSerializer

  @action(detail=False, methods=['get'], url_path="transaction/start")
  def _transaction_start(self, request):
    message = {"status_code" : None}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as channel:
      channel.connect(ENVIRON_ADDRESS)
      channel.send('')
      channel.recv(BYTE_LIMIT)
    return Response({})

  @action(detail=False, methods=['get'], url_path="ask/system")
  def _ask_system(self, request):
    ring = {}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as channel:
      channel.connect(ENVIRON_ADDRESS)
      channel.send(b'echo')
      ring = json.loads(channel.recv(BYTE_LIMIT).decode('utf-8'))
    return Response(ring)
