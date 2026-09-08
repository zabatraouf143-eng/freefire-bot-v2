import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# توكن البوت
TOKEN = "7911762145:AAH6vj80YFf0u2M5bUqZq2k8W9x7Y6z5V4U"  # ضع توكنك هنا

# قواعد البيانات وإعدادات المطور
user_data_db = {}
ADMIN_USERNAME = "raouf100K"
ADMIN_ID = 8890160605  # ايدك الخاص لتأكيد الصلاحيات

# روابط الاشتراك الإجباري
REQUIRED_TELEGRAM_CHANNEL = "https://t.me/dray_ff_bot"  # قناة تليجرام
REQUIRED_YOUTUBE_CHANNEL = "https://youtube.com/@ON_DRAY"  # قناة يوتيوب

# قواميس اللغات (10 لغات متكاملة 100%)
LANGUAGES = {
    "ar": {
        "welcome": (
            "🔥 أهلاً بك يا بطل في بوت شحن جواهر فري فاير مجاناً!\n🆔 اختر من القائمة"
            " أدناه ما يناسبك لتجميع النقاط وشحن حسابك."
        ),
        "profile": "👤 معلومات الحساب:\n🆔 ايدي: {}\n💰 نقاطك: {} نقطة",
        "earn": (
            "🎁 طريقة الحصول على النقاط:\n\n1️⃣ الإحالة: شارك رابطك الخاص، وأي"
            " شخص ينضم عبرك ويجمع 40 نقطة، تحصل أنت فوراً على 25 نقطة!\n2️⃣"
            " شارك في المسابقة واربح نقاطاً!"
        ),
        "store": "🛒 قائمة المتجر وعروض الجواهر (تخفيض 30%):",
        "support": "📞 الدعم الفني: للإبلاغ عن مشكلة أو الاستفسار تواصل مع المطور.",
        "lang_select": "🌍 اختر لغتك المفضلة / Select your language:",
        "admin_panel": "🛠 لوحة التحكم الخاصة بالمطور:",
        "back": "⬅️ العودة للقائمة الرئيسية",
        "points": "نقاط",
        "sub_required": (
            "⚠️ عذراً يا بطل، يجب عليك الاشتراكات الإجبارية أولاً لتتمكن من استخدام"
            " البوت:"
        ),
        "sub_btn_tg": "📢 اشترك في قناة التليجرام",
        "sub_btn_yt": "📺 اشترك في قناة اليوتيوب",
        "check_sub": "✅ لقد اشتركت، تحقق من الاشتراك",
    },
    "en": {
        "welcome": (
            "🔥 Welcome hero to the free Free Fire diamonds bot!\n🆔 Choose"
            " from the menu below to collect points and top up your account."
        ),
        "profile": "👤 Account Info:\n🆔 ID: {}\n💰 Your Points: {} points",
        "earn": (
            "🎁 How to get points:\n\n1️⃣ Referral: Share your link, and anyone"
            " who joins through you collects 40 points, you get 25 points"
            " instantly!\n2️⃣ Participate in the competition and win points!"
        ),
        "store": "🛒 Store & Diamond Offers (30% OFF):",
        "support": (
            "📞 Technical Support: Contact the developer for any issues."
        ),
        "lang_select": "🌍 Select your language:",
        "admin_panel": "🛠 Developer Control Panel:",
        "back": "⬅️ Back to Main Menu",
        "points": "points",
        "sub_required": (
            "⚠️ Sorry hero, you must complete the mandatory subscriptions first"
            " to use the bot:"
        ),
        "sub_btn_tg": "📢 Subscribe to Telegram Channel",
        "sub_btn_yt": "📺 Subscribe to YouTube Channel",
        "check_sub": "✅ I Have Subscribed, Check",
    },
    "fr": {
        "welcome": (
            "🔥 Bienvenue héros sur le bot de recharge de diamants Free Fire"
            " gratuit !\n🆔 Choisissez dans le menu ci-dessous pour"
            " accumuler des points."
        ),
        "profile": "👤 Infos du compte:\n🆔 ID: {}\n💰 Vos points: {} points",
        "earn": (
            "🎁 Comment gagner des points:\n\n1️⃣ Parrainage: Partagez votre lien,"
            " toute personne qui rejoint et accumule 40 points vous rapporte"
            " 25 points !\n2️⃣ Participez au concours et gagnez des points !"
        ),
        "store": "🛒 Boutique et Offres de Diamants (-30%):",
        "support": "📞 Support Technique: Contactez le développeur.",
        "lang_select": "🌍 Choisissez votre langue:",
        "admin_panel": "🛠 Panneau de contrôle du développeur:",
        "back": "⬅️ Retour au menu principal",
        "points": "points",
        "sub_required": (
            "⚠️ Désolé héros, vous devez d'abord vous abonner pour utiliser le"
            " bot :"
        ),
        "sub_btn_tg": "📢 S'abonner au canal Telegram",
        "sub_btn_yt": "📺 S'abonner à la chaîne YouTube",
        "check_sub": "✅ Je me suis abonné, vérifier",
    },
    "es": {
        "welcome": (
            "🔥 ¡Bienvenido héroe al bot de diamantes gratis de Free Fire!\n🆔"
            " Elige del menú para acumular puntos."
        ),
        "profile": "👤 Info de Cuenta:\n🆔 ID: {}\n💰 Tus Puntos: {} puntos",
        "earn": (
            "🎁 Cómo ganar puntos:\n\n1️⃣ Referidos: ¡Comparte tu enlace y gana"
            " puntos!\n2️⃣ ¡Participa en el concurso y gana puntos!"
        ),
        "store": "🛒 Tienda y Ofertas de Diamantes:",
        "support": "📞 Soporte Técnico:",
        "lang_select": "🌍 Selecciona tu idioma:",
        "admin_panel": "🛠 Panel de Control:",
        "back": "⬅️ Volver al Menú Principal",
        "points": "puntos",
        "sub_required": "⚠️ Debes suscribirte primero:",
        "sub_btn_tg": "📢 Suscribirse a Telegram",
        "sub_btn_yt": "📺 Suscribirse a YouTube",
        "check_sub": "✅ Ya me suscribí",
    },
    "de": {
        "welcome": (
            "🔥 Willkommen Held beim kostenlosen Free Fire Diamanten Bot!\n🆔"
            " Wähle aus dem Menü."
        ),
        "profile": (
            "👤 Kontoinformationen:\n🆔 ID: {}\n💰 Deine Punkte: {} Punkte"
        ),
        "earn": (
            "🎁 Wie man Punkte bekommt:\n\n1️⃣ Empfehlung: Teile deinen"
            " Link!\n2️⃣ Nimm am Wettbewerb teil und gewinne Punkte!"
        ),
        "store": "🛒 Shop & Diamanten Angebote:",
        "support": "📞 Technischer Support:",
        "lang_select": "🌍 Sprache wählen:",
        "admin_panel": "🛠 Entwickler-Steuerpult:",
        "back": "⬅️ Zurück zum Hauptmenü",
        "points": "Punkte",
        "sub_required": "⚠️ Bitte abonnieren:",
        "sub_btn_tg": "📢 Telegram abonnieren",
        "sub_btn_yt": "📺 YouTube abonnieren",
        "check_sub": "✅ Überprüfen",
    },
    "tr": {
        "welcome": (
            "🔥 Free Fire ücretsiz elmas botuna hoş geldin kahraman!\n🆔 Puan"
            " toplamak için menüden seç."
        ),
        "profile": "👤 Hesap Bilgileri:\n🆔 ID: {}\n💰 Puanların: {} puan",
        "earn": (
            "🎁 Puan kazanma yolları:\n\n1️⃣ Davet: Bağlantını paylaş!\n2️⃣"
            " Yarışmaya katıl ve puan kazan!"
        ),
        "store": "🛒 Mağaza ve Elmas Teklifleri:",
        "support": "📞 Teknik Destek:",
        "lang_select": "🌍 Dil Seçin:",
        "admin_panel": "🛠 Geliştirici Paneli:",
        "back": "⬅️ Ana Menüye Dön",
        "points": "puan",
        "sub_required": "⚠️ Önce abone olmalısın:",
        "sub_btn_tg": "📢 Telegram'a Abone Ol",
        "sub_btn_yt": "📺 YouTube'a Abone Ol",
        "check_sub": "✅ Abone Oldum",
    },
    "it": {
        "welcome": (
            "🔥 Benvenuto eroe nel bot di diamanti Free Fire gratuiti!\n🆔"
            " Scegli dal menu."
        ),
        "profile": "👤 Info Account:\n🆔 ID: {}\n💰 I tuoi punti: {} punti",
        "earn": (
            "🎁 Come ottenere punti:\n\n1️⃣ Invito: Condividi il tuo link!\n2️⃣"
            " Partecipa al concorso e vinci punti!"
        ),
        "store": "🛒 Negozio e Offerte di Diamanti:",
        "support": "📞 Supporto Tecnico:",
        "lang_select": "🌍 Seleziona la lingua:",
        "admin_panel": "🛠 Pannello di Controllo:",
        "back": "⬅️ Torna al Menu Principale",
        "points": "punti",
        "sub_required": "⚠️ Devi iscriverti prima:",
        "sub_btn_tg": "📢 Iscriviti a Telegram",
        "sub_btn_yt": "📺 Iscriviti a YouTube",
        "check_sub": "✅ Ho effettuato l'iscrizione",
    },
    "ru": {
        "welcome": (
            "🔥 Добро пожаловать, герой, в бот бесплатных алмазов Free Fire!\n🆔"
            " Выберите в меню."
        ),
        "profile": "👤 Информация об аккаунте:\n🆔 ID: {}\n💰 Ваши очки: {} очков",
        "earn": (
            "🎁 Как получить очки:\n\n1️⃣ Рефералы: Поделитесь ссылкой!\n2️⃣"
            " Участвуйте в конкурсе и выигрывайте очки!"
        ),
        "store": "🛒 Магазин и предложения алмазов:",
        "support": "📞 Техническая поддержка:",
        "lang_select": "🌍 Выберите язык:",
        "admin_panel": "🛠 Панель разработчика:",
        "back": "⬅️ Главное меню",
        "points": "очков",
        "sub_required": "⚠️ Подпишитесь на каналы:",
        "sub_btn_tg": "📢 Канал Telegram",
        "sub_btn_yt": "📺 Канал YouTube",
        "check_sub": "✅ Проверить подписку",
    },
    "pt": {
        "welcome": (
            "🔥 Bem-vindo herói ao bot de diamantes Free Fire grátis!\n🆔 Escolha"
            " no menu."
        ),
        "profile": "👤 Informações da Conta:\n🆔 ID: {}\n💰 Seus pontos: {} pontos",
        "earn": (
            "🎁 Como ganhar pontos:\n\n1️⃣ Indicação: Compartilhe seu link!\n2️⃣"
            " Participe do concurso e ganhe pontos!"
        ),
        "store": "🛒 Loja e Ofertas de Diamantes:",
        "support": "📞 Suporte Técnico:",
        "lang_select": "🌍 Selecione seu idioma:",
        "admin_panel": "🛠 Painel de Controle:",
        "back": "⬅️ Voltar ao Menu Principal",
        "points": "pontos",
        "sub_required": "⚠️ Você precisa se inscrever primeiro:",
        "sub_btn_tg": "📢 Inscrever-se no Telegram",
        "sub_btn_yt": "📺 Inscrever-se no YouTube",
        "check_sub": "✅ Verificar inscrição",
    },
    "zh": {
        "welcome": (
            "🔥 欢迎英雄来到免费 Free Fire 钻石机器人！\n🆔 从下方菜单中选择以收集积分。"
        ),
        "profile": "👤 账户信息:\n🆔 ID: {}\n💰 你的积分: {} 积分",
        "earn": (
            "🎁 如何获得积分:\n\n1️⃣ 邀请好友: 分享您的链接！\n2️⃣ 参与比赛并赢取积分！"
        ),
        "store": "🛒 商店与钻石优惠:",
        "support": "📞 技术支持:",
        "lang_select": "🌍 选择语言:",
        "admin_panel": "🛠 开发者面板:",
        "back": "⬅️ 返回主菜单",
        "points": "积分",
        "sub_required": "⚠️ 请先完成订阅：",
        "sub_btn_tg": "📢 订阅电报频道",
        "sub_btn_yt": "📺 订阅YouTube频道",
        "check_sub": "✅ 我已订阅",
    },
}
# دوال المساعدة للغة والتحقق من المطور
def get_user_lang(user_id):
    if user_id not in user_data_db:
        user_data_db[user_id] = {
            "lang": "ar",
            "points": 0.0,
            "invited_count": 0,
        }
    return user_data_db[user_id]["lang"]


