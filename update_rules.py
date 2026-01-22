import requests
import os
from datetime import datetime

# Настройки
SOURCE_URL = "https://raw.githubusercontent.com/ImMALWARE/dns.malw.link/master/hosts"
# PROXY_IP удален, так как мы берем IP из строк
CUSTOM_FILE = "custom_domains.txt"
OUTPUT_FILE = "my_ready_rules.txt"

# Ключевые слова для авто-поиска в интернет-списке
KEYWORDS = [
    "openai", "chatgpt", "oaistatic", "oaiusercontent", "sora.com", 
    "google", "gemini", "googleapis", "withgoogle", "pki.goog", "notebooklm", 
    "claude", "anthropic", "grok", "x.ai", "deepl"
]

def main():
    unique_domains = set()
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    result = [
        f"! Название: AI Unlocker Rules",
        f"! Последнее обновление: {now}",
        f"! Источник: {SOURCE_URL} + {CUSTOM_FILE}",
        f"! Игнорирует 0.0.0.0 (рекламные блокировки)",
        ""
    ]

    # 1. Личный список (Теперь ожидается формат: IP DOMAIN)
    result.append("! --- Личный список (custom_domains.txt) ---")
    if os.path.exists(CUSTOM_FILE):
        with open(CUSTOM_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip().lower()
                # Пропускаем пустые строки и комментарии
                if not line or line.startswith(('#', '!')):
                    continue

                parts = line.split()
                # Проверяем, что в строке есть хотя бы 2 части (IP и Домен)
                if len(parts) >= 2:
                    current_ip = parts[0]
                    domain = parts[-1]
                    
                    # Пропускаем, если IP это 0.0.0.0 (обычно это блокировка рекламы)
                    if current_ip == "0.0.0.0":
                        continue

                    if domain not in unique_domains:
                        unique_domains.add(domain)
                        # Используем IP из файла (current_ip), а не общий
                        result.append(f"||{domain}^$dnsrewrite={current_ip}")
    
    # 2. Интернет-список
    try:
        response = requests.get(SOURCE_URL)
        if response.status_code == 200:
            result.append("\n! --- Авто-дополнение из интернета ---")
            lines = response.text.splitlines()
            for line in lines:
                line = line.strip().lower()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    current_ip = parts[0] # Берем IP из начала строки
                    
                    # Очистка домена от http/https и путей
                    raw_domain = parts[-1].replace("http://", "").replace("https://", "").split('/')[0]
                    
                    # Проверяем, подходит ли домен под наши ключевые слова
                    if any(key in raw_domain for key in KEYWORDS):
                        # Важно: Пропускаем, если IP 0.0.0.0, иначе мы заблокируем сервис вместо разблокировки
                        if current_ip == "0.0.0.0":
                            continue

                        if raw_domain not in unique_domains:
                            unique_domains.add(raw_domain)
                            # Подставляем IP, который был указан в hosts файле
                            result.append(f"||{raw_domain}^$dnsrewrite={current_ip}")
    except Exception as e:
        print(f"Ошибка при загрузке из интернета: {e}")

    # 3. Сохранение
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    print(f"Успешно! Обновлено в {now}")

if __name__ == "__main__":
    main()
