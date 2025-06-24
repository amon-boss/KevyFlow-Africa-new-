import os import logging from aiogram import Bot, Dispatcher, executor, types from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton from keep_alive import keep_alive

Logging

logging.basicConfig(level=logging.INFO)

Variables d'environnement

BOT_TOKEN = os.getenv("BOT_TOKEN") ADMIN_ID = int(os.getenv("ADMIN_ID")) GROUP_ID = int(os.getenv("GROUP_ID")) INVIT_LINK = os.getenv("INVIT_LINK")

bot = Bot(token=BOT_TOKEN) dp = Dispatcher(bot)

Clavier des moyens de paiement

payment_keyboard = InlineKeyboardMarkup(row_width=1) payment_keyboard.add( InlineKeyboardButton("🟠 Orange Money 💰", callback_data="orange"), InlineKeyboardButton("🟡 MTN Money 💰", callback_data="mtn"), InlineKeyboardButton("🔵 Wave 💰", callback_data="wave") )

Dictionnaire des numéros de paiement

payment_numbers = { "orange": "+2250768388770", "mtn": "+2250504652480", "wave": "+2250768388770"  # Même numéro pour wave }

Message de bienvenue quand l'utilisateur démarre le bot

@dp.message_handler(commands=['start']) async def start_cmd(message: types.Message): await message.answer( "👋 Salut et bienvenue sur KevyFlowBot !😎⚔️\n\n" "Ce canal est réservé aux membres ayant payé l'accès🔐\n\n" "🎟️ PRIX À PAYER: 2500F\n\n" "Étapes à suivre pour payer:\n" "1️⃣ Choisissez une méthode de paiement 💵\n" "2️⃣ Envoyez une capture d'écran du paiement 🧾\n" "3️⃣ Votre capture sera traitée, après validation vous serez ajouté ✅", reply_markup=payment_keyboard )

Gestion des boutons de méthode de paiement

@dp.callback_query_handler(lambda c: c.data in payment_numbers) async def handle_payment_choice(callback_query: types.CallbackQuery): method = callback_query.data number = payment_numbers[method]

await bot.send_message(
    callback_query.from_user.id,
    f"✅ Vous avez choisi ({callback_query.data.upper()})\n\n"
    f"Veuillez effectuer le paiement sur le numéro suivant :\n👉🏼 {number} 💳\n\n"
    "Ensuite, faites une capture d'écran du paiement et envoyez-la ici.🤝\n"
    "Je vous attends ☺️🙏🏼"
)
await callback_query.answer()

Réception de la capture d'écran de paiement

@dp.message_handler(content_types=types.ContentType.PHOTO) async def handle_photo(message: types.Message): if message.photo: photo_id = message.photo[-1].file_id caption = ( f"🧾 Nouvelle capture d'écran reçue !\n" f"👤 De: @{message.from_user.username or message.from_user.full_name}\n" f"🆔 ID: {message.from_user.id}" )

keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("✅ Valider", callback_data=f"valider_{message.from_user.id}"),
        InlineKeyboardButton("❌ Refuser", callback_data=f"refuser_{message.from_user.id}")
    )

    await bot.send_photo(ADMIN_ID, photo=photo_id, caption=caption, reply_markup=keyboard)
    await message.reply("✅ Capture reçue. Elle est en cours de vérification par l'administration.")

Validation ou refus de l'accès par l'admin

@dp.callback_query_handler(lambda c: c.data.startswith("valider_") or c.data.startswith("refuser_")) async def process_validation(callback_query: types.CallbackQuery): action, user_id = callback_query.data.split("_") user_id = int(user_id)

if action == "valider":
    await bot.send_message(user_id,
        "🎉 Félicitations !\n"
        "Ta capture a été validée avec succès.\n"
        "Clique sur le bouton ci-dessous pour rejoindre le canal privé 👇🏼")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🚀 Rejoindre le canal", url=INVIT_LINK))

    await bot.send_message(user_id, "👇🏼 Clique ici :", reply_markup=keyboard)
else:
    await bot.send_message(user_id,
        "😔 Dommage !\n"
        "Ta capture n'a pas été acceptée. Veuillez réessayer ou contacter l'assistance.")

await callback_query.answer()

if name == 'main': keep_alive() executor.start_polling(dp, skip_updates=True)

