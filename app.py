from flask import Flask
import requests

app = Flask(__name__)

def get_price_from_bitget():
    url = "https://api.bitget.com/api/spot/v1/market/ticker?symbol=btcusdt_spbl"
    try:
        response = requests.get(url)
        print("Bitget response:", response.text)
        data = response.json()
        return float(data["data"]["close"])  # <- corectat aici
    except Exception as e:
        print("Bitget error:", e)
        return None


def get_price_from_mexc():
    url = "https://api.mexc.com/api/v3/ticker/price?symbol=BTCUSDT"
    try:
        response = requests.get(url)
        print("MEXC response:", response.text)
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print("MEXC error:", e)
        return None

@app.route("/")
def index():
    bitget_price = get_price_from_bitget()
    mexc_price = get_price_from_mexc()

    if bitget_price is None or mexc_price is None:
        return "<h1>⚠️ Eroare la citirea prețurilor</h1>"

    spread = ((mexc_price - bitget_price) / bitget_price) * 100
    return f"""
    <h1>BTC Spread Monitor</h1>
    <p><b>Bitget Spot:</b> {bitget_price} USDT</p>
    <p><b>MEXC Spot:</b> {mexc_price} USDT</p>
    <p><b>Spread:</b> {spread:.2f}%</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
