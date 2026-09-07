import telebot
from telebot import types
import sqlite3
import threading
import time
from flask import Flask

# التوكن الأصلي الخاص بك
TOKEN = "8765104365:AAGEZbHSJ1MMp26tIeyE0Dievbm9-lzgxjM"
bot = telebot.TeleBot(TOKEN)
DEV_USERNAME = "raouf100"

# إعداد قاعدة البيانات وجداولها الأساسية
conn = sqlite3.connect("bot_database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users_data (
    user_id INTEGER PRIMARY KEY,
    points_collected REAL DEFAULT 0,
    referrer INTEGER,
    ref_rewarded INTEGER DEFAULT 0,
    language TEXT DEFAULT 'ar'
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
    PRIMARY KEY(user_id, category)
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

# نظام الترجمات الشامل
translations = {
    "ar": {
        "welcome": "🔥 مرحباً بك في بوت شحن فري فاير!\n\n👥 عدد المستخدمين الكلي: {total_users}\nاستخدم القائمة أدناه للبدء:",
        "btn_profile": "الملف الشخصي 👤",
        "btn_links": "تجميع النقاط 🔗",
        "btn_ref": "رابط الإحالة 👥",
        "btn_points_info": "طرق كسب النقاط ℹ️",
        "btn_store": "المتجر 🛒",
        "btn_support": "الدعم 📞",
        "btn_admin": "لوحة المطور ⚙️",
        "btn_lang": "تغيير اللغة 🌐",
        "btn_daily_comp": "المسابقات اليومية 🏆",
        "profile": "👤 **معلومات الحساب:**\n🆔 ايدي: `{user_id}`\n💰 رصيدك: {points} نقطة",
        "ref": "👥 **نظام الإحالة:**\nشارك رابطك مع أصدقائك لكسب النقاط:\n`{ref_link}`",
        "support": "📞 للدعم والتواصل، يراسل المطور عبر: @{DEV_USERNAME}",
        "back": "رجوع 🔙",
        "sub_required": "⚠️ **يرجى الاشتراكات في القنوات أولاً:**\n📢 Telegram: [قناتنا](https://t.me/your_channel)",
        "sub_check_btn": "✅ لقد اشتركت",
        "not_subscribed__yet": "❌ عذراً، لم تقم بالاشتراك في القنوات بعد!"
    },
    "en": {
        "welcome": "🔥 Welcome to Free Fire Top-up Bot!\n\n👥 Total Users: {total_users}\nUse the menu below to start:",
        "btn_profile": "Profile 👤",
        "btn_links": "Collect Points 🔗",
        "btn_ref": "Referral Link 👥",
        "btn_points_info": "How to Earn ℹ️",
        "btn_store": "Store 🛒",
        "btn_support": "Support 📞",
        "btn_admin": "Admin ⚙️",
        "btn_lang": "Change Language 🌐",
        "btn_daily_comp": "Daily Competitions 🏆",
        "profile": "👤 **Account Info:**\n🆔 ID: `{user_id}`\n💰 Balance: {points} pts",
        "ref": "👥 **Referral System:**\nShare your link:\n`{ref_link}`",
        "support": "📞 Support: @{DEV_USERNAME}",
        "back": "Back 🔙",
        "sub_required": "⚠️ **Please subscribe to channels first:**\n📢 Telegram",
        "sub_check_btn": "✅ Subscribed",
        "not_subscribed__yet": "❌ You haven't subscribed yet!"
    }
}

def get_trans(lang="ar", key=""):
    lang_dict = translations.get(lang, translations["ar"])
    return lang_dict.get(key, translations["ar"].get(key, key))

def get_user_lang(user_id):
    cursor.execute("SELECT language FROM users_data WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row and row[0]:
        return row[0]
    return "ar"

print("Part 1 loaded successfully.")
def get_main_menu_markup(lang="ar"):
    cursor.execute("SELECT COUNT(*) FROM users_data")
    total_users = cursor.fetchone()[0]
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_profile = types.InlineKeyboardButton(get_trans(lang, "btn_profile"), callback_data="menu_profile")
    btn_links = types.InlineKeyboardButton(get_trans(lang, "btn_links"), callback_data="menu_links")
    btn_ref = types.InlineKeyboardButton(get_trans(lang, "btn_ref"), callback_data="menu_ref")
    btn_points = types.InlineKeyboardButton(get_trans(lang, "btn_points_info"), callback_data="menu_points_info")
    btn_store = types.InlineKeyboardButton(get_trans(lang, "btn_store"), callback_data="menu_store")
    btn_support = types.InlineKeyboardButton(get_trans(lang, "btn_support"), callback_data="menu_support")
    btn_admin = types.InlineKeyboardButton(get_trans(lang, "btn_admin"), callback_data="menu_admin")
    btn_lang = types.InlineKeyboardButton(get_trans(lang, "btn_lang"), callback_data="menu_lang")
    btn_daily = types.InlineKeyboardButton(get_trans(lang, "btn_daily_comp"), callback_data="menu_daily_comp")
    
    markup.add(btn_profile, btn_links)
    markup.add(btn_ref, btn_points)
    markup.add(btn_store, btn_support)
    markup.add(btn_daily, btn_lang)
    markup.add(btn_admin)
    return markup

def get_store_markup(lang="ar"):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # أسعار الجواهر مخفضة بـ 30%
    markup.add(
        types.InlineKeyboardButton("💎 110 جواهر - 35 نقطة (تخفيض 30%)", callback_data="store_110"),
        types.InlineKeyboardButton("💎 341 جوهرة - 100 نقطة (تخفيض 30%)", callback_data="store_341"),
        types.InlineKeyboardButton("💎 720 جوهرة - 200 نقطة (تخفيض 30%)", callback_data="store_720"),
        types.InlineKeyboardButton(get_trans(lang, "back"), callback_data="main_menu")
    )
    return markup

def get_lang_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🇩🇿 العربية", callback_data="set_lang_ar"),
        types.InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en"),
        types.InlineKeyboardButton("🇪🇸 Español", callback_data="set_lang_es"),
        types.InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")
    )
    return markup

print("Part 2 loaded successfully.")
def get_links_markup(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    categories = [
        ("🔗 رابط 1 (cutw)", "cat_cutw"),
        ("🔗 رابط 2 (clks)", "cat_clks"),
        ("🔗 رابط 3 (earn)", "cat_earn"),
        ("🔗 رابط 4 (pe)", "cat_pe"),
        ("🔗 رابط 5 (adfl)", "cat_adfl"),
        ("🔗 رابط 6 (cat6)", "cat_6"),
        ("🔗 رابط 7 (cat7)", "cat_7"),
        ("🔗 رابط 8 (cat8)", "cat_8"),
        ("🔗 رابط 9 (cat9)", "cat_9"),
        ("🔗 رابط 10 (cat10)", "cat_10")
    ]
    for text, cat in categories:
        markup.add(types.InlineKeyboardButton(text, callback_data=cat))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="main_menu"))
    return markup

