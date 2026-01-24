from datetime import datetime

from telebot.types import CallbackQuery, Message
from data import bot, db
from buttons import *
from config import ADMINS

DATA = {}


def driver_user_id(driver_id_number):
    res = db.select_driver_user_id(driver_id_number)[0]
    return res


def prabeg(machine_num):
    res = db.select_fuel_output_machine_distance(machine_num)
    return res[0]

def machine_number():
    result = db.select_avto_tigach()
    numbers_list = []
    for item in result:
        numbers_list.append(item[0])

    return numbers_list

def county_func():
    result = db.select_county()
    county_list = []
    for item in result:
        county_list.append(item[0])
    return county_list

def driver_name(driver_id_number):
    result = db.select_driver_name(driver_id_number)
    return result[0]


@bot.callback_query_handler(func=lambda call: call.data == "fuel_output")
def fuel_output(call : CallbackQuery):
    chat_id = call.message.chat.id
    if chat_id in ADMINS:
        bot.send_message(chat_id, "Qaysi oyga chiqim qilmoqchisiz?", reply_markup=month(1))

@bot.callback_query_handler(func=lambda call: call.data == "fuel_input")
def fuel_input(call : CallbackQuery):
    chat_id = call.message.chat.id
    if chat_id in ADMINS:
        bot.send_message(chat_id, "Qaysi oyga kirim qilmoqchisiz?", reply_markup=month(0))






@bot.callback_query_handler(func=lambda call: call.data.split("|")[0] == "month")
def callback(call: CallbackQuery):
    chat_id = call.message.chat.id
    month_number = call.data.split("|")[2]
    index = int(call.data.split("|")[3])
    message_id = call.message.message_id
    if month_number == "01":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Yanvar oyining kunini tanlang", reply_markup=month_name(month_number, index))

    if month_number == "02":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Fevral oyining kunini tanlang", reply_markup=month_name(month_number, index))

    if month_number == "03":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Mart oyining kunini tanlang", reply_markup=month_name(month_number, index))

    if month_number == "04":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Aprel oyining kunini tanlang", reply_markup=month_name(month_number, index))

    if month_number == "05":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"May oyining kunini tanlang", reply_markup=month_name(month_number, index))

    if month_number == "06":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Iyun oyining kunini tanlang", reply_markup=month_name(month_number, index))

    if month_number == "07":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Iyul oyining kunini tanlang", reply_markup=month_name(month_number, index))

    if month_number == "08":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Avgust oyining kunini tanlang", reply_markup=month_name(month_number, index))

    if month_number == "09":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Sentyabr oyining kunini tanlang", reply_markup=month_name(month_number, index))

    if month_number == "10":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Oktyabr oyining kunini tanlang", reply_markup=month_name(month_number, index))

    if month_number == "11":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Noyabr oyining kunini tanlang", reply_markup=month_name(month_number, index))

    if month_number == "12":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Dakabr oyining kunini tanlang", reply_markup=month_name(month_number, index))




@bot.callback_query_handler(func=lambda call: call.data.count(".") == 4)
def checking_the_day(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    id_num = call.data.split(".")[-2]
    from_user_id = call.from_user.id
    day, mon, yil, row_id, index = call.data.split(".")
    selected_date = f"{day}.{mon}.{yil}"

    if id_num not in DATA:
        DATA[id_num] = {}

    DATA[id_num][from_user_id] = {"data": selected_date, "index": index}

    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text=f"Zayafka №: {id_num}\n"
                               f"{selected_date} shu sanada quyilgan mashina raqamini tanglang", reply_markup=avto_num_button())

@bot.callback_query_handler(func=lambda call: call.data == "Back_01")
def back_01(call: CallbackQuery):
    chat_id = call.message.chat.id
    back, id_num = call.data.split("|")

    bot.send_message(chat_id, "Qaysi oyga kirim qilmoqchisiz?", reply_markup=month(id_num))

@bot.callback_query_handler(func=lambda call: call.data in machine_number())
def select_machine(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    from_user_id = call.from_user.id
    machine = call.data
    id_num1 = call.message.text.split("yafka №: ")
    id_num2 = id_num1[1].split("\n")
    id_num = id_num2[0]


    if from_user_id == list(DATA[id_num])[0]:
        DATA[id_num][from_user_id]["machine"] = machine

    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text=
                          f"Zayafka №: {id_num}\n"
                          f"Sana: {DATA[id_num][from_user_id]["data"]}\n"
                          f"Mashina № {DATA[id_num][from_user_id]["machine"]}\n"
                          f"Qaysi viloyatga ketayabdi?",
                          reply_markup=county_button())


