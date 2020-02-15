from pprint import pprint as print

import os
import json
import socket
import random

import ipc

class transaction(ipc.daemon.Demonize):
  HAS_TRANSACTION = False
  PINPAD_SOCKET_ADDRESS = ('localhost', 9000)
  PINPAD_STONECODE = '164185121'
  DEFAULT_BYTES_TRANSPORT_LEN = int(os.environ["DEFAULT_BYTES_TRANSPORT_LEN"])

  def hastransaction(self):
    return self.response(self.HAS_TRANSACTION)

  def start_transaction(self):
    if self.scheduler["PERIPHERALS_STATUS_HASPINPAD"]:
      if self.HAS_TRANSACTION:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as channel:
          # Conecta ao socket do pinpad
          channel.connect(self.PINPAD_SOCKET_ADDRESS)
          # Ativa o stone code e inicia a máquina
          # Espera a resposta da ativação
          active_message = 'ativar --stonecode %s' % self.PINPAD_STONECODE
          channel.send(active_message.encode())
          stdout = channel.recv(self.DEFAULT_BYTES_TRANSPORT_LEN)
          # Inicia uma transação
          # Espera a resposta da transação
          hash = "%032x" % random.getrandbits(128)
          pay_message = 'pagar --valor 0.01 -id %s' % hash.upper()
          channel.send(pay_message.encode())
          stdout = channel.recv(self.DEFAULT_BYTES_TRANSPORT_LEN).decode('utf-8')
          # Espera o resultado da transação
          self.scheduler["LAST_TRANSACTION"] = json.loads(stdout)
          # HACK: Inseri os itens da lista no mesmo escopo para 1 json só
          _wise_response = dict()
          for _bad_response in self.scheduler["LAST_TRANSACTION"]:
            _wise_response.update(_bad_response)
          self.scheduler["LAST_TRANSACTION"] = _wise_response.copy()
          # HACK: Fiz um strip dentro do holder_name pra remover os espaços
          # A melhor forma de resolver este problema é fazer dentro do servidor C#
          self.scheduler["LAST_TRANSACTION"]["response"]["holder_name"] = self.scheduler["LAST_TRANSACTION"]["response"]["holder_name"].strip()
          self.HAS_TRANSACTION = False
    return self.response(None)
