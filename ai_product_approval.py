import pyodbc
import ollama
import time
import schedule
from datetime import datetime

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

def connect_to_database():
    """Veritabanına bağlanır"""
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        print(f"✅ Veritabanına bağlandı - {datetime.now()}")
        return conn
    except Exception as e:
        print(f"❌ Veritabanı bağlantı hatası: {e}")
        return None

def get_pending_products(conn):
    """Onay bekleyen ürünleri getirir"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ProductId, PName, PDesc, PPrice, PStock, PKyk 
            FROM Product 
            WHERE PStatus = 0
        """)
        products = cursor.fetchall()
        print(f"📋 {len(products)} adet onay bekleyen ürün bulundu")
        return products
    except Exception as e:
        print(f"❌ Ürün getirme hatası: {e}")
        return []

def evaluate_product_with_ai(product):
    """LLM ile ürün değerlendirmesi yapar"""
    try:
        prompt = f"""
Sen bir e-ticaret sitesi moderatörüsün. Aşağıdaki ürün bilgilerini incele:

Ürün Adı: {product[1]}
Açıklama: {product[2]}
Fiyat: {product[3]} TL
Stok: {product[4]} adet
Yurt: {product[5]}

Kontrol kriterleri:
1. Ürün adında veya açıklamasında küfür, hakaret, lanet gibi kelimeler var mı?
2. +18 içerik var mı?
3. Uygunsuz veya yasaklı ürün mü?
4. Açıklama çok kısa (5 kelimeden az) veya anlamsız mı?

Eğer yukarıdaki kriterlerden herhangi biri varsa RED yaz.
Eğer hiçbiri yoksa ONAY yaz.

Sadece ONAY veya RED yaz. Başka hiçbir şey yazma.
"""
        
        response = ollama.chat(model='mistral:7b', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        decision = response['message']['content'].strip().upper()
        
        if 'ONAY' in decision:
            return 'ONAY'
        elif 'RED' in decision:
            return 'RED'
        else:
            return 'ERROR'
            
    except Exception as e:
        print(f"❌ AI değerlendirme hatası: {e}")
        return 'ERROR'

def update_product_status(conn, product_id, status):
    """Ürün durumunu günceller"""
    try:
        cursor = conn.cursor()
        if status == 'ONAY':
            cursor.execute("UPDATE Product SET PStatus = 1 WHERE ProductId = ?", product_id)
            print(f"✅ Ürün {product_id} onaylandı")
        elif status == 'RED':
            cursor.execute("UPDATE Product SET PStatus = 2 WHERE ProductId = ?", product_id)
            print(f"❌ Ürün {product_id} reddedildi")
        
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Durum güncelleme hatası: {e}")
        return False

def process_pending_products():
    """Onay bekleyen ürünleri işler"""
    print(f"\n🤖 AI Ürün Onay Sistemi Başladı - {datetime.now()}")
    
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        products = get_pending_products(conn)
        
        for product in products:
            product_id = product[0]
            print(f"\n📦 Ürün {product_id} değerlendiriliyor...")
            print(f"   Ad: {product[1]}")
            print(f"   Açıklama: {product[2]}")
            
            decision = evaluate_product_with_ai(product)
            print(f"   AI Kararı: {decision}")
            
            if decision in ['ONAY', 'RED']:
                update_product_status(conn, product_id, decision)
            else:
                print(f"   ⚠️ AI karar veremedi, admin onayı bekleyecek")
        
        if not products:
            print("📭 Onay bekleyen ürün yok")
            
    except Exception as e:
        print(f"❌ Genel hata: {e}")
    finally:
        conn.close()
        print("🔚 İşlem tamamlandı\n")

def main():
    """Ana fonksiyon"""
    print("🚀 AI Ürün Onay Sistemi Başlatıldı")
    print("⏰ Her 5 dakikada bir kontrol edilecek")
    print("🛑 Durdurmak için Ctrl+C")
    
    # İlk çalıştırma
    process_pending_products()
    
    # Her 5 dakikada bir çalıştır
    schedule.every(5).minutes.do(process_pending_products)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1 dakika bekle
    except KeyboardInterrupt:
        print("\n👋 Sistem durduruldu")

if __name__ == "__main__":
    main() 