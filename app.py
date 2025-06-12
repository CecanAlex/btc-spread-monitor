import requests
import time
from flask import Flask
import os

app = Flask(__name__)

BOT_TOKEN = "7937640625:AAEEF0_gwnr0EUD4-JFIgFeSkK9o1iugDpo"
CHAT_ID = "739630214"
SPREAD_THRESHOLD = -0.5  # în procente

def get_bitget_price():
    url = "https://api.bitget.com/api/spot/v1/market/ticker?symbol=animeusdt_spbl"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data["data"]["close"])
    except Exception as e:
        print("Eroare Bitget:", e)
        return None

def get_mexc_price():
    url = "https://contract.mexc.com/api/v1/contract/ticker?symbol=ANIME_USDT"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data["data"]["lastPrice"])
    except Exception as e:
        print("Eroare MEXC:", e)
        return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print("Eroare la trimiterea mesajului Telegram:", e)
        return False

last_notification_time = 0

@app.route('/')
def index():
    global last_notification_time
    bitget_price = get_bitget_price()
    mexc_price = get_mexc_price()

    if bitget_price is None or mexc_price is None:
        return "Eroare la obținerea prețurilor"

    spread_percent = ((mexc_price - bitget_price) / bitget_price) * 100
    spread_percent_rounded = round(spread_percent, 2)

    output = f"""
    ANIME Spread Monitor<br>
    Bitget Spot: {bitget_price} USDT<br>
    MEXC Futures: {mexc_price} USDT<br>
    Spread: {spread_percent_rounded}%
    """

    # trimite notificare dacă spread > 0.5% și a trecut cel puțin 1 minut
    current_time = time.time()
    if abs(spread_percent) > SPREAD_THRESHOLD and current_time - last_notification_time > 60:
        msg = f"⚠️ Spread ANIME/USDT = {spread_percent_rounded}%\n🟢 Bitget: {bitget_price} USDT\n🔴 MEXC: {mexc_price} USDT"
        send_telegram_message(msg)
        last_notification_time = current_time

    return output

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)




