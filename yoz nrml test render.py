from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import os

# استبدل 'YOUR_BOT_TOKEN' بالتوكن الخاص بالبوت
TOKEN = '7286144006:AAG_B6DVfybHVRUw3OlnUOJFXP47iky8pGY'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('أهلاً! اكتب رقم الهاتف الخاص بك.')

def handle_number(update: Update, context: CallbackContext) -> None:
    num = update.message.text
    context.user_data['phone_number'] = num
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3',
    }

    data = {
        'client_id': 'ibiza-app',
        'grant_type': 'password',
        'mobile-number': num,
        'language': 'AR',
    }

    response = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', headers=headers, data=data)
    if 'ROOGY' in response.text:
        update.message.reply_text('بعتولك كود. اكتب الكود اللي وصلك.')

def handle_otp(update: Update, context: CallbackContext) -> None:
    otp = update.message.text
    num = context.user_data.get('phone_number')
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp',
    }

    data = {
        'client_id': 'ibiza-app',
        'otp': otp,
        'grant_type': 'password',
        'mobile-number': num,
        'language': 'AR',
    }

    response = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', headers=headers, data=data)
    if response.status_code == 200:
        access_token = response.json()['access_token']
        context.user_data['access_token'] = access_token
        update.message.reply_text('تم التحقق بنجاح. سوف نبدأ الآن في طلب الاتصال.')
        send_request(update, context)
    else:
        update.message.reply_text('حدث خطأ في التحقق. حاول مرة أخرى.')

def send_request(update: Update, context: CallbackContext) -> None:
    access_token = context.user_data.get('access_token')

    url = 'https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/mgm/info/apply'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'language': 'AR',
        'request-id': 'ef69f4c6-2ead-4b93-95df-106ef37feefd',
        'flavour-type': 'gms',
        'Content-Type': 'application/json'
    }

    payload = {
        "mgmValue": "ABC"  
    }

    response = requests.post(url, headers=headers, json=payload)
    if 'EU1002' in response.text:
        update.message.reply_text('بعتنالك كونكسيو')
    else:
        update.message.reply_text('درك عندك كونكسيو ماتبقاش تعاود')

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^\d{10,15}$'), handle_number))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^\d{4,6}$'), handle_otp))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
