# الجزء الأول: التهيئة، إعدادات اللغات، وقاعدة البيانات الأساسية
import os
import telebot
from telebot import types

TOKEN = "8765104365:AAGEZbHSJ1MMp26tIeyE0Dievbm9-lzgxjM"
bot = telebot.TeleBot(TOKEN)

# تخزين مؤقت لبيانات المستخدمين (اللغة، الحالات، إلخ)
user_data = {}
# تخزين لوحة المطورين والمساعدين المسموح لهم
developers = [1234567890]  # ضع آيدي المطور الأساسي هنا
assistants = []  # قائمة المساعدين

# تخزين المسابقات اليومية
daily_contests = []

# أسعار الجواهر (تم تخفيض الأسعار بنسبة 30%)
gem_prices = {
    "100_gems": 70,   # مثال بعد تخفيض 30%
    "500_gems": 350,
    "1000_gems": 700
}

# روابط التجميع (الـ 5 القديمة + الـ 5 الجديدة المطلوبة)
# كل رابط وعدد النقاط الخاص به (افتراضياً تبدأ بنقاط معينة قابلة للتعديل من لوحة المطور)
earning_links = {
    "cutw": {"name": "cutw", "points": 10},
    "clks": {"name": "clks", "points": 10},
    "earn": {"name": "earn", "points": 10},
    "pe": {"name": "pe", "points": 10},
    "adfl": {"name": "adfl", "points": 10},
    # الأزرار الجديدة المضافة:
    "زر1": {"name": "زر1", "points": 10},
    "زر2": {"name": "زر2", "points": 10},
    "زر3": {"name": "زر3", "points": 10},
    "زر4": {"name": "زر4", "points": 10},
    "زر5": {"name": "زر5", "points": 10}
}

# قواميس اللغات الشاملة لترجمة كل كلمة وحرف داخل البوت
TRANSLATIONS = {
    "ar": {
        "welcome": "أهلاً بك في بوت شحن وتجميع النقاط!",
        "main_menu": "القائمة الرئيسية:",
        "points_collection": "تجميع النقاط",
        "daily_contests": "المسابقات اليومية",
        "dev_panel": "لوحة المطور",
        "back": "رجوع",
        "invalid_code": "الكود خاطئ! حاول مجدداً.",
        "valid_code": "الكود صحيح! تم إضافة النقاط لرصيدك.",
        "enter_code_prompt": "الرجاء إرسال الكود لتحقيقه:",
        "lang_changed": "تم تغيير اللغة بنجاح إلى العربية.",
    },
    "es": {
        "welcome": "¡Bienvenido al bot de recarga y acumulación de puntos!",
        "main_menu": "Menú principal:",
        "points_collection": "Colección de puntos",
        "daily_contests": "Concursos diarios",
        "dev_panel": "Panel de desarrollador",
        "back": "Volver",
        "invalid_code": "¡Código incorrecto! Inténtalo de nuevo.",
        "valid_code": "¡Código correcto! Se han añadido los puntos a tu saldo.",
        "enter_code_prompt": "Por favor, envía el código para verificarlo:",
        "lang_changed": "Idioma cambiado con éxito al español.",
    }
    # يمكن إضافة لغات أخرى هنا مع ترجمة شاملة لكل حرف
}

def get_text(user_id, key):
    lang = user_data.get(user_id, {}).get("lang", "ar")
    return TRANSLATIONS.get(lang, TRANSLATIONS["ar"]).get(key, key)
# الجزء الثاني: نظام اللغة، الأزرار الأساسية، والتعامل مع أخطاء الأكواد
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"lang": "ar", "points": 0}
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton(get_text(user_id, "points_collection")),
        types.KeyboardButton(get_text(user_id, "daily_contests"))
    )
    if user_id in developers or user_id in assistants:
        markup.add(types.KeyboardButton(get_text(user_id, "dev_panel")))
    
    # زر تغيير اللغة
    markup.add(types.KeyboardButton("🌍 تغيير اللغة / Cambiar Idioma"))
    
    bot.send_message(message.chat.id, get_text(user_id, "welcome"), reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text in ["🌍 تغيير اللغة / Cambiar Idioma"])
