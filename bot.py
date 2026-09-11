import os
import telebot
from telebot import types
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# ⚠️ ОБЯЗАТЕЛЬНО: Вставь сюда свой токен от @BotFather между кавычками
TOKEN = "8875086325:AAHB6W_-Mp6Q7MeMwfjnRgXkIKHO7ruIYaI"
bot = telebot.TeleBot(TOKEN)

# Словарь с переводами всех текстов
TRANSLATIONS = {
    'ru': {
        'welcome': "Привет! Я RoboLanguage. На каком языке вы хотите чтобы я писал?",
        'changed': "Язык успешно изменен на Русский! 🇷🇺",
        'unknown_btn': "Пожалуйста, используйте кнопки меню."
    },
    'en': {
        'welcome': "Hello! I am RoboLanguage. What language do you want me to write in?",
        'changed': "Language successfully changed to English! 🇺🇸",
        'unknown_btn': "Please, use the menu buttons."
    }
}

# Функция для создания кнопок выбора языка
def get_language_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_ru = types.KeyboardButton("Русский 🇷🇺")
    btn_en = types.KeyboardButton("English 🇺🇸")
    markup.add(btn_ru, btn_en)
    return markup

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Автоматически определяем язык интерфейса из профиля Telegram пользователя
    user_lang_code = message.from_user.language_code
    
    # Если у пользователя в Telegram стоит русский ('ru', 'be', 'uk' и т.д.), выбираем 'ru'
    if user_lang_code and user_lang_code.startswith('ru'):
        lang = 'ru'
    else:
        # Для всех остальных по умолчанию ставим английский
        lang = 'en'
    
    # Берем текст приветствия на нужном языке
    welcome_text = TRANSLATIONS[lang]['welcome']
    
    # Отправляем сообщение и прикрепляем кнопки выбора языка
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_language_keyboard())

# Обработка нажатий на кнопки смены языка
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Русский 🇷🇺":
        lang = 'ru'
        text_reply = TRANSLATIONS[lang]['changed']
        # Отправляем подтверждение и заново выводим приветствие, но уже на русском
        bot.send_message(message.chat.id, text_reply)
        bot.send_message(message.chat.id, TRANSLATIONS[lang]['welcome'], reply_markup=get_language_keyboard())
        
    elif message.text == "English 🇺🇸":
        lang = 'en'
        text_reply = TRANSLATIONS[lang]['changed']
        # Отправляем подтверждение и заново выводим приветствие, но уже на английском
        bot.send_message(message.chat.id, text_reply)
        bot.send_message(message.chat.id, TRANSLATIONS[lang]['welcome'], reply_markup=get_language_keyboard())
        
    else:
        # Если пользователь отправил обычный текст вместо нажатия на кнопку,
        # бот ответит на языке его профиля
        user_lang_code = message.from_user.language_code
        lang = 'ru' if user_lang_code and user_lang_code.startswith('ru') else 'en'
        bot.send_message(message.chat.id, TRANSLATIONS[lang]['unknown_btn'])

# --- ЭТОТ БЛОК НУЖЕН СТРОГО ДЛЯ RENDER (ЧТОБЫ СЕРВЕР НЕ ВЫДАВАЛ ОШИБКУ) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_check():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), HealthCheckHandler)
    server.serve_forever()
# ------------------------------------------------------------------------

if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    print("Бот RoboLanguage успешно запущен...")
    bot.infinity_polling()
