from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import db

# Avtomashinani databasedan olib button shaklga ozgartirib beradi

def avto_num_button():
    markup = InlineKeyboardMarkup(row_width=3)
    result = db.select_avto_tigach()
    btns = []
    for res in result:
        number, rusun = res
        btn = InlineKeyboardButton(f"{number} | {rusun}", callback_data=f"{number}")
        btns.append(btn)
    markup.add(*btns)
    return markup

def del_avto_num_button():
    markup = InlineKeyboardMarkup(row_width=3)
    result = db.select_avto_tigach()
    btns = []
    for res in result:
        number, rusun = res
        btn = InlineKeyboardButton(f"{number} | {rusun}", callback_data=f"{number}|del3")
        btns.append(btn)
    markup.add(*btns)
    return markup


# Viloyat nomlarini databaseda olib button shakliga ozgartirib beradi

def county_button():
    markup = InlineKeyboardMarkup(row_width=2)
    result = db.select_county()
    btns = []
    for res in result:
        for county in res:
            btn = InlineKeyboardButton(f"{county}", callback_data=f"{county}")
            btns.append(btn)
    markup.add(*btns)
    return markup

def del_county_button():
    markup = InlineKeyboardMarkup(row_width=2)
    result = db.select_county()
    btns = []
    for res in result:
        for county in res:
            btn = InlineKeyboardButton(f"{county}", callback_data=f"{county}|del1")
            btns.append(btn)
    markup.add(*btns)
    return markup


# Xaydovchilarni databasedan olib button shaklga otkazib beradi

def driver_button():
    markup = InlineKeyboardMarkup(row_width=2)
    result = db.select_driver()
    btns = []
    for res in result:
        id_number, full_name = res
        try:
            f = full_name.split(" ")[0]
            i = full_name.split(" ")[1]
        except Exception as a:
            f, i, s, h = full_name.split(" ")
        btn = InlineKeyboardButton(f"{f} {i}", callback_data = f"driver:{id_number}")
        btns.append(btn)
    markup.add(*btns)
    return markup

def del_driver_button():
    markup = InlineKeyboardMarkup(row_width=2)
    result = db.select_driver()
    btns = []
    for res in result:
        id_number, full_name = res
        try:
            f = full_name.split(" ")[0]
            i = full_name.split(" ")[1]
        except Exception as a:
            f, i, s, h = full_name.split(" ")
        btn = InlineKeyboardButton(f"{f} {i}", callback_data = f"{id_number}|del2")
        btns.append(btn)
    markup.add(*btns)
    return markup





def selection_yes_no_button_sender():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("Yes", callback_data="Yes_sender")
    btn2 = InlineKeyboardButton("No", callback_data="No_sender")
    markup.add(btn1, btn2)
    return markup

def selection_yes_no_button_receiver():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("Yes", callback_data="Yes_receiver")
    btn2 = InlineKeyboardButton("No", callback_data="No_receiver")
    markup.add(btn1, btn2)
    return markup

def select_fuel_id():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("Chiqim qilish", callback_data="fuel_output")
    btn2 = InlineKeyboardButton("Kirim qilish", callback_data="fuel_input")
    markup.add(btn1, btn2)
    return markup

def quantity_litr_buttons(current_quantity=0, amount=None, action=None):


    quantity = current_quantity
    if action == "plus":
        quantity += amount
    if action == "minus":
        quantity -= amount

    markup = InlineKeyboardMarkup(row_width=4)
    btn1 = InlineKeyboardButton("-1", callback_data="quantity|1|minus")
    btn2 = InlineKeyboardButton("-10", callback_data="quantity|10|minus")
    btn3 = InlineKeyboardButton("-100", callback_data="quantity|100|minus")
    btn4 = InlineKeyboardButton("-1000", callback_data="quantity|1000|minus")
    btn = InlineKeyboardButton(f"{quantity}", callback_data=f"quantity|{quantity}")
    btn5 = InlineKeyboardButton("+1", callback_data="quantity|1|plus")
    btn6 = InlineKeyboardButton("+10", callback_data="quantity|10|plus")
    btn7 = InlineKeyboardButton("+100", callback_data="quantity|100|plus")
    btn8 = InlineKeyboardButton("+1000", callback_data="quantity|1000|plus")
    markup.add(btn1, btn2, btn3, btn4)
    markup.add(btn)
    markup.add(btn5, btn6, btn7, btn8)
    return markup


def quantity_distance_buttons(current_distance=0, amount=None, action=None):


    quantity = current_distance
    if action == "plus":
        quantity += amount
    if action == "minus":
        quantity -= amount

    markup = InlineKeyboardMarkup(row_width=6)
    btn1 =  InlineKeyboardButton("-1", callback_data="distance|quantity|1|minus")
    btn2 =  InlineKeyboardButton("-10", callback_data="distance|quantity|10|minus")
    btn3 =  InlineKeyboardButton("-100", callback_data="distance|quantity|100|minus")
    btn4 =  InlineKeyboardButton("-1000", callback_data="distance|quantity|1000|minus")
    btn5 =  InlineKeyboardButton("-10000", callback_data="distance|quantity|10000|minus")
    btn6 =  InlineKeyboardButton("-100000", callback_data="distance|quantity|100000|minus")
    btn7 =  InlineKeyboardButton(f"{quantity}", callback_data=f"distance|quantity|{quantity}")
    btn8 =  InlineKeyboardButton("+1", callback_data="distance|quantity|1|plus")
    btn9 =  InlineKeyboardButton("+10", callback_data="distance|quantity|10|plus")
    btn10 = InlineKeyboardButton("+100", callback_data="distance|quantity|100|plus")
    btn11 = InlineKeyboardButton("+1000", callback_data="distance|quantity|1000|plus")
    btn12 = InlineKeyboardButton("+10000", callback_data="distance|quantity|10000|plus")
    btn13 = InlineKeyboardButton("+100000", callback_data="distance|quantity|100000|plus")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    markup.add(btn7)
    markup.add(btn8, btn9, btn10, btn11, btn12, btn13)
    return markup

def managers_buttons():
    admins_id = db.select_all_admins()
    markup = InlineKeyboardMarkup(row_width=1)
    for admin in admins_id:
        btn = InlineKeyboardButton(text=admin, callback_data=f"del4|admin|{admin}")
        markup.add(btn)
    return markup
