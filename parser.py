import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_channel_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {"URL": url, "Название": "Ошибка", "Описание": "HTTP " + str(response.status_code), "Подписчики": "—"}
        
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("meta", property="og:title")
        description = soup.find("meta", property="og:description")
        extra_info = soup.find("div", class_="tgme_page_extra")

        name = title["content"] if title else "Не найдено"
        desc_text = ""
        if description:
            desc_text = description["content"]
            if "subscribers" in desc_text:
                desc_text = desc_text.split("subscribers")[-1].strip("– ").strip()

        subscribers = "—"
        if extra_info and "subscribers" in extra_info.text:
            subscribers = extra_info.text.replace("subscribers", "").strip()

        return {"URL": url, "Название": name, "Описание": desc_text, "Подписчики": subscribers}
    except Exception as e:
        return {"URL": url, "Название": "Ошибка", "Описание": str(e), "Подписчики": "—"}

# Читаем список ссылок
with open("channels.txt", "r", encoding="utf-8") as f:
    links = [line.strip() for line in f if line.strip()]

# Собираем данные
results = []
for link in links:
    print(f"Обрабатывается: {link}")
    info = get_channel_info(link)
    results.append(info)
    time.sleep(1.5)  # Пауза между запросами

# Сохраняем в Excel
df = pd.DataFrame(results)
df.to_excel("telegram_channels_nologin.xlsx", index=False)
print("✅ Готово: данные сохранены в telegram_channels_nologin.xlsx")
