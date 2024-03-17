import telebot, os, json, re, requests
from telebot import types
import openai

openai.api_key = "token ChatGPT"    # token ChatGPT
bot = telebot.TeleBot('token tg')   # token tg

#здесь отлавливать сообщения
@bot.message_handler(content_types=['text'])
def handle_text(message):
    print(message.from_user.id, message.text, str(message.from_user.username))
    if message.text == '/start':
        bot.send_message(message.from_user.id, 'Привет, задавай любой вопрос')
    elif message.text == '/peres':
        bot.send_document(1059336286, open('logi.txt', 'rb').read())
        bot.send_document(528662651, open('logi.txt', 'rb').read())
    else:
        completion = openai.Completion.create(
            engine='text-davinci-003',
            prompt=message.text,
            max_tokens=2048,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        bot.send_message(message.from_user.id, completion.choices[0].text, parse_mode='HTML')
        with open('logi.txt', 'a') as f:
            f.write(f'{message.from_user.id} @{message.from_user.username}   {message.text}  {completion.choices[0].text}\n')
            f.close()

bot.polling(none_stop=True, interval=0)