def is_admin(user):
    # التحقق التلقائي إذا كان المستخدم هو المطور رؤوف عبر الـ Username أو الـ ID
    return (user.username and user.username.lower() == ADMIN_USERNAME.lower()) or (
        user.id == ADMIN_ID
    )


# فحص الاشتراك الإجباري في قنوات تليجرام ويوتيوب
async def check_subscription(user_id, context: ContextTypes.DEFAULT_TYPE):
    # ملاحظة: لتأكيد الاشتراك الفعلي في تليجرام يتم استدعاء get_chat_member
    # هنا نقوم بالتحقق الافتراضي أو السماح للمطور بالدور مباشرة
    if user_id == ADMIN_ID:
        return True

    # إذا كان المستخدم مسجل مسبقاً أنه اشترك
    if user_data_db.get(user_id, {}).get("subscribed", False):
        return True

    return False


async def show_subscription_required(update: Update, context: ContextTypes.DEFAULT_TYPE, lang="ar"):
    t = LANGUAGES[lang]
    keyboard = [
        [
            InlineKeyboardButton(
                t["sub_btn_tg"], url=REQUIRED_TELEGRAM_CHANNEL
            )
        ],
        [
            InlineKeyboardButton(
                t["sub_btn_yt"], url=REQUIRED_YOUTUBE_CHANNEL
            )
        ],
        [
            InlineKeyboardButton(
                t["check_sub"], callback_data="verify_subscription"
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.message.edit_text(
            t["sub_required"], reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            t["sub_required"], reply_markup=reply_markup
        )
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if user_id not in user_data_db:
        user_data_db[user_id] = {
            "lang": "ar",
            "points": 0.0,
            "invited_count": 0,
            "subscribed": False,
        }

    # معالجة نظام الإحالة عبر رابط البوت (إذا دخل شخص عن طريق رابط شخص آخر)
    args = context.args
    if args and len(args) > 0:
        try:
            referrer_id = int(args[0])
            if referrer_id != user_id and referrer_id in user_data_db:
                user_data_db[user_id]["referred_by"] = referrer_id
        except ValueError:
            pass

    lang = user_data_db[user_id]["lang"]
    t = LANGUAGES[lang]

    # التحقق من الاشتراك الإجباري أولاً (إلا إذا كان المطور)
    if not await check_subscription(user_id, context):
        await show_subscription_required(update, context, lang)
        return

    admin_check = is_admin(user)

    keyboard = [
        [
            InlineKeyboardButton(
                "👤 الملف الشخصي", callback_data="profile"
            )
        ],
        [
            InlineKeyboardButton(
                "🔗 تجميع النقاط (روابط)", callback_data="earn_points"
            )
        ],
        [InlineKeyboardButton("💎 متجر فري فاير", callback_data="store")],
        [InlineKeyboardButton("ℹ️ طريقة جمع النقاط", callback_data="how_earn")],
        [InlineKeyboardButton("📞 الدعم الفني", callback_data="support")],
        [InlineKeyboardButton("🌍 تغيير اللغة", callback_data="change_lang")],
    ]

    if admin_check:
        keyboard.append(
            [InlineKeyboardButton("🛠 لوحة التحكم", callback_data="admin_panel")]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(t["welcome"], reply_markup=reply_markup)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    user_id = user.id

    if user_id not in user_data_db:
        user_data_db[user_id] = {
            "lang": "ar",
            "points": 0.0,
            "invited_count": 0,
            "subscribed": False,
        }

    data = query.data
    lang = user_data_db[user_id]["lang"]
    t = LANGUAGES[lang]

    if data == "verify_subscription":
        # محاكاة تأكيد الاشتراك
        user_data_db[user_id]["subscribed"] = True
        await query.message.edit_text(
            "✅ تم التحقق من اشتراكك بنجاح! أهلاً بك.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            t["back"], callback_data="main_menu"
                        )
                    ]
                ]
            ),
        )

    elif data == "profile":
        points = user_data_db[user_id]["points"]
        text = t["profile"].format(user_id, points)
        keyboard = [
            [InlineKeyboardButton(t["back"], callback_data="main_menu")]
        ]
        await query.message.edit_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "how_earn":
        text = t["earn"]
        keyboard = [
            [InlineKeyboardButton(t["back"], callback_data="main_menu")]
        ]
        await query.message.edit_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "store":
        text = f"{t['store']}\n\n💎 770 نقطة = 110 جوهرة\n💎 2150 نقطة = 220 جوهرة\n💎 3100 نقطة = 330 جوهرة\n💎 5050 نقطة = 570 جوهرة"
        keyboard = [
            [InlineKeyboardButton(t["back"], callback_data="main_menu")]
        ]
        await query.message.edit_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "earn_points":
        bot_username = context.bot.username
        referral_link = f"https://t.me/{bot_username}?start={user_id}"
        invited = user_data_db[user_id]["invited_count"]
        text = (
            f"🔗 شارك رابط الإحالة الخاص بك:\n{referral_link}\n\n📊 أي شخص"
            f" ينضم عبر رابطك ويجمع 40 نقطة، تحصل أنت على 25 نقطة!\n👥 عدد"
            f" الأشخاص الذين دعيتهم: {invited}"
        )
        keyboard = [
            [InlineKeyboardButton(t["back"], callback_data="main_menu")]
        ]
        await query.message.edit_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "change_lang":
        keyboard = [
            [
                InlineKeyboardButton("العربية 🇸🇦", callback_data="lang_ar"),
                InlineKeyboardButton("English 🇬🇧", callback_data="lang_en"),
            ],
            [
                InlineKeyboardButton("Français 🇫🇷", callback_data="lang_fr"),
                InlineKeyboardButton("Español 🇪🇸", callback_data="lang_es"),
            ],
            [
                InlineKeyboardButton("Deutsch 🇩🇪", callback_data="lang_de"),
                InlineKeyboardButton("Türkçe 🇹🇷", callback_data="lang_tr"),
            ],
            [
                InlineKeyboardButton("Italiano 🇮🇹", callback_data="lang_it"),
                InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru"),
            ],
            [
                InlineKeyboardButton("Português 🇵🇹", callback_data="lang_pt"),
                InlineKeyboardButton("中文 🇨🇳", callback_data="lang_zh"),
            ],
            [InlineKeyboardButton(t["back"], callback_data="main_menu")],
        ]
        await query.message.edit_text(
            t["lang_select"], reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("lang_"):
        chosen_lang = data.split("_")[1]
        user_data_db[user_id]["lang"] = chosen_lang
        new_t = LANGUAGES[chosen_lang]
        await query.message.edit_text(
            f"✅ {new_t['welcome']}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            new_t["back"], callback_data="main_menu"
                        )
                    ]
                ]
            ),
        )

    elif data == "admin_panel":
        if is_admin(user):
            await query.message.edit_text(
                "🛠 مرحباً بك يا مطورنا رؤوف في لوحة التحكم الخاصة بالبوت.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                t["back"], callback_data="main_menu"
                            )
                        ]
                    ]
                ),
            )
        else:
            await query.answer("عذراً، هذه اللوحة للمطور فقط!", show_alert=True)

    elif data == "main_menu":
        new_lang = get_user_lang(user_id)
        new_t = LANGUAGES[new_lang]
        admin_check = is_admin(user)

        keyboard = [
            [
                InlineKeyboardButton(
                    "👤 الملف الشخصي", callback_data="profile"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔗 تجميع النقاط (روابط)", callback_data="earn_points"
                )
            ],
            [InlineKeyboardButton("💎 متجر فري فاير", callback_data="store")],
            [
                InlineKeyboardButton(
                    "ℹ️ طريقة جمع النقاط", callback_data="how_earn"
                )
            ],
            [InlineKeyboardButton("📞 الدعم الفني", callback_data="support")],
            [InlineKeyboardButton("🌍 تغيير اللغة", callback_data="change_lang")],
        ]
        if admin_check:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        "🛠 لوحة التحكم", callback_data="admin_panel"
                    )
                ]
            )

        await query.message.edit_text(
            new_t["welcome"], reply_markup=InlineKeyboardMarkup(keyboard)
        )


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 البوت يعمل الآن بنجاح...")
    app.run_polling()
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 البوت يعمل الآن بنجاح...")
    app.run_polling()

if __name__ == "__main__":
    main()

