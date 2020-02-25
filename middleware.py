import os
import json
import uuid
import requests
import time
from sh import git, reboot, python, kill
from datetime import datetime
import subprocess
import threading

class middleware:
  '''
  '''

  def ask_for_authentication(self):
    """
    Pede autorização para o watchman para começar a operar.
    Isso só acontecerá se o box não estiver cadastrado no sistema watchman. Para operar, a variável
    RODABOX_WAS_VALIDATED tem que ser True e o RODABOX_TOKEN_WATCHMAN deve estar preenchido. Caso
    o totem mude, a tentativa de autenticação se manterá.
    """
    macaddress = hex(uuid.getnode())

    ask_address = "http://%s:%s/ask_for_authentication" % (
      os.environ["RODABOX_SERVER_API_HOST"],
      os.environ["RODABOX_SERVER_API_PORT"]
    )
    token_address = "http://%s:%s/api/v1/auth/token/login" % (
      os.environ["RODABOX_SERVER_API_HOST"],
      os.environ["RODABOX_SERVER_API_PORT"]
    )
    response = requests.get(
      ask_address,
      params={ "macaddress" : macaddress },
      headers={ 'content-type': 'application/json' }
    )
    response = response.json()
    if response["isRegistered"]:
      token_response = requests.post(
        token_address,
        data=json.dumps({
          "email": "%s@rodaconveniencia.com.br" % macaddress,
          "password": macaddress
        }),
        headers={ 'content-type': 'application/json' }
      )
      token_response = token_response.json()
      with open('./.environ', 'r') as file:
        environ = json.loads(file.read())
        environ["RODABOX_TOKEN_WATCHMAN"] = "Token " + token_response["auth_token"]
      with open('./.environ', 'w') as file:
        json.dump(environ, file, sort_keys=True, ensure_ascii=True, indent=2)
      return token_response["auth_token"]
    return None

  def check_github_updates(self) -> bool:
    '''
    Busca atualizações do pacote no github. Ao fazer isso, automaticamente mudará a versão no
    aquivo environ. Este sistema de atualização automatica irá acontecer todos os dias as 3am.
    Para a operação de reboot acontecer, o crontab foi definido para reboot todos os dias as 3am.
    Ao iniciar este serviço, a atualização será dada automaticamente. Se houver atualização o
    sistema irá reiniciar logo em seguida.
    '''
    pull_command = 'pull https://%s:x-oauth-basic@github.com/rodaconveniencia/rodabox.git master' % (
      self.RODABOX_TOKEN_GITHUB
    )
    stdout = git(pull_command.split()).strip()

    return not stdout.startswith('Already up to date.')

  def _backpack_service(self):
    ''' Inicia o django em background '''
    command = 'python backpack/manage.py runserver %s:%s' % (
      os.environ["RODABOX_SERVER_BACKPACK_HOST"],
      os.environ["RODABOX_SERVER_BACKPACK_PORT"]
    )
    process = subprocess.Popen(command.split(), env=os.environ).pid
    self.pids.append(process)

  def _ipc_service(self):
    ''' Inicia o ipc em background '''
    command = 'python ipc/manage.py demonize %s:%s' % (
      os.environ["RODABOX_SERVER_IPC_HOST"],
      os.environ["RODABOX_SERVER_IPC_PORT"]
    )
    process = subprocess.Popen(command.split(), env=os.environ).pid
    self.pids.append(process)

  def _pinpad_service(self):
    ''' Inicia o pinpad em background '''
    command = 'mono pinpad/bin/Debug/SimpleConsoleApp.exe'.split()
    process = subprocess.Popen(command).pid
    self.pids.append(process)

  def __init__(self):
    self.pids = list()
    # Prepara as variáveis do sistema
    with open('./.environ', 'r') as file:
      environ = json.loads(file.read())
    for key, value in environ.items():
      os.environ[key] = value
      exec("self.%s = '%s'" % (key, value))

    if self.check_github_updates():
      with open('./.environ', 'r') as file:
        environ = json.loads(file.read())
      environ["RODABOX_UPDATED_AT"] = str(datetime.now())
      environ["RODABOX_LAST_GIT_COMMIT"] = git("rev-parse HEAD".split()).strip()
      python("./backpack/manage.py makemigrations".split())
      python("./backpack/manage.py migrate".split())
      with open('./.environ', 'w') as file:
        json.dump(environ, file, sort_keys=True, indent=2, ensure_ascii=False)
      reboot()

    while True:
      token = self.ask_for_authentication()
      if token != None:
        os.environ["RODABOX_TOKEN_WATCHMAN"] = token
        break
      time.sleep(1)

    threading.Thread(target=self._backpack_service).start()
    threading.Thread(target=self._ipc_service).start()
    threading.Thread(target=self._pinpad_service).start()

    while True:
      try:
        input()
      except KeyboardInterrupt:
        for pid in self.pids:
          pass

if __name__ == '__main__':
  middleware()
