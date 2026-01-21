from telebot.types import Message

from buttons import managers_buttons
from data import db, bot


DATA = {}
DATA_DRIVER = {}

# Databasedan haydovchini JShShIR larini olib ro'yxat qilib qaytaradigon funksiya

def all_driver_number():
    driver_number = db.select_all_driver_id()
    ids_num = []
    for i in driver_number:
        ids_num.append(i[0])
    return ids_num


# Databasega haydovchini ma'lumotlarini qo'shish jarayonini tekshirish

def check_driver_number_id(message: Message):
    chat_id = message.chat.id
    telegram_id = message.from_user.id
    driver_number = message.text
    ids_num = all_driver_number()
    if isinstance(driver_number, str):
        if len(driver_number) == 14:
            if driver_number.isdigit():
                if int(driver_number) in ids_num:
                    db.update_table_driver(telegram_id, driver_number)
                    bot.send_message(chat_id, "Chat id ma'lumotlar omboriga muvaffaqiyatli qo'shildi")
                else:
                    bot.send_message(chat_id, "Kiritilgan JShShIR ma'lumotlar omboridan topilmadi"
                                              "Ilimos Menegerga murojat qiling\n"
                                              "@Muhammad_aziz06\n")
            else:
                bot.send_message(chat_id, "Iltimos JShShIRni raqamlar bilan yozing harf ishlatmang!!!\n"
                                        "Qayta urunish uchun /start ni bosing")

        else:
            bot.send_message(chat_id, f"Kiritilgan JShShIR {len(driver_number)} xonalik ekan, 14 xonalik bo'lishi kerak\n"
                                    "Qayta urunish uchun /start ni bosing")

    else:
        bot.send_message(chat_id, "JShShIRni matn ko'rinishida yozing, rasm yoki video tashlamang!!\n"
                                "Qayta urunish uchun /start ni bosing")


# Databasega avtomashinani kiritishni jarayonini tekshirish

def check_machines_number(message: Message):
    chat_id = message.chat.id
    number = message.text
    if type(number)  == str:
        DATA["avto_number"] = number

        msg = bot.send_message(chat_id, "Avtomashina rusummini kiriting")
        bot.register_next_step_handler(msg, check_machines_rusum)

def check_machines_rusum(message: Message):
    chat_id = message.chat.id
    rusm = message.text
    number = DATA["avto_number"]
    db.insert_into_avto_tigach(number, rusm)
    del DATA["avto_number"]
    bot.send_message(chat_id, "Ma'lumot saqlandi")


# Databasega haydovchini qo'shish jarayonini tekshirish

def check_driver_number(message: Message):
    chat_id = message.chat.id
    from_user = message.from_user.id
    driver_number = message.text
    if isinstance(driver_number, str):
        if len(driver_number) == 14:
            DATA_DRIVER[from_user] = {"drive_number" :driver_number}
            msg = bot.send_message(chat_id, f"Haydovchi F.I.SHni kiriting")
            bot.register_next_step_handler(msg, check_driver_name)
        else:
            bot.send_message(chat_id, "Xato boshidan boshla")

    else:
        bot.send_message(chat_id, "JShShIRni matn korinishida kiriting va boshidan boshlang")

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


# Databasega meneger qo'shish jarayonini tekshirish

def chek_parol(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    fullname = message.from_user.full_name

    parol = message.text
    if isinstance(parol, str):
        if parol == '523050770800':
            db.insert_meneger(from_user_id, fullname)
            bot.send_message(chat_id, "Managerlar ro'yxatiga qo'shildingiz tabriklayman")
        else:
            bot.send_message(chat_id, "error kod 404")
    else:
        bot.send_message(chat_id, "error kod 404")


# Databasega admin qo'shishni tekshirish

def check_admin_id(message: Message):
    chat_id = message.chat.id
    from_user = message.from_user.full_name
    admin_id = message.text
    if isinstance(admin_id, str):
        if 7 < len(admin_id) < 14:
            db.insert_admin(admin_id, from_user)
            bot.send_message(chat_id, "Admin muvaffaqiyatli qo'shildi")
        else:
            bot.send_message(chat_id, "7 xona va 14 xona orasidagi xonaga teng bolsin")
    else:
        bot.send_message(chat_id, "faqat matn kiriting, rasm va video tashlama")


# Databasedan adminni o'chirish jarayonini tekshirish

def del_admin(message: Message):
    chat_id = message.chat.id
    admin_id = message.text
    if isinstance(admin_id, str):
        if 7 < len(admin_id) < 14:
            db.delete_admin(admin_id)
            bot.send_message(chat_id, "Admin muvaffaqiyatli o'chirildi")
        else:
            bot.send_message(chat_id, "7 xona va 14 xona orasidagi xonaga teng bolsin")
    else:
        bot.send_message(chat_id, "faqat matn kiriting, rasm va video tashlama")

def del_manager(message: Message):
    chat_id = message.chat.id
    parol = message.text
    if isinstance(parol, str):
        if parol == '52305077080043':
            bot.send_message(chat_id, "Qaysi Managerni o'chirmoqchi bo'lsangiz ustiga bosing", reply_markup=managers_buttons())
        else:
            bot.send_message(chat_id, "error kod 404")
    else:
        bot.send_message(chat_id, "error kod 404")
