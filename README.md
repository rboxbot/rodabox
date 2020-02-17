<p align="center">
  <img src="./lab-logotype.svg"/>
</p>
# Rodabox
Roda box é um serviço de pagamento e telemetria para dispositivos embarcados Raspberry Pi 3 da Roda Conveniência LTDA. Este container contém a pasta **/home/rodabox** com as seguintes camadas:

* **BackPack**:
	* lógica do serviço e banco de dados;
	* API interna de conexão com o frontend;
	* serviços de envio e recebimento de dados do servidor **Watchman**;
	* backlog;
* **IPC** (internal process communication):
	* intercomunicação dos periféricos;
	* sockets para comunicação intrelaçada;
	* auto-atualização periódica por chave de acesso e GitHub;
	* processamento de comandos em tempo real;
* **Pinpad**
	* socket server para comunicação intrelaçada;
	* comandos de ativação, pagamento, estorno e cancelamento;
* **User Interface**
	* interface do usuário;
	* relacionamento entre usuário e periféricos.

## BackPack

## IPC

## Pinpad
