using Microtef.Core;
using Microtef.Core.Authorization;
using Pinpad.Sdk.Model.Exceptions;
using SimpleConsoleApp.CmdLine.Options;
using System;
using SimpleConsoleApp.Extension;
using System.Collections.Generic;
using System.Linq;
using Poi.Sdk.Authorization.Report;
using Poi.Sdk.Cancellation.Report;
using Pinpad.Sdk.Model;
using Microtef.Core.Staging;
using System.IO;
using System.Net;
using SimpleConsoleApp.SocketServidor;
using Pinpad.Sdk;

namespace SimpleConsoleApp.PaymentCore
{
    /// <summary>
    /// <see cref="ICardPaymentAuthorizer"/> wrapper, responsible for connect to
    /// the pinpad, transaction operation, cancelation, show transactions on the
    /// console and closing connection with the pinpads.
    /// </summary>

    internal sealed class AuthorizationCore
    {
        public void LogError(object error)
        {
          string sLogFormat = DateTime.Now.ToShortDateString().ToString()+" "+DateTime.Now.ToLongTimeString().ToString()+" :  \n";
          string logPath = "logio.txt";

          StreamWriter logFile = new StreamWriter(logPath, true);
          logFile.WriteLine(sLogFormat + error);
          logFile.WriteLine("-----------------------------------------------------------------------------------");
          logFile.Flush();
          logFile.Close();
        }

        private static AuthorizationCore Instance { get; set; }

        /// <summary>
        /// All transactions tried (approved, not approved and canceled).
        /// </summary>
        private ICollection<TransactionTableEntry> Transactions { get; set; }

        /// <summary>
        /// Stone authorizer core.
        /// </summary>
        public ICardPaymentAuthorizer StoneAuthorizer { get; set; }

        /// <summary>
        /// If the <see cref="Instance"/> is eligible to use.
        /// </summary>
        public bool IsUsable { get { return this.StoneAuthorizer == null ? false : true; } }

        /// <summary>
        /// Static constructor to create the <see cref="Instance"/>.
        /// </summary>

        public PinpadCommunication Ping {get; set;}
        public bool hasPing;
        public bool hasConnection;

        static AuthorizationCore()
        {
            AuthorizationCore.Instance = new AuthorizationCore();

            // Setup integration environment. Comment the lines below if you want to process a transaction in the production endpoint:
            // If it's false, the authorizer wil always point to the production endpoint:
            FallbackSettings.EnableFallback = false;

            // Integration endpoint to the authorizer
            FallbackSettings.FallbackAuthorizerUri = "https://sandbox-auth-integration.stone.com.br/";

            // Integration endpoint to TMS (Terminal Management System), responsible for updating pinpad tables with supported brands and cards
            FallbackSettings.FallbackTmsUri = "https://tms-staging.stone.com.br/";

            // Integration endpoint to PHC (Poi Host Communication)
            FallbackSettings.FallbackPhcUri= "https://poihostcommunication-stg.stone.com.br/";
        }

        /// <summary>
        /// Basic constructor.
        /// </summary>
        public AuthorizationCore()
        {
            this.Transactions = new List<TransactionTableEntry>();

            // TODO: MOCK!
            //TransactionTableEntry t = new TransactionTableEntry(new TransactionEntry()
            //    {
            //        Amount = 12,
            //        CaptureTransaction = true,
            //        InitiatorTransactionKey = "123555888970",
            //        Type = TransactionType.Debit
            //    }, false)
            //{
            //    CardholderName = "ROHANA / CERES",
            //    StoneId = "7878565612112",
            //    BrandName = "MASTERCARD"
            //};
            //this.Transactions.Add(t);

            //t = new TransactionTableEntry(new TransactionEntry()
            //    {
            //        Amount = 8.99m,
            //        CaptureTransaction = true,
            //        InitiatorTransactionKey = "123555888971",
            //        Type = TransactionType.Credit
            //    }, true)
            //{
            //    CardholderName = "ROHANA / CERES",
            //    StoneId = "7878565612116",
            //    BrandName = "VISA"
            //};
            //this.Transactions.Add(t);
        }

