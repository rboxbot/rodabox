import os
import sys
import glob
import time
import json
import socket
import inspect
import asyncio
import workers
import collections.abc

import threading
from threading import Thread
from datetime import datetime
from flatten_dict import flatten
from os.path import dirname, basename, isfile, join

os.environ['DEFAULT_BYTES_TRANSPORT_LEN'] = '100000'

def debug(message):
  print("[DAEMON - %s] - %s" % (datetime.now(), message))

class Demonize:
  @classmethod
  def response(self, response, wait=0.25, nice=0):
    time.sleep(wait)
    os.nice(nice)
    return response

  @classmethod
  def isConnected(self):
    checker_host = checker_port = interface = ('8.8.8.8', 53)
    try:
      socket.setdefaulttimeout(3)
      socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(interface)
      return True
    except:
      return False

class TaskService:
  def __init__(self, scheduler):
    self.scheduler = scheduler

class _hint_subthread(Thread):
  def run(self):
    try:
      last_checked_response = {self.name: self.process()}
      self.service.scheduler.update(last_checked_response)

      while True:
        if last_checked_response[self.name] != self.process():
          last_checked_response[self.name] = self.process()
          self.service.scheduler.update(last_checked_response)
          debug("Detect change at %s." % self.name)
    except Exception as ex:
      debug("A exception as ocurred at %s: %s" % (self.name, ex))

  def __init__(self, pid, process, service):
    self.process = process
    self.service = service
    Thread.__init__(self, name=pid)
    self.daemon = True

class demonize:

  def _update_nested_dictionary(self, d, u):
    '''
    Atualiza nested dictionary
    '''
    for k, v in u.items():
      if isinstance(v, collections.abc.Mapping):
        d[k] = self._update_nested_dictionary(d.get(k, {}), v)
      else:
        d[k] = v
    return d

  def _underscore_reducer(self, k1, k2):
    if k1 is None:
      return k2
    else:
      return k1.upper() + '_' + k2.upper()

  def package(self):
    '''
      SUFIX: Programação reflexiva

      Essa função vai retornar todos os módulos deste pacote.
      Se reload=True, vai listar e recarregar os módulos do pacote.
    '''
    # Busca todos os módulos do pacote
    foolish = self.service.scheduler.copy()
    paths = glob.glob(join(dirname(workers.__file__), "*.py"))
    # Remove todos os módulos que não fazem parte do escopo de reinicialização. E.g.: daemon, __init__.py
    modules = [basename(f)[:-3] for f in paths if isfile(f) and not '__init__' in f]
    for module in modules:
      # Importa automaticamente todos os módulos do pacote
      exec('import workers.%s' % module)
      # Busca as classes dos módulos
      module = "workers.%s" % module
      clsmembers = inspect.getmembers(sys.modules[module], inspect.isclass)
      clsmembers = dict((name, instance) for name, instance in clsmembers)
      for membername, clsmember in clsmembers.items():
        # busca todas as funções na classe do loop
        clsmember.scheduler = self.service.scheduler
        clsmethods = inspect.getmembers(clsmember, inspect.isfunction)
        for methodname, clsmethod in clsmethods:
          if not methodname.startswith("_"):
            response = eval("%s.%s().%s" % (module, membername, methodname))
            foolish = self._update_nested_dictionary(foolish, {module.replace('workers.', ''): { membername: { methodname: response }}})
    return flatten(foolish, reducer=self._underscore_reducer)

  def workit(self):
    last_checked_response = self.service.scheduler.copy()
    for pid, instance in self.package().items():
      if pid != 'started_at':
        debug("Listen process %s." % pid)
        self.service.scheduler[pid] = None
        self.threads = _hint_subthread(pid, instance, self.service).start()

    while True:
      connection, address = self.socket.accept()
      try:
        message = connection.recv(self.DEFAULT_BYTES_TRANSPORT_LEN).decode('utf-8')
        if message != '':
          stdout = json.dumps(self.service.scheduler).encode()
          self.service.scheduler["TERMINAL_PARSER_HASCOMMANDLINE"] = True
          self.service.scheduler["TERMINAL_LAST_COMMAND_LINE"] = message
          # Aqui é enviado o self.scheduler
          connection.send(stdout)
      except Exception as ex:
        debug("Internal response error: %s." % str(ex))

  def __init__(self, host, port, *args, **kwargs):
    self.DEFAULT_HOST_ENVIRON = host
    self.DEFAULT_PORT_ENVIRON = port
    self.DEFAULT_BYTES_TRANSPORT_LEN = int(os.environ['DEFAULT_BYTES_TRANSPORT_LEN'])

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind((self.DEFAULT_HOST_ENVIRON, self.DEFAULT_PORT_ENVIRON))
    self.socket.listen(1)

    self.threads = None
    self.service = TaskService(scheduler=dict(
      started_at=str(datetime.now())
    ))
