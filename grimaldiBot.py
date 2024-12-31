import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuración de logging para ver los errores del bot
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# URL de la API pública de CoinGecko para obtener el precio de BTC
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

# Función que obtiene el precio de Bitcoin desde la API de CoinGecko
def obtener_precio_btc():
    try:
        response = requests.get(url)
        data = response.json()
        return data['bitcoin']['usd']
    except Exception as e:
        logger.error(f"Error al obtener el precio de Bitcoin: {e}")
        return None

# Comando /precio: Envia el precio actual de Bitcoin
async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    precio_btc = obtener_precio_btc()
    if precio_btc:
        await update.message.reply_text(f"El precio actual de Bitcoin es: ${precio_btc} USD")
    else:
        await update.message.reply_text("Hubo un error al obtener el precio de Bitcoin.")

# Comando /start: Saludo inicial
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot de precios de Bitcoin. Usa el comando /precio para obtener el precio actual de Bitcoin.")

# Función principal para ejecutar el bot
def main():
    # Reemplaza con el token de tu bot
    application = Application.builder().token("7993918602:AAHPZjOTbjHw9h7F3Z8XseFP6upbR4dRe_w").build()

    # Registrar los comandos /start y /precio
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("precio", precio))

    # Comienza a escuchar por mensajes
    application.run_polling()

if __name__ == '__main__':
    main()
