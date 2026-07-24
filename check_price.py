import requests
import time
import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

TARGET_PRICE = 210000     # adjust to your target (per kg, ₹)
DIRECTION = "below"       # "above" or "below"

def get_silver_price():
    url = f"https://bcast.slnbullion.com/VOTSBroadcastStreaming/Services/xml/GetLiveRateByTemplateID/sln?_={int(time.time()*1000)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=10)
    text = resp.text

    for line in text.splitlines():
        if "India Silver" in line:
            parts = [p.strip() for p in line.split("\t") if p.strip()]
            bid = float(parts[2])
            ask = float(parts[3])
            mid_price = (bid + ask) / 2
            return mid_price
    raise ValueError("India Silver row not found in response")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})

def main():
    price = get_silver_price()
    print(f"Current India Silver rate: {price}")

    condition_met = (price >= TARGET_PRICE if DIRECTION == "above" else price <= TARGET_PRICE)

    if condition_met:
        send_telegram_message(
            f"🚨 Silver Alert!\nCurrent rate: ₹{price:.0f}\nTarget ({DIRECTION}): ₹{TARGET_PRICE}"
        )

if __name__ == "__main__":
    main()
