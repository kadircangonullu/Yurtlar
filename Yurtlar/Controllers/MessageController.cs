using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using Yurtlar.Models;
using System.Data.Entity;

namespace Yurtlar.Controllers
{
    public class MessageController : Controller
    {
        private KykMarketEntities db = new KykMarketEntities();

        // GET: Message
        public ActionResult Index()
        {
            if (Session["UserId"] == null)
                return RedirectToAction("Login", "Home");

            int currentUserId = (int)Session["UserId"];
            
            // Kullanıcının tüm mesajlaşma geçmişini getir
            var conversations = GetConversations(currentUserId);
            
            ViewBag.Conversations = conversations;
            ViewBag.CurrentUserId = currentUserId;
            
            return View();
        }

        // Ürün detayından mesaj gönderme
        [HttpPost]
        public ActionResult SendProductMessage(int productId, string message)
        {
            if (Session["UserId"] == null)
                return Json(new { success = false, message = "Oturum açmanız gerekiyor" }, JsonRequestBehavior.AllowGet);

            try
            {
                int senderId = (int)Session["UserId"];
                
                // Ürünü ve sahibini bul
                var product = db.Product.Find(productId);
                if (product == null)
                    return Json(new { success = false, message = "Ürün bulunamadı" }, JsonRequestBehavior.AllowGet);

                // Kendine mesaj göndermeyi engelle
                if (product.UserId == senderId)
                    return Json(new { success = false, message = "Kendinize mesaj gönderemezsiniz" }, JsonRequestBehavior.AllowGet);

                // Mesajı kaydet
                var newMessage = new Message
                {
                    SenderId = senderId,
                    ReceiverId = product.UserId,
                    Content = message,
                    ProductId = productId,
                    SentAt = DateTime.Now,
                    IsRead = false
                };

                db.Message.Add(newMessage);
                db.SaveChanges();

                return Json(new { 
                    success = true, 
                    message = "Mesaj gönderildi",
                    messageId = newMessage.MessageId,
                    sentAt = newMessage.SentAt
                }, JsonRequestBehavior.AllowGet);
            }
            catch (Exception ex)
            {
                return Json(new { success = false, message = "Mesaj gönderilirken hata oluştu: " + ex.Message }, JsonRequestBehavior.AllowGet);
            }
        }

        // Belirli bir kullanıcıyla mesajlaşma
        public ActionResult ChatWithUser(int userId)
        {
            if (Session["UserId"] == null)
                return RedirectToAction("Login", "Home");

            int currentUserId = (int)Session["UserId"];
            
            // Kullanıcının var olup olmadığını kontrol et
            var user = db.Users.Find(userId);
            if (user == null)
                return RedirectToAction("Index");

            // İki kullanıcı arasındaki mesajları getir
            var messages = db.Message
                .Where(m => (m.SenderId == currentUserId && m.ReceiverId == userId) ||
                           (m.SenderId == userId && m.ReceiverId == currentUserId))
                .OrderBy(m => m.SentAt)
                .Include(m => m.Product)
                .ToList();

            // Okunmamış mesajları okundu olarak işaretle
            var unreadMessages = messages.Where(m => m.ReceiverId == currentUserId && m.IsRead != true).ToList();
            foreach (var msg in unreadMessages)
            {
                msg.IsRead = true;
            }
            db.SaveChanges();

            ViewBag.Messages = messages;
            ViewBag.OtherUser = user;
            ViewBag.CurrentUserId = currentUserId;
            
            return View();
        }

        // Mesaj gönderme (AJAX)
        [HttpPost]
        public ActionResult SendMessage(int receiverId, string content, int? productId = null)
        {
            if (Session["UserId"] == null)
                return Json(new { success = false, message = "Oturum açmanız gerekiyor" }, JsonRequestBehavior.AllowGet);

            try
            {
                int senderId = (int)Session["UserId"];
                
                var newMessage = new Message
                {
                    SenderId = senderId,
                    ReceiverId = receiverId,
                    Content = content,
                    ProductId = productId,
                    SentAt = DateTime.Now,
                    IsRead = false
                };

                db.Message.Add(newMessage);
                db.SaveChanges();

                return Json(new { 
                    success = true, 
                    messageId = newMessage.MessageId,
                    sentAt = newMessage.SentAt
                }, JsonRequestBehavior.AllowGet);
            }
            catch (Exception ex)
            {
                return Json(new { success = false, message = "Mesaj gönderilirken hata oluştu" }, JsonRequestBehavior.AllowGet);
            }
        }

