import ollama

def test_ai():
    """AI'nın çalışıp çalışmadığını test eder"""
    try:
        print("🤖 AI test ediliyor...")
        
        response = ollama.chat(model='mistral:7b', messages=[
            {
                'role': 'user',
                'content': 'Ürün: Test Kitabı, Açıklama: Bu bir test kitabıdır. Onay/Red kararı ver. Sadece ONAY veya RED yaz.'
            }
        ])
        
        decision = response['message']['content'].strip().upper()
        print(f"AI Yanıtı: {decision}")
        
        if 'ONAY' in decision:
            print("✅ AI ONAY verdi - Sistem çalışıyor!")
        elif 'RED' in decision:
            print("❌ AI RED verdi - Sistem çalışıyor!")
        else:
            print("⚠️ AI farklı yanıt verdi")
            
        return True
        
    except Exception as e:
        print(f"❌ AI test hatası: {e}")
        return False

if __name__ == "__main__":
    test_ai() 