@bot.callback_query_handler(func=lambda call: "del" in call.data)
def delete_county(call: CallbackQuery):
    chat_id = call.message.chat.id
    if call.data.split("|")[1] == "del1":
        county_name = call.data.split("|")[0]
        db.delete_county(county_name)
        bot.send_message(chat_id, "Viloyat muvaffaqiyatli o'chirildi")

    elif call.data.split("|")[1] == "del2":
        driver_id = call.data.split("|")[0]
        db.delete_table_driver(driver_id)
        bot.send_message(chat_id, "Shafor muvaffaqiyatli o'chirildi")

    elif call.data.split("|")[1] == "del3":
        machine_number = call.data.split("|")[0]
        db.delete_avto_tigach(machine_number)
        bot.send_message(chat_id, "Mashina muvaffaqiyatli o'chirildi")

    elif call.data.split("|")[0] == "del4":
        admin_id = call.data.split("|")[2]
        db.delete_admin(admin_id)
        bot.send_message(chat_id, "Admin muvaffaqiyatli o'chirildi")



@bot.callback_query_handler(func=lambda call: call.data in county_func())
def check_county(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    from_user_id = call.from_user.id
    county = call.data
    id_num1 = call.message.text.split("yafka №: ")
    id_num2 = id_num1[1].split("\n")
    id_num = id_num2[0]
    if from_user_id == list(DATA[id_num])[0]:
        DATA[id_num][from_user_id]["county"] = county

    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text=
                          f"Zayafka №: {id_num}\n"
                          f"Sana: {DATA[id_num][from_user_id]["data"]}\n"
                          f"Mashina № {DATA[id_num][from_user_id]["machine"]}\n"
                          f"Manzil: {DATA[id_num][from_user_id]["county"]} ga qaysi shafyor ketayabdi\n",
                          reply_markup=driver_button())

@bot.callback_query_handler(func=lambda call: call.data.startswith("driver:"))
def check_driver(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    from_user_id = call.from_user.id
    drivers, driver_id = call.data.split(":")
    driver_chat_id = driver_user_id(driver_id)
    id_num1 = call.message.text.split("yafka №: ")
    id_num2 = id_num1[1].split("\n")
    id_num = id_num2[0]
    DATA[id_num][from_user_id]["driver_chat_id"] = driver_chat_id

    if from_user_id == list(DATA[id_num])[0]:
        DATA[id_num][from_user_id]["drivers"] = driver_id
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text=
                          f"Zayafka №: {id_num}\n"
                          f"Sana: {DATA[id_num][from_user_id]["data"]}\n"
                          f"Mashina № {DATA[id_num][from_user_id]["machine"]}\n"
                          f"Manzil: {DATA[id_num][from_user_id]["county"]}\n"
                          f"Haydovchi: {driver_name(DATA[id_num][from_user_id]["drivers"])}\n"
                          f"Mashinaga quyilgan yoqilg'i miqdorni tanlang",
                          reply_markup=quantity_litr_buttons())

@bot.callback_query_handler(func=lambda call: call.data.split("|")[0] == "quantity" and len(call.data.split("|")) == 3)
def check_quantity(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    id_num1 = call.message.text.split("yafka №: ")
    id_num2 = id_num1[1].split("\n")
    id_num = id_num2[0]
    current_quantity = int(call.message.reply_markup.keyboard[1][0].text)
    from_user_id = call.from_user.id
    quantity, amount, action = call.data.split("|")
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text=
                          f"Zayafka №: {id_num}\n"
                          f"Sana: {DATA[id_num][from_user_id]["data"]}\n"
                          f"Mashina № {DATA[id_num][from_user_id]["machine"]}\n"
                          f"Manzil: {DATA[id_num][from_user_id]["county"]}\n"
                          f"Haydovchi: {driver_name(DATA[id_num][from_user_id]["drivers"])}\n"
                          f"Mashinaga quyilgan yoqilg'i miqdorni tanlang",
                          reply_markup=quantity_litr_buttons(current_quantity=current_quantity, amount=int(amount), action=action))

