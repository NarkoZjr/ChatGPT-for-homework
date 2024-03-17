from telegram import Update # python-telegram-bot==13.13
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
import openai # openai==0.27.0
from fake_useragent import UserAgent # fake_useragent==1.4.0 
import time

TOKEN = '' 
OPENAI_API_KEY = ''
PROXY_HOST = ''
PROXY_PORT = ''
LOGIN = ''
PASSWORD = ''

# Установите ключ API для OpenAI
openai.api_key = OPENAI_API_KEY

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я здесь, чтобы отвечать на ваши запросы.')

def send_openai_request(user_message: str, proxy_dict: dict, headers: dict) -> str:
    try:
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=user_message,
            max_tokens=2048,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            proxies=proxy_dict,
            headers=headers
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        return f'Error from OpenAI: {e}'

def echo(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    # Создаем заголовки и словарь прокси
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    proxy_dict = {'http': f'http://{LOGIN}:{PASSWORD}@{PROXY_HOST}:{PROXY_PORT}',
                  'https': f'http://{LOGIN}:{PASSWORD}@{PROXY_HOST}:{PROXY_PORT}'}

    time.sleep(5)

    openai_response = send_openai_request(user_message, proxy_dict, headers)

    truncated_response = openai_response[:4096]

    update.message.reply_text(truncated_response)

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
