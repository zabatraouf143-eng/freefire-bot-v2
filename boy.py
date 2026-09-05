import telebot
from telebot import types
import sqlite3

TOKEN = "8765104365:AAGEZbHSJ1MMp26tIeyE0Dievbm9-lzgxjM"
bot = telebot.TeleBot(TOKEN)
DEV_USERNAME = "your_username"

conn = sqlite3.connect("bot_database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users_data (
    user_id INTEGER PRIMARY KEY,
    points_collected INTEGER DEFAULT 0
)
""")
conn.commit()

translations = {
    "ar": {
        "welcome": "🔥 مرحباً بك في بوت شحن فري فير المجاني!\n\n🆔 اختر من القائمة أدناه لجمع النقاط وشحن حسابك.",
        "btn_profile": "الملف الشخصي 👤", "btn_links": "جمع النقاط 🔗", "btn_ref": "الأصدقاء 👥",
        "btn_points_info": "طريقة جمع النقاط ℹ️", "btn_store": "متجر فري فير 🛒", "btn_support": "الدعم 📞", "btn_admin": "لوحة المطور ⚙️",
        "profile": "👤 **معلومات الحساب:**\n\n🆔 الآيدي: `{user_id}`\n💎 النقاط: `{collected}`",
        "ref": "👥 **نظام الدعوات:**\n\nرابط الدعوة:\n`{ref_link}`\n\n📊 الأصدقاء المحالون: {refs}",
        "support": "📞 للدعم تواصل مع المطور: @{DEV_USERNAME}", "back": "العودة للقائمة الرئيسية 🔙"
    },
    "en": {
        "welcome": "🔥 Welcome to Free Fire free top-up bot!\n\n🆔 Choose from the menu below.",
        "btn_profile": "Profile 👤", "btn_links": "Collect Points 🔗", "btn_ref": "Referral 👥",
        "btn_points_info": "How to earn ℹ️", "btn_store": "Store 🛒", "btn_support": "Support 📞", "btn_admin": "Admin ⚙️",
        "profile": "👤 **Account Info:**\n\n🆔 ID: `{user_id}`\n💎 Points: `{collected}`",
        "ref": "👥 **Referral System:**\n\nLink:\n`{ref_link}`\n\n📊 Invited: {refs}",
        "support": "📞 Support: @{DEV_USERNAME}", "back": "Back 🔙"
    },
    "fr": {
        "welcome": "🔥 Bienvenue sur le bot de recharge Free Fire!\n\n🆔 Choisissez dans le menu.",
        "btn_profile": "Profil 👤", "btn_links": "Points 🔗", "btn_ref": "Parrainage 👥",
        "btn_points_info": "Info ℹ️", "btn_store": "Boutique 🛒", "btn_support": "Support 📞", "btn_admin": "Admin ⚙️",
        "profile": "👤 **Compte :**\n\n🆔 ID : `{user_id}`\n💎 Points : `{collected}`",
        "ref": "👥 **Parrainage :**\n\nLien :\n`{ref_link}`\n\n📊 Parrainés : {refs}",
        "support": "📞 Support : @{DEV_USERNAME}", "back": "Retour 🔙"
    },
    "es": {
        "welcome": "🔥 ¡Bienvenido al bot de Free Fire!\n\n🆔 Elige una opción.",
        "btn_profile": "Perfil 👤", "btn_links": "Puntos 🔗", "btn_ref": "Referidos 👥",
        "btn_points_info": "Info ℹ️", "btn_store": "Tienda 🛒", "btn_support": "Soporte 📞", "btn_admin": "Admin ⚙️",
        "profile": "👤 **Perfil:**\n\n🆔 ID: `{user_id}`\n💎 Puntos: `{collected}`",
        "ref": "👥 **Referidos:**\n\nEnlace:\n`{ref_link}`\n\n📊 Total: {refs}",
        "support": "📞 Soporte: @{DEV_USERNAME}", "back": "Volver 🔙"
    },
    "de": {
        "welcome": "🔥 Willkommen beim Free Fire Bot!\n\n🆔 Wähle aus dem Menü.",
        "btn_profile": "Profil 👤", "btn_links": "Punkte 🔗", "btn_ref": "Empfehlung 👥",
        "btn_points_info": "Info ℹ️", "btn_store": "Shop 🛒", "btn_support": "Support 📞", "btn_admin": "Admin ⚙️",
        "profile": "👤 **Profil:**\n\n🆔 ID: `{user_id}`\n💎 Punkte: `{collected}`",
        "ref": "👥 **Empfehlung:**\n\nLink:\n`{ref_link}`\n\n📊 Eingeladen: {refs}",
        "support": "📞 Support: @{DEV_USERNAME}", "back": "Zurück 🔙"
    },
    "tr": {
        "welcome": "🔥 Free Fire botuna hoş geldin!\n\n🆔 Menüden seç.",
        "btn_profile": "Profil 👤", "btn_links": "Puanlar 🔗", "btn_ref": "Referans 👥",
        "btn_points_info": "Bilgi ℹ️", "btn_store": "Mağaza 🛒", "btn_support": "Destek 📞", "btn_admin": "Yönetici ⚙️",
        "profile": "👤 **Profil:**\n\n🆔 ID: `{user_id}`\n💎 Puan: `{collected}`",
        "ref": "👥 **Referans:**\n\nBağlantı:\n`{ref_link}`\n\n📊 Davet: {refs}",
        "support": "📞 Destek: @{DEV_USERNAME}", "back": "Geri 🔙"
    },
    "ru": {
        "welcome": "🔥 Добро пожаловать в бот Free Fire!\n\n🆔 Выберите в меню.",
        "btn_profile": "Профиль 👤", "btn_links": "Баллы 🔗", "btn_ref": "Рефералы 👥",
        "btn_points_info": "Инфо ℹ️", "btn_store": "Магазин 🛒", "btn_support": "Поддержка 📞", "btn_admin": "Админ ⚙️",
        "profile": "👤 **Профиль:**\n\n🆔 ID: `{user_id}`\n💎 Баллы: `{collected}`",
        "ref": "👥 **Рефералы:**\n\nСсылка:\n`{ref_link}`\n\n📊 Приглашено: {refs}",
        "support": "📞 Поддержка: @{DEV_USERNAME}", "back": "Назад 🔙"
    },
    "id": {
        "welcome": "🔥 Selamat datang di bot Free Fire!\n\n🆔 Pilih menu di bawah.",
        "btn_profile": "Profil 👤", "btn_links": "Poin 🔗", "btn_ref": "Referral 👥",
        "btn_points_info": "Info ℹ️", "btn_store": "Toko 🛒", "btn_support": "Dukungan 📞", "btn_admin": "Admin ⚙️",
        "profile": "👤 **Profil:**\n\n🆔 ID: `{user_id}`\n💎 Poin: `{collected}`",
        "ref": "👥 **Referral:**\n\nLink:\n`{ref_link}`\n\n📊 Diundang: {refs}",
        "support": "📞 Dukungan: @{DEV_USERNAME}", "back": "Kembali 🔙"
    },
    "hi": {
        "welcome": "🔥 फ्री फायर बॉट में आपका स्वागत है!\n\n🆔 नीचे मेनू से चुनें।",
        "btn_profile": "प्रोफ़ाइल 👤", "btn_links": "पॉइंट्स 🔗", "btn_ref": "रेफरल 👥",
        "btn_points_info": "जानकारी ℹ️", "btn_store": "स्टोर 🛒", "btn_support": "सहायता 📞", "btn_admin": "एडमिन ⚙️",
        "profile": "👤 **प्रोफ़ाइल:**\n\n🆔 आईडी: `{user_id}`\n💎 पॉइंट्स: `{collected}`",
        "ref": "👥 **रेफरल:**\n\nलिंक:\n`{ref_link}`\n\n📊 आमंत्रित: {refs}",
        "support": "📞 सहायता: @{DEV_USERNAME}", "back": "वापस 🔙"
    },
    "pt": {
        "welcome": "🔥 Bem-vindo ao bot do Free Fire!\n\n🆔 Escolha no menu.",
        "btn_profile": "Perfil 👤", "btn_links": "Pontos 🔗", "btn_ref": "Indicação 👥",
        "btn_points_info": "Info ℹ️", "btn_store": "Loja 🛒", "btn_support": "Suporte 📞", "btn_admin": "Admin ⚙️",
        "profile": "👤 **Perfil:**\n\n🆔 ID: `{user_id}`\n💎 Pontos: `{collected}`",
        "ref": "👥 **Indicação:**\n\nLink:\n`{ref_link}`\n\n📊 Indicados: {refs}",
        "support": "📞 Suporte: @{DEV_USERNAME}", "back": "Voltar 🔙"
    }
}
# --- الجزء الثاني: الدوال الأساسية ولوحة التحكم والنظام ---

LANG = "ar"  # اللغة الافتراضية

def get_trans(key, lang=LANG):
    return translations.get(lang, translations["ar"]).get(key, key)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    cursor.execute("SELECT points_collected FROM users_data WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.execute("INSERT INTO users_data (user_id, points_collected) VALUES (?, 0)", (user_id,))
        conn.commit()
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(get_trans("btn_profile"), callback_data="menu_profile"),
        types.InlineKeyboardButton(get_trans("btn_links"), callback_data="menu_links"),
        types.InlineKeyboardButton(get_trans("btn_ref"), callback_data="menu_ref"),
        types.InlineKeyboardButton(get_trans("btn_points_info"), callback_data="menu_points_info"),
        types.InlineKeyboardButton(get_trans("btn_store"), callback_data="menu_store"),
        types.InlineKeyboardButton(get_trans("btn_support"), callback_data="menu_support")
    )
    
    # زر لوحة المطور يظهر فقط للمطور
    if str(user_id) == str(DEV_USERNAME) or message.from_user.username == DEV_USERNAME:
        markup.add(types.InlineKeyboardButton(get_trans("btn_admin"), callback_data="menu_admin"))
        
    bot.send_message(message.chat.id, get_trans("welcome"), parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.from_user.id
    data = call.data
    back_text = get_trans("back")
    
    if data == "menu_profile":
        cursor.execute("SELECT points_collected FROM users_data WHERE user_id = ?", (user_id,))
        res = cursor.fetchone()
        collected = res[0] if res else 0
        msg = translations[LANG]["profile"].format(user_id=user_id, collected=collected)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(back_text, callback_data="back_home"))
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        
    elif data == "menu_ref":
        ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        msg = translations[LANG]["ref"].format(ref_link=ref_link, refs=0)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(back_text, callback_data="back_home"))
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        
    elif data == "menu_admin":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔍 البحث عن مستخدم بايدي (ID)", callback_data="admin_search_user"),
            types.InlineKeyboardButton(back_text, callback_data="back_home")
        )
        bot.edit_message_text("⚙️ **لوحة تحكم المطور:**\n\nاختر العملية المطلوبة:", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        
    elif data == "admin_search_user":
        msg = bot.send_message(call.message.chat.id, "🆔 أرسل ايدي (ID) المستخدم للبحث عنه:")
        bot.register_next_step_handler(msg, admin_search_user_process)
        
    elif data.startswith("adm_deduct_") or data.startswith("adm_add_"):
        action, target_id = data.split("_")[1], data.split("_")[2]
        action_name = "خصم" if action == "deduct" else "إضافة"
        msg = bot.send_message(call.message.chat.id, f"📥 أرسل عدد النقاط التي تريد {action_name}ها:")
        bot.register_next_step_handler(msg, admin_modify_points_process, action, target_id)
        
    elif data == "back_home":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(get_trans("btn_profile"), callback_data="menu_profile"),
            types.InlineKeyboardButton(get_trans("btn_links"), callback_data="menu_links"),
            types.InlineKeyboardButton(get_trans("btn_ref"), callback_data="menu_ref"),
            types.InlineKeyboardButton(get_trans("btn_points_info"), callback_data="menu_points_info"),
            types.InlineKeyboardButton(get_trans("btn_store"), callback_data="menu_store"),
            types.InlineKeyboardButton(get_trans("btn_support"), callback_data="menu_support")
        )
        if str(user_id) == str(DEV_USERNAME):
            markup.add(types.InlineKeyboardButton(get_trans("btn_admin"), callback_data="menu_admin"))
        bot.edit_message_text(get_trans("welcome"), call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
# --- الجزء الثالث والأخير: دوال لوحة التحكم ومعالجة النقاط ---

def admin_search_user_process(message):
    try:
        target_id = int(message.text.strip())
        cursor.execute("SELECT user_id, points_collected FROM users_data WHERE user_id = ?", (target_id,))
        user = cursor.fetchone()
        if not user:
            bot.send_message(message.chat.id, "❌ خطأ: هذا المستخدم غير موجود في قاعدة بيانات البوت.")
            return
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("➖ خصم نقاط", callback_data=f"adm_deduct_{target_id}"),
            types.InlineKeyboardButton("➕ إضافة نقاط", callback_data=f"adm_add_{target_id}")
        )
        bot.send_message(
            message.chat.id,
            f"✅ تم العثور على المستخدم:\n🆔 ايدي: `{user[0]}`\n💎 مجموع النقاط: `{user[1]}`",
            parse_mode="Markdown",
            reply_markup=markup
        )
    except ValueError:
        bot.send_message(message.chat.id, "❌ خطأ: يجب إدخال ايدي (ID) صحيح يتكون من أرقام فقط.")

def admin_modify_points_process(message, action, target_id):
    try:
        amount = int(message.text.strip())
        target_id = int(target_id)
        if action == "deduct":
            cursor.execute("UPDATE users_data SET points_collected = MAX(0, points_collected - ?) WHERE user_id = ?", (amount, target_id))
            msg_text = f"✅ تم خصم {amount} نقطة بنجاح من مجموع نقاط المستخدم."
        else:
            cursor.execute("UPDATE users_data SET points_collected = points_collected + ? WHERE user_id = ?", (amount, target_id))
            msg_text = f"✅ تم إضافة {amount} نقطة بنجاح لمجموع نقاط المستخدم."
        conn.commit()
        bot.send_message(message.chat.id, msg_text)
    except ValueError:
        bot.send_message(message.chat.id, "❌ خطأ: يرجى إدخال رقم صحيح.")

@bot.callback_query_handler(func=lambda call: call.data in ["menu_links", "menu_points_info", "menu_store", "menu_support"])
def handle_other_menus(call):
    data = call.data
    back_text = get_trans("back")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(back_text, callback_data="back_home"))
    
    if data == "menu_links":
        msg = "🔗 **قسم جمع النقاط:**\n\nاختر المنصة أو الرابط المناسب للبدء في تجميع النقاط."
    elif data == "menu_points_info":
        msg = "ℹ️ **طريقة جمع النقاط:**\n\n- قم بجمع النقاط عبر الروابط والإحالات واستبدالها بجواهر فري فاير."
    elif data == "menu_store":
        msg = "🛒 **متجر فري فاير:**\n\nاستبدل نقاطك المجمعة بجواهر حقيقية داخل اللعبة."
    elif data == "menu_support":
        msg = translations[LANG]["support"].format(DEV_USERNAME=DEV_USERNAME)
    
    bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

if __name__ == "__main__":
    bot.infinity_polling()

