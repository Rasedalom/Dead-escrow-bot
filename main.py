import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
print("TOKEN VALUE:", TOKEN)
deals = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Escrow Bot is Active ✅")

async def deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("Usage: /deal buyer seller amount")
        return

    buyer = context.args[0]
    seller = context.args[1]
    amount = context.args[2]

    trade_id = random.randint(10000, 99999)

    deals[str(trade_id)] = {
        "buyer": buyer,
        "seller": seller,
        "amount": amount
    }

    await update.message.reply_text(
        f"💰 Funds Escrowed!\n\n"
        f"🆔 Trade ID: {trade_id}\n"
        f"💵 Amount: ₹{amount}\n"
        f"👤 Buyer: @{buyer}\n"
        f"👤 Seller: @{seller}"
    )

async def release(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /release TRADE_ID")
        return

    trade_id = context.args[0]

    if trade_id in deals:
        deal = deals[trade_id]

        await update.message.reply_text(
            f"✅ Funds Released!\n\n"
            f"🆔 Trade ID: {trade_id}\n"
            f"💵 Amount: ₹{deal['amount']}\n"
            f"👤 Buyer: @{deal['buyer']}\n"
            f"👤 Seller: @{deal['seller']}"
        )

        del deals[trade_id]
    else:
        await update.message.reply_text("Invalid Trade ID")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("deal", deal))
app.add_handler(CommandHandler("release", release))

app.run_polling()
