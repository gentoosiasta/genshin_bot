""" Bot de Genshin Impact para Telegram """
import os
import sys
import logging
import json
from dotenv import load_dotenv
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError
from imagenes_personajes import IMAGENES
from enka_user import general_info, character_info

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

LOCK_FILE = "/tmp/genshin_bot.lock"

# Configura el logging para ver los errores
# Configura el logging para que escriba en un archivo y también en la consola.
logging.basicConfig(
    level=logging.WARN, # Nivel mínimo de los mensajes a registrar
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/var/log/genshin_bot.log"), # Manejador para escribir en el archivo 'bot.log'
        logging.StreamHandler()        # Manejador para mostrar los logs en la consola
    ]
)

def load_users(file_path="users.json") -> None:
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_id(data, file_path="users.json") -> None:
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
        

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía un mensaje de bienvenida con la lista de comandos."""
    nombre_usuario = update.effective_user.first_name

    # Crea una lista de todas las claves disponibles para el mensaje
    nombres_disponibles = ", ".join(sorted(IMAGENES.keys()))

    mensaje_bienvenida = (
        f"¡Hola, {nombre_usuario}! 👋\n\n"
        "Usa el comando `/build <nombre>` para recibir una o más imágenes.\n\n"
        "**Nombres disponibles:**\n"
        f"`{nombres_disponibles}`\n\n"
        "Usa el comando `/char_info <nombre> <personaje>` para obtener información del personaje.\n\n"
        "Usa el comando `/user_info <nombre>` para obtener información de un usuario.\n\n"
        "Puedes agregar usuarios con el comando `/set_user <nombre> <id>`."
    )

    await update.message.reply_text(mensaje_bienvenida, parse_mode='Markdown')

async def enviar_imagen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Busca un nombre en el diccionario y envía todas las imágenes asociadas."""
    try:
        # Obtiene el nombre solicitado por el usuario (en minúsculas)
        nombre_clave = context.args[0].lower()
    except IndexError:
        await update.message.reply_text("Por favor, especifica un nombre. Ejemplo: /build raiden")
        return

    # Busca la lista de URLs en el diccionario
    lista_urls = IMAGENES.get(nombre_clave)

    if lista_urls:
        # Si se encontraron URLs, se envían
        await update.message.reply_text(f"Enviando builds para '{nombre_clave}'...")

        # Opción 1: Enviar como un álbum (si hay entre 2 y 10 imágenes)
        if 1 < len(lista_urls) <= 10:
            media_group = [InputMediaPhoto(url) for url in lista_urls]
            try:
                await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media_group)
            except TelegramError as e:
                await update.message.reply_text(f"Hubo un error al crear el álbum. Error: {e}")
                # Si falla el álbum, se envían una por una como respaldo
                for url in lista_urls:
                    try:
                       await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)
                    except TelegramError as e_photo:
                       await update.message.reply_text(f"No se pudo enviar la build desde {url}. Error: {e_photo}")

        # Opción 2: Enviar una por una (si es solo una imagen o más de 10)
        else:
            for url in lista_urls:
                try:
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)
                except TelegramError as e:
                    # Informa al usuario si una URL específica falla
                    await update.message.reply_text(f"No se pudo enviar la build desde {url}. Asegúrate de que sea un enlace directo válido. Error: {e}")

    else:
        # Si el nombre no está en el diccionario
        await update.message.reply_text(f"Lo siento, no encontré builds para '{nombre_clave}'. Usa /start para ver la lista de nombres disponibles.")

async def set_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Guarda el ID del usuario en un archivo."""
    try:
        user_name = context.args[0].lower()
        user_id = context.args[1]
    except IndexError:
        await update.message.reply_text("Por favor, especifica un nombre y un ID. Ejemplo: /set_user nombre 123456789")
        return

    # Comprueba que el nombre sea válido
    if not user_name.isalnum():
        await update.message.reply_text("El nombre no es válido. Por favor, especifica un nombre válido.")
        return

    # Comprueba que el ID sea válido
    if not user_id.isdigit():
        await update.message.reply_text("El ID no es válido. Por favor, especifica un ID válido.")
        return

    users = load_users()

    users[user_name] = {"id": user_id}
    save_user_id(users)

    await update.message.reply_text(f"ID {user_id} guardado para {user_name}.")

async def get_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Obtiene la información del usuario especificado."""
    try:
        user_name = context.args[0].lower()
    except IndexError:
        await update.message.reply_text("Por favor, especifica un nombre. Ejemplo: /user_info nombre")
        return

    users = load_users()

    try:
        user = users[user_name]
    except KeyError:
        await update.message.reply_text(f"Lo siento, no encontré información para '{user_name}'")
        return

    await update.message.reply_text(f"Mostrando información de {user_name} (ID: {user['id']})")

    await general_info(user['id'], update)
    
async def get_character_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Obtiene la información del personaje especificado."""
    try:
        user_name = context.args[0].lower()
        character_name = context.args[1].lower()
        
    except IndexError:
        await update.message.reply_text("Por favor, especifica un nombre de usuario y un personaje. Ejemplo: /char_info nombre personaje")
        return
    
    users = load_users()

    try:
        user = users[user_name]
    except KeyError:
        await update.message.reply_text(f"Lo siento, no encontré información para '{user_name}'")
        return

    await update.message.reply_text(f"Mostrando información del personaje {character_name} de {user_name} (ID: {user['id']})")

    await character_info(user['id'], character_name, update)


def main() -> None:
    """Inicia el bot."""
    print("Iniciando bot...")
    application = Application.builder().token(BOT_TOKEN).build()

    # Registra los manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("build", enviar_imagen))
    application.add_handler(CommandHandler("set_user", set_user_id))
    application.add_handler(CommandHandler("user_info", get_user_info))
    application.add_handler(CommandHandler("char_info", get_character_info))

    # Inicia el bot para que escuche peticiones
    print("Bot iniciado. Presiona Ctrl+C para detener.")
    application.run_polling()

def check_lock() -> None:
    """Comprueba si hay una instancia en ejecución."""
    if os.path.exists(LOCK_FILE):
        print("Ya hay una instancia en ejecución.")
        sys.exit()
    else:
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))

def remove_lock() -> None:
    """Elimina el archivo de bloqueo."""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

if __name__ == '__main__':
    try:
        check_lock()
        main()

    finally:
        remove_lock()