        /// <summary>
        /// Return the static <see cref="Instance"/>.
        /// </summary>
        /// <returns><see cref="Instance"/></returns>
        public static AuthorizationCore GetInstance()
        {
            return AuthorizationCore.Instance;
        }

        /// <summary>
        /// Try to connect to the pinpad.
        /// </summary>
        /// <param name="activation">Data to connect to the pinpad.</param>
        /// <returns>True if the pinpad was found and connected.</returns>
        public void TryActivate (ActivateOption activation)
        {
            try
            {
                // Stone code nosso teste : 792976231
                // Stone code deles : 185346049
                // Stone code producao roda: 137346812
                // Tries to connect to one pinpad:
                this.StoneAuthorizer = DeviceProvider
                    .ActivateAndGetOneOrFirst(activation.StoneCode, new DisplayableMessages() { ApprovedMessage = "Aprovada", DeclinedMessage = "Negada", InitializationMessage = "Iniciando...", MainLabel = "Roda!", ProcessingMessage = "Processando..." }, activation.Port);

                // Show result:
                this.StoneAuthorizer.ShowPinpadOnConsole();
                SocketServidor.Server.SendReturn("[{\"status_code\": \"200\"},  {\"message\": \"Terminal pronto para ser utilizado!\"}, {\"error\": \" None \"}]");

            }
            catch (PinpadNotFoundException)
            {

                this.LogError("Pinpad nao encontrado.");
                Console.WriteLine("Pinpad nao encontrado.");
                SocketServidor.Server.SendReturn("[{\"status_code\": \"404\"},  {\"message\": \"Pinpad nao encontrado\"}, {\"error\": \"None\"}]");

            }
            catch (Exception ex)
            {
                this.LogError("Nâo foi possível ativar o terminal. \n" + ex);
                // Console.WriteLine(ex);
                Console.WriteLine("Erro ao ativar o terminal. Você está usando o StoneCode correto?");
                SocketServidor.Server.SendReturn("[{\"status_code\": \"500\"},  {\"message\": \"Erro ao ativar o terminal. Voce esta usando o StoneCode correto?\"}, {\"error\": \"" + ex + "\"}]");
            }

        }
        /// <summary>
        /// Authorizes a payment.
        /// </summary>
        /// <param name="transaction">Transaction to authorize.</param>
        /// <returns>The report returned from Stone Authorizer, or null if something
        /// went wrong.</returns>
        public IAuthorizationReport Authorize(TransactionOption transaction)
        {
            // Verify if the authorizer is eligible to do something:
            if (this.IsUsable == false) {
              return null;
             }

            // Setup transaction data:
            TransactionEntry transactionEntry = new TransactionEntry()
            {
                Amount = transaction.Amount,
                CaptureTransaction = true,
                InitiatorTransactionKey = transaction.Itk,
                Type = transaction.AccountType
            };

            IAuthorizationReport authReport = null;

            try
            {

                Server.hasThrowError = false;

                // Authorize the transaction setup and return it's value:
                ResponseStatus authorizationStatus;
                authReport = this.StoneAuthorizer.Authorize(transactionEntry, out authorizationStatus);

                // Show result on console:
                if (authReport.WasSuccessful == true)
                {
                    Console.WriteLine("Autorizado.");
                    authReport.ShowTransactionOnScreen();
                    this.Transactions.Add(new TransactionTableEntry(authReport, false));
                }
                else
                {
                    authReport.ShowErrorOnTransaction();
                    SocketServidor.Server.SendReturn("[{\"status_code\": \"500\"},  {\"message\": \"Ocorreu um erro na transacao\"}, {\"error\": \" None \"}]");
                    Server.hasThrowError = true;
                    this.Transactions.Add(new TransactionTableEntry(authReport, true));
                }
            }
            catch (CardHasChipException)
            {
                this.LogError("O cartao possui chip. For favor, insira-o.");
                Console.WriteLine("O cartao possui chip. For favor, insira-o.");
                SocketServidor.Server.SendReturn("[{\"status_code\": \"401\"},  {\"message\": \"O cartao possui chip. For favor, insira-o.\"}, {\"error\": \" None \" }]");
                Server.hasThrowError = true;
                this.Transactions.Add(new TransactionTableEntry(transactionEntry, true));
            }
            catch (ExpiredCardException)
            {
                this.LogError("Cartão expirado.");
                Console.WriteLine("Cartão expirado.");
                SocketServidor.Server.SendReturn("[{\"status_code\": \"401\"},  {\"message\": \"Cartao Expirado\"}, {\"error\": \" None \" }]");
                Server.hasThrowError = true;
                this.Transactions.Add(new TransactionTableEntry(transactionEntry, true));
            }
            catch (Exception ex)
            {

                this.LogError("Erro na transação \n" + ex);
                Console.WriteLine(ex);
                Console.WriteLine("Ocorreu um erro na transacao.");
                if (Server.hasThrowError == false) {
                  SocketServidor.Server.SendReturn("[{\"status_code\": \"500\"},  {\"message\": \"Ocorreu um erro na transacao\"}, {\"error\": \" None \"}]");
                }

                this.Transactions.Add(new TransactionTableEntry(transactionEntry, true));
            }

            return authReport;
        }


