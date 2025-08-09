using Microsoft.AspNet.SignalR;
using System;
using System.Threading.Tasks;

namespace Yurtlar.Hubs
{
    public class ChatHub : Hub
    {
        public void Send(string senderId, string receiverId, string message)
        {
            // Her iki kullanıcıya mesajı gönder
            Clients.Group(senderId).receiveMessage(senderId, message);
            Clients.Group(receiverId).receiveMessage(senderId, message);
        }

        public override Task OnConnected()
        {
            string userId = Context.QueryString["userId"];
            Groups.Add(Context.ConnectionId, userId);
            return base.OnConnected();
        }
    }
}