import pexpect
import time
import sys



class PinpadComunication():
    def __init__(self):
      self.application = "sudo mono /home/queiroz/Documents/totemdjango/pinpad/SimpleConsoleApp/bin/Debug/SimpleConsoleApp.exe"

    def try_init(self):
      self.child = pexpect.spawn(self.application, timeout=20)
      self.child.expect('[sudo]') #ou sucesso
      self.child.sendline('149093')

      # self.child.sendline('ativar --stoneCode 185346049')
      self.child.sendline('ativar --stoneCode 164185121')
      autentica_maq = self.child.expect(['RodaReference.TotemOn', pexpect.TIMEOUT], timeout=20)
      print(self.child.after)

      if autentica_maq == 0:
          print("Máquina está on!")
          return True

      if autentica_maq == 1:
          print('Não consegui ligar a máquina')
          self.child.sendline('sair')
          return False

    def new_trasaction(self, value):
      self.child.sendline('pagar --valor ' + str(value) + ' -id roda1454')
      transaction = self.child.expect(['sucesso', 'System.NullReferenceException', 'System.InvalidCastException', pexpect.TIMEOUT], timeout=50)
      # print("roda_log: ", str(self.child))
      print('leitura :', self.child.after)

      if transaction == 0:
          print("transação encerrada com sucesso!")
          return 44001

      elif transaction == 1:
          print("Transação não aprovada!")
          return 44002

      elif transaction == 2:
          print("Invalid Hexadecimal")
          # print('after ',self.child.after)
          self.new_trasaction(value)


      elif transaction == 3:
          print("provavelmente erro no programa")
          # print('after ',self.child.after)
          return 44004
          # self.child.sendline('sair')
      else:
        return 400

    def try_finish(self):
      self.child.sendline('sair')


#   CARTÃO DEMORA PRA PASSAR

#   System.NullReferenceException: Object reference not set to an instance of an object
#   at SimpleConsoleApp.PaymentCore.TransactionTableEntry..ctor (Poi.Sdk.Authorization.Report.IAuthorizationReport
#   report, System.Boolean isCancelled) [0x00036] in <c95870c5e2ee489d8a46b92bec956d9d>:0


#   PROBLEMA CARTÃO NUBANK

#   System.InvalidOperationException: Sequence contains no matching element
