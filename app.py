from flask import Flask
import requests
import time
import threading
import os

app = Flask(__name__)

TOKEN = "7937640625:AAEEF0_gwnr0EUD4-JFIgFeSkK9o1iugDpo"
CHAT_ID = "5811898391"

def get_bitget_price():
    url = "https://api.bitget.com/api/spot/v1/market/ticker?symbol=ANIMEUSDT_SPBL"
    response = requests.get(url)
    data = response.json()
    return float(data["data"]["last"])

def get_mexc_futures_price():
    url = "https://www.mexc.com/open/api/v2/market/ticker?symbol=ANIME_USDT"
    response = requests.get(url)
    data = response.json()
    for item in data["data"]:
        if item["symbol"] == "ANIME_USDT":
            return float(item["last"])
    return None

def calculate_and_notify():
    while True:
        try:
            bitget_price = get_bitget_price()
            mexc_price = get_mexc_futures_price()
            if bitget_price is None or mexc_price is None:
                print("Eroare la obținerea datelor.")
                continue

            spread_percent = ((mexc_price - bitget_price) / bitget_price) * 100
            message = (
                f"ANIME Spread Monitor\n"
                f"Bitget Spot: {bitget_price} USDT\n"
                f"MEXC Futures: {mexc_price} USDT\n"
                f"Spread: {spread_percent:.2f}%"
            )

            print(message)

            if abs(spread_percent) >= 0.5:
                send_telegram_notification(message)

        except Exception as e:
            print("Eroare:", e)

        time.sleep(60)  # verifică la fiecare 60 de secunde

def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

@app.route("/")
def home():
    return "ANIME Spread Monitor rulează..."

if __name__ == "__main__":
    threading.Thread(target=calculate_and_notify).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



