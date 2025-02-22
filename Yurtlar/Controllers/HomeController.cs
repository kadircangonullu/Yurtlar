using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace Yurtlar.Controllers
{
    public class HomeController : Controller
    {

        public ActionResult YönetimSayfa()
        {
            return View(); 
        }

        public ActionResult OnaySayfam()
        {
            return View();
        }

        public ActionResult UrunleriListele() {

            return View();
        }

        public ActionResult SatisEkle()
        {
            return View();
        }

        public ActionResult Login()
        {

            return View();
        }
        // GET: Home
        public ActionResult Index()
        {
            return View();
        }
    }
}