def handle_link_click(call, category):
    user_id = call.from_user.id
    current_time = time.time()
    
    # التحقق من وقت الانتظار (Cooldown)
    cursor.execute("SELECT last_action_time FROM user_category_cooldowns WHERE user_id = ? AND category = ?", (user_id, category))
    row = cursor.fetchone()
    
    if row and (current_time - row[0] < 3600): # ساعة انتظار مثلاً
        remaining = int(3600 - (current_time - row[0]))
        bot.answer_callback_query(call.id, f"⚠️ انتظر {remaining//60} دقيقة قبل تجميع هذا الرابط مجدداً.", show_alert=True)
        return

    # جلب النقاط الخاصة بهذا الرابط
    temp_cursor = conn.cursor()
    temp_cursor.execute("SELECT points FROM category_points WHERE category = ?", (category,))
    p_row = temp_cursor.fetchone()
    points = p_row[0] if p_row else 2.0

    # جلب رابط عشوائي من الفئة
    temp_cursor.execute("SELECT id, url, code FROM links WHERE category = ? AND used = 0 ORDER BY RANDOM() LIMIT 1", (category,))
    link_row = temp_cursor.fetchone()
    
    if not link_row:
        bot.answer_callback_query(call.id, "❌ عذراً، لا توجد روابط متاحة حالياً في هذه الفئة.", show_alert=True)
        return

    link_id, url, code = link_row
    bot.answer_callback_query(call.id, "✅ تم جلب الرابط بنجاح! يرجى إدخال الكود لتأكيد النقاط.")
    
    # إرسال الرابط للمستخدم وطلب إدخال الكود
    msg = bot.send_message(call.message.chat.id, f"🔗 **رابط التجميع:** {url}\n\nأرسل الكود الموجود في الرابط هنا لتأكيد نقاطك:")
    bot.register_next_step_handler(msg, verify_link_code_step, category, code, points, link_id)

