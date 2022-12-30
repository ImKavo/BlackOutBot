import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_config import API_KEY

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_KEY)

# Initializing a memory storage
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Входная точка диалога
@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    """
    Conversation's entry point
    """
    await bot.send_message(message.chat.id, 'Привіт, {user}! 👋'.format(user=message.from_user.full_name))

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("Магазин 🛒", "Про нас ❔")

    await bot.send_message(message.chat.id, 'Цей бот допоможе тобі при блекаутах!\n'
                                            'Зігрійся, залишайся з Інтернетом та електроенергією!', reply_markup=markup)


@dp.message_handler(lambda message: message.text in ["Меню 🚪"])
async def cmd_shop(message: types.Message):
    """
    Menu button
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("Магазин 🛒", "Про нас ❔")
    await bot.send_message(message.chat.id, "Вихід у меню...", reply_markup=markup)


@dp.message_handler(lambda message: message.text in ["Магазин 🛒", "🔙Магазин 🛒", "Скасувати ❌"])
async def cmd_shop(message: types.Message):
    """
    Shop entry point
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("Зарядні станції 🔋", "Starlink 💫", "Персональне замовлення 🤝", "Меню 🚪")
    await bot.send_message(message.chat.id, "Ласкаво просимо в наш магазин!", reply_markup=markup)


@dp.message_handler(lambda message: message.text in ["Зарядні станції 🔋"])
async def cmd_charging_stations(message: types.Message):
    """
    Charging stations choice
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("Ecoflow Delta 2", "Ecoflow Delta Pro", "Ecoflow River 2",
               "Ecoflow River 2 Max", "Ecoflow River 2 Pro", "🔙Магазин 🛒")

    # Ecoflow Delta 2
    await bot.send_photo(chat_id=message.chat.id, photo=open('media/ecoflow_delta2.png', 'rb'))
    await bot.send_message(message.chat.id, "Ecoflow Delta 2 ⬆️\n52.600₴", reply_markup=markup)

    # Ecoflow Delta Pro
    await bot.send_photo(chat_id=message.chat.id, photo=open('media/ecoflow_deltapro.png', 'rb'))
    await bot.send_message(message.chat.id, "Ecoflow Delta Pro ⬆️\n157.000₴", reply_markup=markup)

    # Ecoflow River 2
    await bot.send_photo(chat_id=message.chat.id, photo=open('media/ecoflow_river2.png', 'rb'))
    await bot.send_message(message.chat.id, "Ecoflow River 2 ⬆️\n15.700₴", reply_markup=markup)

    # Ecoflow River 2 Max
    await bot.send_photo(chat_id=message.chat.id, photo=open('media/ecoflow_river2max.png', 'rb'))
    await bot.send_message(message.chat.id, "Ecoflow River 2 Max ⬆️\n28.700₴", reply_markup=markup)

    # Ecoflow River 2 Pro
    await bot.send_photo(chat_id=message.chat.id, photo=open('media/ecoflow_river2pro.png', 'rb'))
    await bot.send_message(message.chat.id, "Ecoflow River 2 Pro ⬆️\n36.500₴", reply_markup=markup)


@dp.message_handler(lambda message: message.text in ["Starlink 💫"])
async def cmd_starlink(message: types.Message):
    """
    Starlink choice
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("Starlink 2 gen.", "🔙Магазин 🛒")
    # Starlink 2 gen.
    await bot.send_photo(chat_id=message.chat.id, photo=open('media/starlink_2gen.png', 'rb'))
    await bot.send_message(message.chat.id, "Starlink 2 gen. ⬆️\n36.000₴", reply_markup=markup)


@dp.message_handler(lambda message: message.text in ["Ecoflow Delta 2", "Ecoflow Delta Pro", "Ecoflow River 2",
                                                     "Ecoflow River 2 Max", "Ecoflow River 2 Pro", "Starlink 2 gen."])
async def cmd_checkout(message: types.Message):
    """
    Checkout function
    """
    product = message.text
    if product == "Ecoflow Delta 2":
        product_price = "52.600₴"
    elif product == "Ecoflow Delta Pro":
        product_price = "157.000₴"
    elif product == "Ecoflow River 2":
        product_price = "15.700₴"
    elif product == "Ecoflow River 2 Max":
        product_price = "28.700₴"
    elif product == "Ecoflow River 2 Pro":
        product_price = "36.500₴"
    elif product == "Starlink 2 gen.":
        product_price = "36.000₴"

    await bot.send_message(message.chat.id, '🔲---- Мій чек ----🔲\n'
                                            'Продукт: {product}\n'
                                            'Ціна: {product_price}\n'
                                            '🔲----------------🔲'.format(product=message.text, product_price=product_price))

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("Підтвердити ✅", "Скасувати ❌", "🔙Магазин 🛒", "Меню 🚪")

    await bot.send_message(message.chat.id, 'Чи все правильно? 🤔', reply_markup=markup)


@dp.message_handler(lambda message: message.text in ["Підтвердити ✅"])
async def cmd_checkout_yes(message: types.Message):
    """
    Checkout confirmed
    """
    await bot.send_message(message.chat.id, "Дякуємо!\n"
                                            "Тепер перешліть Ваш чек нашому адміну, "
                                            "та домовтеся щодо оплати та доставки:")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("Меню 🚪")
    await bot.send_message(message.chat.id, "https://t.me/illiakoshel", reply_markup=markup)


@dp.message_handler(lambda message: message.text in ["Персональне замовлення 🤝"])
async def cmd_personal_order(message: types.Message):
    """
    Personal order
    """
    await bot.send_message(message.chat.id, "Контакт для персональних замовлень:")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("Меню 🚪")
    await bot.send_message(message.chat.id, "https://t.me/illiakoshel", reply_markup=markup)


@dp.message_handler(lambda message: message.text in ["Про нас ❔"])
async def cmd_about_us(message: types.Message):
    """
    About us button action
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("Магазин 🛒", "Про нас ❔")
    await bot.send_message(message.chat.id, "Наша місія - допомогати українцям у скрутні часи 🫶\n"
                                            "Тому ми купляємо різне приладдя та продаємо його за мінімальними цінами.\n"
                                            "Також, 10% з нашого прибутку йдуть на допомогу ЗСУ - "
                                            "купляючи через цього бота, Ви допомагаєте нашій армії! 💪🇺🇦\n"
                                            "Щодо якості - ми даємо довгосрочні гарантії на продукти з нашого "
                                            "магазину та робимо все, що в наших силах, щоб все працювало коректно.\n"
                                            "А магазин у вигляді телеграм-бота - "
                                            "це, на нашу думку, дуже сучасно та зручно для наших клієнтів 💛\n\n"
                                            "У разі виникнення складнощів та питань:\n"
                                            "✈️Телеграм: @illiakoshel або @kavooo_q\n"
                                            "📞Телефон: +380993705838\n"
                                            "🤖Розробник бота: @kavooo_q", reply_markup=markup)


# Функция для теста состояния бота
@dp.message_handler(commands=['test'])
async def comm_test(message: types.Message):
    """
    Command to test the bot state
    """
    await bot.send_message(message.chat.id, "The state is normal")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)