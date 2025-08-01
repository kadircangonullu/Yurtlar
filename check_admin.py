import pyodbc

# Database connection
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=tcp:kykmarketserver.database.windows.net,1433;"
    "DATABASE=KYKMarketDb;"
    "UID=adminuser;"
    "PWD=1E*DCkf.4!d*h6;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

cursor = conn.cursor()

# Check if Admin table exists and has data
try:
    cursor.execute("SELECT COUNT(*) FROM Admin")
    admin_count = cursor.fetchone()[0]
    print(f"✅ Admin tablosunda {admin_count} kullanıcı var")
    
    if admin_count > 0:
        cursor.execute("SELECT AdminId, Name, Password FROM Admin")
        admins = cursor.fetchall()
        print("\nMevcut admin kullanıcıları:")
        for admin in admins:
            print(f"  ID: {admin[0]}, Kullanıcı Adı: {admin[1]}, Şifre: {admin[2]}")
        
        print(f"\n🔑 Admin Giriş Bilgileri:")
        print(f"  Kullanıcı Adı: {admins[0][1]}")
        print(f"  Şifre: {admins[0][2]}")
        print(f"\n🌐 Admin Giriş URL'i:")
        print(f"  http://localhost:port/Admin/Login")
        print(f"  veya")
        print(f"  https://yurtlar.azurewebsites.net/Admin/Login")
        
    else:
        print("❌ Admin tablosunda kullanıcı yok!")
        print("Admin kullanıcısı oluşturulmalı...")
        
except Exception as e:
    print(f"❌ Admin tablosu hatası: {e}")
    print("Admin tablosu oluşturulmalı...")

conn.close() 