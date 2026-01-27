import os
import threading
import time  # Vaqtinchalik kutishlar uchun
from http.server import HTTPServer, BaseHTTPRequestHandler
from data import bot, db
import handlers


# --- HEALTH CHECK SERVER ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"OK")

    # Loglarni terminalda ko'paytirmaslik uchun log_message'ni o'chirib qo'yamiz
    def log_message(self, format, *args):
        return


def run_health_check_server():
    port = int(os.environ.get("PORT", 10000))  # Render odatda 10000 portni ishlatadi
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"Health check server {port}-portda ishlamoqda...")
    server.serve_forever()


if __name__ == '__main__':
    # 1. Serverni birinchi bo'lib ishga tushiramiz
    threading.Thread(target=run_health_check_server, daemon=True).start()

    try:
        # 2. Bazani tayyorlash
        db.create_table_avto_tigach()
        db.create_table_county()
        db.create_table_driver()
        db.create_table_fuel_info()
        db.admins()
        db.tgmenegers()

        print("Eski sessiyalar tozalanmoqda...")
        bot.remove_webhook()
        time.sleep(1)  # Telegram serverlariga "nafas rostlash" uchun vaqt

        print("Bot polling rejimida ishga tushdi!")
        # 3. Infinity polling - Eng oxirgi qator bo'lishi shart
        bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=30)

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        time.sleep(5)  # Xato bo'lsa darrov restart bo'lib ketmasligi uchun