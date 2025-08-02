import ollama

def check_manual_rules(name, desc):
    """Manuel kuralları kontrol eder"""
    name = name.lower()
    desc = desc.lower()
    
    # Küfür kelimeleri
    bad_words = ['lanet', 'kahrolası', 'siktir', 'berbat', 'kötü', 'rezalet', 'pis', 'çirkin']
    
    # Küfür kontrolü
    for word in bad_words:
        if word in name or word in desc:
            print(f"   🚫 Küfür tespit edildi: '{word}'")
            return 'RED'
    
    # Kısa açıklama kontrolü (5 kelimeden az)
    word_count = len(desc.split())
    if word_count < 5:
        print(f"   📝 Açıklama çok kısa: {word_count} kelime")
        return 'RED'
    
    # +18 içerik kontrolü
    adult_words = ['cinsel', 'pornografik', 'şiddet', 'kan', 'ölüm']
    for word in adult_words:
        if word in name or word in desc:
            print(f"   🔞 +18 içerik tespit edildi: '{word}'")
            return 'RED'
    
    return 'PASS'  # Manuel kuralları geçti

def test_manual_rules():
    """Manuel kurallar testi"""
    
    test_cases = [
        {
            "name": "Normal Ürün",
            "desc": "Temiz laptop, yeni durumda, hiç kullanılmamış",
            "expected": "PASS"
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
        },
        {
            "name": "Uzun Açıklama",
            "desc": "Bu kitap çok güzel ve temiz durumda",
            "expected": "PASS"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test['name']}")
        print(f"   Ad: {test['name']}")
        print(f"   Açıklama: {test['desc']}")
        
        result = check_manual_rules(test['name'], test['desc'])
        print(f"   Manuel Karar: {result}")
        
        if result == test['expected']:
            print(f"   ✅ Doğru karar!")
        else:
            print(f"   ❌ Yanlış karar! Beklenen: {test['expected']}")

if __name__ == "__main__":
    test_manual_rules() 