        /// <summary>
        /// Shows the transactions performed so far in the current execution
        /// of the program.
        /// </summary>
        /// <param name="showOptions">Information to filter the data to be logged.</param>
        public void ShowTransactions (ShowTransactionsOption showOptions)
        {
            if (showOptions.ShowAll == true)
            {
                this.LogError("Consulta de todas as transações.");
                Console.WriteLine("TODAS AS TRANSACOES:");
                this.Transactions.ShowTransactionsOnScreen();
            }

            if (showOptions.ShowOnlyApproved == true)
            {
                this.LogError("Consulta transações aprovadas.");
                Console.WriteLine("APENAS TRANSACOES APROVADAS:");
                this.Transactions.ShowTransactionsOnScreen((t, e) => t.IsCaptured == true);
            }

            if (showOptions.ShowOnlyCancelledOrNotApproved == true)
            {
                this.LogError("Consulta transações não aprovadas.");
                Console.WriteLine("APENAS TRANSACOES NAO APROVADAS:");
                this.Transactions.ShowTransactionsOnScreen((t, e) => t.IsCaptured == false);
            }
        }
        /// <summary>
        /// Cancel a transaction.
        /// </summary>
        /// <param name="cancelation">Cancelation info.</param>
        internal void Cancel(CancelationOption cancelation)
        {
            ICancellationReport cancelReport = this.StoneAuthorizer
                .Cancel(cancelation.StoneId, cancelation.Amount);

            if (cancelReport.WasSuccessful == true)
            {
                this.LogError("TRANSACAO {0} CANCELADA COM SUCESSO. " + cancelation.StoneId);
                SocketServidor.Server.SendReturn("[{\"status_code\": \"200\"},  {\"message\": \"TRANSACAO " + cancelation.StoneId + " CANCELADA COM SUCESSO.\"}, {\"error\": \"None\" }]");

                Console.WriteLine();

                TransactionTableEntry transaction = this.Transactions
                    .Where(t => t.StoneId == cancelation.StoneId)
                    .FirstOrDefault();

                if (transaction != null)
                {
                    transaction.IsCaptured = false;
                }
            }
            else
            {
                this.LogError("TRANSACAO {0} NAO PODE SER CANCELADA. " + cancelation.StoneId);
                SocketServidor.Server.SendReturn("[{\"status_code\": \"401\"},  {\"message\": \"TRANSACAO " + cancelation.StoneId + " NAO PODE SER CANCELADA.\"}, {\"error\": \" None \" }]");
            }
        }
        /// <summary>
        /// Closes pinpad connection.
        /// </summary>
        internal void ClosePinpad()
        {
            this.StoneAuthorizer.PinpadFacade.Communication
                .ClosePinpadConnection(this.StoneAuthorizer.PinpadMessages.MainLabel);
                SocketServidor.Server.SendReturn("[{\"status_code\": \"200\"},  {\"message\": \"CONEXAO COM PINPAD ENCERRADA COM SUCESSO \"}, {\"error\": \" None \" }]");

        }

        internal void LastTransaction(){
            Console.WriteLine("chamou status");
          }
    }
}
