import os
import threading
from flask import Flask
import telebot
from telebot import types
import sqlite3
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Free Fire Bot is alive and running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

TOKEN = "8765104365:AAGEZbHSJ1MMp26tIeyE0Dievbm9-lzgxjM"
DEV_USERNAME = "raouf100K"
CHANNEL_TG = "ONDRAY_FF"
CHANNEL_YT = "https://youtube.com/@dray-xit?si=mV4JOtKwFFIZ1mND"

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("bot_database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users_data (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    balance INTEGER DEFAULT 0,
    points_collected REAL DEFAULT 0,
    referrer INTEGER,
    ref_rewarded INTEGER DEFAULT 0,
    language TEXT DEFAULT 'ar',
    sub_attempts INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    url TEXT,
    code TEXT,
    used INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS link_points (
    category TEXT PRIMARY KEY,
    points REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_category_cooldowns (
    user_id INTEGER,
    category TEXT,
    last_action_time REAL,
    PRIMARY KEY (user_id, category)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    user_id INTEGER PRIMARY KEY
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS competitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT
)
""")
conn.commit()

translations = {
    "ar": {
        "welcome": "🔥 أهلاً بك يا بطل في بوت شحن فري فاير مجاناً!\n\n🆔 اختر من القائمة أدناه ما يناسبك لتجميع النقاط وشحن حسابك.\n👥 عدد المستخدمين: {total_users}",
        "btn_profile": "الملف الشخصي 👤",
        "btn_links": "تجميع النقاط (روابط) 🔗",
        "btn_ref": "رصيد الإحالة 👥",
        "btn_points_info": "طريقة جمع النقاط ℹ️",
        "btn_store": "متجر فري فاير 🛒",
        "btn_support": "الدعم الفني 📞",
        "btn_admin": "لوحة التحكم ⚙️",
        "btn_lang": "تغيير اللغة 🌐",
        "btn_competitions": "المسابقات اليومية 🏆",
        "profile": "👤 **معلومات حسابك:**\n\n🆔 الآيدي: `{user_id}`\n💎 النقاط المجمعة: `{collected}` نقطة",
        "ref": "👥 **نظام الإحالة:**\n\nشارك رابط الإحالة الخاص بك:\n`{ref_link}`\n\nأي شخص يدخل عبر رابطك ويجمع 35 نقطة، ستحصل أنت على **20 نقطة** مجاناً!\n📊 عدد الأشخاص الذين دعيتهم: {refs}",
        "support": "📞 للدعم تواصل مع المطور حصرياً عبر:\n@{DEV_USERNAME}",
        "back": "العودة للقائمة الرئيسية 🔙",
        "sub_req": "⚠️ يشترط الاشتراك في قنواتنا لتشغيل البوت:\n\n📢 قناة تيليجرام: @ONDRAY_FF\n📺 قناة اليوتيوب: {CHANNEL_YT}\n\nبعد الاشتراك، اضغط على الزر أدناه:",
        "sub_btn": "✅ تمت الاشتراك",
        "not_sub": "❌ لم تقم بالاشتراك في القنوات بعد! يرجى الاشتراك ثم المحاولة مرة أخرى."
    },
    "en": {
        "welcome": "🔥 Welcome to Free Fire top-up bot!\n\n🆔 Choose from the menu below.\n👥 Total Users: {total_users}",
        "btn_profile": "Profile 👤",
        "btn_links": "Collect Points 🔗",
        "btn_ref": "Referral 👥",
        "btn_points_info": "How to earn ℹ️",
        "btn_store": "Store 🛒",
        "btn_support": "Support 📞",
        "btn_admin": "Admin ⚙️",
        "btn_lang": "Change Language 🌐",
        "btn_competitions": "Daily Competitions 🏆",
        "profile": "👤 **Account Info:**\n\n🆔 ID: `{user_id}`\n💎 Points: `{collected}`",
        "ref": "👥 **Referral System:**\n\nYour link:\n`{ref_link}`\n\nGet **20 points** when your referral reaches 35 points!\n📊 Invited: {refs}",
        "support": "📞 Support: @{DEV_USERNAME}",
        "back": "Back 🔙",
        "sub_req": "⚠️ Subscription required:\n\n📢 Telegram: @ONDRAY_FF\n📺 YouTube: {CHANNEL_YT}\n\nClick below after subscribing:",
        "sub_btn": "✅ Subscribed",
        "not_sub": "❌ You haven't subscribed yet! Please subscribe and try again."
    },
    "fr": {
        "welcome": "🔥 Bienvenue sur le bot Free Fire!\n\n🆔 Choisissez dans le menu.\n👥 Utilisateurs: {total_users}",
        "btn_profile": "Profil 👤",
        "btn_links": "Points 🔗",
        "btn_ref": "Parrainage 👥",
        "btn_points_info": "Info ℹ️",
        "btn_store": "Boutique 🛒",
        "btn_support": "Support 📞",
        "btn_admin": "Admin ⚙️",
        "btn_lang": "Changer la langue 🌐",
        "btn_competitions": "Compétitions 🏆",
        "profile": "👤 **Compte :**\n\n🆔 ID : `{user_id}`\n💎 Points : `{collected}`",
        "ref": "👥 **Parrainage :**\n\nLien :\n`{ref_link}`\n\nGagnez **20 points** quand votre filleul atteint 35 points!\n📊 Parrainés : {refs}",
        "support": "📞 Support : @{DEV_USERNAME}",
        "back": "Retour 🔙",
        "sub_req": "⚠️ Abonnement requis:\n\n📢 Telegram : @ONDRAY_FF\n📺 YouTube : {CHANNEL_YT}\n\nCliquez ci-dessous:",
        "sub_btn": "✅ Abonné",
        "not_sub": "❌ Vous n'êtes pas abonné!"
    }
}
translations.update({
    "es": {
        "welcome": "🔥 ¡Bienvenido al bot de Free Fire!\n\n🆔 Elige del menú a continuación.\n👥 Usuarios totales: {total_users}",
        "btn_profile": "Perfil 👤",
        "btn_links": "Puntos 🔗",
        "btn_ref": "Referidos 👥",
        "btn_points_info": "Cómo ganar ℹ️",
        "btn_store": "Tienda 🛒",
        "btn_support": "Soporte 📞",
        "btn_admin": "Admin ⚙️",
        "btn_lang": "Cambiar idioma 🌐",
        "btn_competitions": "Competiciones 🏆",
        "profile": "👤 **Información de cuenta:**\n\n🆔 ID: `{user_id}`\n💎 Puntos: `{collected}`",
        "ref": "👥 **Sistema de referidos:**\n\nTu enlace:\n`{ref_link}`\n\n¡Gana **20 puntos** cuando tu referido alcance 35 puntos!\n📊 Invitados: {refs}",
        "support": "📞 Soporte: @{DEV_USERNAME}",
        "back": "Volver 🔙",
        "sub_req": "⚠️ Suscripción requerida:\n\n📢 Telegram: @ONDRAY_FF\n📺 YouTube: {CHANNEL_YT}",
        "sub_btn": "✅ Susكريتو",
        "not_sub": "❌ ¡No te has suscrito!"
    },
    "de": {
        "welcome": "🔥 Willkommen beim Free Fire Bot!\n\n🆔 Wähle aus dem Menü unten.\n👥 Gesamte Benutzer: {total_users}",
        "btn_profile": "Profil 👤",
        "btn_links": "Punkte sammeln 🔗",
        "btn_ref": "Empfehlung 👥",
        "btn_points_info": "Wie man verdient ℹ️",
        "btn_store": "Shop 🛒",
        "btn_support": "Support 📞",
        "btn_admin": "Admin ⚙️",
        "btn_lang": "Sprache ändern 🌐",
        "btn_competitions": "Wettbewerbe 🏆",
        "profile": "👤 **Kontoinformationen:**\n\n🆔 ID: `{user_id}`\n💎 Punkte: `{collected}`",
        "ref": "👥 **Empfehlungssystem:**\n\nIhr Link:\n`{ref_link}`\n\nErhalten Sie **20 Punkte**, wenn Ihre Empfehlung 35 Punkte erreicht!\n📊 Eingeladen: {refs}",
        "support": "📞 Support: @{DEV_USERNAME}",
        "back": "Zurück 🔙",
        "sub_req": "⚠️ Abonnement erforderlich:\n\n📢 Telegram: @ONDRAY_FF\n📺 YouTube: {CHANNEL_YT}",
        "sub_btn": "✅ Abonniert",
        "not_sub": "❌ Sie haben nicht abonniert!"
    },
    "tr": {
        "welcome": "🔥 Free Fire yükleme botuna hoş geldiniz!\n\n🆔 Aşağıdaki menüden seçim yapın.\n👥 Toplam Kullanıcı: {total_users}",
        "btn_profile": "Profil 👤",
        "btn_links": "Puan Topla 🔗",
        "btn_ref": "Referans 👥",
        "btn_points_info": "Nasıl kazanılır ℹ️",
        "btn_store": "Mağaza 🛒",
        "btn_support": "Destek 📞",
        "btn_admin": "Yönetici ⚙️",
        "btn_lang": "Dili Değiştir 🌐",
        "btn_competitions": "Yarışmalar 🏆",
        "profile": "👤 **Hesap Bilgileri:**\n\n🆔 ID: `{user_id}`\n💎 Puanlar: `{collected}`",
        "ref": "👥 **Referans Sistemi:**\n\nBağlantınız:\n`{ref_link}`\n\nReferansınız 35 puana ulaştığında **20 puan** kazanın!\n📊 Davet edilen: {refs}",
        "support": "📞 Destek: @{DEV_USERNAME}",
        "back": "Geri 🔙",
        "sub_req": "⚠️ Abonelik gerekiyor:\n\n📢 Telegram: @ONDRAY_FF\n📺 YouTube: {CHANNEL_YT}",
        "sub_btn": "✅ Abone Olundu",
        "not_sub": "❌ Abone olmadınız!"
    },
    "br": {
        "welcome": "🔥 Bem-vindo ao bot de recarga Free Fire!\n\n🆔 Escolha no menu abaixo.\n👥 Total de usuários: {total_users}",
        "btn_profile": "Perfil 👤",
        "btn_links": "Coletar Pontos 🔗",
        "btn_ref": "Indicação 👥",
        "btn_points_info": "Como ganhar ℹ️",
        "btn_store": "Loja 🛒",
        "btn_support": "Suporte 📞",
        "btn_admin": "Admin ⚙️",
        "btn_lang": "Mudar idioma 🌐",
        "btn_competitions": "Competições 🏆",
        "profile": "👤 **Informações da Conta:**\n\n🆔 ID: `{user_id}`\n💎 Pontos: `{collected}`",
        "ref": "👥 **Sistema de Indicação:**\n\nSeu link:\n`{ref_link}`\n\nGanhe **20 pontos** quando sua indicação atingir 35 pontos!\n📊 Convidados: {refs}",
        "support": "📞 Suporte: @{DEV_USERNAME}",
        "back": "Voltar 🔙",
        "sub_req": "⚠️ Inscrição necessária:\n\n📢 Telegram: @ONDRAY_FF\n📺 YouTube: {CHANNEL_YT}",
        "sub_btn": "✅ Inscrito",
        "not_sub": "❌ Você não se inscreveu!"
    }
})

def get_trans(lang="ar", key=""):
    lang_dict = translations.get(lang, translations["ar"])
    return lang_dict.get(key, translations["ar"].get(key, key))

def get_user_lang(user_id):
    cursor.execute("SELECT language FROM users_data WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row and row[0]:
        return row[0]
    return "ar"

def get_link_points(category):
    cursor.execute("SELECT points FROM link_points WHERE category = ?", (category,))
    row = cursor.fetchone()
    if row:
        return row[0]
    defaults = {"short": 2.0, "shirink": 2.0, "link": 2.0, "ex": 1.5, "Oo": 1.0, "cutw": 2.0, "clks": 2.0, "earn": 2.0, "pe": 2.0, "adfl": 2.0}
    return defaults.get(category, 2.0)

def get_main_menu_markup(lang="ar"):
    cursor.execute("SELECT COUNT(*) FROM users_data")
    total_users = cursor.fetchone()[0]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(get_trans(lang, 'btn_profile'), callback_data="menu_profile"),
        types.InlineKeyboardButton(get_trans(lang, 'btn_links'), callback_data="menu_links"),
        types.InlineKeyboardButton(get_trans(lang, 'btn_ref'), callback_data="menu_ref"),
        types.InlineKeyboardButton(get_trans(lang, 'btn_points_info'), callback_data="get_points_info"),
        types.InlineKeyboardButton(get_trans(lang, 'btn_store'), callback_data="menu_ff"),
        types.InlineKeyboardButton(get_trans(lang, 'btn_competitions'), callback_data="menu_competitions"),
        types.InlineKeyboardButton(get_trans(lang, 'btn_support'), callback_data="menu_support"),
        types.InlineKeyboardButton(get_trans(lang, 'btn_lang'), callback_data="menu_lang"),
        types.InlineKeyboardButton(get_trans(lang, 'btn_admin'), callback_data="menu_admin")
    )
    return markup
def check_forced_subscription(message):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    try:
        chat_member = bot.get_chat_member(f"@{CHANNEL_TG}", user_id)
        if chat_member.status in ['member', 'creator', 'administrator']:
            return True
    except Exception:
        pass

    cursor.execute("SELECT sub_attempts FROM users_data WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    attempts = row[0] if row else 0

    if attempts == 0:
        cursor.execute("UPDATE users_data SET sub_attempts = 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(get_trans(lang, 'sub_btn'), callback_data="check_sub_again"))
        bot.send_message(
            user_id,
            get_trans(lang, 'sub_req').format(CHANNEL_YT=CHANNEL_YT),
            reply_markup=markup
        )
        return False
    elif attempts == 1:
        cursor.execute("UPDATE users_data SET sub_attempts = 2 WHERE user_id = ?", (user_id,))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(get_trans(lang, 'sub_btn'), callback_data="check_sub_again"))
        bot.send_message(
            user_id,
            get_trans(lang, 'not_sub') + "\n\n" + get_trans(lang, 'sub_req').format(CHANNEL_YT=CHANNEL_YT),
            reply_markup=markup
        )
        return False
    else:
        return True

@bot.callback_query_handler(func=lambda call: call.data == "check_sub_again")
def cb_check_sub(call):
    user_id = call.from_user.id
    lang = get_user_lang(user_id)
    try:
        chat_member = bot.get_chat_member(f"@{CHANNEL_TG}", user_id)
        if chat_member.status in ['member', 'creator', 'administrator']:
            bot.answer_callback_query(call.id, "✅ تم التحقق بنجاح!")
            cursor.execute("SELECT COUNT(*) FROM users_data")
            total_users = cursor.fetchone()[0]
            bot.edit_message_text(
                get_trans(lang, 'welcome').format(total_users=total_users),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_main_menu_markup(lang)
            )
            return
    except Exception:
        pass
    bot.answer_callback_query(call.id, "❌ لم تقم بالاشتراك بعد!", show_alert=True)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    
    if not check_forced_subscription(message):
        return

    args = message.text.split()
    referrer = None
    if len(args) > 1:
        try:
            ref_id = int(args[1])
            if ref_id != user_id:
                referrer = ref_id
        except ValueError:
            pass

    cursor.execute("SELECT user_id, balance, points_collected FROM users_data WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.execute("INSERT INTO users_data (user_id, username, referrer) VALUES (?, ?, ?)", (user_id, username, referrer))
        conn.commit()
        if referrer:
            cursor.execute("SELECT user_id, points_collected FROM users_data WHERE user_id = ?", (referrer,))
            ref_user = cursor.fetchone()
            if ref_user:
                new_ref_pts = ref_user[1] + 20
                cursor.execute("UPDATE users_data SET points_collected = ? WHERE user_id = ?", (new_ref_pts, referrer))
                conn.commit()
                try:
                    bot.send_message(referrer, "🎁 مبروك! لقد حصلت على 20 نقطة لأن شخصاً ما انضم عبر رابط الإحالة الخاص بك.")
                except Exception:
                    pass

    lang = get_user_lang(user_id)
    cursor.execute("SELECT COUNT(*) FROM users_data")
    total_users = cursor.fetchone()[0]
    
    bot.send_message(
        message.chat.id,
        get_trans(lang, 'welcome').format(total_users=total_users),
        reply_markup=get_main_menu_markup(lang)
    )

def show_links_menu(call):
    user_id = call.from_user.id
    lang = get_user_lang(user_id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    categories = [
        ("short", "رابط 1"), ("shirink", "رابط 2"), ("link", "رابط 3"), 
        ("ex", "رابط 4"), ("Oo", "رابط 5"), ("cutw", "cutw"), 
        ("clks", "clks"), ("earn", "earn"), ("pe", "pe"), ("adfl", "adfl")
    ]
    for cat, name in categories:
        pts = get_link_points(cat)
        markup.add(types.InlineKeyboardButton(f"{name} ({pts} نقطة)", callback_data=f"get_link_{cat}"))
    markup.add(types.InlineKeyboardButton(get_trans(lang, 'back'), callback_data="back_to_main"))
    
    bot.edit_message_text(
        "🔗 **اختر أحد الروابط أدناه لتخطيها وجمع النقاط:**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

def show_store_menu(call):
    user_id = call.from_user.id
    lang = get_user_lang(user_id)
    # الأسعار مخفضة بنسبة 30%
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("💎 100 جوهرة -> 35 نقطة (تخفيض 30%)", callback_data="buy_100"),
        types.InlineKeyboardButton("💎 310 جوهرة -> 100 نقطة (تخفيض 30%)", callback_data="buy_310"),
        types.InlineKeyboardButton("💎 520 جوهرة -> 160 نقطة (تخفيض 30%)", callback_data="buy_520"),
        types.InlineKeyboardButton(get_trans(lang, 'back'), callback_data="back_to_main")
    )
    bot.edit_message_text(
        "🛒 **متجر شحن فري فاير (أسعار مخفضة 30%):**\nاختر الباقة المناسبة لك:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

def show_competitions_menu(call):
    user_id = call.from_user.id
    lang = get_user_lang(user_id)
    cursor.execute("SELECT id, text FROM competitions")
    comps = cursor.fetchall()
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    if comps:
        for comp_id, comp_text in comps:
            markup.add(types.InlineKeyboardButton(f"🏆 مسابقة #{comp_id}", callback_data=f"view_comp_{comp_id}"))
    else:
        markup.add(types.InlineKeyboardButton("لا توجد مسابقات حالياً ❌", callback_data="none"))
        
    markup.add(types.InlineKeyboardButton(get_trans(lang, 'back'), callback_data="back_to_main"))
    
    bot.edit_message_text(
        "🏆 **قسم المسابقات اليومية:**\nاختر مسابقة لعرض تفاصيلها:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    lang = get_user_lang(user_id)
    data = call.data
    
    if data == "menu_profile":
        cursor.execute("SELECT points_collected FROM users_data WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        collected = row[0] if row else 0
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            get_trans(lang, 'profile').format(user_id=user_id, collected=collected),
            call.message.chat.id, call.message.message_id,
            reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(get_trans(lang, 'back'), callback_data="back_to_main"))
        )
    elif data == "menu_links":
        bot.answer_callback_query(call.id)
        show_links_menu(call)
    elif data == "menu_ref":
        bot.answer_callback_query(call.id)
        bot.info = f"https://t.me/{bot.get_me().username}?start={user_id}"
        cursor.execute("SELECT COUNT(*) FROM users_data WHERE referrer = ?", (user_id,))
        refs = cursor.fetchone()[0]
        bot.edit_message_text(
            get_trans(lang, 'ref').format(ref_link=bot.info, refs=refs),
            call.message.chat.id, call.message.message_id,
            reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(get_trans(lang, 'back'), callback_data="back_to_main"))
        )
    elif data == "get_points_info":
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            "ℹ️ **طريقة جمع النقاط:**\n\nاضغط على 'تجميع النقاط'، اختر أي رابط، أكمل التخطي، ثم الصق الكود الذي تحصله هنا لتحصل على النقاط فوراً!",
            call.message.chat.id, call.message.message_id,
            reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(get_trans(lang, 'back'), callback_data="back_to_main"))
        )
    elif data == "menu_ff":
        bot.answer_callback_query(call.id)
        show_store_menu(call)
    elif data == "menu_competitions":
        bot.answer_callback_query(call.id)
        show_competitions_menu(call)
    elif data == "menu_support":
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            get_trans(lang, 'support').format(DEV_USERNAME=DEV_USERNAME),
            call.message.chat.id, call.message.message_id,
            reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(get_trans(lang, 'back'), callback_data="back_to_main"))
        )
    elif data == "menu_lang":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("العربية 🇩🇿", callback_data="lang_ar"),
            types.InlineKeyboardButton("English 🇬🇧", callback_data="lang_en"),
            types.InlineKeyboardButton("Français 🇫🇷", callback_data="lang_fr"),
            types.InlineKeyboardButton("Español 🇪🇸", callback_data="lang_es"),
            types.InlineKeyboardButton("Deutsch 🇩🇪", callback_data="lang_de"),
            types.InlineKeyboardButton("Türkçe 🇹🇷", callback_data="lang_tr"),
            types.InlineKeyboardButton("Português 🇧🇷", callback_data="lang_br"),
            types.InlineKeyboardButton(get_trans(lang, 'back'), callback_data="back_to_main")
        )
        bot.edit_message_text("🌐 اختر اللغة المفضلة لديك:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif data.startswith("lang_"):
        new_lang = data.split("_")[1]
        cursor.execute("UPDATE users_data SET language = ? WHERE user_id = ?", (new_lang, user_id))
        conn.commit()
        bot.answer_callback_query(call.id, "✅ تم تغيير اللغة بنجاح!")
        cursor.execute("SELECT COUNT(*) FROM users_data")
        total_users = cursor.fetchone()[0]
        bot.edit_message_text(
            get_trans(new_lang, 'welcome').format(total_users=total_users),
            call.message.chat.id, call.message.message_id,
            reply_markup=get_main_menu_markup(new_lang)
        )
    elif data == "menu_admin":
        cursor.execute("SELECT user_id FROM admins WHERE user_id = ?", (user_id,))
        if user_id != 55555555 and not cursor.fetchone() and call.from_user.username != DEV_USERNAME:
            bot.answer_callback_query(call.id, "❌ عذراً، هذه اللوحة للمطورين فقط!", show_alert=True)
            return
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("طرد بعض المساعدين 🚫", callback_data="admin_kick"),
            types.InlineKeyboardButton("إضافة مسابقة 🏆", callback_data="admin_add_comp"),
            types.InlineKeyboardButton("تعديل عدد نقاط كل رابط 🔗", callback_data="admin_edit_link_points"),
            types.InlineKeyboardButton(get_trans(lang, 'back'), callback_data="back_to_main")
        )
        bot.edit_message_text("⚙️ **لوحة التحكم الخاصة بالمطور:**", call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif data == "admin_kick":
        msg = bot.send_message(call.message.chat.id, "👤 أرسل الآن آيدي الشخص الذي تريد طرده من المساعدين:")
        bot.register_next_step_handler(msg, admin_kick_process)
    elif data == "admin_add_comp":
        msg = bot.send_message(call.message.chat.id, "🏆 أرسل وصف المسابقة الجديدة ليتم إضافتها لقسم المسابقات اليومية:")
        bot.register_next_step_handler(msg, admin_add_comp_process)
    elif data == "admin_edit_link_points":
        markup = types.InlineKeyboardMarkup(row_width=2)
        cats = ["short", "shirink", "link", "ex", "Oo", "cutw", "clks", "earn", "pe", "adfl"]
        for c in cats:
            markup.add(types.InlineKeyboardButton(f"تعديل نقطة {c}", callback_data=f"set_pts_{c}"))
        markup.add(types.InlineKeyboardButton(get_trans(lang, 'back'), callback_data="menu_admin"))
        bot.edit_message_text("🔗 اختر الرابط لتعديل نقاطه:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif data.startswith("set_pts_"):
        cat_name = data.split("_")[2]
        msg = bot.send_message(call.message.chat.id, f"✍️ أرسل عدد النقاط الجديدة للرابط `{cat_name}` (مثال: 3 أو 4):")
        bot.register_next_step_handler(msg, lambda m: save_new_link_points(m, cat_name))
    elif data.startswith("view_comp_"):
        comp_id = data.split("_")[2]
        cursor.execute("SELECT text FROM competitions WHERE id = ?", (comp_id,))
        row = cursor.fetchone()
        comp_text = row[0] if row else "لا توجد تفاصيل."
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(get_trans(lang, 'back'), callback_data="menu_competitions"))
        bot.edit_message_text(f"🏆 **تفاصيل المسابقة #{comp_id}:**\n\n{comp_text}", call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif data.startswith("get_link_"):
        cat = data.split("_")[2]
        cursor.execute("SELECT id, url, code FROM links WHERE category = ? AND used = 0 ORDER BY RANDOM() LIMIT 1", (cat,))
        row = cursor.fetchone()
        if not row:
            cursor.execute("INSERT INTO links (category, url, code) VALUES (?, ?, ?)", (cat, "https://t.me/ONDRAY_FF", "ONDRAY2026"))
            conn.commit()
            cursor.execute("SELECT id, url, code FROM links WHERE category = ? AND used = 0 ORDER BY RANDOM() LIMIT 1", (cat,))
            row = cursor.fetchone()
        
        link_id, url, code = row[0], row[1], row[2]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔗 اضغط هنا للتوجه للرابط", url=url))
        markup.add(types.InlineKeyboardButton(get_trans(lang, 'back'), callback_data="menu_links"))
        
        bot.edit_message_text(
            f"🔗 **رابط التجميع ({cat}):**\n\n1️⃣ اضغط على الزر أدناه لتخطيه.\n2️⃣ بعد الحصول على الكود، أرسله هنا في الرشاش وسيتم إضافته لرصيدك فوراً!",
            call.message.chat.id, call.message.message_id,
            reply_markup=markup
        )
        msg = bot.send_message(call.message.chat.id, "✍️ أرسل كود التخطي هنا الآن:")
        bot.register_next_step_handler(msg, lambda m: verify_user_code(m, cat, link_id))
    elif data == "back_to_main":
        bot.answer_callback_query(call.id)
        cursor.execute("SELECT COUNT(*) FROM users_data")
        total_users = cursor.fetchone()[0]
        bot.edit_message_text(
            get_trans(lang, 'welcome').format(total_users=total_users),
            call.message.chat.id, call.message.message_id,
            reply_markup=get_main_menu_markup(lang)
        )

def admin_kick_process(message):
    try:
        target_id = int(message.text.strip())
        cursor.execute("DELETE FROM admins WHERE user_id = ?", (target_id,))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ تم طرد المساعد وحذف صلاحياته بنجاح (ID: {target_id}).")
    except ValueError:
        bot.send_message(message.chat.id, "❌ خطأ: يرجى إدخال آيدي صحيح بالأرقام.")

def admin_add_comp_process(message):
    comp_text = message.text.strip()
    cursor.execute("INSERT INTO competitions (text) VALUES (?)", (comp_text,))
    conn.commit()
    bot.send_message(message.chat.id, "✅ تم إضافة المسابقة بنجاح وأصبحت تظهر في قسم المسابقات اليومية!")

def save_new_link_points(message, category):
    try:
        pts = float(message.text.strip())
        cursor.execute("INSERT OR REPLACE INTO link_points (category, points) VALUES (?, ?)", (category, pts))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ تم تحديث نقاط الرابط `{category}` لتصبح `{pts}` نقطة بنجاح!")
    except ValueError:
        bot.send_message(message.chat.id, "❌ خطأ: يرجى إدخال رقم صحيح.")

def verify_user_code(message, category, link_id):
    user_id = message.from_user.id
    user_code = message.text.strip()
    
    cursor.execute("SELECT code FROM links WHERE id = ?", (link_id,))
    row = cursor.fetchone()
    
    if row and row[0] == user_code:
        cursor.execute("UPDATE links SET used = 1 WHERE id = ?", (link_id,))
        points_gain = get_link_points(category)
        cursor.execute("UPDATE users_data SET points_collected = points_collected + ? WHERE user_id = ?", (points_gain, user_id))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ **الكود صحيح!** تم إضافة {points_gain} نقطة إلى رصيدك بنجاح 🎉")
    else:
        bot.send_message(message.chat.id, "❌ **الكود خاطئ!** يرجى التأكد من إتمام الاختصار بشكل صحيح وإرسال الكود مجدداً.")

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.infinity_polling()