def change_language_menu(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("العربية 🇩🇿", callback_data="lang_ar"),
        types.InlineKeyboardButton("Español 🇪🇸", callback_data="lang_es")
    )
    bot.send_message(message.chat.id, "اختر لغتك المفضلة / Elija su idioma preferido:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def set_language(call):
    user_id = call.from_user.id
    lang = call.data.split("_")[1]
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]["lang"] = lang
    
    bot.answer_callback_query(call.id, "Done")
    bot.send_message(call.message.chat.id, get_text(user_id, "lang_changed"))
    # تحديث القائمة الرئيسية بالكامل باللغة الجديدة المطلوبة
    send_welcome(call.message)
# الجزء الثالث: أزرار تجميع النقاط (الـ 10 أزرار)، تعديل النقاط، ولوحة المطور
@bot.message_handler(func=lambda msg: msg.text in ["تجميع النقاط", "Colección de puntos"])
def points_collection_menu(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # الأزرار الـ 10 (القديمة + الجديدة المطلوبة)
    links = ["cutw", "clks", "earn", "pe", "adfl", "زر1", "زر2", "زر3", "زر4", "زر5"]
    buttons = []
    for link in links:
        points_val = earning_links.get(link, {}).get("points", 10)
        buttons.append(types.InlineKeyboardButton(f"{link} ({points_val} نقاط)", callback_data=f"earn_{link}"))
    
    markup.add(*buttons)
    bot.send_message(message.chat.id, "اختر أحد روابط التجميع أدناه:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("earn_"))
def handle_earn_link(call):
    link_name = call.data.split("_")[1]
    user_id = call.from_user.id
    points_to_give = earning_links.get(link_name, {}).get("points", 10)
    
    # رسالة وهمية لطلب الكود بعد الاختصار
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, f"أكمل اختصار الرابط {link_name} ثم أرسل الكود هنا للتحقق وإضافة {points_to_give} نقاط.")
    # تخزين حالة المستخدم أنه ينتظر كود لهذا الرابط
    user_data[user_id]["waiting_for_code"] = link_name

@bot.message_handler(func=lambda msg: user_data.get(msg.from_user.id, {}).get("waiting_for_code"))
def verify_code(message):
    user_id = message.from_user.id
    entered_code = message.text.strip()
    link_name = user_data[user_id]["waiting_for_code"]
    
    # محاكاة التحقق من الكود (يمكنك ربطه بالكود الحقيقي للأكواد الصحيحة)
    correct_code = "1234"  # مثال على الكود الصحيح
    
    if entered_code == correct_code:
        points_to_add = earning_links.get(link_name, {}).get("points", 10)
        user_data[user_id]["points"] = user_data[user_id].get("points", 0) + points_to_add
        bot.send_message(message.chat.id, get_text(user_id, "valid_code") + f" (+{points_to_add} نقطة)")
        user_data[user_id].pop("waiting_for_code", None)
    else:
        bot.send_message(message.chat.id, get_text(user_id, "invalid_code"))
# الجزء الرابع: لوحة المطور (طرد المساعدين، إضافة المسابقات، وتعديل النقاط)
@bot.message_handler(func=lambda msg: msg.text in ["لوحة المطور", "Panel de desarrollador"])
def dev_panel_menu(message):
    user_id = message.from_user.id
    if user_id not in developers and user_id not in assistants:
        bot.send_message(message.chat.id, "عذراً، هذه اللوحة للمطورين والمساعدين فقط.")
        return
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("طرد مساعد"),
        types.KeyboardButton("إضافة مسابقة"),
        types.KeyboardButton("تعديل عدد نقاط كل رابط"),
        types.KeyboardButton("رجوع")
    )
    bot.send_message(message.chat.id, "مرحباً بك في لوحة المطور. اختر الإجراء المطلوب:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "طرد مساعد")
def kick_assistant_prompt(message):
    user_id = message.from_user.id
    if user_id not in developers:
        return
    msg = bot.send_message(message.chat.id, "أكتب الآيدي (ID) الشخص الذي تريد طرده من مساعدتك:")
    bot.register_next_step_handler(msg, process_kick_assistant)

def process_kick_assistant(message):
    try:
        target_id = int(message.text.strip())
        if target_id in assistants:
            assistants.remove(target_id)
            bot.send_message(message.chat.id, f"تم طرد المشرف أو المساعد ذو الآيدي {target_id} بنجاح.")
        else:
            bot.send_message(message.chat.id, "هذا الشخص ليس في قائمة المساعدين.")
    except ValueError:
        bot.send_message(message.chat.id, "الآيدي غير صحيح، يجب أن يكون أرقاماً.")

@bot.message_handler(func=lambda msg: msg.text == "إضافة مسابقة")
def add_contest_prompt(message):
    user_id = message.from_user.id
    if user_id not in developers and user_id not in assistants:
        return
    msg = bot.send_message(message.chat.id, "اكتب وصف هذه المسابقة:")
    bot.register_next_step_handler(msg, process_add_contest)

def process_add_contest(message):
    contest_text = message.text
    daily_contests.append(contest_text)
    bot.send_message(message.chat.id, "تمت إضافة المسابقة بنجاح ونقلها إلى زر المسابقات اليومية في القائمة الرئيسية.")

@bot.message_handler(func=lambda msg: msg.text == "تعديل عدد نقاط كل رابط")
def edit_link_points_prompt(message):
    user_id = message.from_user.id
    if user_id not in developers:
        return
    markup = types.InlineKeyboardMarkup(row_width=2)
    links = ["cutw", "clks", "earn", "pe", "adfl", "زر1", "زر2", "زر3", "زر4", "زر5"]
    buttons = [types.InlineKeyboardButton(link, callback_data=f"editpts_{link}") for link in links]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "اختر الرابط الذي تريد تعديل نقاطه:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("editpts_"))
def select_link_to_edit(call):
    link_name = call.data.split("_")[1]
    msg = bot.send_message(call.message.chat.id, f"اكتب عدد النقاط الجديدة التي تريد أن يعطيها الرابط {link_name}:")
    bot.register_next_step_handler(msg, lambda m: save_new_link_points(m, link_name))

def save_new_link_points(message, link_name):
    try:
        new_points = int(message.text.strip())
        if link_name in earning_links:
            earning_links[link_name]["points"] = new_points
            bot.send_message(message.chat.id, f"تم تحديث نقاط الرابط {link_name} لتصبح {new_points} نقطة بنجاح.")
        else:
            bot.send_message(message.chat.id, "حدث خطأ، الرابط غير موجود.")
    except ValueError:
        bot.send_message(message.chat.id, "الرجاء إدخال رقم صحيح لعدد النقاط.")

@bot.message_handler(func=lambda msg: msg.text in ["رجوع", "Volver"])
def back_to_main(message):
    send_welcome(message)

@bot.message_handler(func=lambda msg: msg.text in ["المسابقات اليومية"])
def show_daily_contests(message):
    user_id = message.from_user.id
    if not daily_contests:
        bot.send_message(message.chat.id, "لا توجد مسابقات يومية حالياً.")
        return
    contests_text = "🎉 **قائمة المسابقات اليومية:**\n\n" + "\n".join([f"- {c}" for c in daily_contests])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("رجوع"))
    bot.send_message(message.chat.id, contests_text, parse_mode="Markdown", reply_markup=markup)

# تشغيل البوت
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()

