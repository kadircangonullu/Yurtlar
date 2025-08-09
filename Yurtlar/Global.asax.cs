using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.Routing;

namespace Yurtlar
{
    public class MvcApplication : System.Web.HttpApplication
    {
        protected void Application_Start()
        {
            AreaRegistration.RegisterAllAreas();
            RouteConfig.RegisterRoutes(RouteTable.Routes);
        }

        protected void Application_PostAuthenticateRequest(Object sender, EventArgs e)
        {
            if (HttpContext.Current.Session != null && HttpContext.Current.Session["UserId"] != null)
            {
                System.Security.Principal.GenericPrincipal userPrincipal =
                    new System.Security.Principal.GenericPrincipal(
                        new System.Security.Principal.GenericIdentity(HttpContext.Current.Session["UserId"].ToString()), null);
                HttpContext.Current.User = userPrincipal;
            }
        }

    }
}