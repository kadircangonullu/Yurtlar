import ollama

def test_bad_words():
    """Küfürlü içerik testi"""
    
    test_cases = [
        {
            "name": "Normal Ürün",
            "desc": "Temiz laptop, yeni durumda",
            "expected": "ONAY"
        },
        {
            "name": "Kısa Açıklama",
            "desc": "Kitap",
            "expected": "RED"
        },
        {
            "name": "Küfürlü Ürün",
            "desc": "Bu lanet kitap çok berbat",
            "expected": "RED"
        },
        {
            "name": "Hakaretli Ürün",
            "desc": "Bu kitap çok kötü ve berbat",
            "expected": "RED"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test['name']}")
        print(f"   Ad: {test['name']}")
        print(f"   Açıklama: {test['desc']}")
        
        prompt = f"""
Sen bir e-ticaret sitesi moderatörüsün. Aşağıdaki ürün bilgilerini incele:

Ürün Adı: {test['name']}
Açıklama: {test['desc']}

Kontrol kriterleri:
1. Ürün adında veya açıklamasında küfür, hakaret, lanet gibi kelimeler var mı?
2. +18 içerik var mı?
3. Uygunsuz veya yasaklı ürün mü?
4. Açıklama çok kısa (5 kelimeden az) veya anlamsız mı?

Eğer yukarıdaki kriterlerden herhangi biri varsa RED yaz.
Eğer hiçbiri yoksa ONAY yaz.

Sadece ONAY veya RED yaz. Başka hiçbir şey yazma.
"""
        
        try:
            response = ollama.chat(model='mistral:7b', messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ])
            
            decision = response['message']['content'].strip().upper()
            print(f"   AI Kararı: {decision}")
            
            if 'ONAY' in decision:
                result = "ONAY"
            elif 'RED' in decision:
                result = "RED"
            else:
                result = "ERROR"
            
            if result == test['expected']:
                print(f"   ✅ Doğru karar!")
            else:
                print(f"   ❌ Yanlış karar! Beklenen: {test['expected']}")
                
        except Exception as e:
            print(f"   ❌ Hata: {e}")

if __name__ == "__main__":
    test_bad_words() 