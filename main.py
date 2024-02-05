import telebot
from telebot import types
import webbrowser
import psycopg2
import datetime
bot = telebot.TeleBot('6619693167:AAHUr5kfzBIg0c_s8VHFrqPTeEUxofYPCMk')
conn = psycopg2.connect(
        dbname="chatebana",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
     )
cur = conn.cursor()

# cur.execute("SELECT * FROM ваша_таблица")
# rows = cur.fetchall()
# for row in rows:
#  print(row)
#
   # Закрытие курсора и подключения
   # cur.close()
   # conn.close()

#Обработчик команды /site and /website
@bot.message_handler(commands= ['site', 'website'])
def site(message):
    webbrowser.open('https://prokudry.ru/')

# Обработчик команды /help
@bot.message_handler(commands = ['help'])
def main(message):
    bot.send_message(message.chat.id, '<em><u>Cпасение утопающих — дело рук самих утопающих</u></em>', parse_mode='html')

def get_specialty_masters(specialty):
    cur.execute("SELECT first_name FROM masters WHERE specialty = %s ", (specialty,))
    mastersbrend = cur.fetchall()
    return [master[0] for master in mastersbrend]

def get_first_name_masters(first_name):
        cur.execute("SELECT first_name FROM masters WHERE first_name = %s ", (first_name,))
        mastersname = cur.fetchall()
        return [master[0] for master in mastersname]

def get_time_masters(order_time):
    cur.execute("SELECT order_time FROM orders2 WHERE order_time = %s ", (order_time,))
    masterstime = cur.fetchall()
    return [master[0] for master in masterstime]
def get_date_masters(order_date):
    cur.execute("SELECT order_date FROM orders2 WHERE order_date = %s ", (order_date,))
    mastersdate = cur.fetchall()
    return [master[0] for master in mastersdate]

def get_ordersdatetime_for_master(datezapic, timezapic):
    cur.execute(
            "SELECT order_date FROM orders2 WHERE order_date =  %s AND order_time =  %s",(datezapic, timezapic,))
    orders = cur.fetchall()
    return orders

    # возвращаем список имен мастеров
def get_orders_for_master(chosen_master):
    cur.execute("SELECT order_date FROM orders2 inner join masters on orders2.master_id = public.masters.id WHERE masters.first_name = %s group by order_date",(chosen_master,))
    orders = cur.fetchall()
    return orders
def get_orderstime_for_master(orders_date):
    cur.execute("SELECT order_time FROM orders2 inner join masters on orders2.master_id = public.masters.id WHERE order_date = %s group by order_time",(orders_date,))
    orders1 = cur.fetchall()
    return orders1

# def get_specialty_masters(specialty):
#     cur.execute("SELECT order_date FROM orders inner join masters on orders.master_id = public.masters.id WHERE specialty = %s ", (specialty,))
#     mastersdate = cur.fetchall()
#     return [orderdate[0] for orderdate in mastersdate]  # возвращаем список имен мастеров

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Отправка сообщения с кнопками
    keyboard = types.InlineKeyboardMarkup()
    button0 = types.InlineKeyboardButton('Перейти на сайт для записи', url = 'https://prokudry.ru/')
    button1 = types.InlineKeyboardButton(text='Прайс', callback_data='button1_pressed')
    button2 = types.InlineKeyboardButton(text='Запись', callback_data='button2_pressed')
    button3 = types.InlineKeyboardButton(text='Контакты', callback_data='button3_pressed')
    keyboard.add(button0)
    keyboard.add(button1, button2)
    keyboard.add(button3)
    file = open('./prophoto.png', 'rb')
    bot.send_photo(message.chat.id, file,
                   caption= 'Здравствуйте, {0.first_name}. Вас приветствует помощник, меня зовут Кудряшка.'.format(message.from_user))

    bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)


