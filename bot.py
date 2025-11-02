from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import os, csv
from datetime import datetime

# -------------------------------------
# LẤY TOKEN TỪ ENV (KHÔNG LỘ TOKEN)
# -------------------------------------
TOKEN = os.getenv("BOT_TOKEN")   # <-- không sửa dòng này

# -------------------------------------
# LINK MINI APP (Netlify)
# -------------------------------------
WEBAPP_URL = "https://genuine-quokka-3f4c4f.netlify.app"  # <-- giữ nguyên hoặc thay link mới

RUNS_FILE = "runs.csv"


# -------------------------------------
# GHI LƯỢT CHẠY & ĐẾM THỐNG KÊ
# -------------------------------------
def save_run():
    today = datetime.now().strftime("%Y-%m-%d")
    file_exists = os.path.isfile(RUNS_FILE)

    if not file_exists:
        with open(RUNS_FILE, "w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(["date"])

    with open(RUNS_FILE, "a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([today])

    total = 0
    today_count = 0

    with open(RUNS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            if row["date"] == today:
                today_count += 1

    return total, today_count


# -------------------------------------
# LỆNH /start
# -------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total, today = save_run()

    keyboard = [
        [InlineKeyboardButton("Open Inventory App", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]

    await update.message.reply_text(
        f"✅ Bot is running\n"
        f"▶️ Total runs: {total}\n"
        f"📅 Runs today: {today}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# -------------------------------------
# CHẠY BOT
# -------------------------------------
def main():
    if not TOKEN:
        raise ValueError("❌ BOT_TOKEN chưa được khai báo trong Railway / GitHub Secrets")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == "__main__":
    main()
