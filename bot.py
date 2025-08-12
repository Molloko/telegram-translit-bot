# 1.Импорт библиотек
import logging
import os
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
from aiogram.types import Message  # ловим все обновления этого типа
from aiogram.filters.command import Command  # обрабатываем команды /start, /help и другие

# 2. Инициализация объектов
TOKEN = os.getenv('TOKEN')
# Используем твой токен из заготовки, а если он не указан — берём из переменной окружения TOKEN
bot = Bot(token= TOKEN if not TOKEN else TOKEN)
dp = Dispatcher()  # Создаем объект диспетчера. Все хэндлеры(обработчики) должны быть подключены к диспетчеру

# Логирование и в файл, и в консоль
LOG_DIR = os.getenv("LOG_DIR", ".")
os.makedirs(LOG_DIR, exist_ok=True)
log_file_path = os.path.join(LOG_DIR, "bot.log")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ротация лога до 1 МБ, храним 3 копии
file_handler = RotatingFileHandler(log_file_path, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

# чтобы не дублировать хэндлеры при повторном запуске
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

logging.info("Bot is starting")


# Домашнее Задание
# - Включить запись log в файл  ✅
# - Бот принимает кириллицу отдаёт латиницу в соответствии с Приказом МИД по транслитерации ✅
# - Бот работает из-под docker контейнера (готов к этому: переменные окружения, лог в файл) ✅

# 3. Обработка/Хэндлер на команду /start
@dp.message(Command(commands=['start']))
async def proccess_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = (
        f'Привет, {user_name}!\n'
        f'Отправь мне ФИО кириллицей — верну транслитерацию по правилам МИД РФ.\n'
        f'Пример: Иванов Иван Иванович → IVANOV IVAN IVANOVICH'
    )
    logging.info(f'{user_name} {user_id} запустил бота')
    await bot.send_message(chat_id=user_id, text=text)


# 4. Обработка/Хэндлер на любые сообщения
@dp.message()
async def send_transliteration(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text

    # здесь просиходит транлитерация:
    async def transliterate_mfa(src: str) -> str:
        # таблица транслитерации по приказу МИД РФ (паспортная транслитерация)
        mapping = {
            'А': 'A',   'а': 'a',   'Б': 'B',    'б': 'b',   'В': 'V',   'в': 'v',
            'Г': 'G',   'г': 'g',   'Д': 'D',    'д': 'd',   'Е': 'E',   'е': 'e',
            'Ё': 'E',   'ё': 'e',   'Ж': 'ZH',   'ж': 'zh',  'З': 'Z',   'з': 'z',
            'И': 'I',   'и': 'i',   'Й': 'I',    'й': 'i',   'К': 'K',   'к': 'k',
            'Л': 'L',   'л': 'l',   'М': 'M',    'м': 'm',   'Н': 'N',   'н': 'n',
            'О': 'O',   'о': 'o',   'П': 'P',    'п': 'p',   'Р': 'R',   'р': 'r',
            'С': 'S',   'с': 's',   'Т': 'T',    'т': 't',   'У': 'U',   'у': 'u',
            'Ф': 'F',   'ф': 'f',   'Х': 'KH',   'х': 'kh',  'Ц': 'TS',  'ц': 'ts',
            'Ч': 'CH',  'ч': 'ch',  'Ш': 'SH',   'ш': 'sh',  'Щ': 'SHCH','щ': 'shch',
            'Ъ': 'IE',  'ъ': 'ie',  'Ы': 'Y',    'ы': 'y',   'Ь': '',    'ь': '',
            'Э': 'E',   'э': 'e',   'Ю': 'IU',   'ю': 'iu',  'Я': 'IA',  'я': 'ia',
        }
        # Пропускаем пробелы, дефисы и точки как есть; прочие символы — оставляем без изменений
        # Это позволяет вводить ФИО в формате: "Иванов-Петров И.И."
        return ''.join(mapping.get(ch, ch) for ch in src)

    transliterated = await transliterate_mfa(text)

    logging.info(f'{user_name} {user_id}: {text} -> {transliterated}')
    await message.answer(text=transliterated)


# 5. Запуск процесса пуллинга
if __name__ == '__main__':
    dp.run_polling(bot)
