using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using Yurtlar.Models;

namespace Yurtlar.Controllers
{
    public class HomeController : Controller
    {

        KykMarketEntities db = new KykMarketEntities();

        public ActionResult YönetimSayfa()
        {
            return View(); 
        }

        public ActionResult OnaySayfam()
        {
            if (Session["UserId"] == null)
                return RedirectToAction("Login");

            int currentUserId = (int)Session["UserId"];

            // Verileri önce belleğe al, sonra işleme yap
            var urunlerim = db.Product
                .Where(p => p.UserId == currentUserId)
                .ToList() // Veritabanından veriyi çeker
                .Select(p => new ProductViewModel
                {
                    PName = p.PName,
                    PDesc = p.PDesc,
                    PPrice = (float)(p.PPrice ?? 0),  // Nullable decimal/double güvenli dönüşüm
                    PStock = p.PStock ?? 0,
                    PImage = p.PImage,
                    PKyk = p.PKyk,
                    PStatus = (int)p.PStatus
                })
                .ToList();

            return View(urunlerim);
        }



        public ActionResult UrunleriListele()
        {
            if (Session["UserId"] == null)
                return RedirectToAction("Login");

            var urunler = db.Product
                            .Where(p => p.PStatus == 1)
                            .Select(p => new
                            {
                                p.PImage,
                                p.PName,
                                p.PDesc,
                                p.PStock,
                                p.PPrice,
                                p.PKyk,
                                p.Users.Phone
                            })
                            .ToList()
                            .Select(p => new ProductViewModel
                            {
                                PImage = p.PImage,
                                PName = p.PName,
                                PDesc = p.PDesc,
                                PStock = p.PStock.GetValueOrDefault(),
                                PPrice = (float)p.PPrice.GetValueOrDefault(),
                                PKyk = p.PKyk,
                                Phone = p.Phone
                            }).ToList();

            return View(urunler);
        }


        public ActionResult SatisEkle()
        {
            if (Session["UserId"] == null)
                return RedirectToAction("Login");
            return View();
        }

        [HttpPost]
        public ActionResult SatisEkle(HttpPostedFileBase PImage, string PName, string PDesc, float PPrice, int PStock, string PKyk)
        {
            if (Session["UserId"] == null)
                return RedirectToAction("Login");

            int userId = (int)Session["UserId"];
            var user = db.Users.Find(userId);

            Product product = new Product
            {
                PName = PName,
                PDesc = PDesc,
                PPrice = PPrice,
                PStock = PStock,
                PStatus = 0,
                PKyk = PKyk,
                Users = user // ürün artık kullanıcıya bağlandı
            };

            if (PImage != null && PImage.ContentLength > 0)
            {
                using (var reader = new System.IO.BinaryReader(PImage.InputStream))
                {
                    product.PImage = reader.ReadBytes(PImage.ContentLength);
                }
            }

            try
            {
                db.Product.Add(product);
                db.SaveChanges();
            }

            catch (Exception ex)
            {
                throw new Exception("HATA: " + (ex.InnerException?.InnerException?.Message ?? ex.Message));
            }

            TempData["Success"] = "Ürün başarıyla eklendi!";
            return RedirectToAction("UrunleriListele");
        }

        public ActionResult Profilim()
        {
            if (Session["UserId"] == null)
                return RedirectToAction("Login");

            int userId = (int)Session["UserId"];

            var user = db.Users.Find(userId);
            var products = db.Product.Where(p => p.UserId == userId).ToList();

            ViewBag.MyProducts = products;
            return View(user);
        }


        [HttpPost]
        public ActionResult Profilim(Users updatedUser)
        {
            if (Session["UserId"] == null)
                return RedirectToAction("Login");

            int userId = (int)Session["UserId"];
            var user = db.Users.Find(userId);

            if (user != null)
            {
                user.Name = updatedUser.Name;
                user.Surname = updatedUser.Surname;
                user.Phone = updatedUser.Phone;
                user.Mail = updatedUser.Mail;
                user.Password = updatedUser.Password;

                db.SaveChanges();
            }

            return RedirectToAction("Profilim");
        }

        public JsonResult UrunGetir(int id)
        {
            var urun = db.Product.Find(id);
            return Json(urun, JsonRequestBehavior.AllowGet);
        }

        [HttpPost]
        public string UrunSil(int id)
        {
            var urun = db.Product.Find(id);
            if (urun != null)
            {
                db.Product.Remove(urun);
                db.SaveChanges();
                return "ok";
            }
            return "error";
        }

        [HttpPost]
        public ActionResult UrunGuncelle(int id, string PName, string PDesc, float PPrice, int PStock, string PKyk)
        {
            var product = db.Product.Find(id);
            if (product == null)
                return HttpNotFound();

            product.PName = PName;
            product.PDesc = PDesc;
            product.PPrice = PPrice;
            product.PStock = PStock;
            product.PKyk = PKyk;
            product.PStatus = 0; // Değiştiği için tekrar onaya düşsün

            db.SaveChanges();
            return Json(new { success = true });
        }





        public ActionResult Logout()
        {
            Session.Clear(); // tüm sessionları temizler
            return RedirectToAction("Login");
        }


        public ActionResult Login()
        {

            return View();
        }

        [HttpPost]
        public ActionResult Login(string username, string password)
        {
            var user = db.Users.FirstOrDefault(u => u.Mail == username && u.Password == password);

            if (user != null)
            {
                // Giriş başarılı
                Session["UserId"] = user.UserId;
                Session["UserName"] = user.Name;
                return RedirectToAction("Index");
            }
            else
            {
                ViewBag.Error = "Hatalı kullanıcı adı veya şifre!";
                return View();
            }
        }

        // GET
        public ActionResult Register()
        {
            return View();
        }

        // POST
        [HttpPost]
        public ActionResult Register(Users newUser)
        {
            if (ModelState.IsValid)
            {
                db.Users.Add(newUser);
                db.SaveChanges();
                TempData["Success"] = "Kayıt başarılı! Giriş yapabilirsiniz.";
                return RedirectToAction("Login");
            }

            return View(newUser);
        }

        // GET: Home
        public ActionResult Index()
        {
            return View();
        }

        // GET: Hakkımızda
        public ActionResult Hakkimizda()
        {
            return View();
        }

        // GET: İletişim
        public ActionResult Iletisim()
        {
            return View();
        }
    }
}