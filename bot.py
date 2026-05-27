import os
import datetime
import pytz
import requests
import time
from flask import Flask
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler

# បង្កើត Flask App សម្រាប់ទប់ទល់នឹង Port Binding របស់ Render Web Service
app = Flask('')

@app.route('/')
def home():
    return "E11 Lab Gold Bot is Alive and Running!"

def run_web_server():
    # Render នឹងបោះ Port មកឱ្យតាមរយៈ Environment Variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- ផ្នែកប្រព័ន្ធ Bot ផ្ញើរបាយការណ៍របស់បង ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_gold_report():
    cambodia_tz = pytz.timezone('Asia/Phnom_Penh')
    now = datetime.datetime.now(cambodia_tz)
    date_str = now.strftime("%A ទី %d %B %Y")

    message = f"""📊 *របាយការណ៍វិភាគមាសប្រចាំថ្ងៃ (XAU/USD)*
*Institutional Grade Analysis (OANDA Data) | {date_str}*

---
• *Market Structure:* រៀបចំប្រព័ន្ធវិភាគនៅទីនេះ...
---"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        print("Report sent:", response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # 1. រត់ Web Server ញែកចេញជា Thread មួយផ្សេងទៀត ដើម្បីកុំឱ្យទើសដំណើរការរបស់ Bot
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    # 2. រត់ Scheduler សម្រាប់បាញ់របាយការណ៍ទៅ Telegram (ម៉ោង 8:00 ព្រឹក ម៉ោងកម្ពុជា)
    scheduler = BackgroundScheduler(timezone="Asia/Phnom_Penh")
    scheduler.add_job(send_gold_report, 'cron', hour=8, minute=0)
    scheduler.start()
    
    print("Bot & Web Server are running successfully on Free Tier...")
    
    # រក្សាឱ្យ Process ដើររហូត
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        
