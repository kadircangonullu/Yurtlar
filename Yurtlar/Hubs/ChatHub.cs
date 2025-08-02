using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.AspNet.SignalR;
using System.Web;
using System.Web.UI;
using Microsoft.Owin;

namespace Yurtlar.Hubs
{
    public class ChatHub : Hub
    {
        public void Send(string fromUser, string toUser, string message)
        {
            // Tüm istemcilere mesaj gönderir (istersen filtreleyebilirsin)
            Clients.All.receiveMessage(fromUser, toUser, message);
        }
    }
}