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

# Reset the laptop product for AI processing
try:
    cursor.execute("""
        UPDATE Product 
        SET AIApproved = NULL, 
            AIReason = NULL, 
            AIDecisionDate = NULL, 
            RequiresManualReview = NULL
        WHERE ProductId = 10 AND PName = 'laptop'
    """)
    
    conn.commit()
    print("✅ Laptop ürünü AI işlemi için sıfırlandı!")
    print("AI sistemi şimdi bu ürünü işleyecek...")
    
except Exception as e:
    print(f"❌ Hata: {e}")
    conn.rollback()

conn.close() 