@bot.callback_query_handler(func=lambda call: call.data.split("|")[0] == "quantity" and len(call.data.split("|")) == 2)
def check_quantity1(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    message_id = call.message.message_id
    current_quantity = call.message.reply_markup.keyboard[1][0].text
    id_num1 = call.message.text.split("yafka №: ")
    id_num2 = id_num1[1].split("\n")
    id_num = id_num2[0]
    try:
        spd = int(prabeg(DATA[id_num][from_user_id]["machine"]))
    except Exception as e:

        spd = 0
    DATA[id_num][from_user_id]["fuel_quantity"] = current_quantity
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text=
                          f"Zayafka №: {id_num}\n"
                          f"Sana: {DATA[id_num][from_user_id]["data"]}\n"
                          f"Mashina № {DATA[id_num][from_user_id]["machine"]}\n"
                          f"Manzil: {DATA[id_num][from_user_id]["county"]}\n"
                          f"Haydovchi: {driver_name(DATA[id_num][from_user_id]["drivers"])}\n"
                          f"Avtomashinaga quyilgan yoqilgi: {DATA[id_num][from_user_id]["fuel_quantity"]}\n"
                          f"Avtomashinaning spidonametr ko'rsatkichini kirit",
                          reply_markup=quantity_distance_buttons(current_distance=spd))

    # -----------------------------------------------------

@bot.callback_query_handler(
    func=lambda call: call.data.split("|")[0] == "distance" and len(call.data.split("|")) == 4)
def check_distance(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    id_num1 = call.message.text.split("yafka №: ")
    id_num2 = id_num1[1].split("\n")
    id_num = id_num2[0]
    current_distance = int(call.message.reply_markup.keyboard[1][0].text)
    from_user_id = call.from_user.id
    dis, quantity, amount, action = call.data.split("|")
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text=
                          f"Zayafka №: {id_num}\n"
                          f"Sana: {DATA[id_num][from_user_id]["data"]}\n"
                          f"Mashina № {DATA[id_num][from_user_id]["machine"]}\n"
                          f"Manzil: {DATA[id_num][from_user_id]["county"]}\n"
                          f"Haydovchi: {driver_name(DATA[id_num][from_user_id]["drivers"])}\n"
                          f"Avtomashinaga quyilgan yoqilg'i miqdori: {DATA[id_num][from_user_id]["fuel_quantity"]}\n"
                          f"Avtomashinaning spidonametr ko'rsatkichini kirit ",
                          reply_markup=quantity_distance_buttons(current_distance=current_distance, amount=int(amount),
                                                             action=action))

@bot.callback_query_handler(
    func=lambda call: call.data.split("|")[0] == "distance" and len(call.data.split("|")) == 3)
def check_distance1(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    message_id = call.message.message_id
    current_distance = call.message.reply_markup.keyboard[1][0].text
    id_num1 = call.message.text.split("yafka №: ")
    id_num2 = id_num1[1].split("\n")
    id_num = id_num2[0]
    DATA[id_num][from_user_id]["walking_distance"] = current_distance
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text=
                          f"Zayafka №: {id_num}\n"
                          f"Sana: {DATA[id_num][from_user_id]["data"]}\n"
                          f"Mashina № {DATA[id_num][from_user_id]["machine"]}\n"
                          f"Manzil: {DATA[id_num][from_user_id]["county"]}\n"
                          f"Haydovchi: {driver_name(DATA[id_num][from_user_id]["drivers"])}\n"
                          f"Avtomashinaga quyilgan yoqilgi: {DATA[id_num][from_user_id]["fuel_quantity"]}\n"
                          f"Avtomashinaning spidonametr ko'rsatkichi: {DATA[id_num][from_user_id]["walking_distance"]}",
                          reply_markup=selection_yes_no_button_sender())


