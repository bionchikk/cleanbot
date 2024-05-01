import time

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
from info.config import BOT_TOKEN,ADMIN_CHAT_ID
from info.text import START_TEXT,INFO_LIST,ROOM_ONFO,KITCHEN_INFO,TOILET_INFO,CORIDOR_INFO,time_for_otions
from bdfile import add_users, find_user_by_id, get_all_info_users, add_order, get_number_of_order, update_order, \
    add_occupation, get_second_name, get_available_times, time_keyboard, \
    generate_date_keyboard, get_available_dates_and_times, get_all_orders_by_user, add_fidback, get_all_orders, \
    count_orders_last_month, calculate_total_profit, calculate_profit_last_month, add_new_shedule,get_free_staff_id
from google_app import update_sheet
from keybords import clean_room,yes_no_markup,order_markup,order_rooms,get_order,info_button,accept_order,ready_order,answer_keyboard,repair_rooms,toilet_order,generate_date_keyboard,generate_time_keyboard,get_clean_often_keyboard,get_menu_keyboard,get_rating_keybord


bot = telebot.TeleBot(BOT_TOKEN)
anwer_dict = {}
user_id = 0
text = ""
duration_hours = 0
date = ""
chosen_time = ""
chosen_date = ""
num_rooms = 0
number = 0
price = 0
anwer_dict={}
num_bath=0
state ={}
admin_group_id = -4136830193
selected_options = {}
text_often =''
staff_id = 0

menu_keybord = InlineKeyboardMarkup().add(InlineKeyboardButton("Меню", callback_data="menu"))
def get_other_options(user_id):
    options = {"Внутри холодильника":25, "Внутри духовки":25, "Внутри кухонных шкафов":25,
               "Помоем посуду":10, "Внутри микроволновки":20, "Погладим белье":20,
               "Помоем окна":15, "Уберем на балконе":20}

    # Получаем выбранные опции для данного пользователя
    user_options = selected_options.get(user_id, [])

    options_markup = InlineKeyboardMarkup(row_width=2)
    for option, value in options.items():
        # Если опция уже выбрана пользователем, не добавляем ее в клавиатуру
        if option not in user_options:
            options_markup.add(InlineKeyboardButton(option, callback_data="options" + option))
    options_markup.add(InlineKeyboardButton("Вернуться к прошлому шагу", callback_data="f"))
    options_markup.add(InlineKeyboardButton("Оформить заказ", callback_data="finnaly_order"))
    return options_markup

@bot.message_handler(commands=['start'])
def info(message):
    global user_id
    user_id= message.from_user.id
    users_id = message.from_user.id
    if users_id not in state:
        state.setdefault(users_id, {'state': None, 'order': {}})
    if users_id not in anwer_dict:
        anwer_dict.setdefault(users_id,{"feedbacks":None,"rating":None,"number":None})

    state[users_id]['state'] = "пользователь начал работу"
    bot.send_message(message.chat.id, f"{START_TEXT}",reply_markup=info_button())



