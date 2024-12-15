import os
import telebot
from datetime import datetime
import pytz
import asyncio
import countryinfo as ci

os.environ['BOT_TOKEN'] = '7832222391:AAHBg9ZFkYlosQTu-SbI5290DmhrrR5x0HM'  
BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

def capital(country):
    c = ci.CountryInfo(country)
    c.capital(country)

def get_time(country, city):
    try:
        timezone = pytz.timezone(f'{country}/{city}')
        country_time = datetime.now(timezone)
        country_time.strftime('%H:%M:%S')
    except pytz.UnknownTimeZoneError:
        pytz.UnknownTimeZoneError

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hey, What country/city time do you wish to know? (Type /time country city)")

@bot.message_handler(commands=['time'])
def reply(message):
    command_text = message.text.removesuffix('/time').strip()  
    parts = command_text.split()


    current_time = asyncio.gather(get_time(parts[1], parts[2]))
    
    if current_time == pytz.UnknownTimeZoneError:
        bot.reply_to(message, f'The Country ({parts[1]}) or City ({parts[2]}) is invalid.')
        return
    bot.reply_to(message, f'The time in {parts[1]}, {parts[2]} is currently {current_time}')

if __name__ == '__main__':
    
    bot.infinity_polling()