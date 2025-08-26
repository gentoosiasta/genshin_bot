import os
import sys
from telegram import Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# TOKEN que obtuviste de BotFather
BOT_TOKEN = "8038008029:AAEG4JrZumIHahwa3q1GX5ddXrcGzrdH-TY"

LOCK_FILE = "/tmp/genshin_bot.lock"

# Diccionario con comandos e imágenes
IMAGENES = {
    "skirk": ["https://ibb.co/VW2W5yNs"],
    "citlali": ["https://ibb.co/hJzghc1k"],
    "escoffier": ["https://ibb.co/nM8jCx8r"],
    "rosaria": ["https://ibb.co/V0X59Yfp", "https://ibb.co/ZRnV1zRX"],
    "arlecchino": ["https://ibb.co/Y4TK2my1"],
    "bennett": ["https://ibb.co/xS9QnbQV"],
    "chevreuse": ["https://ibb.co/zVG3PfK3"],
    "diluc": ["https://ibb.co/SZsjHwr"],
    "gaming": ["https://ibb.co/VWQx4cw3"],
    "hutao": ["https://ibb.co/JR1RQdRj"],
    "mavuika": ["https://ibb.co/8nXrXcX1", "https://ibb.co/PkWsFh2"],
    "xiangling": ["https://ibb.co/WNF6wB1L"],
    "yanfei": ["https://ibb.co/TxfnGccY"],
    "yoimiya": ["https://ibb.co/DPBZTKQn"],
    "dehya": ["https://ibb.co/XkVc4ktk", "https://ibb.co/TB8XqrLz"],
    "barbara": ["https://ibb.co/fV960HbN"],
    "candace": ["https://ibb.co/zWpvWdYS", "https://ibb.co/FkkqmL2P"],
    "furina": ["https://ibb.co/JFmcPG1S"],
    "mona": ["https://ibb.co/zVVJLYNw"],
    "mualani": ["https://ibb.co/60sFtqws"],
    "nilou": ["https://ibb.co/n8qndhrT"],
    "xingqiu": ["https://ibb.co/5XfPJZhy"],
    "yelan": ["https://ibb.co/7dWfC91c"],
    "beidou": ["https://ibb.co/FbCbKFPH"],
    "fischl": ["https://ibb.co/m556Q2X8"],
    "iansan": ["https://ibb.co/VcHTxtJm"],
    "keqing": ["https://ibb.co/h11JPHzt", "https://ibb.co/qLzJDTf6"],
    "ororon": ["https://ibb.co/Nnp9r1hD"],
    "raiden": ["https://ibb.co/nJfcHpC", "https://ibb.co/cSFsGWVR", "https://ibb.co/spsnKTVb"],
    "shogun": ["https://ibb.co/nJfcHpC", "https://ibb.co/cSFsGWVR", "https://ibb.co/spsnKTVb"],
    "sara": ["https://ibb.co/rT94chr"],
    "koujou": ["https://ibb.co/rT94chr"],
    "koujou_sara": ["https://ibb.co/rT94chr"],
    "kuki": ["https://ibb.co/vv47NpZV", "https://ibb.co/0pyq3RN6"],
    "shinobu": ["https://ibb.co/vv47NpZV", "https://ibb.co/0pyq3RN6"],
    "kuki_shinobu": ["https://ibb.co/vv47NpZV", "https://ibb.co/0pyq3RN6"],
    "varesa": ["https://ibb.co/XxWVJvH5"],
    "yae": ["https://ibb.co/cXrQ6Sb4"],
    "yaemiko": ["https://ibb.co/cXrQ6Sb4"],
    "miko": ["https://ibb.co/cXrQ6Sb4"],
    "chasca": ["https://ibb.co/VpxmSmbn"],
    "faruzan": ["https://ibb.co/6RB9yMry"],
    "ifa": ["https://ibb.co/hJrHcsTP"],
    "jean": ["https://ibb.co/NnYGDWs6"],
    "kazuha": ["https://ibb.co/0jswK3Yt"],
    "kaedehara": ["https://ibb.co/0jswK3Yt"],
    "kaedehara_kazuha": ["https://ibb.co/0jswK3Yt"],
    "lanyan": ["https://ibb.co/4hRndbC"],
    "lan_yan": ["https://ibb.co/4hRndbC"],
    "sucrose": ["https://ibb.co/HTwXrjJb"],
    "xianyun": ["https://ibb.co/Zz6GVmNV"],
    "navia": ["https://ibb.co/LDGxM4nv"],
    "noelle": ["https://ibb.co/r2hZB3f7"],
    "xilonen": ["https://ibb.co/v4Sfjvx9"],
    "zhongli": ["https://ibb.co/vC9F3RfR"],
    "baizhu": ["https://ibb.co/M5D4jn07"],
    "collei": ["https://ibb.co/nMC2KTgx"],
    "emilie": ["https://ibb.co/twFD7nDH"],
    "nahida": ["https://ibb.co/vxgQ3fxW"],
    "tighnari": ["https://ibb.co/9jCzsD0"],
    "ayaka": ["https://ibb.co/0p5ztT7K"],
    "kamisato_ayaka": ["https://ibb.co/0p5ztT7K"],
    "charlotte": ["https://ibb.co/8nNFTJJR"],
    "diona": ["https://ibb.co/sd9xrhC6"],
    "ganyu": ["https://ibb.co/yFHT52Fg", "https://ibb.co/xKL3JCSV"],
    "shenhe": ["https://ibb.co/9mqhrz26"],
    "layla": ["https://ibb.co/yFKN065n"],
    "kinich": ["https://ibb.co/mFS3rRJG"]
}

# Función para comandos como /gato, /perro, etc.
async def mostrar_imagen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comando = update.message.text[1:]  # Remueve el "/"
    imagen_url = IMAGENES.get(comando.lower())

    if imagen_url:
        media = [InputMediaPhoto(url) for url in imagen_url]
        await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media)
    else:
        await update.message.reply_text("No tengo imagen para ese comando 😿")

# Inicio del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, usa /<nombre_personaje>, por ejemplo /skirk, para ver la build rápidad de dicho personaje")

def check_lock():
    if os.path.exists(LOCK_FILE):
        print("Ya hay una instancia en ejecución.")
        sys.exit()
    else:
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))

def remove_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

# Ejecutar el bot
if __name__ == "__main__":
    try:
        check_lock()

        app = ApplicationBuilder().token(BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        for comando in IMAGENES.keys():
            app.add_handler(CommandHandler(comando, mostrar_imagen))

        print("Bot corriendo...")
        app.run_polling()

    finally:
        remove_lock()

