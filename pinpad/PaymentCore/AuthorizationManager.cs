using System;
using SimpleConsoleApp.CmdLine;
using SimpleConsoleApp.SocketServidor;
using System;
using System.IO;


namespace SimpleConsoleApp.PaymentCore
{
    /// <summary>
    /// Reads the command line arguments and process the corresponding
    /// action.
    /// </summary>
    internal sealed class AuthorizationManager
    {
        /// <summary>
        /// Initializes the desktop information. If this initialization is missing,
        /// <see cref="MicroPos"/> won't act correctly.
        /// </summary>
        public AuthorizationManager()
        {
            Microtef.Platform.Desktop.DesktopInitializer.Initialize();
        }

        /// <summary>
        /// Reads the next command until an "sair" command is received.
        /// </summary>
        public void Run ()
        {
            bool getOutOfHere = false;
            SocketServidor.Server.WaitClient();
            do
            {
                string command = SocketServidor.Server.ListenSocket();
                if (command == "conexao_perdida_reconectar"){
                  SocketServidor.Server.WaitClient();
                }
                // string command = this.ReadNextCommand();
                getOutOfHere = command.Decode();
            }
            while (getOutOfHere == false);
        }

        /// <summary>
        /// Reads a new command.
        /// </summary>
        /// <returns>The command read.</returns>
        private string ReadNextCommand ()
        {
            Console.Write("> ");
            return Console.ReadLine();
        }
    }
}