def verify_link_code_step(message, category, correct_code, points, link_id):
    user_id = message.from_user.id
    user_code = message.text.strip()
    
    if user_code == correct_code:
        cursor.execute("UPDATE links SET used = 1 WHERE id = ?", (link_id,))
        cursor.execute("UPDATE users_data SET points_collected = points_collected + ? WHERE user_id = ?", (points, user_id))
        
        # تحديث وقت الانتظار
        cursor.execute("""
            INSERT INTO user_category_cooldowns (user_id, category, last_action_time)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, category) DO UPDATE SET last_action_time = ?
        """, (user_id, category, time.time(), time.time()))
        conn.commit()
        
        bot.send_message(message.chat.id, f"✅ مبروك! تمت إضافة {points} نقطة بنجاح إلى رصيدك.")
    else:
        bot.send_message(message.chat.id, "❌ الكود غير صحيح! حاول مجدداً بالضغط على الرابط.")

print("Part 3 loaded successfully.")
def get_admin_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🚫 طرد مساعد", callback_data="adm_kick_admin"),
        types.InlineKeyboardButton("🏆 إضافة مسابقة", callback_data="adm_add_competition"),
        types.InlineKeyboardButton("⚙️ تعديل عدد نقاط كل رابط", callback_data="adm_edit_cat_points"),
        types.InlineKeyboardButton("➕ إضافة رابط جديد", callback_data="adm_addlink"),
        types.InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    args = message.text.split()
    referrer = None
    if len(args) > 1:
        try:
            referrer = int(args[1])
        except ValueError:
            pass

    cursor.execute("SELECT user_id, points_collected, referrer, ref_rewarded FROM users_data WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        cursor.execute("INSERT INTO users_data (user_id, referrer) VALUES (?, ?)", (user_id, referrer))
        conn.commit()
        if referrer and referrer != user_id:
            cursor.execute("SELECT referrer, ref_rewarded FROM users_data WHERE user_id = ?", (referrer,))
            ref_info = cursor.fetchone()
            if ref_info:
                cursor.execute("UPDATE users_data SET points_collected = points_collected + 5 WHERE user_id = ?", (referrer,))
                cursor.execute("UPDATE users_data SET ref_rewarded = 1 WHERE user_id = ?", (user_id,))
                conn.commit()
                try:
                    bot.send_message(referrer, "🎉 مبروك! لقد حصلت على 5 نقاط بسبب إحالة صديق جديد.")
                except:
                    pass

    lang = get_user_lang(user_id)
    cursor.execute("SELECT COUNT(*) FROM users_data")
    total_users = cursor.fetchone()[0]
    welcome_text = get_trans(lang, "welcome").format(total_users=total_users)
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu_markup(lang), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    username = call.from_user.username or ""
    lang = get_user_lang(user_id)
    data = call.data

    if data == "main_menu":
        cursor.execute("SELECT COUNT(*) FROM users_data")
        total_users = cursor.fetchone()[0]
        welcome_text = get_trans(lang, "welcome").format(total_users=total_users)
        bot.edit_message_text(welcome_text, call.message.chat.id, call.message.message_id, reply_markup=get_main_menu_markup(lang), parse_mode="Markdown")

    elif data == "menu_profile":
        cursor.execute("SELECT points_collected FROM users_data WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        points = row[0] if row else 0
        profile_text = get_trans(lang, "profile").format(user_id=user_id, points=points)
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(get_trans(lang, "back"), callback_data="main_menu"))
        bot.edit_message_text(profile_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif data == "menu_links":
        bot.edit_message_text("🔗 اختر الفئة لتجميع النقاط:", call.message.chat.id, call.message.message_id, reply_markup=get_links_markup(user_id))

    elif data.startswith("cat_"):
        handle_link_click(call, data)

    elif data == "menu_store":
        bot.edit_message_text("🛒 اختر الباقة المناسبة للشحن (تخفيض 30%):", call.message.chat.id, call.message.message_id, reply_markup=get_store_markup(lang))

    elif data == "menu_ref":
        ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        ref_text = get_trans(lang, "ref").format(ref_link=ref_link)
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(get_trans(lang, "back"), callback_data="main_menu"))
        bot.edit_message_text(ref_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif data == "menu_points_info":
        info_text = "ℹ️ **كيف تكسب النقاط؟**\n\n1️⃣ ادخل إلى قسم تجميع النقاط.\n2️⃣ اضغط على الروابط واجلب الأكواد.\n3️⃣ شارك رابط الإحالة مع أصدقائك."
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(get_trans(lang, "back"), callback_data="main_menu"))
        bot.edit_message_text(info_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif data == "menu_support":
        support_text = get_trans(lang, "support").format(DEV_USERNAME=DEV_USERNAME)
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(get_trans(lang, "back"), callback_data="main_menu"))
        bot.edit_message_text(support_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif data == "menu_lang":
        bot.edit_message_text("🌐 اختر لغتك المفضلة / Choose your language:", call.message.chat.id, call.message.message_id, reply_markup=get_lang_markup())

    elif data.startswith("set_lang_l"):
        new_lang = data.split("_")[-1]
        cursor.execute("UPDATE users_data SET language = ? WHERE user_id = ?", (new_lang, user_id))
        conn.commit()
        bot.answer_callback_query(call.id, "✅ تم تغيير اللغة بنجاح!")
        callback_handler(call) # تحديث القائمة فوراً

    elif data == "menu_admin":
        if username.lower() == DEV_USERNAME.lower():
            bot.edit_message_text("⚙️ **أهلاً بك يا مطور في لوحة التحكم:**", call.message.chat.id, call.message.message_id, reply_markup=get_admin_markup(), parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ عذراً، هذه القائمة خاصة بالمطور فقط!", show_alert=True)

    elif data == "adm_kick_admin":
        if username.lower() == DEV_USERNAME.lower():
            msg = bot.send_message(call.message.chat.id, "🆔 أرسل ايدي (ID) المساعد المراد طرده:")
            bot.register_next_step_handler(msg, admin_kick_process)
        else:
            bot.answer_callback_query(call.id, "❌ أمر غير مسموح!", show_alert=True)

    elif data == "adm_add_competition":
        if username.lower() == DEV_USERNAME.lower():
            msg = bot.send_message(call.message.chat.id, "🏆 أرسل وصف المسابقة الجديدة ليتم حفظها ونشرها:")
            bot.register_next_step_handler(msg, admin_save_competition_process)
        else:
            bot.answer_callback_query(call.id, "❌ أمر غير مسموح!", show_alert=True)

    elif data == "menu_daily_comp":
        cursor.execute("SELECT description FROM daily_competitions ORDER BY id DESC LIMIT 1")
        comp_row = cursor.fetchone()
        comp_text = comp_row[0] if comp_row else "🏆 لا توجد مسابقات نشطة حالياً، تابعنا لاحقاً!"
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(get_trans(lang, "back"), callback_data="main_menu"))
        bot.edit_message_text(f"🏆 **المسابقة اليومية:**\n\n{comp_text}", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

def admin_kick_process(message):
    try:
        kick_id = int(message.text.strip())
        cursor.execute("DELETE FROM admins WHERE user_id = ?", (kick_id,))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ تم طرد المساعد صاحب الايدي: {kick_id} بنجاح.")
    except ValueError:
        bot.send_message(message.chat.id, "❌ ايدي غير صحيح! أرسل رقماً صالحاً.")

def admin_save_competition_process(message):
    comp_desc = message.text.strip()
    cursor.execute("INSERT INTO daily_competition (description) VALUES (?)", (comp_desc,))
    conn.commit()
    bot.send_message(message.chat.id, "✅ تم حفظ ونشر المسابقة اليومية بنجاح!")

# تشغيل سيرفر فايرل للخادم السحابي
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = threading.Thread(target=run_web)
    t.start()
    
    print("Bot is starting polling with all updates...")
    bot.infinity_polling(skip_pending=True)

