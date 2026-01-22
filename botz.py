import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
# Botingiz kutubxonalari (masalan: import telebot yoki aiogram)

from data import bot, db
import handlers

# --- RENDER PORT XATOSINI TUZATISH UCHUN QISM ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running...")

def run_health_check_server():
    # Render avtomatik PORT o'zgaruvchisini beradi, agar bo'lmasa 8080
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# Serverni alohida oqimda (thread) ishga tushiramiz
threading.Thread(target=run_health_check_server, daemon=True).start()

if __name__ == '__main__':
    db.create_table_avto_tigach()
    db.create_table_county()
    db.create_table_driver()
    db.create_table_fuel_info()
    db.admins()
    db.tgmenegers()
    bot.infinity_polling()
