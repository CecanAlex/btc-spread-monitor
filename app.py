from flask import Flask
import requests

app = Flask(__name__)

def get_price_from_bitget():
    url = "https://api.bitget.com/api/spot/v1/market/ticker?symbol=ANIMEUSDT_spbl"
    try:
        response = requests.get(url)
        data = response.json()
        return float(data["data"]["close"])
    except Exception as e:
        print("Bitget error:", e)
        return None

def get_price_from_mexc():
    url = "https://contract.mexc.com/api/v1/contract/ticker?symbol=ANIME_USDT"
    try:
        response = requests.get(url)
        print("MEXC futures response:", response.text)
        data = response.json()
        return float(data["data"]["lastPrice"])
    except Exception as e:
        print("MEXC futures error:", e)
        return None

@app.route('/')
def index():
    bitget_price = get_price_from_bitget()
    mexc_price = get_price_from_mexc()

    if bitget_price is None or mexc_price is None:
        return "Eroare la obținerea prețurilor."

    spread = ((mexc_price - bitget_price) / bitget_price) * 100

    return f"""
        <h1>ANIME Spread Monitor</h1>
        <p><strong>Bitget Spot:</strong> {bitget_price} USDT</p>
        <p><strong>MEXC Futures:</strong> {mexc_price} USDT</p>
        <p><strong>Spread:</strong> {spread:.2f}%</p>
    """

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


