# Telegram Voice-to-Text Bot

Цей бот конвертує голосові повідомлення у текст, використовуючи Google Speech Recognition.

## Вимоги

1.  **Python 3.8+**
2.  **FFmpeg** (повинно бути встановлено та додано в PATH).
    - [Завантажити FFmpeg](https://ffmpeg.org/download.html)
    - [Інструкція по встановленню](https://phoenixnap.com/kb/ffmpeg-windows) (або загугліть "install ffmpeg windows add to path").

## Встановлення

1.  Встановіть залежності:
    ```bash
    pip install -r requirements.txt
    ```

## Запуск

1.  Запустіть бота:
    ```bash
    python bot.py
    ```
2.  Знайдіть свого бота в Telegram і натисніть **Start**.
3.  Надішліть йому голосове повідомлення.

## Примітка
Якщо бот видає помилку про конвертацію, переконайтеся, що `ffmpeg` доступний у командному рядку (спробуйте ввести `ffmpeg -version` у терміналі).
