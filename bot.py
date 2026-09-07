import os
import threading
import time
import sqlite3
from flask import Flask
import telebot
from telebot import types

app = Flask(__name__)

@app.route('/')
def home():
    return "Free Fire Bot is alive and running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

TOKEN = "8765104365:AAGEZbHSJ1MMp26tIeyE0Dievbm9-lzgxjM"
DEV_USERNAME = "raouf100K"

REQUIRED_CHANNEL_URL = "https://t.me/ONDRAY_FF"
REQUIRED_YT_URL = "https://youtube.com/@dray-xit?si=mV4JOtKwFFIZ1mND"

bot = telebot.TeleBot(TOKEN)

def clear_webhook_and_pending():
    try:
        bot.remove_webhook()
        time.sleep(1)
    except Exception:
        pass

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
    sub_clicks INTEGER DEFAULT 0
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
CREATE TABLE IF NOT EXISTS daily_competitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS category_points (
    category TEXT PRIMARY KEY,
    points REAL
)
""")
conn.commit()

default_points_map = {
    "short": 2.0, "shirink": 2.0, "link": 2.0, "ex": 1.5, "Oo": 1.0,
    "cutw": 10.0, "clks": 10.0, "earn": 10.0, "pe": 10.0, "adfl": 10.0
}
for cat, pts in default_points_map.items():
    cursor.execute("INSERT OR IGNORE INTO category_points (category, points) VALUES (?, ?)", (cat, pts))
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
        "btn_daily_comp": "المسابقات اليومية 🏆",
        "profile": "👤 **معلومات حسابك:**\n\n🆔 الآيدي: `{user_id}`\n💎 النقاط المجمعة: `{collected}` نقطة",
        "ref": "👥 **نظام الإحالة:**\n\nشارك رابط الإحالة الخاص بك:\n`{ref_link}`\n\nأي شخص يدخل عبر رابطك ويجمع 35 نقطة، ستحصل أنت على **20 نقطة** مجاناً!\n📊 عدد الأشخاص الذين دعيتهم: {refs}",
        "support": "📞 للدعم تواصل مع المطور حصرياً عبر:\n@{DEV_USERNAME}",
        "back": "العودة للقائمة الرئيسية 🔙",
        "sub_required": "🚨 **يرجى الاشتراك في القنوات للاستمرار:**\n\n📢 قناة التليغرام:\n{ch_url}\n\n📺 قناة اليوتيوب:\n{yt_url}\n\nبعد الاشتراك، اضغط على زر التحقق 👇",
        "sub_check_btn": "✅ تمت الاشتراك",
        "not_subscribed_yet": "❌ عذراً، يبدو أنك لم تشترك بعد! يرجى الاشتراك في القنوات ثم إعادة الضغط على الزر للمتابعة."
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
        "btn_daily_comp": "Daily Competitions 🏆",
        "profile": "👤 **Account Info:**\n\n🆔 ID: `{user_id}`\n💎 Points: `{collected}`",
        "ref": "👥 **Referral System:**\n\nYour link:\n`{ref_link}`\n\nGet **20 points** when your referral reaches 35 points!\n📊 Invited: {refs}",
        "support": "📞 Support: @{DEV_USERNAME}",
        "back": "Back 🔙",
        "sub_required": "🚨 **Please subscribe to the channels:**\n\n📢 Telegram:\n{ch_url}\n\n📺 YouTube:\n{yt_url}\n\nClick below 👇",
        "sub_check_btn": "✅ Subscribed",
        "not_subscribed_yet": "❌ You haven't subscribed yet! Please subscribe and try again."
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
        "btn_daily_comp": "Compétitions Quotidiennes 🏆",
        "profile": "👤 **Compte :**\n\n🆔 ID : `{user_id}`\n💎 Points : `{collected}`",
        "ref": "👥 **Parrainage :**\n\nLien :\n`{ref_link}`\n\nGagnez **20 points** quand votre filleul atteint 35 points!\n📊 Parrainés : {refs}",
        "support": "📞 Support : @{DEV_USERNAME}",
        "back": "Retour 🔙",
        "sub_required": "🚨 **Veuillez vous abonner aux chaînes:**\n\n📢 Telegram:\n{ch_url}\n\n📺 YouTube:\n{yt_url}\n\nCliquez ci-dessous 👇",
        "sub_check_btn": "✅ Abonné",
        "not_subscribed_yet": "❌ Vous n'êtes pas encore abonné !"
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
        "btn_daily_comp": "Competencias diarias 🏆",
        "profile": "👤 **Información de cuenta:**\n\n🆔 ID: `{user_id}`\n💎 Puntos: `{collected}`",
        "ref": "👥 **Sistema de referidos:**\n\nTu enlace:\n`{ref_link}`\n\n¡Gana **20 puntos** cuando tu referido alcance 35 puntos!\n📊 Invitados: {refs}",
        "support": "📞 Soporte: @{DEV_USERNAME}",
        "back": "Volver 🔙",
        "sub_required": "🚨 **Suscríbete a los canales:**\n\n📢 Telegram:\n{ch_url}\n\n📺 YouTube:\n{yt_url}\n\nHaz clic abajo 👇",
        "sub_check_btn": "✅ Suscrito",
        "not_subscribed_yet": "❌ ¡Aún no te has suscripto!"
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
        "btn_daily_comp": "Tägliche Wettbewerbe 🏆",
        "profile": "👤 **Kontoinformationen:**\n\n🆔 ID: `{user_id}`\n💎 Punkte: `{collected}`",
        "ref": "👥 **Empfehlungssystem:**\n\nIhr Link:\n`{ref_link}`\n\nErhalten Sie **20 Punkte**, wenn Ihre Empfehlung 35 Punkte erreicht!\n📊 Eingeladen: {refs}",
        "support": "📞 Support: @{DEV_USERNAME}",
        "back": "Zurück 🔙",
        "sub_required": "🚨 **Bitte abonnieren Sie die Kanäle:**\n\n📢 Telegram:\n{ch_url}\n\n📺 YouTube:\n{yt_url}\n\nKlicken Sie unten 👇",
        "sub_check_btn": "✅ Abonniert",
        "not_subscribed_yet": "❌ Sie haben noch nicht abonniert!"
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
        "btn_daily_comp": "Günlük Yarışmalar 🏆",
        "profile": "👤 **Hesap Bilgileri:**\n\n🆔 ID: `{user_id}`\n💎 Puanlar: `{collected}`",
        "ref": "👥 **Referans Sistemi:**\n\nBağlantınız:\n`{ref_link}`\n\nReferansınız 35 puana ulaştığında **20 puan** kazanın!\n📊 Davet edilen: {refs}",
        "support": "📞 Destek: @{DEV_USERNAME}",
        "back": "Geri 🔙",
        "sub_required": "🚨 **Kanallara abone olun:**\n\n📢 Telegram:\n{ch_url}\n\n📺 YouTube:\n{yt_url}\n\nAşağıya tıklayın 👇",
        "sub_check_btn": "✅ Abone Oldum",
        "not_subscribed_yet": "❌ Henüz abone olmadınız!"
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
        "btn_daily_comp": "Competições Diárias 🏆",
        "profile": "👤 **Informações da Conta:**\n\n🆔 ID: `{user_id}`\n💎 Pontos: `{collected}`",
        "ref": "👥 **Sistema de Indicação:**\n\nSeu link:\n`{ref_link}`\n\nGanhe **20 pontos** quando sua indicação atingir 35 pontos!\n📊 Convidados: {refs}",
        "support": "📞 Suporte: @{DEV_USERNAME}",
        "back": "Voltar 🔙",
        "sub_required": "🚨 **Inscreva-se nos canais:**\n\n📢 Telegram:\n{ch_url}\n\n📺 YouTube:\n{yt_url}\n\nClique abaixo 👇",
        "sub_check_btn": "✅ Inscrito",
        "not_subscribed_yet": "❌ Você ainda não se inscreveu!"
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

print("Part 1 Updated successfully.")

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
        types.InlineKeyboardButton(get_trans(lang, 'btn_daily_comp'), callback_data="menu_daily_comp"),
        types.InlineKeyboardButton(get_trans(lang, 'btn_support'), callback_data="menu_support"),
        types.InlineKeyboardButton(get_trans(lang, 'btn_lang'), callback_data="menu_lang"),
        types.InlineKeyboardButton(get_trans(lang, 'btn_admin'), callback_data="menu_admin")
    )
    return markup

@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    args = message.text.split()

    cursor.execute("SELECT user_id, language, sub_clicks FROM users_data WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        referrer = None
        if len(args) > 1 and args[1].isdigit():
            ref_id = int(args[1])
            if ref_id != user_id:
                referrer = ref_id
        cursor.execute("INSERT INTO users_data (user_id, username, referrer, language, sub_clicks) VALUES (?, ?, ?, 'ar', 0)", (user_id, username, referrer))
        conn.commit()
        lang = "ar"
        sub_clicks = 0
    else:
        lang = user[1] or "ar"
        sub_clicks = user[2] or 0

    # رسالة طلب الاشتراك الإجباري التكراري (أول مرة تطلعلو بلي مازلت ماشتركتش، والمرة الثانية تفتح البوت)
    if sub_clicks < 1:
        sub_text = get_trans(lang, "sub_required").format(ch_url=REQUIRED_CHANNEL_URL, yt_url=REQUIRED_YT_URL)
        markup_sub = types.InlineKeyboardMarkup(row_width=1)
        markup_sub.add(types.InlineKeyboardButton(get_trans(lang, "sub_check_btn"), callback_data="check_subscription_step"))
        bot.send_message(message.chat.id, sub_text, parse_mode="Markdown", reply_markup=markup_sub)
        return

    cursor.execute("SELECT COUNT(*) FROM users_data")
    total_users = cursor.fetchone()[0]
    welcome_text = translations[lang]["welcome"].format(total_users=total_users)
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu_markup(lang))

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    username = call.from_user.username or ""
    data = call.data
    lang = get_user_lang(user_id)
    back_text = get_trans(lang, "back")

    if data == "check_subscription_step":
        cursor.execute("SELECT sub_clicks FROM users_data WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        clicks = row[0] if row else 0

        if clicks == 0:
            # أول ضغطة: نقولو بلي مزالك ماشتركتش (تكرار تحذيري)
            cursor.execute("UPDATE users_data SET sub_clicks = 1 WHERE user_id = ?", (user_id,))
            conn.commit()
            bot.answer_callback_query(call.id, get_trans(lang, "not_subscribed_yet"), show_alert=True)
            return
        else:
            # ثاني ضغطة: يفتح البوت عادي
            cursor.execute("UPDATE users_data SET sub_clicks = 2 WHERE user_id = ?", (user_id,))
            conn.commit()
            bot.answer_callback_query(call.id, "✅ تم التحقق، أهلاً بك في البوت!")
            cursor.execute("SELECT COUNT(*) FROM users_data")
            total_users = cursor.fetchone()[0]
            welcome_text = translations[lang]["welcome"].format(total_users=total_users)
            bot.send_message(call.message.chat.id, welcome_text, reply_markup=get_main_menu_markup(lang))
            return

    if data == "menu_lang":
        markup_lang = types.InlineKeyboardMarkup(row_width=2)
        markup_lang.add(
            types.InlineKeyboardButton("العربية 🇸🇦", callback_data="setlang_ar"),
            types.InlineKeyboardButton("English 🇺🇸", callback_data="setlang_en"),
            types.InlineKeyboardButton("Français 🇫🇷", callback_data="setlang_fr"),
            types.InlineKeyboardButton("Español 🇪🇸", callback_data="setlang_es"),
            types.InlineKeyboardButton("Deutsch 🇩🇪", callback_data="setlang_de"),
            types.InlineKeyboardButton("Türkçe 🇹🇷", callback_data="setlang_tr"),
            types.InlineKeyboardButton("Português 🇧🇷", callback_data="setlang_br"),
            types.InlineKeyboardButton(back_text, callback_data="back_home")
        )
        bot.send_message(call.message.chat.id, "🌐 اختر لغتك المفضلة / Choose your language:", reply_markup=markup_lang)

    elif data.startswith("setlang_"):
        new_lang = data.split("_")[1]
        cursor.execute("UPDATE users_data SET language = ? WHERE user_id = ?", (new_lang, user_id))
        conn.commit()
        bot.answer_callback_query(call.id, "✅ تم تغيير اللغة بنجاح!")
        
        cursor.execute("SELECT COUNT(*) FROM users_data")
        total_users = cursor.fetchone()[0]
        welcome_text = translations[new_lang]["welcome"].format(total_users=total_users)
        bot.send_message(call.message.chat.id, welcome_text, reply_markup=get_main_menu_markup(new_lang))

    elif data == "menu_profile":
        cursor.execute("SELECT points_collected FROM users_data WHERE user_id = ?", (user_id,))
        res = cursor.fetchone()
        collected = res[0] if res else 0
        msg = get_trans(lang, "profile").format(user_id=user_id, collected=collected)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(back_text, callback_data="back_home"))
        bot.send_message(call.message.chat.id, msg, parse_mode="Markdown", reply_markup=markup)

    elif data == "menu_ref":
        bot_info = bot.get_me()
        ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
        cursor.execute("SELECT COUNT(*) FROM users_data WHERE referrer = ?", (user_id,))
        refs = cursor.fetchone()[0]
        msg = get_trans(lang, "ref").format(ref_link=ref_link, refs=refs)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(back_text, callback_data="back_home"))
        bot.send_message(call.message.chat.id, msg, parse_mode="Markdown", reply_markup=markup)

    elif data == "get_points_info":
        info_text = (
            "🎁 **طريقة الحصول على النقاط:**\n\n"
            "1️⃣ **الإحالة:** شارك رابطك الخاص، وأي شخص ينضم عبرك ويجمع 35 نقطة، تحصل أنت فوراً على **20 نقطة**!\n"
            "2️⃣ **تجميع الروابط:** اختصر الروابط، حمل الملفات وادخل الأكواد لتحصل على النقاط فوراً."
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(back_text, callback_data="back_home"))
        bot.send_message(call.message.chat.id, info_text, parse_mode="Markdown", reply_markup=markup)

    elif data == "menu_support":
        msg = get_trans(lang, "support").format(DEV_USERNAME=DEV_USERNAME)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(back_text, callback_data="back_home"))
        bot.send_message(call.message.chat.id, msg, reply_markup=markup)

    elif data == "menu_ff":
        # تخفيض أسعار الجواهر بنسبة 30% كما طلبت
        markup_ff = types.InlineKeyboardMarkup(row_width=1)
        markup_ff.add(
            types.InlineKeyboardButton("770 نقطة = 110 جوهرة 💎", callback_data="buy_1"),
            types.InlineKeyboardButton("1505 نقطة = 220 جوهرة 💎", callback_data="buy_2"),
            types.InlineKeyboardButton("2170 نقطة = 330 جوهرة 💎", callback_data="buy_3"),
            types.InlineKeyboardButton("3535 نقطة = 570 جوهرة 💎", callback_data="buy_4"),
            types.InlineKeyboardButton(back_text, callback_data="back_home"),
        )
        bot.send_message(call.message.chat.id, "🛒 **قائمة المتجر وعروض الجواهر (بأسعار مخفضة 30%):**", parse_mode="Markdown", reply_markup=markup_ff)

    elif data == "back_home":
        cursor.execute("SELECT COUNT(*) FROM users_data")
        total_users = cursor.fetchone()[0]
        welcome_text = translations[lang]["welcome"].format(total_users=total_users)
        bot.send_message(call.message.chat.id, welcome_text, reply_markup=get_main_menu_markup(lang))

print("Part 2 loaded successfully.")

    elif data == "menu_links":
        markup_links = types.InlineKeyboardMarkup(row_width=1)
        # الروابط القديمة والجديدة التي طلبتها بالترتيب والأسماء بالضبط
        markup_links.add(
            types.InlineKeyboardButton("🔗 short [2 نقاط]", callback_data="cat_short"),
            types.InlineKeyboardButton("🔗 shirink [2 نقاط]", callback_data="cat_shirink"),
            types.InlineKeyboardButton("🔗 link [2 نقاط]", callback_data="cat_link"),
            types.InlineKeyboardButton("🔗 ex [1.5 نقاط]", callback_data="cat_ex"),
            types.InlineKeyboardButton("🔗 Oo [1 نقطة]", callback_data="cat_Oo"),
            types.InlineKeyboardButton("🔗 cutw", callback_data="cat_cutw"),
            types.InlineKeyboardButton("🔗 clks", callback_data="cat_clks"),
            types.InlineKeyboardButton("🔗 earn", callback_data="cat_earn"),
            types.InlineKeyboardButton("🔗 pe", callback_data="cat_pe"),
            types.InlineKeyboardButton("🔗 adfl", callback_data="cat_adfl"),
            types.InlineKeyboardButton(back_text, callback_data="back_home"),
        )
        bot.send_message(call.message.chat.id, "اختر منصة التخطي لتجميع النقاط:", reply_markup=markup_links)

    elif data.startswith("cat_"):
        category = data.split("_", 1)[1]
        cooldown_time = 28800 if category in ["link", "Oo"] else 86400
        
        cursor.execute("SELECT last_action_time FROM user_category_cooldowns WHERE user_id = ? AND category = ?", (user_id, category))
        cd_row = cursor.fetchone()
        
        if cd_row:
            last_time = cd_row[0]
            current_time = time.time()
            if current_time - last_time < cooldown_time:
                remaining_hours = int((cooldown_time - (current_time - last_time)) / 3600)
                remaining_minutes = int(((cooldown_time - (current_time - last_time)) % 3600) / 60)
                bot.answer_callback_query(call.id, f"⚠️ لقد قمت بالتخطي من هذه الخانة مسبقاً. عد بعد {remaining_hours} ساعة و {remaining_minutes} دقيقة.", show_alert=True)
                return

        cursor.execute("SELECT id, url FROM links WHERE category = ? AND used = 0 ORDER BY RANDOM() LIMIT 1", (category,))
        link_row = cursor.fetchone()

        if not link_row:
            bot.answer_callback_query(call.id, "عذراً، لا توجد روابط متاحة حالياً في هذه الخانة!", show_alert=True)
            return

        link_id, url = link_row
        msg = bot.send_message(call.message.chat.id, f"🔗 رابط التخطي لـ ({category}):\n{url}\n\nبعد إتمام التخطي، أرسل الكود هنا في رسالة:")
        bot.register_next_step_handler(msg, verify_link_code, category, link_id)

    elif data == "adm_edit_cat_points":
        # زر تعديل عدد نقاط كل رابط من لوحة المطور
        markup_pts = types.InlineKeyboardMarkup(row_width=1)
        all_cats = ["short", "shirink", "link", "ex", "Oo", "cutw", "clks", "earn", "pe", "adfl"]
        for cat in all_cats:
            cursor.execute("SELECT points FROM category_points WHERE category = ?", (cat,))
            p_row = cursor.fetchone()
            p_val = p_row[0] if p_row else 1.0
            markup_pts.add(types.InlineKeyboardButton(f"تعديل نقاط: {cat} (الحالي: {p_val})", callback_data=f"setpts_{cat}"))
        markup_pts.add(types.InlineKeyboardButton(back_text, callback_data="menu_admin"))
        bot.send_message(call.message.chat.id, "اختر الرابط الذي تريد تعديل عدد نقاطه:", reply_markup=markup_pts)

    elif data.startswith("setpts_"):
        target_cat = data.split("_", 1)[1]
        msg = bot.send_message(call.message.chat.id, f"أدخل عدد النقاط الجديدة للخانة `{target_cat}` (مثال: 3 أو 4):", parse_mode="Markdown")
        bot.register_next_step_handler(msg, admin_save_category_points, target_cat)

def admin_save_category_points(message, category):
    try:
        new_pts = float(message.text.strip())
        cursor.execute("INSERT OR REPLACE INTO category_points (category, points) VALUES (?, ?)", (category, new_pts))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ تم تحديث نقاط الخانة `{category}` إلى `{new_pts}` نقطة بنجاح.", parse_mode="Markdown")
    except ValueError:
        bot.send_message(message.chat.id, "❌ خطأ: يرجى إدخال رقم صحيح أو عشري صحيح.")

def verify_link_code(message, category, link_id):
    if message.text and message.text.startswith("/"):
        return
    user_id = message.from_user.id
    entered_code = message.text.strip()
    lang = get_user_lang(user_id)

    temp_conn = sqlite3.connect("bot_database.db", check_same_thread=False)
    temp_cursor = temp_conn.cursor()

    temp_cursor.execute("SELECT code, used FROM links WHERE id = ?", (link_id,))
    row = temp_cursor.fetchone()
    if not row or row[1] == 1:
        temp_conn.close()
        bot.send_message(message.chat.id, "❌ عذراً، هذا الرابط تم استخدامه من قبل أو أصبح تالفاً. اطلب رابطاً جديداً.", reply_markup=get_main_menu_markup(lang))
        return

    correct_code, used = row

    if entered_code == correct_code:
        # جلب عدد النقاط المخصص لهذه الفئة من قاعدة البيانات
        temp_cursor.execute("SELECT points FROM category_points WHERE category = ?", (category,))
        p_row = temp_cursor.fetchone()
        points = p_row[0] if p_row else 2.0
        
        temp_cursor.execute("UPDATE links SET used = 1 WHERE id = ?", (link_id,))
        temp_cursor.execute("UPDATE users_data SET points_collected = points_collected + ? WHERE user_id = ?", (points, user_id))
        
        current_time = time.time()
        temp_cursor.execute("""
            INSERT INTO user_category_cooldowns (user_id, category, last_action_time) 
            VALUES (?, ?, ?) 
            ON CONFLICT(user_id, category) DO UPDATE SET last_action_time = ?
        """, (user_id, category, current_time, current_time))
        
        temp_cursor.execute("SELECT points_collected, referrer, ref_rewarded FROM users_data WHERE user_id = ?", (user_id,))
        u_info = temp_cursor.fetchone()
        if u_info:
            collected_pts = u_info[0]
            referrer_id = u_info[1]
            ref_rewarded = u_info[2]
            
            if referrer_id and ref_rewarded == 0 and collected_pts >= 35:
                temp_cursor.execute("UPDATE users_data SET points_collected = points_collected + 20 WHERE user_id = ?", (referrer_id,))
                temp_cursor.execute("UPDATE users_data SET ref_rewarded = 1 WHERE user_id = ?", (user_id,))
                try:
                    bot.send_message(referrer_id, "🎉 مبروك! لقد وصل الشخص الذي دعوته إلى 35 نقطة، وتمت إضافة **20 نقطة** إلى رصيدك بنجاح.")
                except:
                    pass

        temp_conn.commit()
        temp_conn.close()
        
        cursor.execute("SELECT COUNT(*) FROM users_data")
        total_users = cursor.fetchone()[0]
        welcome_text = translations[lang]["welcome"].format(total_users=total_users)
        bot.send_message(message.chat.id, f"🎉 تم التحقق بنجاح! تمت إضافة {points} نقطة إلى رصيدك.", reply_markup=get_main_menu_markup(lang))
    else:
        temp_conn.close()
        # رد واضح ومؤكد للمستخدم بأن الكود خاطئ ولم يتم إضافة النقاط
        bot.send_message(message.chat.id, "❌ الكود خاطئ! لم يتم إضافة أي نقاط، يرجى التأكد من الكود وإعادة المحاولة.", reply_markup=get_main_menu_markup(lang))

print("Part 3 loaded successfully.")
    elif data == "menu_daily_comp":
        # زر المسابقات اليومية في الصفحة الرئيسية لعرض آخر مسابقة أضافها المطور
        cursor.execute("SELECT description FROM daily_competitions ORDER BY id DESC LIMIT 1")
        comp_row = cursor.fetchone()
        comp_text = comp_row[0] if comp_row else "🏆 لا توجد مسابقات نشطة حالياً، ترقبونا قريباً!"
        
        markup_comp = types.InlineKeyboardMarkup()
        markup_comp.add(types.InlineKeyboardButton(back_text, callback_data="back_home"))
        bot.send_message(call.message.chat.id, f"🏆 **المسابقات اليومية والفعاليات:**\n\n{comp_text}", parse_mode="Markdown", reply_markup=markup_comp)

    elif data == "adm_kick_admin":
        # زر طرد مساعد من لوحة التحكم
        if username.lower() == DEV_USERNAME.lower():
            msg = bot.send_message(call.message.chat.id, "أدخل ايدي (ID) الشخص الذي تريد طرده من قائمة المساعدين:")
            bot.register_next_step_handler(msg, admin_kick_admin_process)
        else:
            bot.answer_callback_query(call.id, "هذه الخانة مخصصة للمطور الأساسي فقط ❌", show_alert=True)

    elif data == "adm_add_competition":
        # زر إضافة مسابقة جديدة من لوحة المطور
        if username.lower() == DEV_USERNAME.lower():
            msg = bot.send_message(call.message.chat.id, "أكتب وصف المسابقة أو التفاصيل التي تريد نشرها في زر المسابقات اليومية:")
            bot.register_next_step_handler(msg, admin_save_competition_process)
        else:
            bot.answer_callback_query(call.id, "هذه الخانة مخصصة للمطور الأساسي فقط ❌", show_alert=True)

def admin_kick_admin_process(message):
    try:
        kick_id = int(message.text.strip())
        cursor.execute("DELETE FROM admins WHERE user_id = ?", (kick_id,))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ تم طرد المساعد ذو الآيدي ({kick_id}) بنجاح وأصبح غير قادر على الدخول للوحة التحكم.")
    except ValueError:
        bot.send_message(message.chat.id, "❌ خطأ: يرجى إدخال ايدي (ID) صحيح يتكون من أرقام فقط.")

def admin_save_competition_process(message):
    comp_desc = message.text.strip()
    cursor.execute("INSERT INTO daily_competitions (description) VALUES (?)", (comp_desc,))
    conn.commit()
    bot.send_message(message.chat.id, "✅ تم إضافة المسابقة بنجاح، وظهرت الآن في زر 'المسابقات اليومية' في القائمة الرئيسية.")

    elif data == "adm_addlink":
        msg = bot.send_message(call.message.chat.id, "أدخل بيانات الرابط بهذا الشكل:\nالخانة | الرابط | الكود\n\nمثال:\nshort | https://example.com | ABC123")
        bot.register_next_step_handler(msg, admin_add_link_process)

    elif data.startswith("adm_deduct_") or data.startswith("adm_add_"):
        action, target_id = data.split("_")[1], data.split("_")[2]
        msg = bot.send_message(call.message.chat.id, f"أدخل عدد النقاط المراد {'خصمها' if action == 'deduct' else 'إضافتها'}:")
        bot.register_next_step_handler(msg, admin_modify_points_process, action, target_id)

def admin_add_admin_process(message):
    try:
        new_admin_id = int(message.text.strip())
        cursor.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (new_admin_id,))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ تم إضافة هذا المستخدم ({new_admin_id}) لمساعدتك بنجاح.")
    except ValueError:
        bot.send_message(message.chat.id, "❌ خطأ: يرجى إدخال ايدي (ID) صحيح يتكون من أرقام فقط.")

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
            f"✅ تم العثور على المستخدم:\n🆔 ايدي: `{user[0]}`\n📊 مجموع النقاط: {user[1]}",
            parse_mode="Markdown",
            reply_markup=markup
        )
    except ValueError:
        bot.send_message(message.chat.id, "❌ خطأ: يجب إدخال ايدي (ID) صحيح يتكون من أرقام فقط.")

def admin_modify_points_process(message, action, target_id):
    try:
        amount = float(message.text.strip())
        target_id = int(target_id)
        if action == "deduct":
            cursor.execute("UPDATE users_data SET points_collected = MAX(0, points_collected - ?) WHERE user_id = ?", (amount, target_id))
            msg_text = f"✅ تم خصم {amount} نقطة بنجاح من مجموع النقاط."
        else:
            cursor.execute("UPDATE users_data SET points_collected = points_collected + ? WHERE user_id = ?", (amount, target_id))
            msg_text = f"✅ تم إضافة {amount} نقطة بنجاح إلى مجموع النقاط."
        conn.commit()
        bot.send_message(message.chat.id, msg_text)
    except ValueError:
        bot.send_message(message.chat.id, "❌ خطأ: يرجى إدخال رقم صحيح أو عشري صحيح.")

def admin_add_link_process(message):
    try:
        parts = message.text.split("|")
        if len(parts) < 3:
            bot.send_message(message.chat.id, "الصيغة خاطئة. تأكد من استخدام الفاصلة |")
            return
        category = parts[0].strip()
        url = parts[1].strip()
        code = parts[2].strip()

        cursor.execute("INSERT INTO links (category, url, code, used) VALUES (?, ?, ?, 0)", (category, url, code))
        conn.commit()
        bot.send_message(message.chat.id, "تمت إضافة الرابط والكود بنجاح ✅")
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ: {str(e)}")

if __name__ == "__main__":
    t = threading.Thread(target=run_web)
    t.start()
    
    clear_webhook_and_pending()
    
    print("Bot is starting polling with all updates...")
    bot.infinity_polling(skip_pending=True)

