
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

BRAND, MODEL, PRICE_YEN, ENGINE_CC, YEAR = range(5)
TOKEN = "8248943619:AAHF2-sAaKvTRm1KCekMmlVAlY-5ze3rgXk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Введите марку авто.")
    return BRAND

async def brand_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["brand"] = update.message.text
    await update.message.reply_text("Введите модель авто.")
    return MODEL

async def model_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["model"] = update.message.text
    await update.message.reply_text("Введите цену авто (FOB) в иенах. Если 0, используется 130000 ¥")
    return PRICE_YEN

async def price_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        val = int(update.message.text)
    except:
        val = 130000
    context.user_data["price_yen"] = val if val != 0 else 130000
    await update.message.reply_text("Введите объём двигателя (см³)")
    return ENGINE_CC

async def engine_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["engine_cc"] = int(update.message.text)
    except:
        context.user_data["engine_cc"] = 2000
    await update.message.reply_text("Введите год выпуска")
    return YEAR

async def year_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["year"] = int(update.message.text)
    except:
        context.user_data["year"] = 2015

    brand = context.user_data["brand"]
    model = context.user_data["model"]
    fob = context.user_data["price_yen"]
    freight = 130000
    broker = 60000
    rate = 0.55
    total_rub = (fob+freight)*rate + broker
    await update.message.reply_text(f"🚗 {brand} {model}\n💰 Итог: {int(total_rub)} ₽\n📎 https://t.me/wsdauto")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            BRAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, brand_handler)],
            MODEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, model_handler)],
            PRICE_YEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, price_handler)],
            ENGINE_CC: [MessageHandler(filters.TEXT & ~filters.COMMAND, engine_handler)],
            YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, year_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()
