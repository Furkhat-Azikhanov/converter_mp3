# ----Шаг 1: Установка необходимых библиотек----
# Для начала установим необходимые библиотеки:
# pip install pyTelegramBotAPI yt-dlp moviepy

# ----Шаг 2: Создание и настройка бота----
# Создание бота в Telegram
# Найдите BotFather в Telegram.
# Создайте нового бота с помощью команды /newbot.
# Получите токен API, который будет использоваться в вашем скрипте.
# Импорт библиотек и настройка бота
import telebot  # Импортируем библиотеку для создания Telegram-бота
import yt_dlp  # Импортируем библиотеку для скачивания видео с YouTube
from moviepy.editor import *  # Импортируем библиотеку для работы с видеофайлами
import os  # Импортируем библиотеку для работы с файловой системой

API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'  # Замените на ваш токен от BotFather
bot = telebot.TeleBot(API_TOKEN)  # Инициализируем бота с использованием API токена


# ----Шаг 3: Обработчик команды /start----
# Этот обработчик отвечает за приветственное сообщение, 
# которое бот отправляет пользователю, 
# когда тот отправляет команду /start.
# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне ссылку на YouTube видео, и я конвертирую его в MP3.")  # Ответ на команду /start


# ----Шаг 4: Обработчик текстовых сообщений----
#Этот обработчик принимает ссылки на YouTube видео, 
# загружает видео, конвертирует его в MP3 и отправляет 
# пользователю.
# Основной код
# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text  # Получаем текст сообщения (ожидаем, что это будет ссылка)
    if "youtube.com" in url or "youtu.be" in url:  # Проверяем, содержит ли сообщение ссылку на YouTube
        try:
            bot.reply_to(message, "Видео загружается, подождите...")  # Отправляем сообщение о начале загрузки

            # Опции для yt-dlp
            ydl_opts = {
                'format': 'bestaudio/best',  # Выбираем лучший аудиоформат
                'outtmpl': 'downloaded_video.%(ext)s',  # Шаблон имени выходного файла
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # Используем yt-dlp для скачивания видео
                info_dict = ydl.extract_info(url, download=True)  # Извлекаем информацию о видео и скачиваем его
                video_title = info_dict.get('title', 'audio')  # Получаем название видео

            # Конвертируем видео в MP3
            audio = AudioFileClip('downloaded_video.webm')  # Загружаем скачанное видео
            mp3_filename = f"{video_title}.mp3"  # Задаем имя MP3 файла
            audio.write_audiofile(mp3_filename)  # Сохраняем аудиофайл в формате MP3

            # Отправляем MP3 файл пользователю
            with open(mp3_filename, 'rb') as audio_file:
                bot.send_audio(message.chat.id, audio_file)  # Отправляем MP3 файл в чат

            # Удаляем временные файлы
            os.remove('downloaded_video.webm')  # Удаляем скачанное видео
            os.remove(mp3_filename)  # Удаляем MP3 файл после отправки

            # Удаляем сообщение с ссылкой
            bot.delete_message(message.chat.id, message.message_id)  # Удаляем сообщение пользователя с ссылкой
        except Exception as e:  # Обрабатываем исключения
            bot.reply_to(message, f"Произошла ошибка: {e}")  # Отправляем сообщение об ошибке
    else:
        bot.reply_to(message, "Пожалуйста, отправьте корректную ссылку на YouTube видео.")  # Сообщение при некорректной ссылке



# ----Шаг 5: Запуск бота----
#Для запуска бота используем метод polling.
# Запуск бота
bot.polling()  # Запускаем бота в режиме долгого опроса (long polling)
