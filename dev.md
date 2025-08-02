# AI Otomatik Ürün Onay Sistemi

## 🎯 Amaç
Kullanıcılar ürün eklediğinde **Ollama + Mistral:7b** ile otomatik onay/red kararı verilsin.

## 🚀 Hızlı Başlangıç

### 1. Ollama Kurulumu
```bash
winget install Ollama.Ollama
ollama pull mistral:7b
```

### 2. Veritabanı Güncelleme
```sql
ALTER TABLE Product ADD AIDecision NVARCHAR(10) NULL;
ALTER TABLE Product ADD AIConfidence FLOAT NULL;
ALTER TABLE Product ADD AITimestamp DATETIME NULL;
```

### 3. AIService Sınıfı
```csharp
public class AIService
{
    private readonly HttpClient _httpClient = new HttpClient();
    private readonly string _ollamaUrl = "http://localhost:11434/api/generate";
    
    public async Task<string> EvaluateProduct(Product product)
    {
        var prompt = $"Ürün: {product.PName}, Açıklama: {product.PDesc}, Fiyat: {product.PPrice}TL. Onay/Red kararı ver. Sadece 'ONAY' veya 'RED' yaz.";
        
        var request = new { model = "mistral:7b", prompt = prompt };
        var response = await _httpClient.PostAsJsonAsync(_ollamaUrl, request);
        
        // Response işleme...
        return "ONAY"; // veya "RED"
    }
}
```

## 📋 Yapılacaklar

- [ ] `AIService.cs` oluştur
- [ ] `SatisEkle` action'ına AI entegrasyonu ekle
- [ ] Admin panelinde AI kararlarını göster
- [ ] Fallback mekanizması (AI çalışmazsa manuel onay)

## ⚡ Avantajlar
- ✅ API ücreti yok
- ✅ Anlık onay (5 saniye)
- ✅ Admin yükünü azaltır
- ✅ 7/24 çalışır

## ⚠️ Dikkat
- AI kararları %100 güvenilir değil
- Admin override gerekli
- ~4GB RAM kullanır

---
**Süre**: 1 hafta | **Öncelik**: Yüksek
