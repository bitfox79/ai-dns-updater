import requests
import os
from datetime import datetime

# Настройки
SOURCE_URL = "https://raw.githubusercontent.com/ImMALWARE/dns.malw.link/master/hosts"
PROXY_IP = "185.87.51.182"
CUSTOM_FILE = "custom_domains.txt"
OUTPUT_FILE = "my_ready_rules.txt"

# Ключевые слова для авто-поиска
KEYWORDS = [
    "openai", "chatgpt", "oaistatic", "oaiusercontent", "sora.com", 
    "google", "gemini", "googleapis", "withgoogle", "pki.goog", "notebooklm", 
    "claude", "anthropic", "grok", "x.ai", "deepl"
]

def main():
    unique_domains = set()
    # Получаем текущую дату и время
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    result = [
        f"! Название: AI Unlocker Rules",
        f"! Последнее обновление: {now}",
        f"! Источник: {SOURCE_URL}",
        f"! Игнорирует 0.0.0.0 (рекламные блокировки)",
        ""
    ]

    # 1. Личный список
    result.append("! --- Личный список (custom_domains.txt) ---")
    if os.path.exists(CUSTOM_FILE):
        with open(CUSTOM_FILE, "r", encoding="utf-8") as f:
            for line in f:
                domain = line.strip().lower()
                if domain and not domain.startswith(('#', '!', '0.0.0.0')):
                    if domain not in unique_domains:
                        unique_domains.add(domain)
                        result.append(f"||{domain}^$dnsrewrite={PROXY_IP}")
    
    # 2. Интернет-список
    try:
        response = requests.get(SOURCE_URL)
        if response.status_code == 200:
            result.append("\n! --- Авто-дополнение из интернета ---")
            lines = response.text.splitlines()
            for line in lines:
                line = line.strip().lower()
                if not line or line.startswith(('#', '0.0.0.0')):
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    domain = parts[-1].replace("http://", "").replace("https://", "").split('/')[0]
                    if any(key in domain for key in KEYWORDS):
                        if domain not in unique_domains:
                            unique_domains.add(domain)
                            result.append(f"||{domain}^$dnsrewrite={PROXY_IP}")
    except Exception as e:
        print(f"Ошибка: {e}")

    # 3. Сохранение
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    print(f"Успешно! Обновлено в {now}")

if __name__ == "__main__":
    main()
