import socket, json, time
from threading import Thread
from pytz import timezone
import json, ast, datetime

class PinpadComunication(Thread):
    pinpad_status = None
    transaction_status = 404
    ignore_status_response = False

    def __init__(self):
        super(PinpadComunication, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(110)

    def run(self):
        self.pinpad_status = self.socket_init()
        self.try_activate_pinpad()
        self.ignore_status_response = True

        time.sleep(10)
        self.new_trasaction(value=0.01)
        time.sleep(120)
        self.see_transaction(status="todas")

        # while True:
        #     self.s.send(b'status')
        #     self.ignore_status_response = True
        #     received = self.received_message()
        #     print(received)
        #     if received[0]['status_code']  in ('801','802, 803'):
        #         print("perdi ou a conexao com internet ou com o totem, tentando reconectar!")
        #         self.try_activate_pinpad()
        #     else:
        #         self.pinpad_status = True

        #     time.sleep(300)

    def received_message(self):
        try:
            received = self.s.recv(30620)
            received_json = json.loads(received.decode().replace('\n', '<&>'))
            if self.ignore_status_response == True:
                if received_json[0]['status_code'] in ('800', '801', '802', '803'):
                    print(received_json)
                    print("mensagens contantes, pode ignorar")
                    self.received_message()

        except Exception as e:
            print(e)
            received_json = json.loads('[{"status_code": "405"}, {"message":"Pinpad nao responde"}, {"error":"None"}]')

        return received_json

    def socket_init(self):
        try:
            self.s.connect(('localhost', 9000))
            print("Conexão feita com sucesso!")
            return True
        except Exception as ex:
            print("error na conexão", ex)
            return False

    def try_activate_pinpad(self):
        self.s.send(b'ativar --stonecode 164185121')
        self.ignore_status_response = True
        received_json = self.received_message()

        if received_json[0]['status_code'] == '200':
            print("terminal pronto para ser utilizado")
            self.pinpad_status = True

        elif received_json[0]['status_code'] == '500':
            print("Terminal não ativado")
            self.pinpad_status = False

        else:
            print(received_json)
            print("Erro no código!")

    def new_trasaction(self, value):
        if self.pinpad_status:
            self.s.send(str.encode('pagar --valor ' + str(value) + ' -id roda1454'))
            self.ignore_status_response = True
            received_json = self.received_message()

            if received_json[0]['status_code'] == '200':
                print("Transacao aprovada")
                self.transaction_status = 200

            elif received_json[0]['status_code'] == '403':
                print("Transacao nao aprovada")
                self.transaction_status = 403

            else:
                self.transaction_status = 404

        else:
            self.transaction_status = 404
            return 404

    def see_transaction(self, status):
        self.s.send(str.encode('resumo --' + str(status)))
        self.ignore_status_response = True
        received_json = self.received_message()
        #pegando a última transação salva
        print(received_json)
        print("dados: ")
        print(received_json[1])
        print("type")
        print(type(received_json))
        transaction_info = received_json[1]['message'].split('<&>')[-2].split("|")
        transactio_dict = {'stone_id':int(transaction_info[-6]), 'price': float(transaction_info[-5]),
                            'type': transaction_info[-4],'brand': transaction_info[-3], 'cardhold_name': transaction_info[-2],
                            'is_captured': transaction_info[-1]}

        return transactio_dict

    def cancel_transaction(self, stoneid, value):
        self.s.send(str.encode('cancelar --stoneid '+ str(stoneid) + ' --valor ' + str(value)))
        received_json = self.received_message()
        print(received_json)


PinpadComunication().start()
