import telebot
from telebot import types

bot = telebot.TeleBot("7779559381:AAFU-tFNw6Bdo7o2TiT3HEp2UD_CuycL084")

# Глобальные переменные для хранения корзины
user_carts = {}

# Ссылки на изображения товаров (замените на реальные)
burger_images = {
    "classic": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDfPSOfNj6wVTYs3pvZQ4eMcLpgy_Fv0pXMA&s",
    "cheese": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuO1B4d5FSW5C5ji6ltCWCWHwKWgFbk_8u7w&s",
    "veggie": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQTFz0Znuelzy2lrBkqnRH4ngD0LBxiv7_sHw&s"
}


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Посмотреть товары")
    btn2 = types.KeyboardButton("Корзина 🛒")
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id,
                     "Привет! Добро пожаловать в наш магазин.",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Посмотреть товары")
def show_categories(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Бургеры 🍔")
    btn2 = types.KeyboardButton("Пицца 🍕")
    btn3 = types.KeyboardButton("Напитки 🥤")
    btn4 = types.KeyboardButton("Назад 🔙")
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Бургеры 🍔")
def show_burgers(message):
    # Отправляем первый бургер
    markup1 = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Добавить в корзину", callback_data="burger_classic")
    markup1.add(btn1)
    bot.send_photo(message.chat.id, burger_images["classic"],
                   caption="Классический бургер 🍔\nЦена: 300₽",
                   reply_markup=markup1)

    # Отправляем второй бургер
    markup2 = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton("Добавить в корзину", callback_data="burger_cheese")
    markup2.add(btn2)
    bot.send_photo(message.chat.id, burger_images["cheese"],
                   caption="Чизбургер 🧀🍔\nЦена: 350₽",
                   reply_markup=markup2)

    # Отправляем третий бургер
    markup3 = types.InlineKeyboardMarkup()
    btn3 = types.InlineKeyboardButton("Добавить в корзину", callback_data="burger_veggie")
    markup3.add(btn3)
    bot.send_photo(message.chat.id, burger_images["veggie"],
                   caption="Вег бургер 🥗🍔\nЦена: 320₽",
                   reply_markup=markup3)


@bot.callback_query_handler(func=lambda call: call.data.startswith("burger_"))
def add_to_cart(call):
    user_id = call.from_user.id

    # Инициализация корзины если нужно
    if user_id not in user_carts:
        user_carts[user_id] = []

    # Определяем какой товар добавить
    if call.data == "burger_classic":
        item = {"name": "Классический бургер 🍔", "price": 300}
    elif call.data == "burger_cheese":
        item = {"name": "Чизбургер �🍔", "price": 350}
    elif call.data == "burger_veggie":
        item = {"name": "Вег бургер 🥗🍔", "price": 320}

    # Добавляем в корзину
    user_carts[user_id].append(item)

    bot.answer_callback_query(call.id, f"{item['name']} добавлен в корзину!")


@bot.message_handler(func=lambda message: message.text == "Корзина 🛒")
def show_cart(message):
    user_id = message.from_user.id

    if user_id not in user_carts or len(user_carts[user_id]) == 0:
        bot.send_message(message.chat.id, "Ваша корзина пуста")
        return

    cart_text = "🛒 Ваша корзина:\n\n"
    total = 0

    for item in user_carts[user_id]:
        cart_text += f"{item['name']} - {item['price']}₽\n"
        total += item['price']

    cart_text += f"\nИтого: {total}₽"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Очистить корзину")
    btn2 = types.KeyboardButton("Оформить заказ")
    btn3 = types.KeyboardButton("Назад 🔙")
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, cart_text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Очистить корзину")
def clear_cart(message):
    user_id = message.from_user.id
    user_carts[user_id] = []
    bot.send_message(message.chat.id, "Корзина очищена")


@bot.message_handler(func=lambda message: message.text == "Назад 🔙")
def back_to_main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Посмотреть товары")
    btn2 = types.KeyboardButton("Корзина 🛒")
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, "Главное меню:", reply_markup=markup)


bot.polling()