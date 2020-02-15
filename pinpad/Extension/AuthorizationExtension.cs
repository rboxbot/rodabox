using Microtef.Core;
using System;
using System.Collections.Generic;
using MarkdownLog;
using System.Linq;
using Pinpad.Sdk.Model;
using SimpleConsoleApp.PaymentCore;
using Poi.Sdk.Authorization.Report;
using Poi.Sdk.Authorization.TypeCode;
using System.IO;
using SimpleConsoleApp.SocketServidor;

namespace SimpleConsoleApp.Extension
{
    /// <summary>
    /// Extensions for <see cref="ICardPaymentAuthorizer"/>.
    /// </summary>
    internal static class AuthorizationExtension
    {
        /// <summary>
        /// Show a brief description of the pinpad.
        /// </summary>
        /// <param name="pinpads">Pinpad to log on console.</param>

        public static void Log(object info, string filename)
        {
          string sLogFormat = DateTime.Now.ToShortDateString().ToString()+" "+DateTime.Now.ToLongTimeString().ToString()+" :  \n";
          string logPath = filename + ".txt";

          StreamWriter logFile = new StreamWriter(logPath, true);
          logFile.WriteLine(sLogFormat + info);
          logFile.WriteLine("-----------------------------------------------------------------------------------");
          logFile.Flush();
          logFile.Close();
        }

        public static void ShowPinpadOnConsole(this ICardPaymentAuthorizer pinpad)
        {
            ICollection<ICardPaymentAuthorizer> pinpads = new List<ICardPaymentAuthorizer>();

            pinpads.Add(pinpad);

            Console.WriteLine(
                   pinpads.Select(s => new
                   {
                       PortName = s.PinpadFacade.Communication.ConnectionName,
                       Manufacturer = s.PinpadFacade.Infos.ManufacturerName.Replace(" ", ""),
                       SerialNumber = s.PinpadFacade.Infos.SerialNumber.Replace(" ", "")
                   })
                .ToMarkdownTable());
        }
        /// <summary>
        /// Show a bulleted list with the information about the transaction.
        /// </summary>
        /// <param name="transaction">Transaction to log on console.</param>
        public static void ShowTransactionOnScreen (this IAuthorizationReport transaction)
        {
            List<string> lines = new List<string>();

            lines.Add(string.Format("Stone ID: {0}", transaction.AcquirerTransactionKey));
            lines.Add(string.Format("Valor: {0}", transaction.Amount));
            lines.Add(string.Format("Tipo: {0}", transaction.TransactionType == AccountType.Credit ? "Credito" : "Debito"));
            lines.Add(string.Format("Bandeira: {0}", transaction.Card.BrandName));
            lines.Add(string.Format("Nome do portador: {0}", transaction.Card.CardholderName));
            lines.Add(string.Format("Digitos do cartao: {0}", transaction.Card.MaskedPrimaryAccountNumber));

            string stoneId =  string.Format("\"stone_id\": \"{0}\"", transaction.AcquirerTransactionKey);
            string valorTrans = string.Format("\"value\": \"{0}\"", transaction.Amount);
            string tipoTras = string.Format("\"type\": \"{0}\"", transaction.TransactionType == AccountType.Credit ? "Credito" : "Debito");
            string bandeira = string.Format("\"brand\": \"{0}\"", transaction.Card.BrandName);
            string nomeComp = string.Format("\"holder_name\": \"{0}\"", transaction.Card.CardholderName);
            string numeroCartao = string.Format("\"account_number\": \"{0}\"", transaction.Card.MaskedPrimaryAccountNumber);


            Console.WriteLine("TRANSACAO APROVADA:");
            Console.Write(lines.ToArray()
                               .ToMarkdownBulletedList());

            SocketServidor.Server.SendReturn("[{\"status_code\": \"200\"},  {\"response\":{" + stoneId + ',' +  valorTrans + ',' + tipoTras + ',' + bandeira + ',' + nomeComp + ',' + numeroCartao + "}}, {\"error\": \" None \"}]");
            Server.hasThrowError = true;

            Log(lines.ToArray().ToMarkdownBulletedList(), "vendslog");
        }
        /// <summary>
        /// Shows the error that occurred while processing a transaction.
        /// </summary>
        /// <param name="failedTransaction">Failed transaction to log on console.</param>
        public static void ShowErrorOnTransaction (this IAuthorizationReport failedTransaction)
        {
            List<string> lines = new List<string>();

            lines.Add(string.Format("Codigo de erro: {0}", failedTransaction.ResponseCode));
            lines.Add(string.Format("Razao do erro: {0}", failedTransaction.ResponseReason));

            Console.WriteLine("TRANSACAO NAO APROVADA:");
            Console.Write(lines.ToArray().ToMarkdownBulletedList());
            // SocketServidor.Server.SendReturn("[{\"status_code\": \"403\"},  {\"message\": \"Transacao nao aprovada.\"}, {\"error\": \" " + lines.ToArray().ToMarkdownBulletedList() + " \"}]");

            Log("Transação não aprovada, erro: \n" + lines.ToArray().ToMarkdownBulletedList(), "logio");
            // Log(lines.ToArray().ToMarkdownBulletedList(), "logio");
        }
        /// <summary>
        /// Log all transactions in the console. It allows the user to filter between approved,
        /// not approved (or canceled) or all transactions.
        /// Also, it's possible to draw a graphic relating approved and not approved transactions.
        /// </summary>
        /// <param name="transactions">All transactions in this execution of the program.</param>
        /// <param name="predicate">Filter.</param>
        /// <param name="showGraphic">If the graphic should be logged.</param>
        public static void ShowTransactionsOnScreen (this ICollection<TransactionTableEntry> transactions,
            Func<TransactionTableEntry, int, bool> predicate = null, bool showGraphic = false)
        {
            List<TransactionTableEntry> entries = new List<TransactionTableEntry>();

            if (predicate != null)
            {
                entries.AddRange(transactions.Where(predicate));
            }
            else
            {
                entries.AddRange(transactions);
            }

            Console.Write(entries.ToMarkdownTable());
            SocketServidor.Server.SendReturn("[{\"status_code\": \"200\"},  {\"message\": \"MOSTRAR TRANSACOES " + entries.ToMarkdownTable() + "\"}, {\"error\": \" None \"}]");

            if (showGraphic == true)
            {
                int approvedCount = transactions.Where(t => t.IsCaptured == true)
                                                .Count();
                int notApprovedCount = transactions.Where(t => t.IsCaptured == false)
                                                                .Count();

                var graphic = new Dictionary<string, int>
                {
                    { "Total", transactions.Count},
                    { "Aprovadas", approvedCount },
                    { "Nao aprovadas", notApprovedCount },
                };

                Console.Write(graphic.ToMarkdownBarChart());
                SocketServidor.Server.SendReturn("[{\"status_code\": \"200\"},  {\"message\": \"MOSTRAR TRANSACOES " + graphic.ToMarkdownBarChart() + "\"}, {\"error\": \" None \"}]");

            }
        }
    }
}
