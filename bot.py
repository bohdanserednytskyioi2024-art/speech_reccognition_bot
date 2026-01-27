import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# 1. Налаштування логування (ТЕПЕР ПРАЦЮЄ)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. Конфігурація FFmpeg
win_ffmpeg_path = r"C:\Users\Bohdan\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
if os.path.exists(win_ffmpeg_path):
    os.environ["PATH"] += os.pathsep + win_ffmpeg_path
    # Додаткова вказівка для pydub, якщо вона все ще не бачить ffmpeg
    AudioSegment.converter = os.path.join(win_ffmpeg_path, "ffmpeg.exe")
    
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Надішли мені голосове повідомлення, і я перетворю його на текст.")

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_message = await update.message.reply_text("Обробляю голосове повідомлення...")
    
    # Створюємо унікальні імена файлів, щоб уникнути конфліктів при одночасних запитах
    user_id = update.message.from_user.id
    ogg_file = f"temp_{user_id}.ogg"
    wav_file = f"temp_{user_id}.wav"
    
    try:
        # Отримуємо файл
        voice_file = await context.bot.get_file(update.message.voice.file_id)
        await voice_file.download_to_drive(ogg_file)
        
        # Конвертація
        try:
            audio = AudioSegment.from_ogg(ogg_file)
            audio.export(wav_file, format="wav")
        except Exception as e:
            logger.error(f"FFmpeg conversion error: {e}")
            await status_message.edit_text("Помилка при конвертації. Переконайтеся, що FFmpeg встановлено.")
            return

        # Розпізнавання
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="uk-UA")
                await status_message.edit_text(f"📜 Розпізнаний текст:\n\n{text}")
            except sr.UnknownValueError:
                await status_message.edit_text("Не вдалося розпізнати мову.")
            except sr.RequestError:
                await status_message.edit_text("Помилка сервісу Google.")
                
    except Exception as e:
        logger.error(f"General error: {e}")
        await status_message.edit_text(f"Виникла помилка: {e}")
        
    finally:
        # Видалення файлів
        for f in [ogg_file, wav_file]:
            if os.path.exists(f):
                os.remove(f)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.VOICE, voice_handler))
    
    print("Бот запущений...")
    application.run_polling()