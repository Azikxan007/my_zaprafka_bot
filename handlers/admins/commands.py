import os
from datetime import datetime

from telebot.types import Message, BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from data import bot, db


from buttons.inline import select_fuel_id, del_county_button, del_driver_button, del_avto_num_button

from handlers.admins.texthandlers import check_driver_number_id, check_machines_number, check_driver_number, chek_parol, \
    check_admin_id, check_del_admin

# 1. command.py turgan joy: /handlers/admins/
# 2. Uch marta yuqoriga chiqib asosiy papkaga boramiz: /
current_file_path = os.path.abspath(__file__)
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

# 3. Asosiy papkadan database/main.db ga yo'l chizamiz
db_path = os.path.join(base_dir, 'database', 'main.db')

# from config import ADMINS
MANAGERS = db.select_all_menegers()
ADMINS = db.select_all_admins()


for manager_id in MANAGERS:
    bot.set_my_commands(
        commands=[
            BotCommand("start", "Botni ishga tushurish"),
            BotCommand("admins", "Admin buyruqlari"),
            BotCommand("help", "O'lmaganligini tekshirish"),
            BotCommand("getdb", "Malumotlar bazasi nusxasini olish"),
            BotCommand("add_machines", "Avtomashina davlat raqamini qo'shish"),
            BotCommand("del_machines", "Avtomashina davlat raqamini o'chirish"),
            BotCommand("add_county", "Viloyatlarni qoshish"),
            BotCommand("del_county", "Viloyatlarni o'chirish"),
            BotCommand("add_driver", "Haydovchilarni qo'shish"),
            BotCommand("del_driver", "Haydovchilarni o'chirish")
        ],
        scope=BotCommandScopeChat(manager_id)

    )

bot.set_my_commands(
    commands=[
    BotCommand("start", "Botni ishga tushurish"),
    BotCommand("admins", "Admin panelga o'tish")
    ],
    scope=BotCommandScopeDefault()
)

DATA = {}
DATA_DRIVER = {}


@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    if chat_id in ADMINS:
        bot.send_message(chat_id, f"Assalomu alaykum {full_name}\n hush kelibsiz\nBiror amalni bajarish uchun /admins buyrug'ini kiriting")

    elif chat_id in MANAGERS:
        pass

    else:
        msg = bot.send_message(chat_id, f"Assalomu alaykum {full_name}\n"
                                  f"Iltimos tasdiqlanish uchun JShShIR ni kiriting")
        bot.register_next_step_handler(msg, check_driver_number_id)

@bot.message_handler(commands=['help'])
def help_message(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Men hali o'lganim yoq tirikman")


@bot.message_handler(commands=['admins'])
def admins(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    if chat_id in ADMINS or MANAGERS:
        bot.send_message(chat_id, f"Assalomu alaykum {full_name}\nAdmin panelga hush kelibsiz")
        bot.send_message(chat_id, "Yoqilgi", reply_markup=select_fuel_id())

    else:
        bot.send_message(chat_id, f"{full_name}\nAdmin panelga kirish uchun sizda ruxsat yoq")


@bot.message_handler(commands=['getdb'])
def send_db(message):
    chat_id = message.chat.id
    if chat_id in MANAGERS:
        # Fayl yo'li to'g'riligini va mavjudligini tekshirish
        if not os.path.exists(db_path):
            bot.reply_to(message, "Xato: Baza fayli topilmadi!")
            return

        try:
            with open(db_path, 'rb') as f:
                bot.send_document(
                    chat_id=chat_id,
                    document=f,
                    caption=f"Baza nusxasi\nVaqt: {datetime.now().strftime('%H:%M:%S')}",
                    timeout=60  # Katta fayllar uchun vaqtni uzaytiramiz
                )
        except Exception as e:
            bot.send_message(chat_id, f"Faylni yuborishda texnik xato: {e}")
    else:
        bot.send_message(chat_id, "Sizga bunday ma'lumot berilmaydi!!!")


@bot.message_handler(commands=['del_info'])
def del_info(message: Message):
    chat_id = message.chat.id
    if chat_id in MANAGERS:
        db.delete_table_fuel_info()
        bot.send_message(chat_id, "Yoqilgi malumotlari o'chirildi")
    else:
        bot.send_message(chat_id, "Sizga bunday malumotni boshqarishga yo'l qo'ymaymiz")


@bot.message_handler(commands=['add_machines'])
def add_machines_number(message: Message):
    chat_id = message.chat.id
    if chat_id in MANAGERS:
        msg = bot.send_message(chat_id, "Avtomashina davlat raqamini kiriting")
        bot.register_next_step_handler(msg, check_machines_number)
    else:
        bot.send_message(chat_id, "Sizga bunday ma'lumot qo'shishga ruxsat berilmaydi!!!")

@bot.message_handler(commands=['del_machines'])
def del_machines_number(message: Message):
    chat_id = message.chat.id
    if chat_id in MANAGERS:
        bot.send_message(chat_id, "Qaysi Avtomashinani ochirmoqchisiz?", reply_markup=del_avto_num_button())



@bot.message_handler(commands=['add_county'])
def add_county_name(message: Message):
    chat_id = message.chat.id
    if chat_id in MANAGERS:
        msg = bot.send_message(chat_id, "Viloyat nomini kiriting")
        bot.register_next_step_handler(msg, check_county_name)

def check_county_name(message: Message):
    chat_id = message.chat.id
    county_name = message.text
    db.insert_into_county(county_name)
    bot.send_message(chat_id, "Ma'lumot saqlandi")


@bot.message_handler(commands=['del_county'])
def del_county_name(message: Message):
    chat_id = message.chat.id
    if chat_id in MANAGERS:
        bot.send_message(chat_id, "Qaysi viloyatni ochirmoqchisiz?", reply_markup=del_county_button())




@bot.message_handler(commands=['add_driver'])
def add_driver(message: Message):
    chat_id = message.chat.id
    if chat_id in MANAGERS:
        msg = bot.send_message(chat_id, "Haydovchi shaxsiy raqamini kiriting")
        bot.register_next_step_handler(msg, check_driver_number)

@bot.message_handler(commands=['del_driver'])
def del_driver(message: Message):
    chat_id = message.chat.id
    if chat_id in MANAGERS:
        bot.send_message(chat_id, "Qaysi shafyotni ochirmoqchisiz?", reply_markup=del_driver_button())


@bot.message_handler(commands=['add_meneger'])
def add_meneger(message: Message):
    chat_id = message.chat.id
    parol = bot.send_message(chat_id, "Iltimos maxfiy kalitni kiriting")
    bot.register_next_step_handler(parol, chek_parol)



@bot.message_handler(commands=['del_admin'])
def del_admin(message: Message):
    chat_id = message.chat.id
    if chat_id in MANAGERS:
        msg = bot.send_message(chat_id, "Iltimos adminni tanlang", reply_markup=lls)
        bot.register_next_step_handler(msg, check_del_admin)
    else:
        bot.send_message(chat_id, "error kod 404")

@bot.message_handler(commands=['add_admin'])
def insert_admin(message: Message):
    chat_id = message.chat.id
    manager = MANAGERS
    if chat_id in manager:
        msg = bot.send_message(chat_id, "Iltimos adminning telegram user id raqamini kiriting")
        bot.register_next_step_handler(msg, check_admin_id)
    else:
        bot.send_message(chat_id, "error kod 404")
