using Microsoft.Owin;
using Owin;

[assembly: OwinStartup(typeof(Yurtlar.Startup))]

namespace Yurtlar
{
    public class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            app.MapSignalR();
        }
    }
}
