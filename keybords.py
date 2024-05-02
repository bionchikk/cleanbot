
from datetime import datetime, timedelta
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def clean_room():
    rooms_list = ["Комната", "Кухня", "Санузел", "Коридор"]
    clean_room_list = InlineKeyboardMarkup()
    for rooms in rooms_list:
        clean_room_list.add(InlineKeyboardButton(rooms, callback_data=rooms))
    return clean_room_list


def yes_no_markup():
    yes_no_markup = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton("Да", callback_data='yes')
    no_button = InlineKeyboardButton("Нет", callback_data='no')
    yes_no_markup.row(yes_button, no_button)
    return yes_no_markup



def order_markup():
    order_button = ["Простой калькулятор",  "Калькулятор цены после ремонта"]
    order_markup = InlineKeyboardMarkup()
    for order in order_button:
        order_markup.add(InlineKeyboardButton(order, callback_data=order))
    return order_markup


def order_rooms():
    order_rooms = InlineKeyboardMarkup()
    for order in range(1, 5 + 1):
        if order == 1:
            text = f"{order} комната🧹"
            x = "rooms" + str(order)
            print(x)
            order_rooms.add(InlineKeyboardButton(text=text, callback_data="rooms" + str(order)))
        else:
            text = f"{order} комнат🧹"
            order_rooms.add(InlineKeyboardButton(text=text, callback_data="rooms" + str(order)))
    return order_rooms


def get_order():
    get_order = InlineKeyboardMarkup()
    order_get_button = InlineKeyboardButton("Заказать", callback_data="order_get")
    order_not_button = InlineKeyboardButton("Вернусь позже", callback_data="not_order")
    get_order.add(order_get_button, order_not_button)
    return get_order


def ready_for_order():
    ready_for_order = InlineKeyboardMarkup()
    ready_for_order_button = InlineKeyboardButton("Оформить заказ", callback_data='ready_for_order')
    ready_for_order.add(ready_for_order_button)
    return ready_for_order

def info_button():
    info_button = InlineKeyboardMarkup()
    ready_for_order_button = InlineKeyboardButton("Оформить заказ", callback_data='ready_for_order')
    button_info = InlineKeyboardButton("Информация о уборке", callback_data='info_clean')
    menu_button = InlineKeyboardButton("Меню", callback_data="menu")
    info_button.add(button_info, ready_for_order_button,menu_button)
    return info_button


def accept_order():
    accept_order = InlineKeyboardMarkup()
    accept_button = InlineKeyboardButton("Принять", callback_data="accept")
    accept_order.add(accept_button)
    return accept_order

def ready_order():
    ready_order_markup = InlineKeyboardMarkup()
    ready_order_button = InlineKeyboardButton("Заказ выполнен", callback_data="order_ready")
    ready_order_markup.add(ready_order_button)
    return ready_order_markup

def answer_keyboard():
    answer_keybord = InlineKeyboardMarkup()
    ans_yes = InlineKeyboardButton("ДА", callback_data="yes_ans")
    ans_no = InlineKeyboardButton("Нет", callback_data="no_ans")
    answer_keybord.add(ans_no, ans_yes)
    return answer_keybord

def repair_rooms():
    repair_rooms = InlineKeyboardMarkup()
    for order in range(1, 5 + 1):
        if order == 1:
            text = f"{order} комната🧹"
            repair_rooms.add(InlineKeyboardButton(text=text, callback_data="repair" + str(order)))
        else:
            text = f"{order} комнат🧹"
            repair_rooms.add(InlineKeyboardButton(text=text, callback_data="repair" + str(order)))
    return repair_rooms


def toilet_order():
    toilet_order = InlineKeyboardMarkup()
    for toilet in range(1, 3 + 1):
        if toilet == 1:
            toilet_order.add(InlineKeyboardButton(f"{toilet} санузел🛀", callback_data="bath" + str(toilet)))
        else:
            toilet_order.add(InlineKeyboardButton(f"{toilet} санузла🛀", callback_data="bath" + str(toilet)))
    return toilet_order


def generate_date_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    today = datetime.now()
    for i in range(7):
        next_day = today + timedelta(days=i)
        if next_day.weekday() < 5:
            callback_data = "day_" + next_day.strftime("%Y-%m-%d")
            keyboard.add(types.InlineKeyboardButton(text=next_day.strftime("%Y-%m-%d"), callback_data=callback_data))
    return keyboard


def generate_time_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    current_time = datetime.strptime("08:00", "%H:%M")
    end_time = datetime.strptime("15:00", "%H:%M")
    while current_time <= end_time:
        callback_data = "time_" + current_time.strftime("%H:%M")
        keyboard.add((types.InlineKeyboardButton(text=current_time.strftime("%H:%M"),callback_data=callback_data)))
        current_time += timedelta(hours=1)
    return keyboard



def get_clean_often_keyboard():
    often_clean_keyboard =InlineKeyboardMarkup()
    range_clea = ["Раз в неделю(15% скидка)", "Раз в две недели(10% скидка)","Раз в месяц(7% скидка)","1 раз или первый раз"]
    for clean in range_clea:
        often_clean_keyboard.add(InlineKeyboardButton(clean,callback_data="clean_range"+str(clean)))
    return often_clean_keyboard


def get_other_options():
    options = {"Внутри холодильника":25,"Внутри духоки":25,"Внутри кухонных шкафов":25,"Помоем посуду":10,"Внутри микроволновки":20,"Погладим белье":20,"Помоем окна":15,"Уберем на болконе":20}
    options_markup = InlineKeyboardMarkup(row_width=2)
    for option, value in options.items():
        options_markup.add(InlineKeyboardButton(option, callback_data="options" + option))
    options_markup.add(InlineKeyboardButton("Вернуться к прошлому шагу",callback_data="f"))

    return options_markup

def get_menu_keyboard():
    keyboar=InlineKeyboardMarkup()
    keyboar.add(InlineKeyboardButton("Просмотреть мои заказы",callback_data="show_orders"))
    keyboar.add(InlineKeyboardButton("Перейти к расчету ",callback_data="conculate"))
    keyboar.add(InlineKeyboardButton("У меня есть вопрос",callback_data="question"))
    return keyboar



def get_rating_keybord():
    rating_markup =InlineKeyboardMarkup(row_width=5)
    for i in range(1,5+1):
        rating_markup.add(InlineKeyboardButton(i,callback_data="rating"+str(i)))
    return rating_markup