# Обработчик нажатия кнопок
@bot.callback_query_handler(func=lambda call: True)
def button_pressed(call):
    #Уровень первый
    #Прайс
    if call.data == 'button1_pressed':
        new_message = 'Выберите город для просмотра прайса'
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Казань', callback_data='kazan')
        new_button1 = types.InlineKeyboardButton(text='Санкт-Петербург', callback_data='piter')
        new_button2 = types.InlineKeyboardButton(text='Назад', callback_data='backmenu')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=new_message, reply_markup=new_keyboard)
   #Запись
    elif call.data == 'button2_pressed':
        new_message = 'В каком городе вы хотите записаться?'
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Казань', callback_data='kazan1')
        new_button1 = types.InlineKeyboardButton(text='Санкт-Петербург', callback_data='piter1')
        new_button2 = types.InlineKeyboardButton(text='Назад', callback_data='backmenu')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=new_message, reply_markup=new_keyboard)
    #Контакты
    elif call.data == 'button3_pressed':
        new_message = 'Контакты'
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='WhatsApp', url='https://wa.me/79668772126')
        new_button1 = types.InlineKeyboardButton(text='Telegram', url='https://t.me/witch_tusya')
        new_button2 = types.InlineKeyboardButton(text='Назад', callback_data='backmenu')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=new_message, reply_markup=new_keyboard)
    #Назад в главное меню
    elif call.data == 'backmenu':
        keyboard = types.InlineKeyboardMarkup()
        button0 = types.InlineKeyboardButton('Перейти на сайт для записи', url='https://prokudry.ru/')
        button1 = types.InlineKeyboardButton(text='Прайс', callback_data='button1_pressed')
        button2 = types.InlineKeyboardButton(text='Запись', callback_data='button2_pressed')
        button3 = types.InlineKeyboardButton(text='Контакты', callback_data='button3_pressed')
        keyboard.add(button0)
        keyboard.add(button1, button2)
        keyboard.add(button3)
        # file = open('./prophoto.png', 'rb')
        # bot.send_photo(call.message.chat.id, file,
        #                 caption='Здравствуйте, {0.first_name}. Вас приветствует помощник, меня зовут Кудряшка.'.format(
        #                     call.message.from_user))

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text ='Выберите кнопку:', reply_markup=keyboard)

    elif call.data == 'backmenu1':
        keyboard = types.InlineKeyboardMarkup()
        button0 = types.InlineKeyboardButton('Перейти на сайт для записи', url='https://prokudry.ru/')
        button1 = types.InlineKeyboardButton(text='Прайс', callback_data='button1_pressed')
        button2 = types.InlineKeyboardButton(text='Запись', callback_data='button2_pressed')
        button3 = types.InlineKeyboardButton(text='Контакты', callback_data='button3_pressed')
        keyboard.add(button0)
        keyboard.add(button1, button2)
        keyboard.add(button3)
        file = open('./prophoto.png', 'rb')
        bot.send_photo(call.message.chat.id, file,
                        caption='Здравствуйте, {0.first_name}. Вас приветствует помощник, меня зовут Кудряшка.'.format(
                            call.message.from_user))

        bot.send_message(call.message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)

    #Уровень второй
    #Прайс Казань
    elif call.data == 'kazan':
        new_message = 'Какая услуга вас интерисует?'
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Стрижка по КМ', callback_data='strizka')
        new_button1 = types.InlineKeyboardButton(text='Биозавивка', callback_data='biozavivca')
        new_button2 = types.InlineKeyboardButton(text='Окрашивание волос', callback_data='okrachivan')
        new_button3 = types.InlineKeyboardButton(text='Укладка кудрей', callback_data='ykladka')
        new_button4 = types.InlineKeyboardButton(text='Уходовые процедуры', callback_data='yxod')
        new_button5 = types.InlineKeyboardButton(text='Консультация по КМ', callback_data='konsylt')
        new_button6 = types.InlineKeyboardButton(text='Консультация online', callback_data='konsyltonline')
        new_button7 = types.InlineKeyboardButton(text='Увлажнение паром', callback_data='parom')
        new_button8 = types.InlineKeyboardButton(text='Назад', callback_data='backprice')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2, new_button3)
        new_keyboard.add(new_button4, new_button5)
        new_keyboard.add(new_button6, new_button7)
        new_keyboard.add(new_button8)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=new_message, reply_markup=new_keyboard)
    #Прайс Питер
    elif call.data == 'piter':
        new_message = 'Какая услуга вас интерисует?'
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Стрижка по КМ', callback_data='strizka')
        new_button1 = types.InlineKeyboardButton(text='Биозавивка', callback_data='biozavivca')
        new_button2 = types.InlineKeyboardButton(text='Окрашивание волос', callback_data='okrachivan')
        new_button3 = types.InlineKeyboardButton(text='Укладка кудрей', callback_data='ykladka')
        new_button4 = types.InlineKeyboardButton(text='Уходовые процедуры', callback_data='yxod')
        new_button5 = types.InlineKeyboardButton(text='Консультация по КМ', callback_data='konsylt')
        new_button6 = types.InlineKeyboardButton(text='Консультация online', callback_data='konsyltonline')
        new_button7 = types.InlineKeyboardButton(text='Увлажнение паром', callback_data='parom')
        new_button8 = types.InlineKeyboardButton(text='Назад', callback_data='backprice')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2, new_button3)
        new_keyboard.add(new_button4, new_button5)
        new_keyboard.add(new_button6, new_button7)
        new_keyboard.add(new_button8)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=new_message, reply_markup=new_keyboard)
    #Запись Казань
    elif call.data == 'kazan1':
        new_message = 'Какая услуга вас интерисует?'
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Стрижка по КМ', callback_data='strizka1')
        new_button1 = types.InlineKeyboardButton(text='Биозавивка', callback_data='biozavivca1')
        new_button2 = types.InlineKeyboardButton(text='Окрашивание волос', callback_data='okrachivan1')
        new_button3 = types.InlineKeyboardButton(text='Укладка кудрей', callback_data='ykladka1')
        new_button4 = types.InlineKeyboardButton(text='Уходовые процедуры', callback_data='yxod1')
        new_button5 = types.InlineKeyboardButton(text='Консультация по КМ', callback_data='konsylt1')
        new_button6 = types.InlineKeyboardButton(text='Консультация online', callback_data='konsyltonline1')
        new_button7 = types.InlineKeyboardButton(text='Увлажнение паром', callback_data='parom1')
        new_button8 = types.InlineKeyboardButton(text='Назад', callback_data='backzapic')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2, new_button3)
        new_keyboard.add(new_button4, new_button5)
        new_keyboard.add(new_button6, new_button7)
        new_keyboard.add(new_button8)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=new_message, reply_markup=new_keyboard)
    #Запись Питер
    elif call.data == 'piter1':
        new_message = 'Какая услуга вас интерисует?'
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Стрижка по КМ', callback_data='strizka1')
        new_button1 = types.InlineKeyboardButton(text='Биозавивка', callback_data='biozavivca1')
        new_button2 = types.InlineKeyboardButton(text='Окрашивание волос', callback_data='okrachivan1')
        new_button3 = types.InlineKeyboardButton(text='Укладка кудрей', callback_data='ykladka1')
        new_button4 = types.InlineKeyboardButton(text='Уходовые процедуры', callback_data='yxod1')
        new_button5 = types.InlineKeyboardButton(text='Консультация по КМ', callback_data='konsylt1')
        new_button6 = types.InlineKeyboardButton(text='Консультация online', callback_data='konsyltonline1')
        new_button7 = types.InlineKeyboardButton(text='Увлажнение паром', callback_data='parom1')
        new_button8 = types.InlineKeyboardButton(text='Назад', callback_data='backzapic')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2, new_button3)
        new_keyboard.add(new_button4, new_button5)
        new_keyboard.add(new_button6, new_button7)
        new_keyboard.add(new_button8)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=new_message, reply_markup=new_keyboard)
    #Назад в Прайс
    elif call.data == 'backprice':
        new_message = 'Выберите город для записи'
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Казань', callback_data='kazan')
        new_button1 = types.InlineKeyboardButton(text='Санкт-Петербург', callback_data='piter')
        new_button2 = types.InlineKeyboardButton(text='Назад', callback_data='backmenu')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=new_message, reply_markup=new_keyboard)
    #Назад в Запись
    elif call.data == 'backzapic':
        new_message = 'Выберите город для записи'
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Казань', callback_data='kazan1')
        new_button1 = types.InlineKeyboardButton(text='Санкт-Петербург', callback_data='piter1')
        new_button2 = types.InlineKeyboardButton(text='Назад', callback_data='backmenu')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=new_message, reply_markup=new_keyboard)
    #Услуги
    elif call.data == 'strizka':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button2 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuprice')
        new_keyboard.add(new_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text = 'Вы смотрите прайс на Стрижку по КМ', reply_markup=new_keyboard)
        document1 = open('strizka.pdf', 'rb')
        bot.send_document(call.message.chat.id, document1)
    elif call.data == 'biozavivca':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button2 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuprice')
        new_keyboard.add(new_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text = 'Вы смотрите прайс на Биозавивку', reply_markup=new_keyboard)
        document1 = open('biozavivca.pdf', 'rb')
        bot.send_document(call.message.chat.id, document1)
    elif call.data == 'okrachivan':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button2 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuprice')
        new_keyboard.add(new_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text = 'Вы смотрите прайс на Окрашивание', reply_markup=new_keyboard)
        document1 = open('strizkapokgm.pdf', 'rb')
        bot.send_document(call.message.chat.id, document1)
    elif call.data == 'ykladka':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button2 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuprice')
        new_keyboard.add(new_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы смотрите прайс на Укладку ', reply_markup=new_keyboard)
        document1 = open('ykladka.pdf', 'rb')
        bot.send_document(call.message.chat.id, document1)
    elif call.data == 'yxod':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button2 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuprice')
        new_keyboard.add(new_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text = 'Вы смотрите прайс Уход ', reply_markup=new_keyboard)
        document1 = open('yxodovprocedyrki.pdf', 'rb')
        bot.send_document(call.message.chat.id, document1)
    elif call.data == 'konsylt':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button2 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuprice')
        new_keyboard.add(new_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text = 'Вы смотрите прайс на Констультацию', reply_markup=new_keyboard)
        document1 = open('konsylt.pdf', 'rb')
        bot.send_document(call.message.chat.id, document1)
    elif call.data == 'konsyltonline':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button2 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuprice')
        new_keyboard.add(new_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text = 'Вы смотрите прайс на Консультацию онлайн', reply_markup=new_keyboard)
        document1 = open('konsyltonlain.pdf', 'rb')
        bot.send_document(call.message.chat.id, document1)
    elif call.data == 'parom':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button2 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuprice')
        new_keyboard.add(new_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text = 'Вы смотрите прайс на Увлажнение паром', reply_markup=new_keyboard)
        document1 = open('yxodovprocedyrki.pdf', 'rb')
        bot.send_document(call.message.chat.id, document1)

    #Назад в прайс с услугами
    elif call.data == 'backmenuprice':
        new_message = 'Какая услуга вас интерисует?'
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Стрижка по КМ', callback_data='strizka')
        new_button1 = types.InlineKeyboardButton(text='Биозавивка', callback_data='biozavivca')
        new_button2 = types.InlineKeyboardButton(text='Окрашивание волос', callback_data='okrachivan')
        new_button3 = types.InlineKeyboardButton(text='Укладка кудрей', callback_data='ykladka')
        new_button4 = types.InlineKeyboardButton(text='Уходовые процедуры', callback_data='yxod')
        new_button5 = types.InlineKeyboardButton(text='Консультация по КМ', callback_data='konsylt')
        new_button6 = types.InlineKeyboardButton(text='Консультация online', callback_data='konsyltonline')
        new_button7 = types.InlineKeyboardButton(text='Увлажнение паром', callback_data='parom')
        new_button8 = types.InlineKeyboardButton(text='Назад', callback_data='backzapic')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2, new_button3)
        new_keyboard.add(new_button4, new_button5)
        new_keyboard.add(new_button6, new_button7)
        new_keyboard.add(new_button8)
        bot.send_message(chat_id=call.message.chat.id,
                              text=new_message, reply_markup=new_keyboard)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id + 1)

    # Услуги
    elif call.data == 'strizka1':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Бренд-мастер', callback_data='brend')
        new_button1 = types.InlineKeyboardButton(text='Топ-мастер', callback_data='top')
        new_button2 = types.InlineKeyboardButton(text='Мастер 1 категории', callback_data='master1')
        new_button3 = types.InlineKeyboardButton(text='Мастер младшей категории', callback_data='mastersmall')
        new_button4 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuzapiska')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2, new_button3)
        new_keyboard.add(new_button4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали запись на Стрижку по КМ. \nДалее выберите уровень мастера к которому хотите записаться', reply_markup=new_keyboard)
    elif call.data == 'biozavivca1':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Бренд-мастер', callback_data='brend')
        new_button1 = types.InlineKeyboardButton(text='Топ-мастер', callback_data='top')
        new_button2 = types.InlineKeyboardButton(text='Мастер 1 категории', callback_data='master1')
        new_button3 = types.InlineKeyboardButton(text='Мастер младшей категории', callback_data='mastersmall')
        new_button4 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuzapiska')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2, new_button3)
        new_keyboard.add(new_button4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали запись на Биозавивку. \nДалее выберите уровень мастера к которому хотите записаться',
                              reply_markup=new_keyboard)
    elif call.data == 'okrachivan1':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Бренд-мастер', callback_data='brend')
        new_button1 = types.InlineKeyboardButton(text='Топ-мастер', callback_data='top')
        new_button2 = types.InlineKeyboardButton(text='Мастер 1 категории', callback_data='master1')
        new_button3 = types.InlineKeyboardButton(text='Мастер младшей категории', callback_data='mastersmall')
        new_button4 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuzapiska')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2, new_button3)
        new_keyboard.add(new_button4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали запись на Окрашивание. \nДалее выберите уровень мастера к которому хотите записаться',
                              reply_markup=new_keyboard)
    elif call.data == 'ykladka1':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Бренд-мастер', callback_data='brend')
        new_button1 = types.InlineKeyboardButton(text='Топ-мастер', callback_data='top')
        new_button2 = types.InlineKeyboardButton(text='Мастер 1 категории', callback_data='master1')
        new_button3 = types.InlineKeyboardButton(text='Мастер младшей категории', callback_data='mastersmall')
        new_button4 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuzapiska')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2, new_button3)
        new_keyboard.add(new_button4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали запись на Укладку. \nДалее выберите уровень мастера к которому хотите записаться',
                              reply_markup=new_keyboard)
    elif call.data == 'yxod1':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Бренд-мастер', callback_data='brend')
        new_button1 = types.InlineKeyboardButton(text='Топ-мастер', callback_data='top')
        new_button2 = types.InlineKeyboardButton(text='Мастер 1 категории', callback_data='master1')
        new_button3 = types.InlineKeyboardButton(text='Мастер младшей категории', callback_data='mastersmall')
        new_button4 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuzapiska')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2, new_button3)
        new_keyboard.add(new_button4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали запись на Уходовые процедуры. \nДалее выберите уровень мастера к которому хотите записаться',
                              reply_markup=new_keyboard)
    elif call.data == 'konsylt1':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Бренд-мастер', callback_data='brend')
        new_button1 = types.InlineKeyboardButton(text='Топ-мастер', callback_data='top')
        new_button2 = types.InlineKeyboardButton(text='Мастер 1 категории', callback_data='master1')
        new_button3 = types.InlineKeyboardButton(text='Мастер младшей категории', callback_data='mastersmall')
        new_button4 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuzapiska')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2, new_button3)
        new_keyboard.add(new_button4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали запись на Консультацию. \nДалее выберите уровень мастера к которому хотите записаться',
                              reply_markup=new_keyboard)
    elif call.data == 'konsyltonline1':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Бренд-мастер', callback_data='brend')
        new_button1 = types.InlineKeyboardButton(text='Топ-мастер', callback_data='top')
        new_button2 = types.InlineKeyboardButton(text='Мастер 1 категории', callback_data='master1')
        new_button3 = types.InlineKeyboardButton(text='Мастер младшей категории', callback_data='mastersmall')
        new_button4 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuzapiska')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2, new_button3)
        new_keyboard.add(new_button4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали запись на Консультацию. \nДалее выберите уровень мастера к которому хотите записаться',
                              reply_markup=new_keyboard)
    elif call.data == 'parom1':
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Бренд-мастер', callback_data='brend')
        new_button1 = types.InlineKeyboardButton(text='Топ-мастер', callback_data='top')
        new_button2 = types.InlineKeyboardButton(text='Мастер 1 категории', callback_data='master1')
        new_button3 = types.InlineKeyboardButton(text='Мастер младшей категории', callback_data='mastersmall')
        new_button4 = types.InlineKeyboardButton(text='Назад', callback_data='backmenuzapiska')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2, new_button3)
        new_keyboard.add(new_button4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали запись на Увлажнение паром. \nДалее выберите уровень мастера к которому хотите записаться',
                              reply_markup=new_keyboard)
    # Назад в запись с услугами
    elif call.data == 'backmenuzapiska':
        new_message = 'Какая услуга вас интерисует?'
        new_keyboard = types.InlineKeyboardMarkup()
        new_button = types.InlineKeyboardButton(text='Стрижка по КМ', callback_data='strizka1')
        new_button1 = types.InlineKeyboardButton(text='Биозавивка', callback_data='biozavivca1')
        new_button2 = types.InlineKeyboardButton(text='Окрашивание волос', callback_data='okrachivan1')
        new_button3 = types.InlineKeyboardButton(text='Укладка кудрей', callback_data='ykladka1')
        new_button4 = types.InlineKeyboardButton(text='Уходовые процедуры', callback_data='yxod1')
        new_button5 = types.InlineKeyboardButton(text='Консультация по КМ', callback_data='konsylt1')
        new_button6 = types.InlineKeyboardButton(text='Консультация online', callback_data='konsyltonline1')
        new_button7 = types.InlineKeyboardButton(text='Увлажнение паром', callback_data='parom1')
        new_button8 = types.InlineKeyboardButton(text='Назад', callback_data='backzapic')
        new_keyboard.add(new_button, new_button1)
        new_keyboard.add(new_button2, new_button3)
        new_keyboard.add(new_button4, new_button5)
        new_keyboard.add(new_button6, new_button7)
        new_keyboard.add(new_button8)
        bot.send_message(chat_id=call.message.chat.id,
                         text=new_message, reply_markup=new_keyboard)
        # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id + 1)
        # bot.send_message(call.message.chat.id, 'Назад')
        # bot.register_next_step_handler(call, on_click)

    elif call.data == 'brend':
        def get_specialty_masters(specialty):
            cur.execute("SELECT first_name FROM masters WHERE specialty = %s ", (specialty,))
            mastersbrend = cur.fetchall()
            return [master[0] for master in mastersbrend]
        mastersbrend = get_specialty_masters('Бренд-мастер')
            # Создаем кнопки с именами мастеров
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons = [telebot.types.KeyboardButton(master) for master in mastersbrend]
        keyboard.add(*buttons)

            # Отправляем сообщение с кнопками
        bot.send_message(call.message.chat.id, "Выберите мастера:", reply_markup=keyboard)
    elif call.data == 'top':
        def get_specialty_masters(specialty):
            cur.execute("SELECT first_name FROM masters WHERE specialty = %s ", (specialty,))
            mastersbrend = cur.fetchall()
            return [master[0] for master in mastersbrend]
        mastersbrend = get_specialty_masters('Топ-мастер')
        # Создаем кнопки с именами мастеров
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons = [telebot.types.KeyboardButton(master) for master in mastersbrend]
        keyboard.add(*buttons)

        # Отправляем сообщение с кнопками
        bot.send_message(call.message.chat.id, "Выберите мастера:", reply_markup=keyboard)
    elif call.data == 'master1':
        def get_specialty_masters(specialty):
            cur.execute("SELECT first_name FROM masters WHERE specialty = %s ", (specialty,))
            mastersbrend = cur.fetchall()
            return [master[0] for master in mastersbrend]
        mastersbrend = get_specialty_masters('Мастер 1 категории')
        # Создаем кнопки с именами мастеров
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons = [telebot.types.KeyboardButton(master) for master in mastersbrend]
        keyboard.add(*buttons)

        # Отправляем сообщение с кнопками
        bot.send_message(call.message.chat.id, "Выберите мастера:", reply_markup=keyboard)
    elif call.data == 'mastersmall':
        def get_specialty_masters(specialty):
            cur.execute("SELECT first_name FROM masters WHERE specialty = %s ", (specialty,))
            mastersbrend = cur.fetchall()
            return [master[0] for master in mastersbrend]
        mastersbrend = get_specialty_masters('Мастер младшей категории')
            # Создаем кнопки с именами мастеров
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        buttons = [telebot.types.KeyboardButton(master) for master in mastersbrend]
        keyboard.add(*buttons)
                # keyboard.add(telebot.types.KeyboardButton(master))

            # Отправляем сообщение с кнопками
        bot.send_message(call.message.chat.id, "Выберите мастера:", reply_markup=keyboard)





