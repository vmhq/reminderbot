import os
import openai
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pytz import timezone
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# Cargar claves desde el entorno
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("❌ Las claves no están configuradas. Verifica tu archivo .env")

# Inicializar OpenAI API
openai.api_key = OPENAI_API_KEY

# Inicializar el programador de tareas
scheduler = BackgroundScheduler()
scheduler.start()

# Diccionario para almacenar los datos del usuario (zona horaria, idioma, recordatorios)
user_data = {}

# Función para determinar el idioma según la zona horaria
def infer_language_from_timezone(location):
    languages = {
        "España": "Español",
        "Argentina": "Español",
        "México": "Español",
        "Colombia": "Español",
        "Chile": "Español",
        "Perú": "Español",
        "Estados Unidos": "Inglés",
        "UK": "Inglés",
        "Francia": "Francés",
        "Alemania": "Alemán",
    }
    # Buscar un idioma basado en el nombre del país/ciudad
    for country, language in languages.items():
        if country.lower() in location.lower():
            return language
    return "Inglés"  # Idioma predeterminado si no se encuentra coincidencia

# Asignar un emoji usando OpenAI
def get_emoji_from_openai(text):
    prompt = (
        f"Analiza este recordatorio y selecciona el emoji más adecuado. "
        f"Solo devuelve el emoji y nada más. Entrada: {text}"
    )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=10,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Manejar la bienvenida y solicitar configuración de zona horaria e idioma
def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if chat_id not in user_data:
        user_data[chat_id] = {}
        update.message.reply_text(
            "¡Hola! 👋 Bienvenido a tu bot de recordatorios inteligentes.\n\n"
            "Antes de empezar, necesito que configures tu zona horaria y idioma. "
            "Por favor, usa el comando:\n"
            "`/set_timezone Ciudad País`\n\n"
            "Por ejemplo:\n`/set_timezone Madrid España`",
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        update.message.reply_text("¡Hola de nuevo! 🥳 Ya tienes configurada tu zona horaria y tu idioma. 😊")

# Configurar zona horaria e idioma
def set_timezone(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 2:
        update.message.reply_text(
            "Por favor, indícame tu ciudad y país, por ejemplo:\n`/set_timezone Madrid España`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    location = " ".join(context.args)
    try:
        # Configurar la zona horaria
        tz = timezone(location.replace(" ", "_"))
        user_data[update.message.chat_id]["timezone"] = tz

        # Inferir idioma y configurarlo
        language = infer_language_from_timezone(location)
        user_data[update.message.chat_id]["language"] = language

        update.message.reply_text(
            f"✅ Zona horaria configurada correctamente: {location} 🌍.\n"
            f"🌐 Idioma detectado: {language}.",
        )
    except Exception as e:
        update.message.reply_text(
            f"⛔ No pude encontrar tu zona horaria o idioma. Asegúrate de escribir correctamente la ciudad y el país.\nError: {str(e)}"
        )

# Procesar mensajes y programar recordatorios
def process_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if "timezone" not in user_data.get(chat_id, {}):
        update.message.reply_text("Por favor, configura primero tu zona horaria con el comando /set_timezone.")
        return

    text = update.message.text or ""
    
    # Usar OpenAI para interpretar el recordatorio
    prompt = (
        f"Analiza este recordatorio y devuelve un JSON estructurado con la información:\n"
        f"- Tipo: 'único' o 'recurrente'.\n"
        f"- Fecha y hora si es único: 'YYYY-MM-DD', 'HH:MM'.\n"
        f"- Día si es recurrente: 'lunes/martes/etc.', 'HH:MM'.\n\n"
        f"Input: {text}"
    )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
    )
    try:
        parsed_data = eval(response.choices[0].text.strip())
    except Exception:
        update.message.reply_text("⛔ No pude entender tu recordatorio. Intenta usar un formato diferente.")
        return

    tz = user_data[chat_id]["timezone"]
    emoji = get_emoji_from_openai(text)

    if parsed_data["tipo"] == "único":
        naive_date = datetime.strptime(f"{parsed_data['fecha']} {parsed_data['hora']}", "%Y-%m-%d %H:%M")
        localized_date = tz.localize(naive_date)
        scheduler.add_job(
            send_reminder,
            trigger="date",
            run_date=localized_date,
            args=[chat_id, f"{emoji} {text}"],
        )
        update.message.reply_text(f"✅ Recordatorio único configurado para: {localized_date.strftime('%Y-%m-%d %H:%M %Z')}")

    elif parsed_data["tipo"] == "recurrente":
        scheduler.add_job(
            send_reminder,
            trigger="cron",
            day_of_week=parsed_data["día"],
            hour=int(parsed_data["hora"].split(':')[0]),
            minute=int(parsed_data["hora"].split(':')[1]),
            timezone=tz.zone,
            args=[chat_id, f"{emoji} {text}"],
        )
        update.message.reply_text(f"✅ Recordatorio recurrente configurado: Todos los {parsed_data['día']} a las {parsed_data['hora']}.")

# Enviar recordatorios
def send_reminder(chat_id, text):
    updater.bot.send_message(chat_id, text)

# Configurar los comandos
def main() -> None:
    global updater
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("set_timezone", set_timezone))
    dispatcher.add_handler(MessageHandler(Filters.text, process_message))

    updater.start_polling()
    updater.idle()