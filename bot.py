import random
from collections import defaultdict
import yt_dlp

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "
8568170013:AAG4fesWoTT-IC8UNHN7TaMkRu2OxO66DvQ"

user_games = {}
leaderboard = defaultdict(int)

menu = ReplyKeyboardMarkup(
    [["🎮 لعبة", "✊✋✌️"], ["📥 تحميل", "🏆 نقاط", "🥇 ليدر بورد"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحبا! اختار من القائمة 👇", reply_markup=menu)

def download_video(url):
    ydl_opts = {"outtmpl": "video.mp4", "format": "mp4"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_chat.id

    # 🎮 لعبة رقم
    if text == "🎮 لعبة":
        user_games[user_id] = random.randint(1, 5)
        await update.message.reply_text("🎲 خمن رقم من 1 إلى 5")

    elif user_id in user_games and text.isdigit():
        guess = int(text)
        if guess == user_games[user_id]:
            await update.message.reply_text("🎉 صح!")
            leaderboard[user_id] += 1
            del user_games[user_id]
        else:
            await update.message.reply_text("❌ خطأ")

    # ✊✋✌️
    elif text == "✊✋✌️":
        await update.message.reply_text("اكتب: rock / paper / scissors")

    elif text in ["rock", "paper", "scissors"]:
        bot = random.choice(["rock", "paper", "scissors"])

        if text == bot:
            result = "تعادل 🤝"
        elif (text == "rock" and bot == "scissors") or \
             (text == "paper" and bot == "rock") or \
             (text == "scissors" and bot == "paper"):
            result = "ربحت 🎉"
            leaderboard[user_id] += 1
        else:
            result = "خسرت 😅"

        await update.message.reply_text(f"البوت اختار: {bot}\n{result}")

    # 📥 تحميل
    elif text == "📥 تحميل":
        await update.message.reply_text("📎 ابعت رابط YouTube / TikTok / Instagram")

    elif any(x in text.lower() for x in ["youtube", "tiktok", "instagram"]):
        await update.message.reply_text("⏳ جاري التحميل...")

        try:
            download_video(text)
            await update.message.reply_video(video=open("video.mp4", "rb"))
        except:
            await update.message.reply_text("❌ ما قدرش يحمل الفيديو")

    # 🏆 نقاط
    elif text == "🏆 نقاط":
        await update.message.reply_text(f"🏆 نقاطك: {leaderboard[user_id]}")

    # 🥇 ليدر بورد
    elif text == "🥇 ليدر بورد":
        if not leaderboard:
            await update.message.reply_text("ما كاش لاعبين 😅")
        else:
            top = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)[:5]
            msg = "🏆 أفضل اللاعبين:\n\n"
            for i, (u, s) in enumerate(top, 1):
                msg += f"{i}. {u} - {s}\n"
            await update.message.reply_text(msg)

    else:
        await update.message.reply_text("استعمل الأزرار 👇")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot is running...")
app.run_polling()
