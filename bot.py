from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

# القراءة من المتغيرات البيئية (آمن)
TOKEN = os.getenv('BOT_TOKEN')  # ← تغيير هنا
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))  # ← تغيير هنا

USERS_FILE = "users.txt"

def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            pass
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(str(user_id) + "\n")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)
    await update.message.reply_text("👋 تم الاشتراك في البوت بنجاح!")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 هذا الأمر مخصص فقط للمدير.")
        return

    if not update.message.text.startswith('/broadcast'):
        return

    message_text = update.message.text.replace('/broadcast', '').strip()
    
    if not message_text:
        await update.message.reply_text("📝 اكتب: /broadcast رسالتك")
        return

    with open(USERS_FILE, "r") as f:
        user_ids = f.read().splitlines()

    for uid in user_ids:
        try:
            msg = await context.bot.send_message(chat_id=int(uid), text=message_text)
            try:
                await context.bot.pin_chat_message(chat_id=int(uid), message_id=msg.message_id)
            except:
                pass
        except Exception as e:
            print(f"❌ فشل الإرسال إلى {uid}: {e}")

    await update.message.reply_text(f"✅ تم الإرسال إلى {len(user_ids)} مشترك")

# تحقق من وجود التوكن
if not TOKEN:
    print("❌ BOT_TOKEN غير موجود في المتغيرات البيئية")
else:
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast))
    print("📢 البوت يعمل...")
    app.run_polling()
