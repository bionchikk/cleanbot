import sqlite3 as sl
from datetime import datetime, timedelta,date
from telebot import types


def add_users(firstname,secondmnme,tel,adress,telegramm_id):
    con = sl.connect("your_bd_name.db")
    with con:
        con.execute("""
                    INSERT INTO Users (firstname, secondname, tel, adress,telegramm_id) 
                    VALUES (?, ?, ?, ?,?);
                """, (firstname ,secondmnme,tel,adress,str(telegramm_id)))


def find_user_by_id(tg_id):
    con = sl.connect("your_bd_name.db")
    with con:
        cursor = con.cursor()
        cursor.execute("""
        SELECT EXISTS(SELECT 1 FROM Users WHERE telegramm_id = ?)
    """, (tg_id,))
    result = cursor.fetchone()[0]
    return bool(result)

def get_all_info_users(tg_id):
    con = sl.connect("your_bd_name.db")
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Users WHERE telegramm_id= ?", (tg_id,))
    result = cursor.fetchone()
    return result


def select_all_staff():
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT second_name FROM Staff""")

    result = cursor.fetchone()
    return result[0]

select_all_staff()

def add_order(tg_id_user, tg_id_staff, price, status,day):
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Orders (id_client, id_staff, price, status,day)
        VALUES (
            (SELECT id FROM Users WHERE telegramm_id = ?), 
            (SELECT id FROM Staff WHERE tg_id = ?), 
            ?, 
            ?,?
        )
    """, (tg_id_user, tg_id_staff, price, status,day))

    conn.commit()
    conn.close()

def get_number_of_order(tg_id_user, tg_id_staff, price, status,day):
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT id FROM Orders 
    WHERE id_client = (SELECT id FROM Users WHERE telegramm_id = ?)
    AND id_staff = (SELECT id FROM Staff WHERE tg_id = ?)
    AND price = ?
    AND status = ?
    AND day = ?
""", (tg_id_user, tg_id_staff, price, status,day))
    result = cursor.fetchone()

    return result

def add_fidback(user_id,order_id,feedback,rating):
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Users WHERE telegramm_id = ?", (user_id,))
    client_id = cursor.fetchone()
    if client_id:
        cursor.execute("""INSERT INTO Feedbacks (id_order, id_client, feedback, rating) 
                                         VALUES (?, ?, ?, ?)""",
                       (order_id, client_id[0], feedback, rating))
        conn.commit()
        conn.close()
        return True
    return False

def get_all_orders():
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Orders WHERE status = 'Выполнен'")
    count = cursor.fetchone()[0]
    conn.close()

    return count


def count_orders_last_month():
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    end_date = datetime.now().replace(day=1)
    start_date = end_date - timedelta(days=30)
    cursor.execute("SELECT COUNT(*) FROM Orders WHERE status = 'Выполнен' AND day BETWEEN ? AND ?",
                   (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))

    count = cursor.fetchone()[0]
    conn.close()

    return count

def calculate_total_profit():
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(price) AS total_profit
        FROM Orders
        WHERE status = 'Выполнен'
    """)
    total_profit = cursor.fetchone()[0]
    conn.close()
    return total_profit

