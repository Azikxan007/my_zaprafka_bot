
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import db

# def database_id_number():
#     return db.fuel_output_row_id()


def month():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("January", callback_data="month|January|01")
    btn2 = InlineKeyboardButton("February", callback_data="month|February|02")
    btn3 = InlineKeyboardButton("March", callback_data="month|March|03")
    btn4 = InlineKeyboardButton("April", callback_data="month|April|04")
    btn5 = InlineKeyboardButton("May", callback_data="month|May|05")
    btn6 = InlineKeyboardButton("June", callback_data="month|June|06")
    btn7 = InlineKeyboardButton("July", callback_data="month|July|07")
    btn8 = InlineKeyboardButton("August", callback_data="month|August|08")
    btn9 = InlineKeyboardButton("September", callback_data="month|September|09")
    btn10 = InlineKeyboardButton("October", callback_data="month|October|10")
    btn11 = InlineKeyboardButton("November", callback_data="month|November|11")
    btn12 = InlineKeyboardButton("December", callback_data="month|December|12")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12)
    return markup


def month_name(month_number):
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
        btn = InlineKeyboardButton(str(f"{day}"), callback_data=str(f"{day}.{month_number}.2026.{database_id_number}"))
        btns.append(btn)
    btn_go_back = InlineKeyboardButton("Back", callback_data="Back_01")
    markup.add(*btns, btn_go_back)

    return markup