        // Mesajları getir (AJAX)
        [HttpGet]
        public JsonResult GetMessages(int userId)
        {
            if (Session["UserId"] == null)
                return Json(null, JsonRequestBehavior.AllowGet);

            int currentUserId = (int)Session["UserId"];
            
            var messages = db.Message
                .Where(m => (m.SenderId == currentUserId && m.ReceiverId == userId) ||
                           (m.SenderId == userId && m.ReceiverId == currentUserId))
                .OrderBy(m => m.SentAt)
                .Select(m => new
                {
                    m.MessageId,
                    m.SenderId,
                    m.ReceiverId,
                    m.Content,
                    m.SentAt,
                    m.ProductId,
                    m.IsRead,
                    ProductName = m.Product != null ? m.Product.PName : null
                })
                .ToList();

            return Json(messages, JsonRequestBehavior.AllowGet);
        }

        // Okunmamış mesaj sayısını getir
        [HttpGet]
        public JsonResult GetUnreadCount()
        {
            if (Session["UserId"] == null)
                return Json(0, JsonRequestBehavior.AllowGet);

            int currentUserId = (int)Session["UserId"];
            
            var count = db.Message
                .Where(m => m.ReceiverId == currentUserId && m.IsRead != true)
                .Count();

            return Json(count, JsonRequestBehavior.AllowGet);
        }

        // Mesajı okundu olarak işaretle
        [HttpPost]
        public ActionResult MarkAsRead(int messageId)
        {
            if (Session["UserId"] == null)
                return Json(new { success = false }, JsonRequestBehavior.AllowGet);

            try
            {
                var message = db.Message.Find(messageId);
                if (message != null && message.ReceiverId == (int)Session["UserId"])
                {
                    message.IsRead = true;
                    db.SaveChanges();
                    return Json(new { success = true }, JsonRequestBehavior.AllowGet);
                }
                return Json(new { success = false }, JsonRequestBehavior.AllowGet);
            }
            catch
            {
                return Json(new { success = false }, JsonRequestBehavior.AllowGet);
            }
        }

        // Kullanıcının konuşmalarını getir
        private List<ConversationViewModel> GetConversations(int currentUserId)
        {
            var conversations = new List<ConversationViewModel>();
            
            // Kullanıcının gönderdiği ve aldığı mesajları grupla
            var userMessages = db.Message
                .Where(m => m.SenderId == currentUserId || m.ReceiverId == currentUserId)
                .Include(m => m.Users) // Sender
                .Include(m => m.Users1) // Receiver
                .Include(m => m.Product)
                .ToList();

            // Her benzersiz kullanıcı için son mesajı bul
            var conversationGroups = userMessages
                .GroupBy(m => m.SenderId == currentUserId ? m.ReceiverId : m.SenderId)
                .Select(g => new
                {
                    OtherUserId = g.Key,
                    OtherUser = g.Key == currentUserId ? g.First().Users : g.First().Users1,
                    LastMessage = g.OrderByDescending(m => m.SentAt).First(),
                    UnreadCount = g.Count(m => m.ReceiverId == currentUserId && m.IsRead != true)
                })
                .OrderByDescending(x => x.LastMessage.SentAt)
                .ToList();

            foreach (var group in conversationGroups)
            {
                if (group.OtherUserId != currentUserId)
                {
                    conversations.Add(new ConversationViewModel
                    {
                        OtherUserId = group.OtherUserId.Value,
                        OtherUserName = group.OtherUser.Name + " " + group.OtherUser.Surname,
                        LastMessage = group.LastMessage.Content,
                        LastMessageTime = group.LastMessage.SentAt.Value,
                        UnreadCount = group.UnreadCount,
                        ProductId = group.LastMessage.ProductId,
                        ProductName = group.LastMessage.Product?.PName
                    });
                }
            }

            return conversations;
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                db.Dispose();
            }
            base.Dispose(disposing);
        }
    }

    public class ConversationViewModel
    {
        public int OtherUserId { get; set; }
        public string OtherUserName { get; set; }
        public string LastMessage { get; set; }
        public DateTime LastMessageTime { get; set; }
        public int UnreadCount { get; set; }
        public int? ProductId { get; set; }
        public string ProductName { get; set; }
    }
} 