def calculate_profit_last_month():
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    end_date = datetime.now().replace(day=1)
    start_date = end_date - timedelta(days=30)
    cursor.execute("SELECT SUM(price) AS total_profit FROM Orders WHERE status = 'Выполнен' AND day BETWEEN ? AND ?",
                   (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
    profit_last_month = cursor.fetchone()[0]
    conn.close()

    return profit_last_month
def update_order(id_order,status):
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE Orders
    SET status =?
    WHERE id = ?""",(status,id_order,))
    conn.commit()
    conn.close()


def get_second_name(id):
    con = sl.connect("your_bd_name.db")
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT second_name FROM staff WHERE tg_id= ?", (id,))
    result = cursor.fetchone()
    return result[0]


def add_occupation(id_staff, day_of_week, start_hour_str, duration_hours, id_order):
    try:
        conn = sl.connect("your_bd_name.db")
        cursor = conn.cursor()

        work_hours = ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]

        sql = '''INSERT INTO shedule (id_staff, day_of_week, "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", id_order) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

        start_hour = datetime.strptime(start_hour_str, "%H:%M").hour
        start_index = work_hours.index(f"{start_hour}:00")

        occupation_values = [0] * start_index
        occupation_values += [1 if f"{start_hour + i}:00" in work_hours else 0 for i in range(duration_hours)]

        occupation_values += [0] * (8 - len(occupation_values))



        cursor.execute(sql, (id_staff, day_of_week, *occupation_values, str(id_order)))

        conn.commit()

    except sl.Error as e:
        print("Ошибка при добавлении занятости:", e)
    finally:
        if conn:
            conn.close()

def add_new_shedule(staff_id):
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    today = date.today()
    cursor.execute(
        "INSERT INTO shedule (id_staff, day_of_week, '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', id_order) VALUES (?, ?, 0, 0, 0, 0, 0, 0, 0, 0, NULL)",
        (staff_id, today))
    conn.commit()
    conn.close()



def get_free_staff_id(day_of_week, start_time, duration_hours):

    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    query = f"SELECT id_staff FROM shedule WHERE day_of_week = ? AND \"{start_time}\" = 0"
    for i in range(1, duration_hours):
        next_time_slot = f"{int(start_time.split(':')[0]) + i}:00"
        query += f" AND \"{next_time_slot}\" = 0"
    cursor.execute(query, (day_of_week,))
    available_staff_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return available_staff_ids[0]


def get_available_dates_and_times():
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    today = datetime.now().date()
    end_of_week = today + timedelta(days=6 - today.weekday())  
    next_week_start = end_of_week + timedelta(days=1)  
    next_week_end = next_week_start + timedelta(days=4) 

    available_dates = []
    for i in range(7):
        current_date = today + timedelta(days=i)
        if current_date.weekday() < 5: 
            formatted_date = current_date.strftime("%Y-%m-%d")
            cursor.execute("SELECT COUNT(*) FROM shedule WHERE day_of_week = ?", (formatted_date,))
            count = cursor.fetchone()[0]
            if count < 8: 
                available_dates.append(formatted_date)

    for i in range((next_week_end - next_week_start).days + 1):
        current_date = next_week_start + timedelta(days=i)
        if current_date.weekday() < 5:  
            formatted_date = current_date.strftime("%Y-%m-%d")
            cursor.execute("SELECT COUNT(*) FROM shedule WHERE day_of_week = ?", (formatted_date,))
            count = cursor.fetchone()[0]
            if count < 8: 
                available_dates.append(formatted_date)

    date_keyboard = generate_date_keyboard(available_dates)

    return date_keyboard

def generate_date_keyboard(available_dates):
    keyboard = types.InlineKeyboardMarkup()
    for date in available_dates:
        callback_data = "date_" + date
        keyboard.add(types.InlineKeyboardButton(text=date, callback_data=callback_data))
    return keyboard

def get_available_times(date):
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM shedule WHERE day_of_week = ?", (date,))
    schedule_data = cursor.fetchone()
    if schedule_data is not None:
        available_times = []
        for time, availability in zip(["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"],
                                      schedule_data[3:]):
            if availability == 0:
                available_times.append(time)
        return available_times
    else:
        return ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00",
                "15:00"]  


def time_keyboard(available_times):
    keyboard = types.InlineKeyboardMarkup()
    for time in available_times:
        callback_data = "time_" + time
        keyboard.add(types.InlineKeyboardButton(text=time, callback_data=callback_data))
    return keyboard
def get_all_orders_by_user(user_id):
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM orders  WHERE id_client = (SELECT id FROM Users WHERE telegramm_id = ?)", (user_id,))
    data = cursor.fetchall()
    return data



def get_tools(amount_gl,amount_cl,amount_vc):
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    cursor.execute("""
            UPDATE Tools
            SET Gloves = Gloves - ?,
             Cloth = Cloth - ?,
             "Vacuum cleaner" = "Vacuum cleaner"-?
        """, (amount_gl, amount_cl,amount_vc))

    conn.commit()
    conn.close()

def return_tools():
    conn = sl.connect("your_bd_name.db")
    cursor  =conn.cursor()
    cursor.execute(""" UPDATE Tools
                        SET "Vacuum cleaner" = "Vacuum cleaner"+2""")
    conn.commit()
    conn.close()


def seelct_all_tools():
    conn = sl.connect("your_bd_name.db")
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM Tools""")
    data = cursor.fetchall()
    conn.commit()
    conn.close()

    return data









