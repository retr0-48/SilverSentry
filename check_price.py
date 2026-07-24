import requests
import time
import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

LOW = 185000
HIGH = 250000
STEP = 5000
STATE_FILE = "state.txt"

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
            return (bid + ask) / 2
    raise ValueError("India Silver row not found in response")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})

def get_bucket(price):
    clamped = max(LOW, min(HIGH, price))
    return int(clamped // STEP) * STEP

def load_last_bucket():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            content = f.read().strip()
            if content:
                return int(content)
    return None

def save_last_bucket(bucket):
    with open(STATE_FILE, "w") as f:
        f.write(str(bucket))

def main():
    price = get_silver_price()
    print(f"Current India Silver rate: {price}")

    current_bucket = get_bucket(price)
    last_bucket = load_last_bucket()

    if last_bucket is None:
        save_last_bucket(current_bucket)
        print(f"First run — initializing at level {current_bucket}, no alert sent")
        return

    if current_bucket != last_bucket:
        direction = "risen to" if current_bucket > last_bucket else "fallen to"
        send_telegram_message(
            f"🔔 Silver has {direction} ₹{current_bucket}\nCurrent rate: ₹{price:.0f}"
        )
        save_last_bucket(current_bucket)
    else:
        print("No level change since last check")

if __name__ == "__main__":
    main()import requests
import time
import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

LOW = 185000
HIGH = 250000
STEP = 5000
STATE_FILE = "state.txt"

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
            return (bid + ask) / 2
    raise ValueError("India Silver row not found in response")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})

def get_bucket(price):
    clamped = max(LOW, min(HIGH, price))
    return int(clamped // STEP) * STEP

def load_last_bucket():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            content = f.read().strip()
            if content:
                return int(content)
    return None

def save_last_bucket(bucket):
    with open(STATE_FILE, "w") as f:
        f.write(str(bucket))

def main():
    price = get_silver_price()
    print(f"Current India Silver rate: {price}")

    current_bucket = get_bucket(price)
    last_bucket = load_last_bucket()

    if last_bucket is None:
        save_last_bucket(current_bucket)
        print(f"First run — initializing at level {current_bucket}, no alert sent")
        return

    if current_bucket != last_bucket:
        direction = "risen to" if current_bucket > last_bucket else "fallen to"
        send_telegram_message(
            f"🔔 Silver has {direction} ₹{current_bucket}\nCurrent rate: ₹{price:.0f}"
        )
        save_last_bucket(current_bucket)
    else:
        print("No level change since last check")

if __name__ == "__main__":
    main()
