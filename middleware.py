import os
import json
import maintainer

class middleware:
  '''
  '''

  def ask_for_authorization(self):
    """
    Pede autorização para o watchman para começar a operar.
    Isso só acontecerá se o box não estiver cadastrado no sistema watchman. Para operar, a variável
    RODABOX_WAS_VALIDATED tem que ser True e o RODABOX_TOKEN_WATCHMAN deve estar preenchido. Caso
    o totem mude, a tentativa de autenticação se manterá.
    """
    pass

  def check_github_updates(self) -> bool:
    '''
    Busca atualizações do pacote no github. Ao fazer isso, automaticamente mudará a versão no
    aquivo environ. Este sistema de atualização automatica irá acontecer todos os dias as 3am.
    Para a operação de reboot acontecer, o crontab foi definido para reboot todos os dias as 3am.
    Ao iniciar este serviço, a atualização será dada automaticamente. Se houver atualização o
    sistema irá reiniciar logo em seguida.
    '''

    print(github.Repo)

    return False

  def _backpack_service(self):
    ''' Inicia o django em background '''
    pass

  def _ipc_service(self):
    ''' Inicia o ipc em background '''
    pass

  def _pinpad_service(self):
    ''' Inicia o pinpad em background '''
    pass

  def __init__(self):
    # Prepara as variáveis do sistema
    with open('./.environ', 'r') as file:
      environ = json.loads(file.read())
      for key, value in environ.items():
        os.environ[key] = value

    self.check_github_updates()

if __name__ == '__main__':
  middleware()
