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

# Add a test product
test_product = {
    'PName': 'Test Ürün - AI İnceleme',
    'PDesc': 'AI test ürünü - öğrenci kullanımına uygun',
    'PPrice': 50.0,
    'PStock': 1,
    'PKyk': 'Test Yurt',
    'UserId': 1,  # Assuming user ID 1 exists
    'PStatus': 0,  # Pending approval
    'PImage': None
}

try:
    cursor.execute("""
        INSERT INTO Product (PName, PDesc, PPrice, PStock, PKyk, UserId, PStatus, PImage, AIApproved, AIReason, AIDecisionDate, RequiresManualReview)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL, NULL)
    """, 
    test_product['PName'], test_product['PDesc'], test_product['PPrice'], 
    test_product['PStock'], test_product['PKyk'], test_product['UserId'], 
    test_product['PStatus'], test_product['PImage'])
    
    conn.commit()
    print("✅ Test ürünü başarıyla eklendi!")
    print(f"Ürün adı: {test_product['PName']}")
    print("AI sistemi bu ürünü işleyecek...")
    
except Exception as e:
    print(f"❌ Hata: {e}")
    conn.rollback()

conn.close() 