@bot.message_handler(func=lambda message: True)
def handle_chosen_master(message):
    if get_first_name_masters(first_name = message.text):

        chosen_master = message.text
        order = get_orders_for_master(chosen_master)

        inline_keyboard = types.ReplyKeyboardMarkup( resize_keyboard=True)
        order_info = []
        for date_time_tuple in order:
            date_str = date_time_tuple[0].strftime("%d.%m.%Y")
            inline_keyboard.add(types.KeyboardButton(date_str))
        bot.send_message(message.chat.id,
                         f"Вы хотите записаться к мастеру {chosen_master}. Если вы согласны, то выберите день. ",
                         reply_markup=inline_keyboard)

        # bot.send_message(message.chat.id, f"Вы хотите записаться на {chosen_master}. Если вы согласны, то выберите время. Иначе нажмите назад.", reply_markup=inline_keyboard)
        return order_info


    elif get_date_masters(order_date=message.text):
        orders_date = message.text
        order = get_orderstime_for_master(orders_date)
        buttoninline= types.InlineKeyboardMarkup()
        inline_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        order_info = []
        for date_time_tuple in order:
            time_str = date_time_tuple[0].strftime("%H:%M")
            inline_keyboard.add(types.KeyboardButton(time_str))
        button1=types.InlineKeyboardButton("Назад", callback_data= 'backmenu1')
        buttoninline.add(button1)

        bot.send_message(message.chat.id, f"Вы хотите записаться на {orders_date}.", reply_markup=inline_keyboard)
        bot.send_message(message.chat.id,"Покеда",
                         reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, "Далее не работает, просьба оплатить разработку", reply_markup = buttoninline)

        return order_info



# Обработчик для обработки нажатий на кнопки inline клавиатуры
# @bot.callback_query_handler(func=lambda call: True)
# def handle_callback_query(call):
#         bot.send_message(call.message.chat.id, f"You have chosen: {date_str}")











# def get_masters_names():
#     cur.execute("SELECT name FROM masters")
#     masters = cur.fetchall()
#     return [master[0] for master in masters]  # возвращаем список имен мастеров

    # Обработчик команды в боте


    # Назад в запись с услугами



# def on_click(message):
#    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)

# @bot.message_handler(func=lambda message: message.text =='Назад', content_types=['text'])
# def delete_message_handler(message):
#         bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
#         bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
#Обработчик команды /site and /website

#bot.polling(none_stop=True)
if __name__ == '__main__':
    bot.infinity_polling()
#bot.infinity_polling()