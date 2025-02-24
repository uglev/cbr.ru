import datetime
import time
import telebot
import os
from dotenv import find_dotenv, load_dotenv, set_key
import urllib.request, urllib.error
import xml.etree.ElementTree as ET
import ssl

# Get variables
dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

# List of values (EUR, USD, etc)
currency = ['EUR', 'USD']

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
ID_MESSAGE = int(os.getenv('ID_MESSAGE'))

bot = telebot.TeleBot(token=TELEGRAM_TOKEN)


def send_message(messages):
    if ID_MESSAGE > 0:
        time.sleep(1)
        try:
            bot.delete_message(chat_id=CHAT_ID, message_id=ID_MESSAGE)
        except:
            print(f"Error deleting message {ID_MESSAGE}")
    new_id_message = bot.send_message(chat_id=CHAT_ID, text=messages)
    set_key(dotenv_file, 'ID_MESSAGE', str(new_id_message.id))


# Datetime +1 day
date_string = datetime.date.today()
date_string += datetime.timedelta(days=1)
date_string = date_string.strftime('%d/%m/%Y')
url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date_string}'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

data = urllib.request.urlopen(url, context=ctx).read()
#print('Retrieved', len(data), 'characters.')
root = ET.fromstring(data)

result = 'Курс основных валют на завтра:\n\n'

for country in root.findall('Valute'):
    if country.find('CharCode').text in currency:
        curName = country.find('Name').text
        nominal = int(country.find('Nominal').text)
        value = country.find('Value').text
    else:
        continue
    value = float(value.replace(',', '.'))
    result += f'{nominal} {curName} = {value} руб.\n'

send_message(result)