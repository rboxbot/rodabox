using SimpleConsoleApp.PaymentCore;

namespace SimpleConsoleApp
{
    internal sealed class Program
    {
        public static void Main (params string[] args)
        {
            // SocketServidor.Server server = new SocketServidor.Server();
            // server.RunServer();
            AuthorizationManager authManager = new AuthorizationManager();
            authManager.Run();
        }
    }
}
