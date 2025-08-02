using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Yurtlar.Models
{
    public class ProductViewModel
    {
        public byte[] PImage { get; set; }
        public string PName { get; set; }
        public string PDesc { get; set; }
        public int PStock { get; set; }
        public float PPrice { get; set; }
        public int PStatus { get; set; }
        public string PKyk { get; set; }
        public string Phone { get; set; }
        public int UserId { get; set; }

    }
}