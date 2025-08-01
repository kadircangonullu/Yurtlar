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

# Check all products with status 0
cursor.execute("""
    SELECT ProductId, PName, PStatus, AIApproved, RequiresManualReview, AIReason, AIDecisionDate
    FROM Product 
    WHERE PStatus = 0
""")

results = cursor.fetchall()
print(f"Onay bekleyen ürün sayısı: {len(results)}")
print("\nÜrün detayları:")
for row in results:
    print(f"ID: {row[0]}, İsim: {row[1]}")
    print(f"  Durum: {row[2]}, AI Onay: {row[3]}, Manuel İnceleme: {row[4]}")
    print(f"  AI Sebep: {row[5]}")
    print(f"  AI Tarih: {row[6]}")
    print()

# Check AI processing criteria
cursor.execute("""
    SELECT COUNT(*) 
    FROM Product 
    WHERE PStatus = 0 AND RequiresManualReview IS NULL
""")

ai_eligible = cursor.fetchone()[0]
print(f"AI işlemi için uygun ürün sayısı: {ai_eligible}")

# Check all AI decisions
cursor.execute("""
    SELECT COUNT(*) as Total,
           SUM(CASE WHEN AIApproved = 1 THEN 1 ELSE 0 END) as Approved,
           SUM(CASE WHEN AIApproved = 0 THEN 1 ELSE 0 END) as Rejected,
           SUM(CASE WHEN RequiresManualReview = 1 THEN 1 ELSE 0 END) as ManualReview
    FROM Product 
    WHERE AIApproved IS NOT NULL
""")

ai_stats = cursor.fetchone()
print(f"\nAI İstatistikleri:")
print(f"  Toplam AI kararı: {ai_stats[0]}")
print(f"  AI Onaylanan: {ai_stats[1]}")
print(f"  AI Reddedilen: {ai_stats[2]}")
print(f"  Manuel İnceleme Gereken: {ai_stats[3]}")

conn.close() 