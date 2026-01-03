
from telebot.types import Message, BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from data import bot, db

from buttons.datatimes import month
from buttons.inline import select_fuel_id #avto_num_button

from config import ADMINS, MANAGERS


for manager_id in MANAGERS:
    bot.set_my_commands(
        commands=[
            BotCommand("admins", "Admin buyruqlari"),
            BotCommand("add_machines", "Avtomashina davlat raqamini qoshish"),
            BotCommand("add_county", "Viloyatlarni qoshish"),
            BotCommand("add_driver", "Haydovchilarni qo'shish")
        ],
        scope=BotCommandScopeChat(manager_id)
    )

bot.set_my_commands(
    commands=[
    BotCommand("start", "Botni ishga tushurish")
    ],
    scope=BotCommandScopeDefault()
)

admin_buyruqlari = ("Buyruqlar\n"
                    "/fuel_input Yoqilg'i kirim qilish\n"
                    "/fuel_output Yoqilg'i chiqim qilish")

DATA = {}
DATA_DRIVER = {}


@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    print(chat_id,"->", full_name)
    bot.send_message(chat_id, f"Assalomu alaykum {full_name}")

@bot.message_handler(commands=['admins'])
def admins(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    if chat_id in ADMINS:
        bot.send_message(chat_id, f"Assalomu alaykum {full_name}\nAdmin panelga hush kelibsiz")
        bot.send_message(chat_id, "Yoqilgi", reply_markup=select_fuel_id())

    else:
        bot.send_message(chat_id, f"Assalomu alaykum {full_name}\nAdmin panelga kirish uchun sizda ruxsat yoq")

@bot.message_handler(commands=['fuel_input'])
def drop_fuel(message: Message):
    chat_id = message.chat.id
    # if chat_id in ADMINS:
    bot.send_message(chat_id, "Qaysi oyga kirim qilmoqchisiz?", reply_markup=month())

@bot.message_handler(commands=['fuel_output'])
def drop_fuel(message: Message):
    chat_id = message.chat.id
    # if chat_id in ADMINS:
    bot.send_message(chat_id, "Qaysi oyga chiqim qilmoqchisiz?", reply_markup=month())

# @bot.message_handler(commands=['add_machines'])
# def add_machines_number(message: Message):
#     chat_id = message.chat.id
#     if chat_id in ADMINS:
#         msg = bot.send_message(chat_id, "Avtomashina davlat raqamini kiriting")
#         bot.register_next_step_handler(msg, check_machines_number)
#
# def check_machines_number(message: Message):
#     chat_id = message.chat.id
#     number = message.text
#     DATA["avto_number"] = number
#     msg = bot.send_message(chat_id, "Avtomashina rusummini kiriting")
#     bot.register_next_step_handler(msg, check_machines_rusum)
#
# def check_machines_rusum(message: Message):
#     chat_id = message.chat.id
#     rsm = message.text
#     number = DATA["avto_number"]
#     db.insert_into_avto_tigach(number, rsm)
#
#     bot.send_message(chat_id, "Ma'lumot saqlandi")


# @bot.message_handler(commands=['add_county'])
# def add_county_name(message: Message):
#     chat_id = message.chat.id
#     if chat_id in ADMINS:
#         msg = bot.send_message(chat_id, "Viloyat nomini kiriting")
#         bot.register_next_step_handler(msg, check_county_name)
#
# def check_county_name(message: Message):
#     chat_id = message.chat.id
#     county_name = message.text
#     db.insert_into_county(county_name)
#     print("Ma'lumot qoshildi")

@bot.message_handler(commands=['add_driver'])
def add_driver(message: Message):
    chat_id = message.chat.id
    if chat_id in ADMINS:
        msg = bot.send_message(chat_id, "Haydovchi shaxsiy raqamini kiriting")
        bot.register_next_step_handler(msg, check_driver_number)

def check_driver_number(message: Message):
    chat_id = message.chat.id
    from_user = message.from_user.id
    driver_number = message.text
    if isinstance(driver_number, str):
        if len(driver_number) == 14:
            DATA_DRIVER[from_user] = {"drive_number" :driver_number}
            msg = bot.send_message(chat_id, f"Haydovchi F.I.SHni kiriting")
            bot.register_next_step_handler(msg, check_driver_name)

def check_driver_name(message: Message):
    chat_id = message.chat.id
    from_user = message.from_user.id
    driver_name = message.text
    driver_number = DATA_DRIVER[from_user]["drive_number"]
    if isinstance(driver_name, str):
        db.insert_into_driver(driver_number, driver_name)
        bot.send_message(chat_id, "Ma'lumot qo'shildi")
    else:
        bot.send_message("/add_driver")