@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    users_id = call.from_user.id
    global date
    global number
    if call.data =="info_clean":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f'{INFO_LIST}', reply_markup=clean_room())
    elif call.data=="Комната":
        state[users_id]['state'] = "пользователь изучает информацию"

        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f'{ROOM_ONFO}')
        bot.send_message(call.message.chat.id,"Желаете продолжить просмотр информации об уборке?",reply_markup=yes_no_markup())
    elif call.data=="Кухня":
        state[users_id]['state'] = "пользователь изучает информацию"
        bot.delete_message(call.message.chat.id, call.message.message_id )
        bot.send_message(call.message.chat.id, f'{KITCHEN_INFO}')
        bot.send_message(call.message.chat.id, "Желаете продолжить просмотр информации об уборке?",
                         reply_markup=yes_no_markup())
    elif call.data =="Санузел":
        state[users_id]['state'] = "пользователь изучает информацию"
        bot.delete_message(call.message.chat.id, call.message.message_id )
        bot.send_message(call.message.chat.id, f'{TOILET_INFO}')
        bot.send_message(call.message.chat.id, "Желаете продолжить просмотр информации об уборке?",
                         reply_markup=yes_no_markup())
    elif call.data=="Коридор":
        state[users_id]['state'] = "пользователь изучает информацию"
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f'{CORIDOR_INFO}')
        bot.send_message(call.message.chat.id, "Желаете продолжить просмотр информации об уборке?",
                         reply_markup=yes_no_markup())
    elif call.data=="yes":
        bot.delete_message(call.message.chat.id, call.message.message_id-1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f'{INFO_LIST}',reply_markup=clean_room())
    elif call.data=="no":
        bot.delete_message(call.message.chat.id, call.message.message_id-1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f'Вы можете расчитать ориентировочную стоимость заказа и оформить его прямо сейчас.\nВыберите нужную опцию:',reply_markup=order_markup())
    elif call.data=="Простой калькулятор":
        state[users_id]['state'] = "пользователь расчитываюе стоимость "
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id,"Выберите количесто комнат для уборки:",reply_markup=order_rooms())
    elif call.data[:-1]=="rooms":
        global num_rooms
        state[users_id]['state'] = "пользователь выбирает кол-во комнат"
        num_rooms = call.data[-1:]
        state[users_id]['order']["rooms"] = num_rooms
        bot.delete_message(call.message.chat.id, call.message.message_id)

        bot.send_message(call.message.chat.id, "Выберите количесто санузлов для уборки:", reply_markup=toilet_order())
    elif call.data[:-1]=='bath':
        global num_bath,price
        state[users_id]['state'] = "пользователь выбирает кол-во ванн"
        num_bath = call.data[-1:]
        bot.delete_message(call.message.chat.id, call.message.message_id)
        price = 31 + int(num_rooms) * 14 + int(num_bath) * 20
        state[users_id]['order']["bath"] = num_bath
        continue_markup = InlineKeyboardMarkup()
        yes_continue =InlineKeyboardButton("Продолжить",callback_data="continue")
        no_continue =InlineKeyboardButton("Оформить заказ на этом этапе ", callback_data="no_continue")
        continue_markup.add(yes_continue,no_continue)
        bot.send_message(call.message.chat.id, f"Вы выбрали  количеcnво комнат ({num_rooms}) и   количество санузлов ({num_bath}) \n"
                                               f"Ориентировочная цена :{31 + int(num_rooms) * 14 + int(num_bath) * 20}",)
        bot.send_message(call.message.chat.id,"Хотите заказать на этом этапе или продолжить выбор опций для заказа?",reply_markup=continue_markup)
    elif call.data =="no_continue":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Вы можете оформить заказ прямо сейчас:", reply_markup=get_order())
    elif call.data =="order_get":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        except telebot.apihelper.ApiException:
            pass
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiException:
            pass
        if find_user_by_id(user_id):
            date_keyboard = get_available_dates_and_times()
            bot.send_message(call.message.chat.id,"Выберите дату:",reply_markup=date_keyboard)

        else:
            name_answer = bot.send_message(call.message.chat.id,"Для дальнейшего оформления заказа нужно ввести ваши данные\nНачнем с имени:")
            bot.register_next_step_handler(name_answer, name_answers)
            state[users_id]['state'] = "пользователь вводит имя"
    elif call.data=="ready_for_order":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f'Вы можете расчитать ориентировочную стоимость заказа и оформить его прямо сейчас.\nВыберите нужную опцию:',reply_markup=order_markup())

    elif call.data=='order_ready':
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        except telebot.apihelper.ApiException:
            pass
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiException:
            pass
        update_order(number[0],"Выполнен")
        bot.send_message(chat_id=-4127668546, text=f"Заказ номер {number[0]} выполнен  ")
        bot.send_message(user_id,text="Ваш заказ выполнен,хотите оставить отзыв?",reply_markup=answer_keyboard())
    elif call.data=="not_order":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        except telebot.apihelper.ApiException:
            pass
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiException:
            pass
        state[users_id]['state'] = "пользователь не хочет заказывать"
        bot.send_message(call.message.chat.id,"Возвращайтесь скорее")
    elif call.data =="yes_ans":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        feedback=bot.send_message(call.message.chat.id,"Напишите свой отзыв:")
        bot.register_next_step_handler(feedback,feedbacks)
    elif call.data =="no_ans":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id,"Спасибо вам за заказ!Ждем вас еще!Что бы сделать новый заказ ,нажмите/start")
    elif call.data=="Калькулятор цены после ремонта":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        furniture_markup = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("Да",callback_data="f-da"),InlineKeyboardButton("Нет",callback_data="f-no"))
        bot.send_message(call.message.chat.id,"Расскажите о квартире.\nВ квартире есть мебель? ",reply_markup=furniture_markup)
    elif call.data=="f-da" :
        state[users_id]['order']['furniture'] = "да"
        bot.delete_message(call.message.chat.id, call.message.message_id)
        windows_markup = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("Да",callback_data="w-da"),InlineKeyboardButton("Нет",callback_data="w-no"))
        bot.send_message(call.message.chat.id,"Нужно вымыть окна?",reply_markup=windows_markup)
    elif call.data =='f-no':
        state[users_id]['order']['furniture'] = "нет"
        bot.delete_message(call.message.chat.id, call.message.message_id)
        windows_markup = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("Да", callback_data="w-da"),
                                                               InlineKeyboardButton("Нет", callback_data="w-no"))
        bot.send_message(call.message.chat.id, "Нужно вымыть окна?", reply_markup=windows_markup)
    elif call.data =='w-da':
        state[users_id]['order']['window'] = "да"
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id,"Выберите количество комнат",reply_markup=repair_rooms())
    elif call.data =='w-no':
        state[users_id]['order']['window'] = "нет"
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id,"Выберите количество комнат",reply_markup=repair_rooms())
    elif call.data[:-1] == "repair":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bronirovanie =InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Забронировать дату заранее",callback_data="bron"))
        num_rooms = call.data[-1:]
        bot.send_message(call.message.chat.id,f"Ваш заказ:\n Наличие мебели:{state[users_id]['order']['furniture']}\n Нужно вымыть окна:{state[users_id]['order']['window']}\n Количество комнат:{num_rooms} ",reply_markup=bronirovanie)
    elif call.data.startswith("date_"):
        global  chosen_date
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        except telebot.apihelper.ApiException:
            pass
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiException:
            pass
        chosen_date = call.data.split('_')[1]
        available_times = get_available_times(chosen_date)
        time_keyboards = time_keyboard(available_times)

        bot.send_message(call.message.chat.id, "Выберите время:", reply_markup=time_keyboards)
    elif call.data.startswith("time_"):
        global chosen_time
        global duration_hours
        global staff_id
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        except telebot.apihelper.ApiException:
            pass
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiException:
            pass
        chosen_time = call.data.split('_')[1]
        user_name = call.from_user.username or call.from_user.first_name or call.from_user.last_name
        info_user = get_all_info_users(user_id)
        duration_hours = int(state[users_id]["order"]["rooms"])*1+int(state[users_id]["order"]["bath"]*1)
        order_text = f"""
                   Заказ:
                   Количество санузлов : {num_bath}
                   Количество комнат : {num_rooms}
                  """
        if selected_options.get(users_id, None) is not None:
            for i in selected_options[users_id]:
                order_text += f"\nДоп. опция: {i}"
                price += time_for_otions[i][1]
        else:
            order_text += "\nДоп. опции не выбраны"


        order_text+= f"""\nИтоговая цена :{price}
                   Время уборки :{duration_hours} часов
                   Номер :{info_user[3]}
                   Адрес: {info_user[4]}
                   Дата: {chosen_date}
                   Время : {chosen_time}
                   Ожидайте звонка от менеджера!"""

        bot.send_message(call.message.chat.id, text=order_text,reply_markup=menu_keybord)
        staff_id = call.from_user.id
        number = get_number_of_order(user_id, staff_id, price, "Ожидается", chosen_date)


        sent=bot.send_message(chat_id=-4127668546, text=order_text + f"\nКлиент: @{user_name}",
                         reply_markup=accept_order())
        time.sleep(60)
        check_button_click(sent,order_text,number)

    elif call.data=="accept":
        staff_id = call.from_user.id
        number = get_number_of_order(user_id,staff_id,price,"Ожидается",chosen_date)
        anwer_dict[users_id]['number'] = number
        add_order(user_id, staff_id, price, "Ожидается", chosen_date)
        add_occupation(staff_id,chosen_date,chosen_time,duration_hours=duration_hours,id_order=number)
        name= get_second_name(staff_id)

        update_sheet(name,chosen_date,chosen_time,duration_hours)
        bot.send_message(chat_id=-4127668546, text=f"Заказ  номер   выполняет @{staff_id} ", reply_markup=ready_order())


    elif call.data=="continue":
        global text
        users_id = call.from_user.id
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        except telebot.apihelper.ApiException:
            pass
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiException:
            pass
        text = f"Состав заказа : кол-во комнат({state[users_id]['order']['rooms']})\n кол-во санузлов({state[users_id]['order']['bath']})"
        bot.send_message(call.message.chat.id,text)
        bot.send_message(call.message.chat.id,"Выберите частоту уборки:",reply_markup=get_clean_often_keyboard())

    elif call.data[:11]=="clean_range":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        except telebot.apihelper.ApiException:
            pass
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiException:
            pass
        global text_often
        often = call.data[11:]
        state[users_id]['order']['often'] = often
        text_often=f"\n Частота уборки {state[users_id]['order']['often']}"
        bot.send_message(call.message.chat.id,text_often)
        bot.send_message(call.message.chat.id,"Выберите дополнительные  опции для уборки",reply_markup=get_other_options(users_id))
    elif call.data=="f":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        except telebot.apihelper.ApiException:
            pass
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiException:
            pass
        bot.send_message(call.message.chat.id, "Выберите частоту уборки:", reply_markup=get_clean_often_keyboard())
        state[users_id]['order']['often'] = None
    elif call.data[:7]=="options":
        option = call.data[7:]
        handle_option_selection(user_id, option)
        bot.answer_callback_query(call.id, text="Вы выбрали: " + option)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=get_other_options(user_id))
    elif call.data =="finnaly_order":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        except telebot.apihelper.ApiException:
            pass
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiException:
            pass
        for i in selected_options[users_id]:
            text+=f"\nДополнительная опция {i}"
        bot.send_message(call.message.chat.id,text+text_often)
        bot.send_message(call.message.chat.id, "Вы можете оформить заказ прямо сейчас:", reply_markup=get_order())
    elif call.data=="menu":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        except telebot.apihelper.ApiException:
            pass
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiException:
            pass
        bot.send_message(call.message.chat.id,"Вы в меню , выберите одну из опций",reply_markup=get_menu_keyboard())
    elif call.data=="show_orders":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        except telebot.apihelper.ApiException:
            pass
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiException:
            pass
        bot.send_message(call.message.chat.id,"Здесь будут мои заказы")
        data= get_all_orders_by_user(users_id)
        if data is not None:
            all_orders = ""
            for item in data:
                id, client_id, worker_id, order_number, status, date_time = item
                if date_time is not None:
                    all_orders += f"\nНомер заказа: {order_number}, Статус: {status}, Дата: {date_time}"
                else:
                    all_orders += f"\nНомер заказа: {order_number}, Статус: {status}, Дата: не указана"
            bot.send_message(call.message.chat.id, text=all_orders, reply_markup=menu_keybord)
        else:
            bot.send_message(call.message.chat.id, text="У вас пока нет заказов", reply_markup=menu_keybord)
    elif call.data=="conculate":
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=order_markup())
    elif call.data=="question":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        except telebot.apihelper.ApiException:
            pass
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiException:
            pass
        bot.send_message(call.message.chat.id,"Если у вас возникли вопросы , напишите мне @bionchik_dima , я постараюсь вам помочь)",reply_markup=menu_keybord)

    elif call.data[:-1]=='rating':
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        except telebot.apihelper.ApiException:
            pass
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except telebot.apihelper.ApiException:
            pass

        anwer_dict[users_id]['rating'] = call.data[6:]
        add_fidback(users_id,anwer_dict[users_id]['number'][0],anwer_dict[users_id]['feedbacks'],anwer_dict[users_id]['rating'])
        bot.send_message(call.message.chat.id,"Спасибо вам за оценку!Будем вас ждать еще",reply_markup=get_menu_keyboard())


