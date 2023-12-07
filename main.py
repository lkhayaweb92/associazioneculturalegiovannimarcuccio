from telebot import types
from settings import *
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

# admin id chat
ADMIN_CHAT_ID = ""

# ChatAperta
ChatAperta = False

#Instagram
instagram_url = "https://www.instagram.com/"

#Tiktok
tiktok_url = "https://www.tiktok.com/"

#Youtube
youtube_url = "https://www.youtube.com/"

#Facebook
facebook_url = "https://www.facebook.com/"

#Whatsapp
whatsapp_url = "https://wa.me/"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"👋 {message.from_user.username}, posso darti informazioni sull'Associazione Culturale Giovanni Marcuccio")

    text = f"Cosa vuoi fare?"

    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=steamMarkup())

def social_markup():
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add('Instagram', 'Facebook')
    markup.add('Youtube', 'TikTok')
    markup.add('Whatsapp')
    markup.add('Indietro')
    return markup

def steamMarkup():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add('📘 info', '🔗 social')
    markup.add('💬 parla con un admin',  '👨‍💻 developer')
    markup.add('❌ exit')
    return markup

def aspi_admin():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔓 Apri chat", callback_data="open_chat"),
               InlineKeyboardButton("🔒 Chiudi chat", callback_data="close_chat"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    global ChatAperta
    chat_id = call.message.chat.id
    if call.data == 'open_chat':
        ChatAperta = True
        bot.send_message(chat_id, "Hai avviato una chat privata con un amministratore. Scrivi il tuo messaggio:")
        bot.register_next_step_handler(call.message, forward_to_admin)
    elif call.data == 'close_chat':
        ChatAperta = False
        bot.send_message(chat_id, "Hai chiuso la chat con l'amministratore.", reply_markup=steamMarkup())

def forward_to_admin(message):
    admin_chat_id = ADMIN_CHAT_ID
    user_chat_id = message.chat.id
    text = f"Messaggio da {message.chat.first_name} ({user_chat_id}): {message.text}"
    admin_msg = bot.send_message(admin_chat_id, text)
    bot.register_next_step_handler(admin_msg, forward_to_user, user_chat_id)

def forward_message(message):
    if ChatAperta:
        admin_chat_id = ADMIN_CHAT_ID
        user_chat_id = message.chat.id
        text = f"Messaggio da {message.chat.first_name} ({user_chat_id}): {message.text}"
        admin_msg = bot.send_message(admin_chat_id, text)
        bot.register_next_step_handler(admin_msg, forward_to_user, user_chat_id)

def forward_to_user(admin_msg, user_chat_id):
    if ChatAperta:
        text = f"Risposta da un amministratore: {admin_msg.text}"
        bot.send_message(user_chat_id, text)

@bot.message_handler(func=lambda m: True)
def any(message):
    forward_message(message)        
    # Verifica se il messaggio è un comando per tornare indietro
    if message.text.lower() == 'indietro':
        # Implementa qui le azioni desiderate per tornare indietro
        bot.reply_to(message, "Tornato indietro!", reply_markup=steamMarkup())  # Esempio di risposta
    elif 'info' in message.text:
        bot.reply_to(message, "Siamo l'AssociazioneCulturaleGiovanniMarcuccio")
    elif 'social' in message.text:
        bot.reply_to(message, "I nostri social dove puoi seguirci.", reply_markup=social_markup())
    elif 'parla con un admin' in message.text:
        bot.reply_to(message, "Chat con admin", reply_markup=aspi_admin())
    elif 'developer' in message.text:
        bot.reply_to(message, "Il bot è stato creato dal nostro tecnico informatico @Step1992.")
    elif 'exit' in message.text:
        bot.reply_to(message, "Ciao 👋, hai chiuso il bot per farlo funzionare digita /start.", reply_markup=types.ReplyKeyboardRemove())
    elif message.text in ['Instagram', 'Facebook', 'Youtube', 'TikTok', 'Whatsapp']:
        link = send_social_link(message.chat.id, message.text)
        if link:
            bot.reply_to(message, f"Ecco il link per {message.text}: {link}")
        else:
            bot.reply_to(message, "La piattaforma selezionata non è valida.")

def send_social_link(chat_id, social_platform):
    social_links = {
        'Instagram': instagram_url,
        'Facebook': facebook_url,
        'Youtube': youtube_url,
        'TikTok': tiktok_url,
        'Whatsapp': whatsapp_url
    }

    if social_platform in social_links:
        link = social_links[social_platform]
        return link
    else:
        return None  # Ritorna None se la piattaforma non è riconosciuta

print('Il bot è attivo')
bot.infinity_polling()