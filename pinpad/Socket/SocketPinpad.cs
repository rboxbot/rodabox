using System.Net.Sockets;
using System;
using System.IO;


namespace SimpleConsoleApp.SocketServidor
{

  public static class Server {

    public static Socket conexao;
    public static NetworkStream socketStream;
    public static TcpListener escutando;
    public static bool hasThrowError;

    static Server(){
      escutando = new TcpListener(9000);
      escutando.Start();
    }

    public static void SendReturn(string message){
      byte[] myWriteBuffer = System.Text.Encoding.ASCII.GetBytes(message);
      socketStream.Write(myWriteBuffer, 0, myWriteBuffer.Length);
    }

    public static void WaitClient(){
      Console.Write("Aguardando Conexão! ");
      conexao = escutando.AcceptSocket();
      socketStream = new NetworkStream(conexao);
    }

    public static string ListenSocket(){
        // TcpListener escutando;
        int conta = 1; //contaremos quantas conexões teremos
        string resp = "";
        Byte[] bytes = new Byte[256];
        String data = null;
        int i;
        // Console.Write("Aguardando Conexões? " + this.escutando.Pending() );

        try{
          Console.Write("Aguardando Comando!");
          // Console.Write("Dados? " + this.escutando.Active);
          i = socketStream.Read(bytes, 0, bytes.Length);
          resp = System.Text.Encoding.ASCII.GetString(bytes, 0, i);

          if( resp == "") {
            resp = "conexao_perdida_reconectar";
          }

        } catch(Exception ex) {
          Console.Write("Erro ! ", ex);
          resp = "Erro!";
        }
        return resp;
    }
  }
}