def check_button_click(message,text):
    if message.content_type == 'text':
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except telebot.apihelper.ApiException:
            pass
        number = get_number_of_order(user_id, staff_id, price, "Ожидается", chosen_date)
        id = get_free_staff_id(chosen_date,chosen_time,duration_hours)
        add_occupation(staff_id, chosen_date, chosen_time, duration_hours=duration_hours, id_order=number[0])
        user = bot.get_chat(id)
        username = user.username
        print(username)
        print(id)
        text+=f"\nЗаказ будет выполнять @{username}"
        bot.send_message(message.chat.id, text,reply_markup=ready_order())

def handle_option_selection(user_id, option):
    if user_id not in selected_options:
        selected_options[user_id] = []
    selected_options[user_id].append(option)


@bot.message_handler(func=lambda message: message.chat.id == ADMIN_CHAT_ID, commands=['all_orders'])
def show_all_orders(message):
    count = get_all_orders()
    bot.send_message(message.chat.id,f"Количество выполненых заказов за все время :{count}")



@bot.message_handler(func=lambda message: message.chat.id == ADMIN_CHAT_ID, commands=['start_day'])
def start_day(message):
    id_staff = message.from_user.id
    add_new_shedule(id_staff)
    user_name = message.from_user.username or message.from_user.first_name or message.from_user.last_name
    bot.send_message(message.chat.id,f"Пользователь @{user_name} начал рабочий день ")



