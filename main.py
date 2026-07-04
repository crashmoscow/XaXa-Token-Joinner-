import os
import requests
import time
from flask import Flask

app = Flask(__name__)

def clean_invite(code):
    if "discord.gg/" in code:
        code = code.split("discord.gg/")[-1]
    elif "discord.com/invite/" in code:
        code = code.split("discord.com/invite/")[-1]
    if "?" in code:
        code = code.split("?")[0]
    return code.strip()

def load_tokens():
    try:
        with open("tokens.txt", "r", encoding="utf-8") as f:
            tokens = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        print(f"✅ {len(tokens)} token yüklendi.")
        return tokens
    except:
        print("❌ tokens.txt okunamadı!")
        return []

def load_servers():
    try:
        with open("servers.txt", "r", encoding="utf-8") as f:
            servers = [clean_invite(line) for line in f if line.strip()]
        print(f"✅ {len(servers)} server yüklendi.")
        return servers
    except:
        print("❌ servers.txt okunamadı!")
        return []

def join_server(token, invite_code):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    url = f"https://discord.com/api/v9/invites/{invite_code}"
    
    try:
        response = requests.post(url, headers=headers, json={}, timeout=15)
        if response.status_code in (200, 204):
            print(f"✅ BAŞARILI → {invite_code}")
            return True
        elif response.status_code == 401:
            print(f"❌ TOKEN GEÇERSİZ → {token[:15]}...")
            return False
        elif response.status_code == 400:
            print(f"❌ CAPTCHA GEREKİYOR → {invite_code}")
            return False
        else:
            print(f"❌ HATA {response.status_code} → {invite_code} | {response.text[:150]}")
            return False
    except Exception as e:
        print(f"❌ BAĞLANTI HATASI → {invite_code} | {e}")
        return False

def auto_join():
    tokens = load_tokens()
    servers = load_servers()
    
    if not tokens or not servers:
        print("Token veya server yok!")
        return
    
    for server in servers:
        print(f"\n🔄 {server} serverına katılınıyor...")
        success_count = 0
        for token in tokens:
            if join_server(token, server):
                success_count += 1
            time.sleep(2.5)  # Rate limit + captcha koruması için
        print(f"📊 {server} için {success_count}/{len(tokens)} başarılı.")

@app.route("/")
def home():
    return "Token Joiner Aktif 🚀<br><a href='/join'>Join'i Manuel Başlat</a>"

@app.route("/join")
def trigger_join():
    auto_join()
    return "Join işlemi tamamlandı! Logları kontrol et."

if __name__ == "__main__":
    print("🚀 Startup otomatik join başlıyor...")
    auto_join()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
