from data import bot, db
import handlers


if __name__ == '__main__':
    db.create_table_avto_tigach()
    db.create_table_county()
    db.create_table_driver()
    db.create_table_fuel_info()
    db.admins()
    db.tgmenegers()
    bot.infinity_polling()
