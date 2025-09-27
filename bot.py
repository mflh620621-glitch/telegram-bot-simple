import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv('BOT_TOKEN')
subscribers = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in subscribers:
        subscribers.append(user_id)
    await update.message.reply_text('✅ تم الاشتراك! استخدم /broadcast للإرسال الجماعي.')

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('📝 اكتب: /broadcast رسالتك هنا')
        return
    
    message = ' '.join(context.args)
    for user_id in subscribers:
        try:
            await context.bot.send_message(user_id,