@bot.message_handler(func=lambda message: message.chat.id == ADMIN_CHAT_ID, commands=['last_m_orders'])
def show_all_orders_in_last_month(message):
    count = count_orders_last_month()
    bot.send_message(message.chat.id, f"Количество выполненых заказов за последний месяц :{count}")

@bot.message_handler(func=lambda message: message.chat.id == ADMIN_CHAT_ID, commands=['profit_last_m'])
def get_profit_last_month(message):
    profit=calculate_profit_last_month()
    bot.send_message(message.chat.id, f'Прибыль за последние 30 дней : {profit}р')

@bot.message_handler(func=lambda message: message.chat.id == ADMIN_CHAT_ID, commands=['all_profit'])
def get_all_profit(message):
    profit = calculate_total_profit()
    bot.send_message(message.chat.id,f'Общая прибыль за все время: {profit}р')






#


def feedbacks(message):
    global anwer_dict
    if validate_address(message.text):
        users_id = message.from_user.id
        state[users_id]['state'] = "пользователь вводит отзыв"
        anwer_dict[users_id]["feedbacks"] = message.text
        bot.send_message(message.chat.id,"Спасибо вам за отзыв!Теперь не могли бы вы поставить оценку ?",reply_markup=get_rating_keybord())

    else:
        bot.send_message(message.chat.id,
                         "Неверный формат данных,!\nВведите корректные данные заново.")
        bot.register_next_step_handler(message, feedbacks)

