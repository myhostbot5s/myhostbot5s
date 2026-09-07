import telebot
from telebot import types
TOKEN = '8969891927:AAGoW1SB2zYa_b3-p8emG5yShKI846cYE10'
ADMIN_ID = 8664763495
CHANNEL_USERNAME = '@YOUR_CHANNEL'

bot = telebot.TeleBot(TOKEN)

def check_sub(user_id):
    if not CHANNEL_USERNAME or CHANNEL_USERNAME == '@YOUR_CHANNEL':
        return True
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
    except:
        pass
    return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if not check_sub(user_id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("اشترك في القناة 📢", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")
        btn2 = types.InlineKeyboardButton("تحقق من الاشتراك ✅", callback_data="check_sub")
        markup.add(btn)
        markup.add(btn2)
        bot.reply_to(message, "عليك الاشتراك في قناة البوت أولاً لتتمكن من استخدامه ⚠️", reply_markup=markup)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('قسم الخدمات 🛍️'), types.KeyboardButton('حسابي 👤'))
    if user_id == ADMIN_ID:
        markup.add(types.KeyboardButton('لوحة التحكم ⚙️'))
        
    bot.reply_to(message, "أهلاً بك في بوت الخدمات والاشتراكات! اختر ما يناسبك:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    
    if message.text == 'قسم الخدمات 🛍️':
        bot.reply_to(message, "قسم الخدمات والمنتجات المتاحة حالياً:\n- تفليش حسابات\n- رشق متابعين\n- تفعيل تليجرام بريميم")
    
    elif message.text == 'حسابي 👤':
        bot.reply_to(message, f"معلومات حسابك:\n- الأيدي: `{user_id}`\n- الحالة: مفعل ✅", parse_mode="Markdown")
        
    elif message.text == 'لوحة التحكم ⚙️' and user_id == ADMIN_ID:
        bot.reply_to(message, "أهلاً بك يا مطورنا في لوحة التحكم الخاصة بالبوت 🛠️")

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_query(call):
    if check_sub(call.from_user.id):
        bot.answer_callback_query(call.id, "شكراً لاشتراكك! تم تفعيل البوت ✅")
        bot.send_message(call.message.chat.id, "أهلاً بك مرة أخرى، أرسل /start للبدء.")
    else:
        bot.answer_callback_query(call.id, "لم تقم بالاشتراك بعد! ❌", show_alert=True)

bot.infinity_polling()
