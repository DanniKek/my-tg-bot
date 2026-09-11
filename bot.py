import os
import telebot
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Сюда вставь токен от @BotFather
TOKEN = "8875086325:AAHB6W_-Mp6Q7MeMwfjnRgXkIKHO7ruIYaI"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Бот успешно запущен на Render и работает без рекламы!")

# Этот блок нужен специально для Render, чтобы он не выдавал ошибку портов
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_check():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), HealthCheckHandler)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    print("Бот запущен...")
    bot.infinity_polling()

