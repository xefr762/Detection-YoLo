#base
import logging
import os
import time

#tg lib
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, ContentType
from aiogram.filters.command import Command

#our func files
from model import predict_class

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(
    level=logging.INFO,
    filename='loggs.log',
    format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
    )

@dp.message(Command(commands=['start']))
async def start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f"Привет, {user_name}! Отправь мне картинку c персонажами WoW, а я скажу, кто на ней находится"
    logging.info(f'{user_name}, {user_id} -- start using bot')
    await bot.send_message(chat_id=user_id, text=text)


#@dp.message(Command(commands=['Send photo']))
async def photo(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id

    # Получаем фото
    photo = message.photo[-1]
    file_id = photo.file_id
    file_name = f"user_photo_{user_id}.jpg"

    await bot.download(file_id, destination=file_name)

    #Записываем логи
    logging.info(f"User {user_name} ({user_id}) sent a photo: {file_name}")

    #Обработка изображения через модель
    try:
        pred_class, proc_time, res_image = predict_class(file_name)
    except Exception as exc:
        logging.error(f"Error with processing image for {user_id} -- {user_name}: {exc}")
        await message.reply('Произошла ошибка при обработке изображения. Попробуйте ещё раз или отправьте другую картинку')
        return

    await message.reply(f"Время работы: {proc_time} секунд")
    result_image_file = FSInputFile(res_image)
    await bot.send_photo(chat_id=user_id, photo=result_image_file)

dp.message.register(start, Command(commands=['start']))
dp.message.register(photo, F.content_type == ContentType.PHOTO)

if __name__ == '__main__':
    dp.run_polling(bot)