@bot.callback_query_handler(func=lambda call: call.data in ['Yes_sender', 'No_sender'])
def check_selection_yes_no_button_sender(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    from_user_id = call.from_user.id
    res = call.data

    id_num1 = call.message.text.split("yafka №: ")
    id_num2 = id_num1[1].split("\n")
    id_num = id_num2[0]

    drivers_chat_id = DATA[id_num][from_user_id]["driver_chat_id"]
    index = DATA[id_num][from_user_id]["index"]
    data = DATA[id_num][from_user_id]["data"]
    machine = DATA[id_num][from_user_id]["machine"]
    county = DATA[id_num][from_user_id]["county"]
    drivers = DATA[id_num][from_user_id]["drivers"]
    liters = DATA[id_num][from_user_id]["fuel_quantity"]
    walking_distance = DATA[id_num][from_user_id]["walking_distance"]
    cr_at = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    if res == 'Yes_sender':
        db.update_table_fuel_output(index, from_user_id, data, machine, county, drivers, liters, walking_distance, cr_at, int(id_num))

        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=
                              f"Zayafka №: {id_num}\n"
                              f"Sana: {DATA[id_num][from_user_id]["data"]}\n"
                              f"Mashina № {DATA[id_num][from_user_id]["machine"]}\n"
                              f"Manzil: {DATA[id_num][from_user_id]["county"]}\n"
                              f"Haydovchi: {driver_name(DATA[id_num][from_user_id]["drivers"])}\n"
                              f"Avtomashinaga quyilgan yoqilgi: {DATA[id_num][from_user_id]["fuel_quantity"]}\n"
                              f"Avtomashinaning spidonametr ko'rsatkichi: {DATA[id_num][from_user_id]["walking_distance"]}")

        bot.send_message(drivers_chat_id, f"Zayafka №: {id_num}\n"
                                          f"Malumotlarni tasdiqlaysizmi?\n"
                                          f"Sana: {data}\n"
                                          f"Mashina: {machine}\n"
                                          f"Ketayotgan manzili: {county}\n"
                                          f"Haydovchi: {drivers}\n"
                                          f"Quyilgan yoqilgi miqdori: {liters}\n"
                                          f"Prabegi: {walking_distance}", reply_markup=selection_yes_no_button_receiver())




    elif res == 'No_sender':
        bot.edit_message_text(chat_id=chat_id, message_id=message_id,  text=f"Nimani xato qildingiz?\nIltimos boshqatdan boshlang")
        del DATA[id_num]

@bot.callback_query_handler(func=lambda call: call.data in ["Yes_receiver", "No_receiver"])
def check_selection_yes_no_button_receiver(call: CallbackQuery):
    chat_id = call.message.chat.id
    id_num1 = call.message.text.split("yafka №: ")
    id_num2 = id_num1[1].split("\n")
    id_num = id_num2[0]
    message_id = call.message.message_id
    rc_at = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    from_user_id = list(DATA[id_num].keys())[0]
    res = call.data
    drivers_chat_id = DATA[id_num][from_user_id]["driver_chat_id"]
    if res == 'Yes_receiver':
        db.update_table_fuel_output_driver(drivers_chat_id, 1, "Qabul qilingan", rc_at, int(id_num))
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=
                              f"Zayafka №: {id_num}\n"
                              f"Sana: {DATA[id_num][from_user_id]["data"]}\n"
                              f"Mashina № {DATA[id_num][from_user_id]["machine"]}\n"
                              f"Manzil: {DATA[id_num][from_user_id]["county"]}\n"
                              f"Haydovchi: {driver_name(DATA[id_num][from_user_id]["drivers"])}\n"
                              f"Avtomashinaga quyilgan yoqilgi: {DATA[id_num][from_user_id]["fuel_quantity"]}\n"
                              f"Avtomashinaning spidonametr ko'rsatkichi: {DATA[id_num][from_user_id]["walking_distance"]}")
        del DATA[id_num]

    else:
        bot.delete_message(drivers_chat_id, message_id)
        msg = bot.send_message(drivers_chat_id, f"Nimasi xato\n"
                                                  f"Iltimos izoh bering")
        bot.register_next_step_handler(msg, checking_the_driver_description, id_num, from_user_id)

def checking_the_driver_description(message: Message, id_num, from_user_id):
    chat_id = message.chat.id
    message_id = message.message_id
    description = message.text
    rc_at = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    if isinstance(description, str):
        db.update_table_fuel_output_driver(chat_id, 0, description, rc_at, row_id=id_num)
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=
                              f"Zayafka №: {id_num}\n"
                              f"Sana: {DATA[id_num][from_user_id]["data"]}\n"
                              f"Mashina № {DATA[id_num][from_user_id]["machine"]}\n"
                              f"Manzil: {DATA[id_num][from_user_id]["county"]}\n"
                              f"Haydovchi: {driver_name(DATA[id_num][from_user_id]["drivers"])}\n"
                              f"Avtomashinaga quyilgan yoqilgi: {DATA[id_num][from_user_id]["fuel_quantity"]}\n"
                              f"Avtomashinaning spidonametr ko'rsatkichi: {DATA[id_num][from_user_id]["walking_distance"]}")
    del DATA[id_num]