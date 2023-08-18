import telebot
import os
from PIL import Image
import pytesseract
import re
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, db, firestore
from firebase_admin import initialize_app
from firebase_admin import storage

cred = credentials.Certificate('chatbot-6e1e3-firebase-adminsdk-iskiw-47ed99ac1e.json')
firebase_admin = firebase_admin.initialize_app(cred, {'databaseURL': 'https://chatbot-6e1e3.firebaseio.com'})
bot = telebot.TeleBot('5806034022:AAG6BNy-EFrE_2vWxMPvXa9MDH-YHZz0D3c')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

user_data = {}

MacBook_models = [
    "Macbook 12",
    "Macbook Air 11.6 2010-2015",
    "Macbook Air 13.3 2010-2017",
    "Macbook Air 13.3 2018-2020 M1",
    "Macbook Air 13.6 2022 M2",
    "Macbook Pro 13.3 2008-2012",
    "Macbook Pro 13.3 2016-2022",
    "Macbook Pro 13.3 Retina late 2012-2015",
    "Macbook Pro 14 2021/2023 M1/M2",
    "Macbook Pro 15.4 Retina 2016-2019",
    "Macbook Pro 15.4 Retina late 2012-2015",
    "Macbook Pro 16 2019-2020",
    "Macbook Pro 16 M1 2021/2023 M1/M2",
    "Назад"
]
phone_models = [
    "iPhone 6/6s",
    "iPhone 7/8/SE2",
    "iPhone 7+/8+",
    "iPhone X/Xs",
    "iPhone XR",
    "iPhone XS Max",
    "iPhone 11",
    "iPhone 11 Pro",
    "iPhone 11 Pro Max",
    "iPhone 12 mini",
    "iPhone 12",
    "iPhone 12 Pro",
    "iPhone 12 Pro Max",
    "iPhone 13 mini",
    "iPhone 13",
    "iPhone 13 Pro",
    "iPhone 13 Pro Maх",
    "iPhone 14",
    "iPhone 14 Pro",
    "iPhone 14 Plus",
    "Назад"
]
AirPods_models = [
    "AirPods 1/2",
    "AirPods Pro",
    "Airpods 3",
    "AirPods Pro 2",
    "Назад"
]
passport_models = [
    "Паспорт",
    "ID",
    "Назад"
]

