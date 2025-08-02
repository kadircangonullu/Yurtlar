import pyodbc

# Veritabanı bağlantı bilgileri
CONNECTION_STRING = """
Driver={ODBC Driver 17 for SQL Server};
Server=tcp:kykmarketserver.database.windows.net,1433;
Database=KYKMarketDb;
UID=adminuser;
PWD=1E*DCkf.4!d*h6;
Encrypt=yes;
TrustServerCertificate=no;
Connection Timeout=30;
"""

def test_connection():
    """Veritabanı bağlantısını test eder"""
    try:
        print("🔗 Veritabanına bağlanmaya çalışılıyor...")
        conn = pyodbc.connect(CONNECTION_STRING)
        print("✅ Veritabanına bağlandı!")
        
        # Onay bekleyen ürün sayısını kontrol et
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Product WHERE PStatus = 0")
        count = cursor.fetchone()[0]
        print(f"📋 Onay bekleyen ürün sayısı: {count}")
        
        # Örnek ürün göster
        cursor.execute("SELECT TOP 1 ProductId, PName, PDesc FROM Product WHERE PStatus = 0")
        product = cursor.fetchone()
        if product:
            print(f"📦 Örnek ürün: ID={product[0]}, Ad={product[1]}, Açıklama={product[2]}")
        else:
            print("📭 Onay bekleyen ürün yok")
        
        conn.close()
        print("✅ Test başarılı!")
        return True
        
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return False

if __name__ == "__main__":
    test_connection() 