import os
import requests
import time
from flask import Flask

app = Flask(__name__)

def load_tokens():
    with open("tokens.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def load_servers():
    if os.path.exists("servers.txt"):
        with open("servers.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def join_server(token, invite_code):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    url = f"https://discord.com/api/v9/invites/{invite_code}"
    try:
        response = requests.post(url, headers=headers, json={}, timeout=10)
        if response.status_code in (200, 204):
            print(f"✅ Başarılı: {token[:20]}... -> {invite_code}")
            return True
        else:
            print(f"❌ Hata: {token[:20]}... -> {invite_code} | Status: {response.status_code} | {response.text[:100]}")
            return False
    except Exception as e:
        print(f"❌ Exception: {token[:20]}... -> {invite_code} | {e}")
        return False

def auto_join():
    tokens = load_tokens()
    servers = load_servers()
    print(f"{len(tokens)} token ve {len(servers)} server yüklendi.")
    
    for server in servers:
        print(f"\n🔄 {server} serverına katılınıyor...")
        for token in tokens:
            join_server(token, server)
            time.sleep(1)  # Rate limit için bekle
        time.sleep(2)

@app.route("/")
def home():
    return "Token Joiner Çalışıyor! <br><a href='/join'>Join Başlat</a>"

@app.route("/join")
def trigger_join():
    auto_join()
    return "Join işlemi tamamlandı!"

if __name__ == "__main__":
    print("Startup'ta otomatik join başlıyor...")
    auto_join()
    # Render için port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