def send_to_manager(user_id):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials.Certificate('chatbot-6e1e3-firebase-adminsdk-iskiw-47ed99ac1e.json')
    db = firestore.client()
    collection_name = 'users'
    doc_ref = db.collection(collection_name).document(user_id)

    doc_snapshot = doc_ref.get()
    print(doc_snapshot)
    target_chat_id = '-1001979094977'
    bot = telebot.TeleBot('5806034022:AAG6BNy-EFrE_2vWxMPvXa9MDH-YHZz0D3c')
    data = doc_snapshot.to_dict()
    data_user = data[user_id]

    if len(data_user) == 5:
        msg = f'''
    NEW ORDER!\n
    Name: {data_user['name']}
    Phone: {data_user['phone']}
    selected_model: {data_user['selected_model']}
    Delivery method: {data_user['delivery_method']}
    sentences_with_keyword: {data_user['sentences_with_keyword']}
    '''
    elif len(data_user) == 7:
        msg = '\n'.join([
            'NEW ORDER!',
            f"Name: {data_user['name']}'"
            f"Phone: {data_user['phone']}",
            f"Selected model: {data_user['selected_model']}",
            f"Delivery method: {data_user['delivery_method']}",
            f"Sentences with keyword: {data_user['sentences_with_keyword']}"
        ]
    '''
    bot.send_message(target_chat_id, msg)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton("Зробити замовлення"),
        telebot.types.KeyboardButton("Відповідь на запитання"),
        telebot.types.KeyboardButton("Акції та пропозиції")
    )
    bot.send_message(message.chat.id, 'Привіт, це магазин твоїх улюблених кейсів Orientalcase 🤍 Обери, що цікавить найбільше?', reply_markup=markup)
    print(user_data) 
@bot.message_handler(func=lambda message: message.text.lower() == "зробити замовлення", content_types=['text'])
def order(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton("/Телефон"),
        telebot.types.KeyboardButton("/MacBook"),
        telebot.types.KeyboardButton("/AirPods"),
        telebot.types.KeyboardButton("/Обкладинки"),
        telebot.types.KeyboardButton("Головне меню")
    )
    bot.send_message(message.chat.id, 'Готові оформити ваше замовлення. Для чого бажаєте придбати кейс?', reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == "Акції та пропозиції", content_types=['text'])
def order(message):
    sales_text = ("Наразі доступні такі акційні пропозиції:\n"
                     "• акція 1+1 = 3. При покупці будь-якого кейса з наявності в нашому шоурумі за адресою м. Київ, вул. Саксаганського, 77 з понеділка по п’ятницю з 10.00 до 19.00.\n"
                     "• при виборі кейсу з кишенею - 6 твоїх фото в подарунок.\n"
                     "• при замовлення комплекту кейсу для MacBook + кейс на телефон знижка -100 грн на комплект.")
    bot.send_message(message.chat.id, sales_text, parse_mode='Markdown')
@bot.message_handler(func=lambda message: message.text.lower() == "назад", content_types=['text'])
def back_to_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton("/Телефон"),
        telebot.types.KeyboardButton("/MacBook"),
        telebot.types.KeyboardButton("/AirPods"),
        telebot.types.KeyboardButton("/Обкладинки"),
        telebot.types.KeyboardButton("Головне меню")
    )
    bot.send_message(message.chat.id, 'Готові оформити ваше замовлення. Для чого бажаєте придбати кейс?', reply_markup=markup)
@bot.message_handler(func=lambda message: message.text.lower() == "головне меню", content_types=['text'])
def main_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton("Зробити замовлення"),
        telebot.types.KeyboardButton("Відповідь на запитання"),
        telebot.types.KeyboardButton("Акції та пропозиції")
    )
    bot.send_message(message.chat.id, 'Привіт, це магазин твоїх улюблених кейсів Orientalcase 🤍 Обери, що цікавить найбільше?', reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == 'Відповідь на запитання', content_types=['text'])
def faq(message):
    faq_text = ("Ми підготували список найпопулярніших запитань. Ознайомитись із запитаннями можна нижче. "
                "Якщо бажає дізнатись відповідь на запитання, то натисни на його номер нижче:\n"
                "/1. Можна замовити зі своїм дизайном?\n"
                "/2. Можна фото, як виглядає певний товар?\n"
                "/3. Які кейси з ременями у вас є?\n"
                "/4. У вас є повернення чи обмін?\n"
                "/5. Протиударний кейс з закритою камерою?\n"
                "/6. Зможете показати, як виглядатиме на певній моделі?\n"
                "/7. Прозорий силікон жовтіє?\n"
                "/8. Можна забрати самовивозом?\n"
                "/9. У вас є подарункове пакування?\n"
                "/10. До кейсу з кишенею йдуть фото в подарунок?\n"
                "/11. Які є варіанти комплектів?")
    
    bot.send_message(message.chat.id, faq_text, parse_mode='Markdown')
@bot.message_handler(commands=['Телефон'])
def phone(message):
    bot.send_message(message.chat.id, "Оберіть модель телефону:", reply_markup=create_phone_keyboard())
def create_phone_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [telebot.types.KeyboardButton(model) for model in phone_models]
    markup.add(*buttons)
    return markup
@bot.message_handler(func=lambda message: message.text in phone_models, content_types=['text'])
def handle_phone_model(message):
    user_id = str(message.from_user.id)
    user_data[user_id] = {}
    user_data[user_id]["selected_model"] = message.text    
    bot.send_message(message.chat.id, "Ви обрали модель: " + message.text)
    bot.send_message(message.chat.id, "Перейдіть на наш сайт за посиланням https://orientalcase.com.ua/phones, оберіть дизайн, з яким бажаєте отримати кейс, та зробіть скрін-шот. Зверніть увагу, що на скрін-шоті має бути добре видно назву дизайну, модель телефону, ціну та інші характеристики, якщо такі , або надішліть посилання з товаром, якмй ви обрали.")
@bot.message_handler(commands=['MacBook'])
def phone(message):
    bot.send_message(message.chat.id, "Оберіть модель MacBook:", reply_markup=create_MacBook_keyboard())
def create_MacBook_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [telebot.types.KeyboardButton(model) for model in MacBook_models]
    markup.add(*buttons)
    return markup
@bot.message_handler(func=lambda message: message.text in MacBook_models, content_types=['text'])
def handle_macbook_model(message):
    user_id = str(message.from_user.id)
    user_data[user_id] = {}
    user_data[user_id]["selected_model"] = message.text    
    bot.send_message(message.chat.id, "Ви обрали модель: " + message.text)
    bot.send_message(message.chat.id, "Перейдіть на наш сайт за посиланням https://orientalcase.com.ua/macbook, оберіть дизайн, з яким бажаєте отримати кейс, та зробіть скрін-шот. Зверніть увагу, що на скрін-шоті має бути добре видно назву дизайну, модель телефону, ціну та інші характеристики, якщо такі є.")
@bot.message_handler(commands=['Обкладинки'])
def phone(message):
    bot.send_message(message.chat.id, "Оберіть модель обкладинки:", reply_markup=create_passport_keyboard())
def create_passport_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [telebot.types.KeyboardButton(model) for model in passport_models]
    markup.add(*buttons)
    return markup
@bot.message_handler(func=lambda message: message.text in passport_models, content_types=['text'])
def handle_passport_model(message):
    user_id = str(message.from_user.id)
    user_data[user_id] = {}
    user_data[user_id]["selected_model"] = message.text    
    bot.send_message(message.chat.id, "Ви обрали модель: " + message.text)
    bot.send_message(message.chat.id, "Перейдіть на наш сайт за посиланням https://orientalcase.com.ua/airpods, оберіть дизайн, з яким бажаєте отримати кейс, та зробіть скрін-шот. Зверніть увагу, що на скрін-шоті має бути добре видно назву дизайну, модель телефону, ціну та інші характеристики, якщо такі є.")
@bot.message_handler(commands=['AirPods'])
def phone(message):
    bot.send_message(message.chat.id, "Оберіть модель AirPods:", reply_markup=create_AirPods_keyboard())
def create_AirPods_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [telebot.types.KeyboardButton(model) for model in AirPods_models]
    markup.add(*buttons)
    return markup
@bot.message_handler(func=lambda message: message.text in AirPods_models, content_types=['text'])
def handle_airpods_model(message):
    user_id = str(message.from_user.id)
    user_data[user_id] = {}
    user_data[user_id]["selected_model"] = message.text    
    bot.send_message(message.chat.id, "Ви обрали модель: " + message.text)
    bot.send_message(message.chat.id, "Перейдіть на наш сайт за посиланням https://orientalcase.com.ua/airpods, оберіть дизайн, з яким бажаєте отримати кейс, та зробіть скрін-шот. Зверніть увагу, що на скрін-шоті має бути добре видно назву дизайну, модель телефону, ціну та інші характеристики, якщо такі є.")
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    if message.text == "/1":
        bot.send_message(message.chat.id, "Так, звісно❤️ Надішліть його нам, щоб дизайнер підготував до друку. Також покажемо, як виглядатиме.")
    elif message.text == "2":
        bot.send_message(message.chat.id, "Так, звісно❤️ Ваш менеджер Володимир вже зовсім скоро надішле фото та відеоогляд.")
    elif message.text == "/3":
        bot.send_message(message.chat.id, "Привіт, в наявності більше 10 кольорів ремінців🙌🏼 Можна обрати прозорий, чорний кейс та будь-який принт. Зовсім скоро ваш менеджер Володимир покаже всі варіанти 🤍")
    elif message.text == "/4":
        bot.send_message(message.chat.id, "Так❣️обмін та повернення можливі протягом 14 днів на кейси з нашого каталогу у випадку, якщо вони не буди в експлуатації. На кейси з власним дизайном, на жаль, немає обміну та повернення.")
    elif message.text == "/5":
        bot.send_message(message.chat.id, "Він буде з відкритою камерою, але має захисні бортики, що виступають над нею🤍 Саме тому він надійно захищає.")
    elif message.text == "/6":
        bot.send_message(message.chat.id, "Так, наш дизайнер підготує для вас візуалізацію❤️")
    elif message.text == "/7":
        bot.send_message(message.chat.id, "Протягом 2-3 місяців 😌 Можемо запропонувати пластиковий прозорий кейс, який не жовтітиме або чорний силіконовий.")
    elif message.text == "/8":
        bot.send_message(message.chat.id, "Так, звісно 🤍 чекаємо на вас за адресою м. Київ, вул. Саксаганського, 77 пн-пт з 10 до 19. Напишіть нам, будь ласка, за годину.")
    elif message.text == "/9":
        bot.send_message(message.chat.id, "Наше стандартне пакування можна використати для подарунку, а також додаємо листівку до кожного замовлення 🤍 Зовсім скоро ваш менеджер Володимир надішле фото.")
    elif message.text == "/10":
        bot.send_message(message.chat.id, "Так, ціна кейсу 350 грн, а також 6 ваших фото йдуть в подарунок 🥰")
    elif message.text == "/11":
        bot.send_message(message.chat.id, "У нас великий вибір комплектів🙌🏼 Зовсім скоро ваш менеджер Володимир покаже всі-всі варіанти.")
    elif message.text == "Далі":
        bot.send_message(message.chat.id, "Ваше ім'я:")
        bot.register_next_step_handler(message, ask_name)
    elif message.text.startswith("http"):
        process_url(message)
def process_url(message):
    url = message.text
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title').get_text()
            price = soup.find('meta', {'itemprop': 'price'})['content']
            
            user_id = str(message.from_user.id)
            user_data[user_id] = {}
            user_data[user_id]["selected_model"] = title
            user_data[user_id]["sentences_with_keyword"] = [f"Модель: {title}", f"Ціна: {price}"]
            
            bot.send_message(message.chat.id, f"Ви обрали:\nМодель: {title}\nЦіна: {price}")
            bot.send_message(message.chat.id, "Тепер натисніть 'Далі' для продовження замовлення.", reply_markup=create_next_keyboard())
        else:
            bot.send_message(message.chat.id, "Не вдалося отримати дані з вказаного URL.")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Виникла помилка при обробці URL.")
def ocr_image(image_path, languages=['ukr', 'rus', 'eng']):
    image = Image.open(image_path)
    recognized_text = pytesseract.image_to_string(image, lang='+'.join(languages))
    return recognized_text
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    file = bot.download_file(file_path)
    photo_path = 'photo.jpg'  
    with open(photo_path, 'wb') as f:
        f.write(file)
        
    recognized_text = ocr_image(photo_path)
    os.remove(photo_path)
    
    sentences_with_keyword = get_sentences_with_keyword(recognized_text, "кейс", "грн")
    if any("кейс" in sentence.lower() for sentence in sentences_with_keyword) and any("грн" in sentence.lower() for sentence in sentences_with_keyword):
        user_id = str(message.from_user.id)
        user_data[user_id]["sentences_with_keyword"] = sentences_with_keyword
        bot.send_message(message.chat.id, "Ви обрали:\n" + "\n".join(sentences_with_keyword))
        bot.send_message(message.chat.id, "Тепер натисніть 'Далі' для продовження замовлення.", reply_markup=create_next_keyboard())
    else:
        bot.send_message(message.chat.id, "На даному фото немає назви або грошової суми. Будь ласка, киньте інше фото.")
def create_next_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("Далі"))
    markup.add(telebot.types.KeyboardButton("Назад"))
    return markup
def get_sentences_with_keyword(text, *keywords):
    keyword_pattern = r'\b(?:' + '|'.join(re.escape(keyword) for keyword in keywords) + r')\b'
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text) 
    sentences_with_keyword = [sentence for sentence in sentences if re.search(keyword_pattern, sentence, re.IGNORECASE)]
    return sentences_with_keyword
def ask_name(message):
    user_id = str(message.from_user.id)
    user_data[user_id]["name"] = message.text
    bot.send_message(message.chat.id, "Ваш номер телефону у форматі +380:")
    bot.register_next_step_handler(message, ask_phone_number)
def ask_phone_number(message):
    user_id = str(message.from_user.id)
    phone_number = message.text
    if re.match(r'^\+380\d{9}$', phone_number):
        user_data[user_id]["phone"] = phone_number
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        markup.add(
            telebot.types.KeyboardButton("Нова пошта"),
            telebot.types.KeyboardButton("Самовивіз"),
            telebot.types.KeyboardButton("Назад")
        )
        bot.send_message(message.chat.id, "Оберіть спосіб доставки:", reply_markup=markup)
        bot.register_next_step_handler(message, ask_delivery_method)
    else:
        bot.send_message(message.chat.id, "Введіть коректний номер телефону у форматі +380XXXXXXXXX:")
        bot.register_next_step_handler(message, ask_phone_number)
def create_delivery_method_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton("Нова пошта"),
        telebot.types.KeyboardButton("Самовивіз"),
        telebot.types.KeyboardButton("Назад")
    )
    return markup
def ask_delivery_method(message):
    user_id = str(message.from_user.id)
    user_data[user_id]["delivery_method"] = message.text   
    if message.text == "Нова пошта":
        bot.send_message(message.chat.id, "Введіть адресу доставки, номер телефону та ПІБ отримувача та номер відділення:")
        bot.register_next_step_handler(message, ask_delivery_address)
    else:
        bot.send_message(message.chat.id, "Дякуємо, ваше замовлення прийнято!")
        store_user_data_in_firebase(user_id, user_data)
        send_to_manager(user_id)
def ask_delivery_address(message):
    user_id = str(message.from_user.id)
    user_data[user_id]["delivery_address"] = message.text
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton("Передоплата"),
        telebot.types.KeyboardButton("Накладний платіж"),
        telebot.types.KeyboardButton("Назад")
    )
    bot.send_message(message.chat.id, "Оберіть спосіб оплати:", reply_markup=markup)
    bot.register_next_step_handler(message, ask_payment_method)
def store_user_data_in_firebase(user_id, user_data):
    try:
        user_id_str = str(user_id)
        users_collection = db.collection('users')
        new_user_doc = users_collection.document(user_id_str).set(user_data)
        print("User data stored in Firebase:", user_data)
        user_data.clear()
    except Exception as e:
        print("Error storing user data in Firebase:", e)
def ask_payment_method(message):
    user_id = str(message.from_user.id)
    user_data[user_id]["payment_method"] = message.text
    if message.text == "Передоплата":
        bot.send_message(message.chat.id, "Дякуємо, ваше замовлення прийнято! Номер для розрахунку: 5555 5555 6666 6666")
    elif message.text == "Накладний платіж":
        bot.send_message(message.chat.id, "Дякуємо, ваше замовлення прийнято!")
    store_user_data_in_firebase(user_id, user_data)
    send_to_manager(user_id)
db = firestore.client()

bot.polling()