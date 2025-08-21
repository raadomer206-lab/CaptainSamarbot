import os
import requests
from flask import Flask, request

# --- إعدادات أساسية ---
app = Flask(__name__)
# المفتاح السري راح ناخذه من مكان آمن اسمه متغيرات البيئة
# راح نضبطه بموقع Render لاحقاً
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/'

# --- دالة إرسال الرسائل ---
def send_message(chat_id, text):
    """ترسل رسالة نصية للمستخدم المحدد."""
    url = TELEGRAM_API_URL + 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

# --- مسار الويب هوك (النقطة اللي تليكرام راح يحچي وياها) ---
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        update = request.get_json()
        if 'message' in update and 'text' in update['message']:
            chat_id = update['message']['chat']['id']
            text = update['message']['text']

            # --- منطق الرد الأولي (مرحلة الاختبار) ---
            # حالياً، نجمة راح ترجع صدى لكلامچ حتى نتأكد كلشي مربوط صح
            response_text = f"يا هلا، وصلني كلامچ: '{text}'"
            send_message(chat_id, response_text)

    return "OK", 200

# --- مسار للتأكد أن السيرفر حي ---
@app.route('/')
def index():
    return "<h1>عقل نجمة يعمل بنجاح!</h1>"