def name_answers(message):
    name = message.text
    if validate_name(name):
        users_id = message.from_user.id
        state[users_id]['state'] = "пользователь вводит фамилию"
        family_answer = bot.send_message(message.chat.id,"Имя есть , теперь давайте запишем вашу фамилию:")
        bot.register_next_step_handler(family_answer,family_answers)
        anwer_dict["name_answer"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Неверный формат данных, ожидалось — Иван Иванов!\nВведите корректные данные заново.")
        bot.register_next_step_handler(message, name_answers)

def family_answers(message):
    users_id = message.from_user.id
    family = message.text
    if validate_name(family):
        anwer_dict["family_answer"]=message.text
        state[users_id]['state'] = "пользователь вводит номер"
        tel_answer = bot.send_message(message.chat.id,"С фамилией покончено , давайте запишем вам номер телефона:")
        bot.register_next_step_handler(tel_answer,tel_answers)
    else:
        bot.send_message(message.chat.id,
                         "Неверный формат данных, ожидалось — Иванов!\nВведите корректные данные заново.")
        bot.register_next_step_handler(message, family_answers)





def tel_answers(message):
    users_id = message.from_user.id
    if phone_number(message.text):
        anwer_dict["tel_answer"]=message.text
        state[users_id]['state'] = "пользователь вводит адрес"
        adres_answer = bot.send_message(message.chat.id,"Осталось последнее , введите свой адрес:")
        bot.register_next_step_handler(adres_answer,adres_answers)
    else:
        bot.send_message(message.chat.id,
                         "Неверный формат данных, ожидалось — +375xxxxxxxxx!\nВведите корректные данные заново.")
        bot.register_next_step_handler(message, tel_answers)




def adres_answers(message):
    users_id = message.from_user.id
    user_name = message.from_user.username or message.from_user.first_name or message.from_user.last_name
    if validate_address(message.text):
        anwer_dict["adres_answer"]=message.text
        state[users_id]['state'] = "пользователь зареган"
        add_users(anwer_dict["name_answer"], anwer_dict["family_answer"],anwer_dict["tel_answer"],anwer_dict["adres_answer"],user_id)
        bot.send_message(message.chat.id,"Регистрация завершена успешно!")
        bot.send_message(message.chat.id,"Выберить свободную дату для заказа:",reply_markup=generate_date_keyboard())
    else:
        bot.send_message(message.chat.id,"Неверный формат данных , повторите ввод")
        bot.register_next_step_handler(message,adres_answers)




def phone_number(phone_number):
    pattern = re.compile(r'^(\+375|375)?\s?(\d{2})[\s.-]?(\d{3})[\s.-]?(\d{2})[\s.-]?(\d{2})$')
    return bool(re.match(pattern, phone_number))
def validate_name(name):
    pattern = r'^[A-Za-zА-Яа-яЁё]+$'
    return bool(re.match(pattern, name))


def validate_address(address):
    return not address.startswith('/')

def main():
    print("run")
    bot.polling(none_stop=True,timeout=25)

if __name__ == "__main__":
    main()