using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace Yurtlar.Controllers
{
    public class AdminController : Controller
    {
        KykMarketEntities db = new KykMarketEntities();

        // Admin Giriş Sayfası (manuel giriş için)
        public ActionResult Login()
        {
            return View();
        }

        [HttpPost]
        public ActionResult Login(string username, string password)
        {
            using (var db = new KykMarketEntities())
            {
                var admin = db.Admin.FirstOrDefault(a => a.Name == username && a.Password == password);
                if (admin != null)
                {
                    Session["IsAdmin"] = true;
                    Session["AdminName"] = admin.Name;
                    return RedirectToAction("Users");
                }
                else
                {
                    ViewBag.Error = "Kullanıcı adı veya şifre yanlış.";
                    return View();
                }
            }
        
        }

        public ActionResult Logout()
        {
            Session.Clear();
            return RedirectToAction("Login");
        }

        // --- KULLANICILAR ---
        public ActionResult Users()
        {
            if (Session["IsAdmin"] == null) return RedirectToAction("Login");

            var users = db.Users.ToList();
            return View(users);
        }

        [HttpPost]
        public ActionResult DeleteUser(int id)
        {
            var user = db.Users.Find(id);
            if (user != null)
            {
                db.Users.Remove(user);
                db.SaveChanges();
            }
            return RedirectToAction("Users");
        }

        [HttpPost]
        public ActionResult EditUser(Users u)
        {
            var user = db.Users.Find(u.UserId);
            if (user != null)
            {
                user.Name = u.Name;
                user.Surname = u.Surname;
                user.Mail = u.Mail;
                user.Phone = u.Phone;
                db.SaveChanges();
            }
            return RedirectToAction("Users");
        }

        // --- ONAY BEKLEYENLER ---
        public ActionResult Approvals()
        {
            if (Session["IsAdmin"] == null) return RedirectToAction("Login");

            var pending = db.Product.Where(p => p.PStatus == 0).ToList();
            return View(pending);
        }

        [HttpPost]
        public ActionResult ApproveProduct(int id)
        {
            var product = db.Product.Find(id);
            if (product != null)
            {
                product.PStatus = 1;
                db.SaveChanges();
            }
            return RedirectToAction("Approvals");
        }

        [HttpPost]
        public ActionResult RejectProduct(int id)
        {
            var product = db.Product.Find(id);
            if (product != null)
            {
                product.PStatus = 2;
                db.SaveChanges();
            }
            return RedirectToAction("Approvals");
        }

        // --- TÜM AKTİF SATIŞLAR ---
        public ActionResult ActiveSales()
        {
            if (Session["IsAdmin"] == null) return RedirectToAction("Login");

            var sales = db.Product.Where(p => p.PStatus == 1).ToList();
            return View(sales);
        }

        [HttpPost]
        public ActionResult DeleteProduct(int id)
        {
            var product = db.Product.Find(id);
            if (product != null)
            {
                db.Product.Remove(product);
                db.SaveChanges();
            }
            return RedirectToAction("ActiveSales");
        }
    }
}