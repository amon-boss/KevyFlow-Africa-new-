from flask import Flask
from keep_alive import keep_alive
from telebot import TeleBot, types
import os
from datetime import datetime
import pytz

bot = TeleBot(os.getenv("BOT_TOKEN"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))
GROUP_ID = int(os.getenv("GROUP_ID"))
INVIT_LINK = os.getenv("INVIT_LINK")

confirmed_users = set()

@bot.message_handler(commands=["start"])
def welcome_user(message):
    welcome = """👋 Salut et bienvenue sur KevyFlowBot !😎⚔️

Ce canal est réservé aux membres ayant payé l'accès🔐

🎟️ PRIX À PAYER: 2500F

Étapes à suivre pour payer:
1️⃣ Choisissez une méthode de paiement 💵
2️⃣ Envoyez une capture d'écran du paiement 🧾
3️⃣ Votre capture sera traitée, après validation vous serez ajouté ✅
"""
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("📲 Orange Money", callback_data="orange")
    btn2 = types.InlineKeyboardButton("🌊 Wave", callback_data="wave")
    btn3 = types.InlineKeyboardButton("📶 MTN Money", callback_data="mtn")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, welcome, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["orange", "wave", "mtn"])
def handle_payment(call):
    methods = {
        "orange": "+2250768388770",
        "wave": "+2250768388770",
        "mtn": "+2250504652480"
    }
    name = {"orange": "Orange Money 📲", "wave": "Wave 🌊", "mtn": "MTN Money 📶"}
    number = methods[call.data]

    text = f"""✅ Vous avez choisi {name[call.data]}.

Veuillez effectuer le paiement sur ce numéro : `{number}`  
Faites une capture d'écran du paiement et envoyez-la ici. 🤝
Je vous attends ☺️🙏🏼"""

    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(content_types=["photo"])
def handle_payment_proof(message):
    if message.chat.type == "private":
        caption = f"""🧾 Nouvelle capture reçue !

👤 Utilisateur : @{message.from_user.username or message.from_user.first_name}
🆔 ID : {message.from_user.id}

Que souhaitez-vous faire ?"""
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("✅ Valider", callback_data=f"valider_{message.from_user.id}")
        btn2 = types.InlineKeyboardButton("❌ Refuser", callback_data=f"refuser_{message.from_user.id}")
        markup.add(btn1, btn2)
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("valider_") or call.data.startswith("refuser_"))
def handle_validation(call):
    user_id = int(call.data.split("_")[1])
    if call.data.startswith("valider_"):
        text = """🎉 Félicitations !
Ta capture a été validée avec succès.
Clique sur le bouton ci-dessous pour rejoindre le canal privé 👇🏼"""

        markup = types.InlineKeyboardMarkup()
        join = types.InlineKeyboardButton("🔓 Rejoindre le canal", url=INVIT_LINK)
        markup.add(join)
        bot.send_message(user_id, text, reply_markup=markup)
    else:
        bot.send_message(user_id, "😩 Dommage ! Ta capture a été refusée. Réessaie ou contacte le support.")

@bot.chat_member_handler()
def handle_chat_member_update(chat_member_update):
    user = chat_member_update.new_chat_member.user
    status = chat_member_update.new_chat_member.status
    if chat_member_update.chat.id == GROUP_ID:
        if status == "member":
            text = f"""🎉 Bienvenue @{user.username or user.first_name} dans KevyFlow Africa 🌍 !

Tu es ici pour gagner, pour progresser et pour te surpasser 💸🔥  
👥 Membres actuels, cliquez sur des réactions pour lui souhaiter la bienvenue !"""
            bot.send_message(GROUP_ID, text)
        elif status == "left":
            goodbye = f"👋 @{user.username or user.first_name} nous a quittés. On espère te revoir bientôt 😔"
            bot.send_message(GROUP_ID, goodbye)

# Auto-message Bonjour à 7h30 GMT
def send_morning():
    text = """☀️ Bonjour la famille 🤠

Aujourd’hui, c’est un nouveau jour pour de nouveaux gains !  
Bonne humeur, bonne vibes et concentration 🔥🎯

🗳️ *Prêt pour les gains d’aujourd’hui ?* 🤞🏼🥲"""

    poll = {
        "question": "Prêt pour les gains d’aujourd’hui ? 🤞🏼🥲",
        "options": ["Oui 🫂😋", "Non 🙂‍↔️😩", "Dans un instant 🕝😎"]
    }
    bot.send_message(GROUP_ID, text, parse_mode="Markdown")
    bot.send_poll(GROUP_ID, poll["question"], poll["options"])

# Auto-message Bonne nuit à 23h GMT
def send_night():
    text = """🌙 Bonne nuit à tous la team KevyFlow 🌍

📌 Qui ne risque rien 🙅🏼‍♂️ n'a rien ❌  
C'est quand tu sais pas que t'es en danger que t'es en danger 😎

🗳️ *La journée a été ?*"""
    poll = {
        "question": "La journée a été ?",
        "options": ["✅ De gains", "❌ De pertes", "🌀 Moyenne"]
    }
    bot.send_message(GROUP_ID, text, parse_mode="Markdown")
    bot.send_poll(GROUP_ID, poll["question"], poll["options"])

# Lancement du bot
keep_alive()

import threading
import time
import pytz
from datetime import datetime

def schedule_loop():
    tz = pytz.timezone("Africa/Abidjan")
    while True:
        now = datetime.now(tz)
        if now.hour == 7 and now.minute == 30:
            send_morning()
        if now.hour == 23 and now.minute == 0:
            send_night()
        time.sleep(60)

threading.Thread(target=schedule_loop).start()
bot.infinity_polling()
