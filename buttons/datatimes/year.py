
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import db

# def database_id_number():
#     return db.fuel_output_row_id()


def month(index):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("January", callback_data=f"month|January|01|{index}")
    btn2 = InlineKeyboardButton("February", callback_data=f"month|February|02|{index}")
    btn3 = InlineKeyboardButton("March", callback_data=f"month|March|03|{index}")
    btn4 = InlineKeyboardButton("April", callback_data=f"month|April|04|{index}")
    btn5 = InlineKeyboardButton("May", callback_data=f"month|May|05|{index}")
    btn6 = InlineKeyboardButton("June", callback_data=f"month|June|06|{index}")
    btn7 = InlineKeyboardButton("July", callback_data=f"month|July|07|{index}")
    btn8 = InlineKeyboardButton("August", callback_data=f"month|August|08|{index}")
    btn9 = InlineKeyboardButton("September", callback_data=f"month|September|09|{index}")
    btn10 = InlineKeyboardButton("October", callback_data=f"month|October|10|{index}")
    btn11 = InlineKeyboardButton("November", callback_data=f"month|November|11|{index}")
    btn12 = InlineKeyboardButton("December", callback_data=f"month|December|12|{index}")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12)
    return markup


def month_name(month_number, index):
    markup = InlineKeyboardMarkup(row_width=5)
    btns = []
    bosh = 1
    oxir = None
    database_id_number = db.fuel_output_row_id()
    if month_number == "01":
        oxir = 31
    if month_number == "02":
        oxir = 28
    if month_number == "03":
        oxir = 31
    if month_number == "04":
        oxir = 30
    if month_number == "05":
        oxir = 31
    if month_number == "06":
        oxir = 30
    if month_number == "07":
        oxir = 31
    if month_number == "08":
        oxir = 31
    if month_number == "09":
        oxir = 30
    if month_number == "10":
        oxir = 31
    if month_number == "11":
        oxir = 30
    if month_number == "12":
        oxir = 31
    for day in range(bosh, oxir + 1):
        btn = InlineKeyboardButton(str(f"{day}"), callback_data=str(f"{day}.{month_number}.2026.{database_id_number}.{index}"))
        btns.append(btn)
    markup.add(*btns)

    return markup
